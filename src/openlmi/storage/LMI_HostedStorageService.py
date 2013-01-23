# Copyright (C) 2012 Red Hat, Inc.  All rights reserved.
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

from openlmi.storage.BaseProvider import BaseProvider
import pywbem
import openlmi.storage.cmpi_logging as cmpi_logging

class LMI_HostedStorageService(BaseProvider):
    """
        Implementation of LMI_HostedStorageService provider.
    """

    @cmpi_logging.trace_method
    def __init__(self, *args, **kwargs):
        super(LMI_HostedStorageService, self).__init__(*args, **kwargs)


    @cmpi_logging.trace_method
    def get_instance(self, env, model):
        """
            Provider implementation of GetInstance intrinsic method.
        """
        # just check keys
        system = model['Antecedent']
        if (system['CreationClassName'] != self.config.system_class_name
                or system['Name'] != self.config.system_name):
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Wrong Antecedent keys.")

        service = model['Dependent']
        if (service['SystemCreationClassName'] != self.config.system_class_name
                or service['SystemName'] != self.config.system_name):
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Wrong Dependent keys.")

        # try to find registered service for the dependent name
        for provider in self.provider_manager.get_service_providers():
            if (service['CreationClassName'] == provider.classname
                    and service['Name'] == provider.classname):
                break
        else:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Wrong Dependent service name.")

        return model

    @cmpi_logging.trace_method
    def enum_instances(self, env, model, keys_only):
        """
            Provider implementation of EnumerateInstances intrinsic method.
        """
        model.path.update({'Dependent': None, 'Antecedent': None})
        for provider in self.provider_manager.get_service_providers():
            model['Antecedent'] = pywbem.CIMInstanceName(
                    classname=self.config.system_class_name,
                    namespace=self.config.namespace,
                    keybindings={
                            'CreationClassName' : self.config.system_class_name,
                            'Name' : self.config.system_name,
                    })
            model['Dependent'] = pywbem.CIMInstanceName(
                    classname=provider.classname,
                    namespace=self.config.namespace,
                    keybindings={
                            'CreationClassName': provider.classname,
                            'Name' : provider.classname,
                            'SystemName': self.config.system_name,
                            'SystemCreationClassName' : self.config.system_class_name
                    })
            yield model

    @cmpi_logging.trace_method
    def references(self, env, object_name, model, result_class_name, role,
                   result_role, keys_only):
        """Instrument Associations."""
        ch = env.get_cimom_handle()

        # If you want to get references for free, implemented in terms
        # of enum_instances, just leave the code below unaltered.
        if ch.is_subclass(object_name.namespace,
                          sub=object_name.classname,
                          super='CIM_Service') or \
                ch.is_subclass(object_name.namespace,
                               sub=object_name.classname,
                               super='CIM_System'):
            return self.simple_refs(env, object_name, model,
                          result_class_name, role, result_role, keys_only)
