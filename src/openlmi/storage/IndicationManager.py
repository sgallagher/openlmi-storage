# Copyright (C) 2013 Red Hat, Inc.  All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# Authors: Jan Safranek <jsafrane@redhat.com>
# -*- coding: utf-8 -*-
"""
    Module for IndicationManager and support classes.
    
    Usage:
    * In your initialization routine, create one IndicationManager instance.
      E.g. one for whole LMI_Storage may be is enough.
    * Call indication_manager.add_filters() with all filters your providers
      support. This method can be called multiple times. For example:
      
      filters = {
          "JobPercentUpdated": {
              "Query" : "SELECT * FROM CIM_InstModification WHERE SourceInstance ISA CIM_ConcreteJob AND SourceInstance.CIM_ConcreteJob::PercentComplete <> PreviousInstance.CIM_ConcreteJob::PercentComplete",
              "Description" : "Modification of Percentage Complete for a Concrete Job.",
          },
          "JobSucceeded": {
              "Query" : "SELECT * FROM CIM_InstModification WHERE SourceInstance ISA CIM_ConcreteJob AND ANY SourceInstance.CIM_ConcreteJob::OperationalStatus[*] = 17 AND ANY SourceInstance.CIM_ConcreteJob::OperationalStatus[*] = 2",
              "Description": "Modification of Operational Status for a Concrete Job to 'Complete' and 'OK'.",
          },
          #...
      }
      instance_manager.add_filters(filters)
      
    * In your provider module, implement indication functions like this:
    
        def authorize_filter(env, fltr, ns, classes, owner):
            indication_manager.authorize_filter(env, fltr, ns, classes, owner)

        def activate_filter (env, fltr, ns, classes, first_activation):
            indication_manager.activate_filter(env, fltr, ns, classes, first_activation)
        
        def deactivate_filter(env, fltr, ns, classes, last_activation):
            indication_manager.deactivate_filter(env, fltr, ns, classes, last_activation)
        
        def enable_indications(env):
            indication_manager.enable_indications(env)
        
        def disable_indications(env):
            indication_manager.disable_indications(env)
                    
    From now on, the IndicationManager will track all subscribed filters. You
    can query the indication_manager.is_subscribed() before you create and
    send an indication. Use indication_manager.send_indication() to send
    your indications.
"""

import pywbem
import openlmi.common.cmpi_logging as cmpi_logging
import socket
import threading
from Queue import Queue

