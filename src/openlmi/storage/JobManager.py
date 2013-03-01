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
Module for job management classes. It provides basic infrastructure for
asynchronous jobs. All necessary CIM classes and indications are implemented
here.

For now, all asynchronous jobs are queued. The queue is processed in separate
thread sequentially. No two jobs can run in parallel.  

Usage:

 * Create MOF file for these classes: 
    * LMI_<name>Job
    * LMI_<name>MethodResult
    * LMI_Affected<name>JobElement
    * LMI_Owning<name>JobElement
    * LMI_Associated<name>JobMethodResult
    Where <name> is prefix of your classes, for example 'Storage'

 * During initialization, create JobManager.
 * When needed. create new Job instance:
   *  Set its execute callback using set_execute_action(). This callback will
      be called when the job is to be executed. It will be called in context
      of JobManager worker thread!
   * Optionally, set cancel callback using set_execute_action(). This callback
     will be called when the job is still queued and is cancelled by
     application. This callback will be called in context of CIMOM callback
     and should be quick!
  * Enqueue the job using JobManager.add_job() method.
  * When your execute callback is called, you can optionally call
    job.change_state() to update percentage of completion. 
  * When your execute callback is called, don't forget to set method result
    using job.finish_method().
    
 * JobManager automatically sends all job-related indications.
 * Job automatically tracks various timestamps.
 * By default, the job automatically disappears after 60 seconds after it
   finishes. Application may set DeleteOnCompletion and TimeBeforeRemoval to
   override this timeout.