class IndicationManager(object):
    """ 
        Helper class for handling of indications using CMPI.
        Only static (=preconfigured, read-only) indication filters are
        supported.
        
        The supported filters must be passed to add_filters method. The filters
        are passed as dictionary
        'filter_id' -> {dictionary 'IndicationFilter property' -> 'value'}.
        There must be at least 'Query' property in each filter, CQL is assumed.
        
        This helper automatically tracks which filters are subscribed. Provider
        can query is_subscribed() to check, if filter with given filter_id
        is subscribed before generating indications.
        
        The CMPI interface to send indications is complicated -
        when an indication is send from CIMOM callback (e.g. get_instance), it
        must use current 'env' parameter of the callback and it would be
        tedious to pass it to IndicationManager each time.
        Therefore IndicationManager creates its own thread, registers it at
        CIMOM using PrepareAttachThread/AttachThread.
          
        As side-effect, indication can be sent from any thread, there is no need
        to call PrepareAttachThread/AttachThread.
    """
    SEVERITY_INFO = pywbem.Uint16(2)  # CIM_Indication.PerceivedSeverity

    @cmpi_logging.trace_method
    def __init__(self, env, filter_classname, nameprefix, namespace):
        self.filters = {}
        self.enabled = False
        self.subscribed_filters = set()
        self.filter_classname = filter_classname
        self.nameprefix = nameprefix
        self.instcreation_classname = "LMI_" + nameprefix + "InstCreation"
        self.instmodification_classname = ("LMI_" + nameprefix
                + "InstModification")
        self.instdeletion_classname = "LMI_" + nameprefix + "InstDeletion"
        self.namespace = namespace

        self.queue = Queue()
        # prepare indication thread
        ch = env.get_cimom_handle()
        new_broker = ch.PrepareAttachThread()
        self.indication_sender = threading.Thread(
                target=self._send_indications_loop, args=(new_broker,))
        self.indication_sender.start()

    @cmpi_logging.trace_method
    def add_filters(self, filters):
        """
            Add new filters to the helper. These filters will be allowed for
            subscription.
        """
        self.filters.update(filters)

    @cmpi_logging.trace_method
    def authorize_filter(self, _env, fltr, _ns, _classes, _owner):
        """ AuthorizeFilter callback from CIMOM. """
        for (_id, _fltr) in self.filters.iteritems():
            if _fltr['Query'] == fltr:
                cmpi_logging.logger.info("%s: InstanceFilter %s: %s "
                        "authorized" % (self.filter_classname, _id, fltr))
                return True
        cmpi_logging.logger.info("%s: InstanceFilter %s denied" %
                (self.filter_classname, fltr))
        return False

    @cmpi_logging.trace_method
    def activate_filter(self, _env, fltr, _ns, _classes, first_activation):
        """ ActivateFilter callback from CIMOM. """
        if first_activation:
            for (_id, _fltr) in self.filters.iteritems():
                if _fltr['Query'] == fltr:
                    self.subscribed_filters.add(_id)
                    cmpi_logging.logger.info("%s: InstanceFilter %s: %s "
                            "started" % (self.filter_classname, _id, fltr))

    @cmpi_logging.trace_method
    def deactivate_filter(self, _env, fltr, _ns, _classes, last_activation):
        """ DeactivateFilter callback from CIMOM. """
        if last_activation:
            for (_id, _fltr) in self.filters.iteritems():
                if _fltr['Query'] == fltr:
                    self.subscribed_filters.remove(_id)
                    cmpi_logging.logger.info("%s: InstanceFilter %s: %s "
                            "stopped" % (self.filter_classname, _id, fltr))

    @cmpi_logging.trace_method
    def enable_indications(self, _env):
        """ EnableIndications callback from CIMOM. """
        self.enabled = True
        cmpi_logging.logger.info("%s: Indications enabled"
                 % (self.filter_classname,))

    @cmpi_logging.trace_method
    def disable_indications(self, _env):
        """ EnableIndications callback from CIMOM. """
        self.enabled = False
        cmpi_logging.logger.info("%s: Indications disabled"
                 % (self.filter_classname,))

    @cmpi_logging.trace_method
    def send_indication(self, indication):
        """ Send indication to all subscribers."""
        self.queue.put(indication)

    @cmpi_logging.trace_method
    def send_instcreation(self, instance, filter_id):
        """
            Send LMI_<nameprefix>InstCreation indication.
        """
        if not self.is_subscribed(filter_id):
            return
        path = pywbem.CIMInstanceName(
                classname=self.instcreation_classname,
                namespace=self.namespace)
        ind = pywbem.CIMInstance(
                self.instcreation_classname,
                path=path)
        ind['SourceInstance'] = instance
        ind['SourceInstanceHost'] = socket.gethostname()
        ind['SourceInstanceModelPath'] = str(instance.path)
        ind['IndicationFilterName'] = ("LMI:" + self.filter_classname + ":"
                + filter_id)
        ind['PerceivedSeverity'] = self.SEVERITY_INFO

        cmpi_logging.logger.info("Sending indication %s for %s" %
                (filter_id, str(path)))
        self.send_indication(ind)

    @cmpi_logging.trace_method
    def send_instmodification(self, old_instance, new_instance, filter_id):
        """
            Send LMI_<nameprefix>InstModification indication.
        """
        if not self.is_subscribed(filter_id):
            return
        path = pywbem.CIMInstanceName(
                classname=self.instmodification_classname,
                namespace=self.namespace)
        ind = pywbem.CIMInstance(
                self.instcreation_classname,
                path=path)
        ind['SourceInstance'] = new_instance
        ind['PreviousInstance'] = old_instance
        ind['SourceInstanceHost'] = socket.gethostname()
        ind['SourceInstanceModelPath'] = str(new_instance.path)
        ind['IndicationFilterName'] = ("LMI:" + self.filter_classname + ":"
                + filter_id)
        ind['PerceivedSeverity'] = self.SEVERITY_INFO

        cmpi_logging.logger.info("Sending indication %s for %s" %
                (filter_id, str(path)))
        self.send_indication(ind)

    @cmpi_logging.trace_method
    def is_subscribed(self, fltr_id):
        """ Return True, if there is someone subscribed for given filter."""
        if not self.enabled:
            return False
        if fltr_id in self.subscribed_filters:
            return True
        return False

    @cmpi_logging.trace_method
    def _send_indications_loop(self, broker):
        """
            This method runs in its own thread. It just sends all enqueued
            indications.
        """
        broker.AttachThread()
        while True:
            indication = self.queue.get()
            cmpi_logging.logger.trace_info("Delivering indication %s" %
                (str(indication.path)))
            broker.DeliverIndication(self.namespace, indication)
            self.queue.task_done()