"""

from datetime import datetime, timedelta
import threading
from Queue import Queue
import pywbem
import openlmi.common.cmpi_logging as cmpi_logging
from pywbem.cim_provider2 import CIMProvider2
import socket

class Job(object):
    """
        Generic abstract class representing one CIM_ConcreteJob.
        It remembers input and output arguments, affected ManagedElements and
        ownine ManagedElement (to be able to create associations to them)
        and all CIM_ConcreteJob properties.
        
        Subclass must implement execute() and cancel() method.
    """

    DEFAULT_TIME_BEFORE_REMOVAL = 5000  # in seconds

    STATE_QUEUED = 1  # Job has not started yet
    STATE_RUNNING = 2  # Job is running
    STATE_FINISHED_OK = 3  # Job finished OK
    STATE_FAILED = 4  # Job finished with error
    STATE_SUSPENDED = 5  # Job is queued and suspended
    STATE_TERMINATED = 6  # Job was queued and terminated

    FINAL_STATES = [STATE_FINISHED_OK, STATE_FAILED, STATE_SUSPENDED,
            STATE_TERMINATED]

    # There is no way how to suspend/terminate running job!

    @cmpi_logging.trace_method
    def __init__(self, job_manager, job_name, input_arguments,
            method_name, affected_elements, owning_element):
        """
            Create new storage job. time_submitted is recorded.
        """

        self.job_manager = job_manager

        # Unique ID
        self.the_id = job_manager.get_next_id()

        # User friendly name of the job
        self.job_name = job_name

        # Dictionary of input arguments, 'parameter_name' -> 'parameter_value'
        # The parameter value must be CIMProperty or something that can be
        # assigned to it.
        self.input_arguments = input_arguments

        # Dictionary of output arguments, 'parameter_name' -> 'parameter_value'
        # The parameter value must be CIMProperty or something that can be
        # assigned to it.
        self.output_arguments = None

        # Method return value, as CIMProperty or something that can be
        # assigned to it.
        self.return_value = None
        # Value of Job.ReturnValueType
        self.return_value_type = None

        # Name of the method
        self.method_name = method_name

        # Time when the job was created
        self.time_submitted = datetime.utcnow()

        # Nr. of seconds before the job is removed when the job finishes
        self.time_before_removal = self.DEFAULT_TIME_BEFORE_REMOVAL

        # If the job should be removed after completion
        self.delete_on_completion = True

        self.percent_complete = 0

        # State of the job
        self.job_state = self.STATE_QUEUED

        # Last change of job state
        self.time_of_last_state_change = self.time_submitted

        # Duration of the job in RUNNING state
        self.elapsed_time = None

        # When the job started (= switched to RUNNING)
        self.start_time = None
        # When the job finished (= switched from RUNNING)
        self.finish_time = None

        # Array of CIMInstanceNames of affected elements, so we can
        # enumerate associations to them.
        self.affected_elements = affected_elements

        # CIMInstanceName to owning element (service), so we can enumerate
        # instances.
        self.owning_element = owning_element

        # Timer used to delete the job after time_before_removal seconds
        self.timer = None

        # CIMError with result code
        self.error = None

        # internal lock to protect state changes from races
        self._lock = threading.RLock()

        self._execute = None
        self._execargs = None
        self._execkwargs = None
        self._cancel = None
        self._cancelargs = None
        self._cancelkwargs = None

    @cmpi_logging.trace_method
    def set_execute_action(self, callback, *args, **kwargs):
        """
            Set callbacks, which will be called when the job is to be
            executed. It is expected that the callback will take some time
            to execute. The callback must change state of the job and
            set output parameters and error.
        """
        self._execute = callback
        self._execargs = args
        self._execkwargs = kwargs

    @cmpi_logging.trace_method
    def set_cancel_action(self, callback, *args, **kwargs):
        """
            Set callbacks, which will be called when the job is to be
            cancelled. The callback must be quick!
        """
        self._cancel = callback
        self._cancelargs = args
        self._cancelkwargs = kwargs

    @cmpi_logging.trace_method
    def finish_method(self, new_state, return_value=None, return_type=None,
            output_arguments=None, error=None):
        """
            Mark the job as finished, with given return value,
            output parameters and error.
        """
        self.return_value = return_value
        self.return_value_type = return_type
        self.output_arguments = output_arguments
        self.error = error
        self.change_state(new_state, 100)

    @cmpi_logging.trace_method
    def change_state(self, new_state, percent=None):
        """
            Change state of a job. (Re-)calculate various times
            based on the state change.
        """
        self.lock()

        cmpi_logging.logger.debug("Job %s: %s changes state from %d to %d"
                % (self.the_id, self.job_name, self.job_state, new_state))

        if self.job_state != new_state:

            # Check if the job has just finished
            if (self.job_state not in self.FINAL_STATES
                    and new_state in self.FINAL_STATES):
                # Remember finish time
                self.finish_time = datetime.utcnow()
                # Remember job execution time.
                if self.start_time:
                    self.elapsed_time = self.finish_time - self.start_time

            # Check if the job has just started
            if new_state == self.STATE_RUNNING:
                self.start_time = datetime.utcnow()

            self.job_state = new_state
            self.time_of_last_state_change = datetime.now()
            # TODO: send indication?

        if percent is None:
            # guess the percentage from status
            if new_state == self.STATE_QUEUED:
                percent = 0
            elif new_state == self.STATE_RUNNING:
                percent = 50
            else:
                percent = 100
        if self.percent_complete != percent:
            self.percent_complete = percent
            self.time_of_last_state_change = datetime.now()
            # TODO: send indication

        # start / update the timer if necesasry
        self.restart_timer()
        self.unlock()

    @cmpi_logging.trace_method
    def _expire(self):
        """
            Callback when a Job completes and time_before_removal second
            passed.
        """
        cmpi_logging.logger.debug("Got timeout for job %s: '%s', removing"
                " the job" % (self.the_id, self.job_name))
        self.job_manager.remove_job(self)

    @cmpi_logging.trace_method
    def restart_timer(self):
        """
            Re-schedule timer for TimeBeforeRemoval because some property has
            changed.
        """
        if not self.job_state in self.FINAL_STATES:
            return

        # Stop the old timer.
        if self.timer:
            self.timer.cancel()
            self.timer = None

        # Start the new timer.
        if self.delete_on_completion:
            now = datetime.utcnow()
            passed = now - self.finish_time
            timeout = self.time_before_removal - passed.total_seconds()
            cmpi_logging.logger.debug("Starting timer for job %s: '%s' for %f"
                    " seconds" % (self.the_id, self.job_name, timeout))
            self.timer = threading.Timer(timeout, self._expire)
            self.timer.start()

    @cmpi_logging.trace_method
    def lock(self):
        """ 
            Lock internal mutex. Other threads will block on subsequent lock().
            The lock is recursive, i.e. can be called multiple times from
            single thread.
        """
        self._lock.acquire()

    @cmpi_logging.trace_method
    def unlock(self):
        """ Unlock internal mutex."""
        self._lock.release()

    @cmpi_logging.trace_method
    def execute(self):
        """
            Start executing the job.
            job_state is already set to STATE_RUNNING.
            At the end, this method must set proper job_state and
            output parameters!
            Any exception is translated to CIMError and appropriate state is
            set.
            This method may update progress using change_state with percents.
        """
        try:
            self._execute(*(self._execargs), **(self._execkwargs))
        except pywbem.CIMError, error:
            self.finish_method(Job.STATE_FAILED, error=error)
        except Exception, ex:
            error = pywbem.CIMError(pywbem.CIM_ERR_FAILED, str(ex))
            self.finish_method(Job.STATE_FAILED, error=error)

    @cmpi_logging.trace_method
    def cancel(self):
        """
            Cancels queued action. The action was not yet started.
        """
        self.change_state(self.STATE_TERMINATED)
        if self._cancel:
            self._cancel(*(self._cancelargs), **(self._cancelkwargs))

    @cmpi_logging.trace_method
    def get_name(self):
        """
            Return CIMInstanceName of the job.
        """
        name = pywbem.CIMInstanceName(
                classname=self.job_manager.job_classname,
                namespace=self.job_manager.namespace,
                keybindings={
                        'InstanceID': self.get_instance_id()
        })
        return name

    @cmpi_logging.trace_method
    def get_instance_id(self, classname=None):
        """ Return InstanceID."""
        if classname is None:
            classname = self.job_manager.job_classname
        return 'LMI:' + classname + ':' + str(self.the_id)

    @staticmethod
    def parse_instance_id(instance_id, job_manager, classname=None):
        """
            Return the last part of instance_id.
            Returns None if the instance_id has wrong format.
        """
        if classname is None:
            classname = job_manager.job_classname
        parts = instance_id.split(":")
        if len(parts) != 3:
            return None
        if parts[0] != 'LMI':
            return None
        if parts[1] != classname:
            return None
        if not parts[2].isdigit():
            return None
        return parts[2]

    @cmpi_logging.trace_method
    def get_pre_call(self):
        """ 
            Return CIMInstance of CIM_InstMethodCall that describes the
            pre-execution values of the extrinisic method invocation.
        """
        path = pywbem.CIMInstanceName(
                classname="CIM_InstMethodCall",
                keybindings={},
                host=socket.gethostname(),
                namespace=self.job_manager.namespace)
        inst = pywbem.CIMInstance(
                classname="CIM_InstMethodCall",
                path=path,
                properties={
                        'MethodName' : self.method_name,
#                        'MethodParameters' : pywbem.CIMProperty(
                                # name="MethodParameters",
                                # type='instance',
                                # value=self._get_method_params(False)),
                        'PreCall' : True,
                })
        src_instance = self._get_cim_instance()
        inst['SourceInstance'] = src_instance
        inst['SourceInstanceModelPath'] = str(src_instance.path)
        return inst

    @cmpi_logging.trace_method
    def get_post_call(self):
        """ 
            Return CIMInstance of CIM_InstMethodCall that describes the
            pre-execution values of the extrinisic method invocation.
        """
        path = pywbem.CIMInstanceName(
                classname="CIM_InstMethodCall",
                keybindings={},
                host=socket.gethostname(),
                namespace=self.job_manager.namespace)
        inst = pywbem.CIMInstance(
                classname="CIM_InstMethodCall",
                path=path,
                properties={
                        'MethodName' : self.method_name,
#                        'MethodParameters' : self._get_method_params(True),
                        'PreCall' : False
        })
        src_instance = self._get_cim_instance()
        inst['SourceInstance'] = src_instance
        inst['SourceInstanceModelPath'] = str(src_instance.path)

        return inst
        if self.return_value_type is not None:
            inst['ReturnValueType'] = self.return_value_type
        if self.return_value is not None:
            inst['ReturnValue'] = self.return_value
        if self.error is not None:
            inst['Error'] = self.error
        return inst

    @cmpi_logging.trace_method
    def _get_cim_instance(self):
        """ Return CIMInstance of this job. """
        return self.job_manager.get_job_instance(self)

    @cmpi_logging.trace_method
    def _get_method_params(self, output=True):
        """
            Return CIMInstance of __MethodParameters for CIM_InstMethodCall
            indication.
        """
        inst = pywbem.CIMInstance(classname="__MethodParameters")
        for (name, value) in self.input_arguments.iteritems():
            inst[name] = value
        if output:
            # overwrite any input parameter
            for (name, value) in self.output_arguments.iteritems():
                inst[name] = value
        return inst

    class ReturnValueType(object):
        Boolean = pywbem.Uint16(2)
        String = pywbem.Uint16(3)
        Char16 = pywbem.Uint16(4)
        Uint8 = pywbem.Uint16(5)
        Sint8 = pywbem.Uint16(6)
        Uint16 = pywbem.Uint16(7)
        Sint16 = pywbem.Uint16(8)
        Uint32 = pywbem.Uint16(9)
        Sint32 = pywbem.Uint16(10)
        Uint64 = pywbem.Uint16(11)
        Sint64 = pywbem.Uint16(12)
        Datetime = pywbem.Uint16(13)
        Real32 = pywbem.Uint16(14)
        Real64 = pywbem.Uint16(15)
        Reference = pywbem.Uint16(16)

class JobManager(object):
    """
        Container of all queued, running or finished LMI_ConcreteJobs.
        It manages instances of one LMI_ConcreteJob subclass.
        In theory, it's possible to have LMI_XJob and LMI_YJob classes,
        managed by two JobManagers, but it was never tested.
    """
    @cmpi_logging.trace_method
    def __init__(self, name, provider_environment, namespace):
        """ 
            Initialize new Manager.
            
            Args:
                name (string): String with classname infix. For example
                    'Storage' for LMI_StorageJob, LMI_StorageJobMethodResult etc.
                
                provider_environment (ProviderEnvironment) - CIMOM environment
                
                namespace (string): namespace of all providers.
        """
        self.jobs = {}
        self.queue = Queue()
        self.worker = threading.Thread(target=self.worker_main)
        self.worker.start()
        self.last_instance_id = 0
        self.name = name
        self.providers = {}
        self.namespace = namespace

        self.job_classname = 'LMI_' + self.name + 'Job'
        self.method_result_classname = "LMI_" + self.name + "MethodResult"
        self.affected_classname = "LMI_Affected" + self.name + "JobElement"
        self.owning_classname = "LMI_Owning" + self.name + "JobElement"
        self.associated_result_classname = ('LMI_Associated' + self.name
                + 'JobMethodResult')
        self.job_provider = None
        self.provider_environment = provider_environment

    @cmpi_logging.trace_method
    def get_providers(self):
        """
            Get dictionary of providers for these classes:

            * LMI_<name>Job
            * LMI_<name>MethodResult
            * LMI_Affected<name>JobElement
            * LMI_Owning<name>JobElement
            * LMI_Associated<name>JobMethodResult
            
            Returns:
                dictionary class_name -> CIMProvider2
        """

        if not self.providers:
            job_provider = LMI_ConcreteJob(self.job_classname, job_manager=self)
            self.providers[self.job_classname] = job_provider
            self.job_provider = job_provider

            provider = LMI_MethodResult(
                    self.method_result_classname, job_manager=self)
            self.providers[self.method_result_classname] = provider

            provider = LMI_AffectedJobElement(
                    self.affected_classname, job_manager=self)
            self.providers[self.affected_classname] = provider

            provider = LMI_OwningJobElement(
                    self.owning_classname, job_manager=self)
            self.providers[self.owning_classname] = provider

            provider = LMI_AssociatedJobMethodResult(
                    self.owning_classname, job_manager=self)
            self.providers[self.associated_result_classname] = provider

        return self.providers

    @cmpi_logging.trace_method
    def add_job(self, job):
        """
            Add new job.
        """
        cmpi_logging.logger.debug("Job %s: '%s' enqueued"
                % (job.the_id, job.job_name))

        self.jobs[job.the_id] = job
        self.queue.put(job)
        # TODO: send indication?

    @cmpi_logging.trace_method
    def remove_job(self, job):
        """
            Remove existing job. Note that jobs are removed automatically
            after a timeout.
        """
        cmpi_logging.logger.debug("Removing job %s: '%s'"
                % (job.the_id, job.job_name))
        del self.jobs[job.the_id]
        # The job may still be in the queue!
        # There is no way, how to remove it.
        # TODO: send indication?

    @cmpi_logging.trace_method
    def get_job_for_instance_id(self, instance_id, classname=None):
        """ Return Job for given InstanceID or None when no such Job exist."""
        if classname is None:
            classname = self.job_classname
        the_id = Job.parse_instance_id(instance_id, self, classname)
        if the_id:
            return self.jobs.get(the_id, None)
        else:
            return None

    @cmpi_logging.trace_method
    def worker_main(self):
        """
            This is the main loop of the job queue.
        """
        while True:
            job = self.queue.get()
            # we need to protect from changes between checking state and
            # setting new state
            job.lock()
            if job.job_state == Job.STATE_QUEUED:
                # the job was not cancelled
                job.change_state(Job.STATE_RUNNING)
                job.unlock()
                cmpi_logging.logger.info("Starting job %s: '%s'" %
                        (job.the_id, job.job_name))

                job.execute()
                if job.error:
                    cmpi_logging.logger.warn("Job %s: '%s' finished with error:"
                            " %s" % (job.the_id, job.job_name, str(job.error)))
                else:
                    cmpi_logging.logger.info("Job %s: '%s' finished OK" %
                            (job.the_id, job.job_name))
            else:
                # just skip suspended and terminated jobs
                job.unlock()

            self.queue.task_done()

    @cmpi_logging.trace_method
    def get_next_id(self):
        """
            Return next unused id.
        """
        self.last_instance_id += 1
        return self.last_instance_id

    @cmpi_logging.trace_method
    def get_job_instance(self, job):
        """
            Return CIMInstance for given job.
            Args:
                job (Job)
            Returns:
                CIMInstance. The instance
        """
        path = pywbem.CIMInstanceName(
                classname=self.job_classname,
                keybindings={'InstanceID': job.get_instance_id()},
                host=socket.gethostname(),
                namespace=self.namespace)
        inst = pywbem.CIMInstance(classname=self.job_classname, path=path)
        inst['InstanceID'] = job.get_instance_id()
        return self.job_provider.get_instance(self.provider_environment, inst)


class LMI_ConcreteJob(CIMProvider2):
    """
        Provider of LMI_ConcreteJob class or its subclass.
    """
    @cmpi_logging.trace_method
    def __init__(self, classname, job_manager):
        self.classname = classname
        self.job_manager = job_manager

    @cmpi_logging.trace_method
    def enum_instances(self, env, model, keys_only):
        """
            Provider implementation of EnumerateInstances intrinsic method.
        """
        model.path.update({'InstanceID': None})
        for job in self.job_manager.jobs.values():
            model['InstanceID'] = job.get_instance_id()
            if keys_only:
                yield model
            else:
                yield self.get_instance(env, model, job)

    @cmpi_logging.trace_method
    def get_instance(self, env, model, job=None):
        """
            Provider implementation of GetInstance intrinsic method.
        """
        if not job:
            instance_id = model['InstanceID']
            job = self.job_manager.get_job_for_instance_id(instance_id)
        if not job:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Job not found.")

        model['DeleteOnCompletion'] = job.delete_on_completion
        model['Name'] = job.job_name

        # convert seconds to timedelta
        seconds = job.time_before_removal
        if seconds:
            delta = timedelta(seconds=seconds)
            model['TimeBeforeRemoval'] = pywbem.CIMDateTime(delta)
        else:
            model['TimeBeforeRemoval'] = pywbem.CIMProperty(
                    name='TimeBeforeRemoval',
                    value=None,
                    type='datetime')

        if job.time_of_last_state_change:
            model['TimeOfLastStateChange'] = pywbem.CIMDateTime(
                    job.time_of_last_state_change)
        else:
            model['TimeOfLastStateChange'] = pywbem.CIMProperty(
                    name='TimeOfLastStateChange',
                    value=None,
                    type='datetime')

        if job.elapsed_time:
            model['ElapsedTime'] = pywbem.CIMDateTime(job.elapsed_time)
        else:
            model['ElapsedTime'] = pywbem.CIMProperty(
                    name='ElapsedTime',
                    value=None,
                    type='datetime')

        model['Description'] = job.job_name

        model['LocalOrUtcTime'] = self.Values.LocalOrUtcTime.UTC_Time
        model['PercentComplete'] = pywbem.Uint16(job.percent_complete)
        if job.start_time:
            model['StartTime'] = pywbem.CIMDateTime(job.start_time)
        else:
            model['StartTime'] = pywbem.CIMProperty(
                    name='StartTime',
                    value=None,
                    type='datetime')

        model['TimeSubmitted'] = pywbem.CIMDateTime(job.time_submitted)

        # set correct state
        if job.job_state == Job.STATE_QUEUED:
            jobstate = self.Values.JobState.New
            opstate = [self.Values.OperationalStatus.Dormant]
        elif job.job_state == Job.STATE_RUNNING:
            jobstate = self.Values.JobState.Running
            opstate = [self.Values.OperationalStatus.OK]
        elif job.job_state == Job.STATE_FINISHED_OK:
            jobstate = self.Values.JobState.Completed
            opstate = [self.Values.OperationalStatus.OK,
                    self.Values.OperationalStatus.Completed]
        elif job.job_state == Job.STATE_SUSPENDED:
            jobstate = self.Values.JobState.Suspended
            opstate = [self.Values.OperationalStatus.OK]
        elif job.job_state == Job.STATE_FAILED:
            jobstate = self.Values.JobState.Exception
            opstate = [self.Values.OperationalStatus.Error,
                    self.Values.OperationalStatus.Completed]
        elif job.job_state == Job.STATE_TERMINATED:
            jobstate = self.Values.JobState.Terminated
            opstate = [self.Values.OperationalStatus.Stopped]

        model['JobState'] = jobstate
        model['OperationalStatus'] = opstate

        return model

    @cmpi_logging.trace_method
    def set_instance(self, env, instance, modify_existing):
        """Return a newly created or modified instance.

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        instance -- The new pywbem.CIMInstance.  If modifying an existing 
            instance, the properties on this instance have been filtered by 
            the PropertyList from the request.
        modify_existing -- True if ModifyInstance, False if CreateInstance

        Return the new instance.  The keys must be set on the new instance. 
        """
        if not modify_existing:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                    "Creation of Job instances is not supported.")

        job = self.job_manager.get_job_for_instance_id(instance['InstanceID'])
        if not job:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Job not found.")

        try:
            job.lock()
            restart_timer = False

            for (key, value) in instance.iteritems():
                if value is None:
                    continue
                if key == 'DeleteOnCompletion':
                    job.delete_on_completion = value
                    restart_timer = True
                elif key == 'TimeBeforeRemoval':
                    job.time_before_removal = value.total_seconds()
                    restart_timer = True
                elif key == 'JobRunTimes':
                    if value != 1:
                        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                                "JobRunTimes property is not supported.")
                elif key == 'LocalOrUtcTime':
                    if value != self.Values.LocalOrUtcTime.UTC_Time:
                        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                                "Setting of LocalOrUtcTime property is not"
                                " supported.")
                else:
                    raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                            "Setting of %s property is not supported." % (key,))

            if restart_timer:
                job.restart_timer()
        finally:
            job.unlock()
        return instance

    @cmpi_logging.trace_method
    def delete_instance(self, env, instance_name):
        """Delete an instance.

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        instance_name -- A pywbem.CIMInstanceName specifying the instance 
            to delete.
        """
        job = self.job_manager.get_job_for_instance_id(
                instance_name['InstanceID'])
        if not job:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Job not found.")
        if not job.job_status in Job.FINAL_STATES:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Job has not finished.")

        self.job_manager.remove_job(job)

    @cmpi_logging.trace_method
    def cim_method_geterrors(self, env, object_name):
        """Implements LMI_StorageJob.GetErrors()

        If JobState is "Completed" and Operational Status is "Completed"
        then no instance of CIM_Error is returned. \nIf JobState is
        "Exception" then GetErrors may return intances of CIM_Error
        related to the execution of the procedure or method invoked by the
        job.\nIf Operatational Status is not "OK" or "Completed"then
        GetErrors may return CIM_Error instances related to the running of
        the job.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method GetErrors() 
            should be invoked.

        Output parameters:
        Errors -- (type pywbem.CIMInstance(classname='CIM_Error', ...)) 
            If the OperationalStatus on the Job is not "OK", then this
            method will return one or more CIM Error instance(s).
            Otherwise, when the Job is "OK", null is returned.
        """
        job = self.job_manager.get_job_for_instance_id(
                object_name['InstanceID'])
        if not job:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Job not found.")

        if job.error is None:
            errors = []
        else:
            errors = [job.error, ]
        out_params = [
                pywbem.CIMParameter(
                        name='errors',
                        value=errors,
                        type='instance',
                        is_array=True,
                        array_size=len(errors))
        ]
        rval = self.Values.GetErrors.Success

        return (rval, out_params)

    @cmpi_logging.trace_method
    def cim_method_requeststatechange(self, env, object_name,
                                      param_requestedstate=None,
                                      param_timeoutperiod=None):
        """Implements LMI_StorageJob.RequestStateChange()

        Requests that the state of the job be changed to the value
        specified in the RequestedState parameter. Invoking the
        RequestStateChange method multiple times could result in earlier
        requests being overwritten or lost. \nIf 0 is returned, then the
        task completed successfully. Any other return code indicates an
        error condition.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method RequestStateChange() 
            should be invoked.
        param_requestedstate --  The input parameter RequestedState (type pywbem.Uint16 self.Values.RequestStateChange.RequestedState) 
            RequestStateChange changes the state of a job. The possible
            values are as follows: \nStart (2) changes the state to
            \'Running\'. \nSuspend (3) stops the job temporarily. The
            intention is to subsequently restart the job with \'Start\'.
            It might be possible to enter the \'Service\' state while
            suspended. (This is job-specific.) \nTerminate (4) stops the
            job cleanly, saving data, preserving the state, and shutting
            down all underlying processes in an orderly manner. \nKill (5)
            terminates the job immediately with no requirement to save
            data or preserve the state. \nService (6) puts the job into a
            vendor-specific service state. It might be possible to restart
            the job.
            
        param_timeoutperiod --  The input parameter TimeoutPeriod (type pywbem.CIMDateTime) 
            A timeout period that specifies the maximum amount of time that
            the client expects the transition to the new state to take.
            The interval format must be used to specify the TimeoutPeriod.
            A value of 0 or a null parameter indicates that the client has
            no time requirements for the transition. \nIf this property
            does not contain 0 or null and the implementation does not
            support this parameter, a return code of \'Use Of Timeout
            Parameter Not Supported\' must be returned.
            
        Output parameters: none
        """
        job = self.job_manager.get_job_for_instance_id(
                object_name['InstanceID'])
        if not job:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Job not found.")

        try:
            job.lock()
            states = self.Values.RequestStateChange.RequestedState
            retcodes = self.Values.RequestStateChange
            if param_requestedstate == states.Suspend:
                if job.job_state != Job.STATE_QUEUED:
                    # Can suspend only queued jobs
                    rval = retcodes.Invalid_State_Transition
                else:
                    job.change_state(Job.STATE_SUSPENDED)
                    rval = retcodes.Completed_with_No_Error

            elif param_requestedstate == states.Terminate:
                if job.job_state not in (Job.STATE_QUEUED, Job.STATE_SUSPENDED):
                    # Can terminate only queued or suspended jobs
                    rval = retcodes.Invalid_State_Transition
                else:
                    job.cancel()
                    rval = retcodes.Completed_with_No_Error

            elif param_requestedstate == states.Start:
                if job.job_state != Job.STATE_SUSPENDED:
                    # Can start only suspended jobs
                    rval = retcodes.Invalid_State_Transition
                else:
                    job.change_state(Job.STATE_QUEUED)
                    # Enqueue the job again, it may be already processed
                    # (we might get the job in the queue twice, but
                    # we have only one worker thread so it won't collide).
                    self.job_manager.add_job(job)
                    rval = retcodes.Completed_with_No_Error

            else:
                rval = retcodes.Invalid_State_Transition
        finally:
            job.unlock()
        return (rval, [])

    @cmpi_logging.trace_method
    def cim_method_killjob(self, env, object_name,
                           param_deleteonkill=None):
        """Implements LMI_StorageJob.KillJob() """
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED)

    @cmpi_logging.trace_method
    def cim_method_geterror(self, env, object_name):
        """Implements LMI_StorageJob.GetError()

        GetError is deprecated because Error should be an array,not a
        scalar.\nWhen the job is executing or has terminated without
        error, then this method returns no CIM_Error instance. However, if
        the job has failed because of some internal problem or because the
        job has been terminated by a client, then a CIM_Error instance is
        returned.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method GetError() 
            should be invoked.

        Output parameters:
        Error -- (type pywbem.CIMInstance(classname='CIM_Error', ...)) 
            If the OperationalStatus on the Job is not "OK", then this
            method will return a CIM Error instance. Otherwise, when the
            Job is "OK", null is returned.
        """
        job = self.job_manager.get_job_for_instance_id(
                object_name['InstanceID'])
        if not job:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Job not found.")

        if job.error is None:
            error = pywbem.CIMParameter(
                        name='error',
                        value=None,
                        type='instance',
                        is_array=False)
        else:
            error = pywbem.CIMParameter(
                        name='error',
                        value=job.error,
                        type='instance')
        rval = self.Values.GetError.Success
        return (rval, [error])

    class Values(object):
        class JobState(object):
            New = pywbem.Uint16(2)
            Starting = pywbem.Uint16(3)
            Running = pywbem.Uint16(4)
            Suspended = pywbem.Uint16(5)
            Shutting_Down = pywbem.Uint16(6)
            Completed = pywbem.Uint16(7)
            Terminated = pywbem.Uint16(8)
            Killed = pywbem.Uint16(9)
            Exception = pywbem.Uint16(10)
            Service = pywbem.Uint16(11)
            Query_Pending = pywbem.Uint16(12)
            # DMTF_Reserved = 13..32767
            # Vendor_Reserved = 32768..65535

        class LocalOrUtcTime(object):
            Local_Time = pywbem.Uint16(1)
            UTC_Time = pywbem.Uint16(2)

        class OperationalStatus(object):
            Unknown = pywbem.Uint16(0)
            Other = pywbem.Uint16(1)
            OK = pywbem.Uint16(2)
            Degraded = pywbem.Uint16(3)
            Stressed = pywbem.Uint16(4)
            Predictive_Failure = pywbem.Uint16(5)
            Error = pywbem.Uint16(6)
            Non_Recoverable_Error = pywbem.Uint16(7)
            Starting = pywbem.Uint16(8)
            Stopping = pywbem.Uint16(9)
            Stopped = pywbem.Uint16(10)
            In_Service = pywbem.Uint16(11)
            No_Contact = pywbem.Uint16(12)
            Lost_Communication = pywbem.Uint16(13)
            Aborted = pywbem.Uint16(14)
            Dormant = pywbem.Uint16(15)
            Supporting_Entity_in_Error = pywbem.Uint16(16)
            Completed = pywbem.Uint16(17)
            Power_Mode = pywbem.Uint16(18)
            Relocating = pywbem.Uint16(19)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 0x8000..

        class GetErrors(object):
            Success = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unspecified_Error = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            Access_Denied = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            # Vendor_Specific = 32768..65535

        class GetError(object):
            Success = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unspecified_Error = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            Access_Denied = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            # Vendor_Specific = 32768..65535

        class RequestStateChange(object):
            Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown_Unspecified_Error = pywbem.Uint32(2)
            Can_NOT_complete_within_Timeout_Period = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Transition_Started = pywbem.Uint32(4096)
            Invalid_State_Transition = pywbem.Uint32(4097)
            Use_of_Timeout_Parameter_Not_Supported = pywbem.Uint32(4098)
            Busy = pywbem.Uint32(4099)
            # Method_Reserved = 4100..32767
            # Vendor_Specific = 32768..65535
            class RequestedState(object):
                Start = pywbem.Uint16(2)
                Suspend = pywbem.Uint16(3)
                Terminate = pywbem.Uint16(4)
                Kill = pywbem.Uint16(5)
                Service = pywbem.Uint16(6)
                # DMTF_Reserved = 7..32767
                # Vendor_Reserved = 32768..65535

class LMI_OwningJobElement(CIMProvider2):
    """ Instrumentation of LMI_OwningJobElement class and its subclasses."""

    @cmpi_logging.trace_method
    def __init__(self, classname, job_manager):
        self.classname = classname
        self.job_manager = job_manager

    @cmpi_logging.trace_method
    def get_instance(self, env, model):
        """Return an instance."""
        instance_id = model['OwnedElement']['InstanceID']
        job = self.job_manager.get_job_for_instance_id(instance_id)
        if not job:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "OwnedElement not found.")

        if job.owning_element != model['OwningElement']:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "OwnedElement is not associated to OwningElement.")
        return model

    @cmpi_logging.trace_method
    def enum_instances(self, env, model, keys_only):
        """Enumerate instances."""
        model.path.update({'OwnedElement': None, 'OwningElement': None})
        for job in self.job_manager.jobs.values():
            if job.owning_element:
                model['OwnedElement'] = job.get_name()
                model['OwningElement'] = job.owning_element
                yield model

    @cmpi_logging.trace_method
    def references(self, env, object_name, model, result_class_name, role,
                   result_role, keys_only):
        """Instrument Associations."""
        ch = env.get_cimom_handle()
        if ch.is_subclass(object_name.namespace,
                  sub=object_name.classname,
                  super='CIM_ManagedElement') or \
            ch.is_subclass(object_name.namespace,
                  sub=object_name.classname,
                  super=self.job_manager.job_classname):
            return self.simple_refs(env, object_name, model,
                          result_class_name, role, result_role, keys_only)

class LMI_AffectedJobElement(CIMProvider2):
    """ Instrumentation of LMI_AffectedJobElement class and its subclasses."""

    @cmpi_logging.trace_method
    def __init__(self, classname, job_manager):
        self.classname = classname
        self.job_manager = job_manager

    @cmpi_logging.trace_method
    def get_instance(self, env, model):
        """Return an instance."""
        instance_id = model['AffectingElement']['InstanceID']
        job = self.job_manager.get_job_for_instance_id(instance_id)
        if not job:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "AffectingElement not found.")

        if model['AffectedElement'] not in job.affected_elements:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "AffectedElement is not associated to AffectingElement.")
        model['ElementEffects'] = [self.Values.ElementEffects.Unknown, ]
        return model

    @cmpi_logging.trace_method
    def enum_instances(self, env, model, keys_only):
        """Enumerate instances."""
        model.path.update({'AffectingElement': None, 'AffectedElement': None})
        for job in self.job_manager.jobs.values():
            for element in job.affected_elements:
                model['AffectingElement'] = job.get_name()
                model['AffectedElement'] = element
                if keys_only:
                    yield model
                else:
                    yield self.get_instance(env, model)

    @cmpi_logging.trace_method
    def references(self, env, object_name, model, result_class_name, role,
                   result_role, keys_only):
        """Instrument Associations."""
        ch = env.get_cimom_handle()
        if ch.is_subclass(object_name.namespace,
                  sub=object_name.classname,
                  super='CIM_ManagedElement') or \
            ch.is_subclass(object_name.namespace,
                  sub=object_name.classname,
                  super=self.job_manager.job_classname):
            return self.simple_refs(env, object_name, model,
                          result_class_name, role, result_role, keys_only)

    class Values(object):
        class ElementEffects(object):
            Unknown = pywbem.Uint16(0)
            Other = pywbem.Uint16(1)
            Exclusive_Use = pywbem.Uint16(2)
            Performance_Impact = pywbem.Uint16(3)
            Element_Integrity = pywbem.Uint16(4)
            Create = pywbem.Uint16(5)


class LMI_MethodResult(CIMProvider2):
    """Instrumentation of LMI_MethodResult class and its subclasses."""

    @cmpi_logging.trace_method
    def __init__(self, classname, job_manager):
        self.classname = classname
        self.job_manager = job_manager

    @cmpi_logging.trace_method
    def get_instance(self, env, model, job=None):
        """Return an instance."""
        if not job:
            instance_id = model['InstanceID']
            job = self.job_manager.get_job_for_instance_id(
                    instance_id, self.classname)
        if not job:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Job not found.")

        model['Description'] = job.job_name
        if job.job_state in Job.FINAL_STATES:
            model['PostCallIndication'] = pywbem.CIMProperty(
                    name='PostCallIndication',
                    value=job.get_post_call())
        else:
            model['PostCallIndication'] = pywbem.CIMProperty(
                    name='PostCallIndication',
                    type='instance',
                    value=None)
        model['PreCallIndication'] = pywbem.CIMProperty(
                    name='PreCallIndication',
                    value=job.get_pre_call())
        return model

    @cmpi_logging.trace_method
    def enum_instances(self, env, model, keys_only):
        """Enumerate instances."""
        model.path.update({'InstanceID': None})
        for job in self.job_manager.jobs.values():
            model['InstanceID'] = job.get_instance_id(
                    classname=self.classname)
            if keys_only:
                yield model
            else:
                yield self.get_instance(env, model, job)

class LMI_AssociatedJobMethodResult(CIMProvider2):
    """ Instrumentation of LMI_AssociatedJobMethodResult class and its subclasses."""

    @cmpi_logging.trace_method
    def __init__(self, classname, job_manager):
        self.classname = classname
        self.job_manager = job_manager

    @cmpi_logging.trace_method
    def get_instance(self, env, model):
        """Return an instance."""
        instance_id = model['Job']['InstanceID']
        job = self.job_manager.get_job_for_instance_id(instance_id)
        if not job:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Job not found.")

        expected_result_id = job.get_instance_id(
                classname=self.job_manager.method_result_classname)
        if model['JobParameters']['InstanceID'] != expected_result_id:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Job is not associated to JobParameters.")
        return model

    @cmpi_logging.trace_method
    def enum_instances(self, env, model, keys_only):
        """Enumerate instances."""
        model.path.update({'JobParameters': None, 'Job': None})
        for job in self.job_manager.jobs.values():
            if job.owning_element:
                model['Job'] = job.get_name()
                model['JobParameters'] = pywbem.CIMInstanceName(
                    classname=self.job_manager.method_result_classname,
                    namespace=self.job_manager.namespace,
                    keybindings={
                        'InstanceID': job.get_instance_id(
                            classname=self.job_manager.method_result_classname)
                })
                yield model

    @cmpi_logging.trace_method
    def references(self, env, object_name, model, result_class_name, role,
                   result_role, keys_only):
        """Instrument Associations."""
        ch = env.get_cimom_handle()
        if ch.is_subclass(object_name.namespace,
                  sub=object_name.classname,
                  super=self.job_manager.method_result_classname) or \
            ch.is_subclass(object_name.namespace,
                  sub=object_name.classname,
                  super=self.job_manager.job_classname):
            return self.simple_refs(env, object_name, model,
                          result_class_name, role, result_role, keys_only)

