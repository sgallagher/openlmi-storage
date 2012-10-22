# OpenLMI Storage Provider
#
# Copyright (C) 2012 Red Hat, Inc.  All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Python Provider for LMI_FileSystemConfigurationService

Instruments the CIM class LMI_FileSystemConfigurationService

"""

from wrapper.common import *
import pywbem
from pywbem.cim_provider2 import CIMProvider2
import util.fs

class LMI_FileSystemConfigurationService(CIMProvider2):
    """Instrument the CIM class LMI_FileSystemConfigurationService 

    POC FileSystemConfigurationService instrumentation.
    
    """

    def __init__ (self, env):
        logger = env.get_logger()
        logger.log_debug('Initializing provider %s from %s' \
                % (self.__class__.__name__, __file__))

    def get_instance(self, env, model):
        """Return an instance.

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        model -- A template of the pywbem.CIMInstance to be returned.  The 
            key properties are set on this instance to correspond to the 
            instanceName that was requested.  The properties of the model
            are already filtered according to the PropertyList from the 
            request.  Only properties present in the model need to be
            given values.  If you prefer, you can set all of the 
            values, and the instance will be filtered for you. 

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, unrecognized 
            or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the CIM Class does exist, but the requested CIM 
            Instance does not exist in the specified namespace)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """
        
        logger = env.get_logger()
        logger.log_debug('Entering %s.get_instance()' \
                % self.__class__.__name__)
        

        #model['AvailableRequestedStates'] = [self.Values.AvailableRequestedStates.<VAL>,] # TODO 
        #model['Caption'] = '' # TODO 
        model['CommunicationStatus'] = self.Values.CommunicationStatus.Communication_OK
        model['Description'] = 'Filesystem creation and mounting service'
        #model['DetailedStatus'] = self.Values.DetailedStatus.<VAL> # TODO 
        #model['ElementName'] = '' # TODO 
        model['EnabledDefault'] = self.Values.EnabledDefault.Enabled
        model['EnabledState'] = self.Values.EnabledState.Enabled
        #model['Generation'] = pywbem.Uint64() # TODO 
        model['HealthState'] = self.Values.HealthState.OK
        #model['InstallDate'] = pywbem.CIMDateTime() # TODO 
        #model['InstanceID'] = '' # TODO 
        model['OperatingStatus'] = self.Values.OperatingStatus.Servicing
        model['OperationalStatus'] = [self.Values.OperationalStatus.OK,] # TODO 
        #model['OtherEnabledState'] = '' # TODO 
        #model['PrimaryOwnerContact'] = '' # TODO 
        model['PrimaryOwnerName'] = 'I am my own master!'
        model['PrimaryStatus'] = self.Values.PrimaryStatus.OK
        model['RequestedState'] = self.Values.RequestedState.Unknown
        model['Started'] = True
        #model['StartMode'] = self.Values.StartMode.<VAL> # TODO 
        #model['Status'] = self.Values.Status.<VAL> # TODO 
        #model['StatusDescriptions'] = ['',] # TODO 
        #model['TimeOfLastStateChange'] = pywbem.CIMDateTime() # TODO 
        model['TransitioningToState'] = self.Values.TransitioningToState.Not_Applicable
        return model

    def enum_instances(self, env, model, keys_only):
        """Enumerate instances.

        The WBEM operations EnumerateInstances and EnumerateInstanceNames
        are both mapped to this method. 
        This method is a python generator

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        model -- A template of the pywbem.CIMInstances to be generated.  
            The properties of the model are already filtered according to 
            the PropertyList from the request.  Only properties present in 
            the model need to be given values.  If you prefer, you can 
            always set all of the values, and the instance will be filtered 
            for you. 
        keys_only -- A boolean.  True if only the key properties should be
            set on the generated instances.

        Possible Errors:
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.enum_instances()' \
                % self.__class__.__name__)
                
        # Prime model.path with knowledge of the keys, so key values on
        # the CIMInstanceName (model.path) will automatically be set when
        # we set property values on the model. 
        model.path.update({'CreationClassName': None, 'SystemName': None,
            'Name': None, 'SystemCreationClassName': None})
        
        model['SystemName'] = LMI_SYSTEM_NAME
        model['SystemCreationClassName'] = LMI_SYSTEM_CLASS_NAME
        model['CreationClassName'] = 'LMI_FileSystemConfigurationService'    
        model['Name'] = 'LMI_FileSystemConfigurationService'
        if keys_only:
            yield model
        else:
            try:
                yield self.get_instance(env, model)
            except pywbem.CIMError, (num, msg):
                if num not in (pywbem.CIM_ERR_NOT_FOUND, 
                               pywbem.CIM_ERR_ACCESS_DENIED):
                    raise

    def set_instance(self, env, instance, modify_existing):
        """Return a newly created or modified instance.

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        instance -- The new pywbem.CIMInstance.  If modifying an existing 
            instance, the properties on this instance have been filtered by 
            the PropertyList from the request.
        modify_existing -- True if ModifyInstance, False if CreateInstance

        Return the new instance.  The keys must be set on the new instance. 

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_NOT_SUPPORTED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, unrecognized 
            or otherwise incorrect parameters)
        CIM_ERR_ALREADY_EXISTS (the CIM Instance already exists -- only 
            valid if modify_existing is False, indicating that the operation
            was CreateInstance)
        CIM_ERR_NOT_FOUND (the CIM Instance does not exist -- only valid 
            if modify_existing is True, indicating that the operation
            was ModifyInstance)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.set_instance()' \
                % self.__class__.__name__)
        # TODO create or modify the instance
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED) # Remove to implement
        return instance

    def delete_instance(self, env, instance_name):
        """Delete an instance.

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        instance_name -- A pywbem.CIMInstanceName specifying the instance 
            to delete.

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_NOT_SUPPORTED
        CIM_ERR_INVALID_NAMESPACE
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, unrecognized 
            or otherwise incorrect parameters)
        CIM_ERR_INVALID_CLASS (the CIM Class does not exist in the specified 
            namespace)
        CIM_ERR_NOT_FOUND (the CIM Class does exist, but the requested CIM 
            Instance does not exist in the specified namespace)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """ 

        logger = env.get_logger()
        logger.log_debug('Entering %s.delete_instance()' \
                % self.__class__.__name__)

        # TODO delete the resource
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED) # Remove to implement
        
    def cim_method_requeststatechange(self, env, object_name,
                                      param_requestedstate=None,
                                      param_timeoutperiod=None):
        """Implements LMI_FileSystemConfigurationService.RequestStateChange()

        Requests that the state of the element be changed to the value
        specified in the RequestedState parameter. When the requested
        state change takes place, the EnabledState and RequestedState of
        the element will be the same. Invoking the RequestStateChange
        method multiple times could result in earlier requests being
        overwritten or lost. \nA return code of 0 shall indicate the state
        change was successfully initiated. \nA return code of 3 shall
        indicate that the state transition cannot complete within the
        interval specified by the TimeoutPeriod parameter. \nA return code
        of 4096 (0x1000) shall indicate the state change was successfully
        initiated, a ConcreteJob has been created, and its reference
        returned in the output parameter Job. Any other return code
        indicates an error condition.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method RequestStateChange() 
            should be invoked.
        param_requestedstate --  The input parameter RequestedState (type pywbem.Uint16 self.Values.RequestStateChange.RequestedState) 
            The state requested for the element. This information will be
            placed into the RequestedState property of the instance if the
            return code of the RequestStateChange method is 0 (\'Completed
            with No Error\'), or 4096 (0x1000) (\'Job Started\'). Refer to
            the description of the EnabledState and RequestedState
            properties for the detailed explanations of the RequestedState
            values.
            
        param_timeoutperiod --  The input parameter TimeoutPeriod (type pywbem.CIMDateTime) 
            A timeout period that specifies the maximum amount of time that
            the client expects the transition to the new state to take.
            The interval format must be used to specify the TimeoutPeriod.
            A value of 0 or a null parameter indicates that the client has
            no time requirements for the transition. \nIf this property
            does not contain 0 or null and the implementation does not
            support this parameter, a return code of \'Use Of Timeout
            Parameter Not Supported\' shall be returned.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.RequestStateChange)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...)) 
            May contain a reference to the ConcreteJob created to track the
            state transition initiated by the method invocation.
            

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, 
            unrecognized or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the target CIM Class or instance does not 
            exist in the specified namespace)
        CIM_ERR_METHOD_NOT_AVAILABLE (the CIM Server is unable to honor 
            the invocation request)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_requeststatechange()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('job', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.RequestStateChange)
        #return (rval, out_params)
        
    def cim_method_stopservice(self, env, object_name):
        """Implements LMI_FileSystemConfigurationService.StopService()

        The StopService method places the Service in the stopped state.
        Note that the function of this method overlaps with the
        RequestedState property. RequestedState was added to the model to
        maintain a record (such as a persisted value) of the last state
        request. Invoking the StopService method should set the
        RequestedState property appropriately. The method returns an
        integer value of 0 if the Service was successfully stopped, 1 if
        the request is not supported, and any other number to indicate an
        error. In a subclass, the set of possible return codes could be
        specified using a ValueMap qualifier on the method. The strings to
        which the ValueMap contents are translated can also be specified
        in the subclass as a Values array qualifier. \n\nNote: The
        semantics of this method overlap with the RequestStateChange
        method that is inherited from EnabledLogicalElement. This method
        is maintained because it has been widely implemented, and its
        simple "stop" semantics are convenient to use.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method StopService() 
            should be invoked.

        Returns a two-tuple containing the return value (type pywbem.Uint32)
        and a list of CIMParameter objects representing the output parameters

        Output parameters: none

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, 
            unrecognized or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the target CIM Class or instance does not 
            exist in the specified namespace)
        CIM_ERR_METHOD_NOT_AVAILABLE (the CIM Server is unable to honor 
            the invocation request)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_stopservice()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #rval = # TODO (type pywbem.Uint32)
        #return (rval, out_params)
        
    def cim_method_modifyfilesystem(self, env, object_name,
                                    param_elementname=None,
                                    param_inuseoptions=None,
                                    param_goal=None,
                                    param_waittime=None,
                                    param_theelement=None):
        """Implements LMI_FileSystemConfigurationService.ModifyFileSystem()

        Start a job to modify a previously created FileSystem. If the
        operation completes successfully and did not require a
        long-running ConcreteJob, it will return 0. If 4096/0x1000 is
        returned, a ConcreteJob will be started to modify the element. A
        Reference to the ConcreteJob will be returned in the output
        parameter Job. If any other value is returned, either the job will
        not be started, or if started, no action will be taken. \nThis
        method MUST return a CIM_Error representing that a single named
        property of a setting (or other) parameter (either reference or
        embedded object) has an invalid value or that an invalid
        combination of named properties of a setting (or other) parameter
        (either reference or embedded object) has been requested. \nThe
        parameter TheElement specifies the FileSystem to be modified. This
        element MUST be associated via ElementSettingData with a
        FileSystemSetting which is in turn associated via
        SettingGeneratedByCapabilities to a FileSystemCapabilities
        supported by this FileSystemConfigurationService. \nThe desired
        settings for the FileSystem are specified by the Goal parameter.
        Goal is an element of class CIM_FileSystemSetting, or a derived
        class, encoded as a string-valued embedded instance parameter;
        this allows the client to specify the properties desired for the
        file system. The Goal parameter includes information that can be
        used by the vendor to compute the required size of the FileSystem.
        If the operation would result in a change in the size of the file
        system, the StorageExtent identified by the ResidesOnExtent
        association will be used to determine how to implement the change.
        If the StorageExtent cannot be expanded to support the goal size,
        an appropriate error value will be returned, and no action will be
        taken. If the operation succeeds, the ResidesOnExtent association
        might reference a different StorageExtent.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method ModifyFileSystem() 
            should be invoked.
        param_elementname --  The input parameter ElementName (type unicode) 
            A end user relevant name for the FileSystem being modified. If
            NULL, then the name will not be changed. If not NULL, this
            parameter will supply a new name for the FileSystem element.
            
        param_inuseoptions --  The input parameter InUseOptions (type pywbem.Uint16 self.Values.ModifyFileSystem.InUseOptions) 
            An enumerated integer that specifies the action to take if the
            FileSystem is still in use when this request is made. This
            option is only relevant if the FileSystem must be made
            unavailable while the request is being executed.
            
        param_goal --  The input parameter Goal (type pywbem.CIMInstance(classname='CIM_FileSystemSetting', ...)) 
            The requirements for the FileSystem element to maintain. This
            is an element of class CIM_FileSystemSetting, or a derived
            class, encoded as a string-valued embedded instance parameter;
            this allows the client to specify the properties desired for
            the file system. If NULL or the empty string, the FileSystem
            service attributes will not be changed. If not NULL, this
            parameter will supply new settings that replace or are merged
            with the current settings of the FileSystem element.
            
        param_waittime --  The input parameter WaitTime (type pywbem.Uint32) 
            An integer that indicates the time (in seconds) that the
            provider must wait before performing the request on this
            FileSystem. If WaitTime is not zero, the method will create a
            job, if supported by the provider, and return immediately. If
            the provider does not support asynchronous jobs, there is a
            possibility that the client could time-out before the job is
            completed. \nThe combination of InUseOptions = \'4\' and
            WaitTime =\'0\' (the default) is interpreted as \'Wait
            (forever) until Quiescence, then Execute Request\' and will be
            performed asynchronously if possible.
            
        param_theelement --  The input parameter TheElement (type REF (pywbem.CIMInstanceName(classname='CIM_FileSystem', ...)) 
            The FileSystem element to modify.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.ModifyFileSystem)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...)) 
            Reference to the job (may be null if job completed).
            

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, 
            unrecognized or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the target CIM Class or instance does not 
            exist in the specified namespace)
        CIM_ERR_METHOD_NOT_AVAILABLE (the CIM Server is unable to honor 
            the invocation request)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_modifyfilesystem()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('job', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.ModifyFileSystem)
        #return (rval, out_params)
        
    def cim_method_deletefilesystem(self, env, object_name,
                                    param_waittime=None,
                                    param_thefilesystem=None,
                                    param_inuseoptions=None):
        """Implements LMI_FileSystemConfigurationService.DeleteFileSystem()

        Start a job to delete a FileSystem. If the FileSystem cannot be
        deleted, no action will be taken, and the Return Value will be
        4097/0x1001. If the method completed successfully and did not
        require a long-running ConcreteJob, it will return 0. If
        4096/0x1000 is returned, a ConcreteJob will be started to delete
        the FileSystem. A Reference to the ConcreteJob will be returned in
        the output parameter Job.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method DeleteFileSystem() 
            should be invoked.
        param_waittime --  The input parameter WaitTime (type pywbem.Uint32) 
            An integer that indicates the time (in seconds) that the
            provider must wait before deleting this FileSystem. If
            WaitTime is not zero, the method will create a job, if
            supported by the provider, and return immediately. If the
            provider does not support asynchronous jobs, there is a
            possibility that the client could time-out before the job is
            completed. \nThe combination of InUseOptions = \'4\' and
            WaitTime =\'0\' (the default) is interpreted as \'Wait
            (forever) until Quiescence, then Delete Filesystem\' and will
            be performed asynchronously if possible.
            
        param_thefilesystem --  The input parameter TheFileSystem (type REF (pywbem.CIMInstanceName(classname='CIM_ManagedElement', ...)) 
            An element or association that uniquely identifies the
            FileSystem to be deleted.
            
        param_inuseoptions --  The input parameter InUseOptions (type pywbem.Uint16 self.Values.DeleteFileSystem.InUseOptions) 
            An enumerated integer that specifies the action to take if the
            FileSystem is still in use when this request is made.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.DeleteFileSystem)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...)) 
            Reference to the job (may be null if job completed).
            

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, 
            unrecognized or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the target CIM Class or instance does not 
            exist in the specified namespace)
        CIM_ERR_METHOD_NOT_AVAILABLE (the CIM Server is unable to honor 
            the invocation request)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_deletefilesystem()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('job', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.DeleteFileSystem)
        #return (rval, out_params)
        
    def cim_method_changeaffectedelementsassignedsequence(self, env, object_name,
                                                          param_managedelements,
                                                          param_assignedsequence):
        """Implements LMI_FileSystemConfigurationService.ChangeAffectedElementsAssignedSequence()

        This method is called to change relative sequence in which order
        the ManagedElements associated to the Service through
        CIM_ServiceAffectsElement association are affected. In the case
        when the Service represents an interface for client to execute
        extrinsic methods and when it is used for grouping of the managed
        elements that could be affected, the ordering represents the
        relevant priority of the affected managed elements with respect to
        each other. \nAn ordered array of ManagedElement instances is
        passed to this method, where each ManagedElement instance shall be
        already be associated with this Service instance via
        CIM_ServiceAffectsElement association. If one of the
        ManagedElements is not associated to the Service through
        CIM_ServiceAffectsElement association, the implementation shall
        return a value of 2 ("Error Occured"). \nUpon successful execution
        of this method, if the AssignedSequence parameter is NULL, the
        value of the AssignedSequence property on each instance of
        CIM_ServiceAffectsElement shall be updated such that the values of
        AssignedSequence properties shall be monotonically increasing in
        correlation with the position of the referenced ManagedElement
        instance in the ManagedElements input parameter. That is, the
        first position in the array shall have the lowest value for
        AssignedSequence. The second position shall have the second lowest
        value, and so on. Upon successful execution, if the
        AssignedSequence parameter is not NULL, the value of the
        AssignedSequence property of each instance of
        CIM_ServiceAffectsElement referencing the ManagedElement instance
        in the ManagedElements array shall be assigned the value of the
        corresponding index of the AssignedSequence parameter array. For
        ManagedElements instances which are associated with the Service
        instance via CIM_ServiceAffectsElement and are not present in the
        ManagedElements parameter array, the AssignedSequence property on
        the CIM_ServiceAffects association shall be assigned a value of 0.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method ChangeAffectedElementsAssignedSequence() 
            should be invoked.
        param_managedelements --  The input parameter ManagedElements (type REF (pywbem.CIMInstanceName(classname='CIM_ManagedElement', ...)) (Required)
            An array of ManagedElements.
            
        param_assignedsequence --  The input parameter AssignedSequence (type [pywbem.Uint16,]) (Required)
            An array of integers representing AssignedSequence for the
            ManagedElement in the corresponding index of the
            ManagedElements parameter.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.ChangeAffectedElementsAssignedSequence)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...)) 
            Reference to the job spawned if the operation continues after
            the method returns. (May be null if the task is completed).
            

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, 
            unrecognized or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the target CIM Class or instance does not 
            exist in the specified namespace)
        CIM_ERR_METHOD_NOT_AVAILABLE (the CIM Server is unable to honor 
            the invocation request)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_changeaffectedelementsassignedsequence()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('job', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.ChangeAffectedElementsAssignedSequence)
        #return (rval, out_params)
        
    def cim_method_createfilesystem(self, env, object_name,
                                    param_goal=None,
                                    param_elementname=None,
                                    param_theelement=None,
                                    param_inextent=None):
        """Implements LMI_FileSystemConfigurationService.CreateFileSystem()

        Start a job to create a FileSystem on a StorageExtent. If the
        operation completes successfully and did not require a
        long-running ConcreteJob, it will return 0. If 4096/0x1000 is
        returned, a ConcreteJob will be started to create the element. A
        Reference to the ConcreteJob will be returned in the output
        parameter Job. If any other value is returned, the job will not be
        started, and no action will be taken. \nThis method MUST return a
        CIM_Error representing that a single named property of a setting
        (or other) parameter (either reference or embedded object) has an
        invalid value or that an invalid combination of named properties
        of a setting (or other) parameter (either reference or embedded
        object) has been requested. \nThe parameter TheElement will
        contain a Reference to the FileSystem if this operation completed
        successfully. \nThe StorageExtent to use is specified by the
        InExtent parameter. If this is NULL, a default StorageExtent will
        be created in a vendor-specific way and used. One way to create
        the default StorageExtent is to use one of the canned settings
        supported by the StorageConfigurationService hosted by the host
        hosting the FileSystemConfigurationService. \nThe desired settings
        for the FileSystem are specified by the Goal parameter. Goal is an
        element of class CIM_FileSystemSetting, or a derived class,
        encoded as a string-valued embedded object parameter; this allows
        the client to specify the properties desired for the file system.
        The Goal parameter includes information that can be used by the
        vendor to compute the size of the FileSystem. If the StorageExtent
        specified here cannot support the goal size, an appropriate error
        value will be returned, and no action will be taken. \nA
        ResidesOnExtent association is created between the created
        FileSystem and the StorageExtent used for it.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method CreateFileSystem() 
            should be invoked.
        param_goal --  The input parameter Goal (type pywbem.CIMInstance(classname='CIM_FileSystemSetting', ...)) 
            The requirements for the FileSystem element to maintain. This
            is an element of class CIM_FileSystemSetting, or a derived
            class, encoded as a string-valued embedded instance parameter;
            this allows the client to specify the properties desired for
            the file system. If NULL or the empty string, the
            FileSystemConfigurationService will use a vendor-specific
            default Goal obtained by using the FileSystemCapabilities
            element specified by the DefaultElementCapabilities
            association to obtain a default FileSystemSetting element.
            
        param_elementname --  The input parameter ElementName (type unicode) 
            A end user relevant name for the FileSystem being created. If
            NULL, a system-supplied default name can be used. The value
            will be stored in the \'ElementName\' property for the created
            element.
            
        param_theelement --  The input parameter TheElement (type REF (pywbem.CIMInstanceName(classname='CIM_FileSystem', ...)) 
            The newly created FileSystem.
            
        param_inextent --  The input parameter InExtent (type REF (pywbem.CIMInstanceName(classname='CIM_StorageExtent', ...)) 
            The StorageExtent on which the created FileSystem will reside.
            If this is NULL, a default StorageExtent will be created in a
            vendor-specific way and used. One way to create the default
            StorageExtent is to use one of the default settings supported
            by the StorageConfigurationService on the same hosting
            ComputerSystem as the FileSystemConfigurationService.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.CreateFileSystem)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...)) 
            Reference to the job (may be null if job completed).
            
        TheElement -- (type REF (pywbem.CIMInstanceName(classname='CIM_FileSystem', ...)) 
            The newly created FileSystem.
            

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, 
            unrecognized or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the target CIM Class or instance does not 
            exist in the specified namespace)
        CIM_ERR_METHOD_NOT_AVAILABLE (the CIM Server is unable to honor 
            the invocation request)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_createfilesystem()' \
                % self.__class__.__name__)

        if param_goal is not None:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, "Goal parameter is not supported.")
        if param_theelement is not None:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, "TheElement parameter is not supported.")
        if param_inextent is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, "InExtent parameter must be specified.")
        if param_inextent["CreationClassName"] != "LMI_LogicalDisk":
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, "InExtent parameter must be LMI_LogicalDisk.")

        label = param_elementname
        path = param_inextent["DeviceID"]

        device = storage.devicetree.getDeviceByPath(path)
        if not logicalDiskManager.isExposed(device):
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, "InExtent parameter must be valid LMI_LogicalDisk.")
            
        fs = util.fs.createFilesystem(device, label)
        if fs:
            out_params = []
            out_params+= [pywbem.CIMParameter('TheElement', type='reference', 
                value=pywbem.CIMInstanceName(classname='LMI_LocalFileSystem', namespace=LMI_NAMESPACE,
                    keybindings = {"CreationClassName" : "LMI_LocalFileSystem",
                        "CSCreationClassName" : LMI_SYSTEM_CLASS_NAME,
                        "CSName" : LMI_SYSTEM_NAME,
                        "Name" : device.path
                }))]
            rval = self.Values.CreateFileSystem.Job_Completed_with_No_Error
            return (rval, out_params)
        else:
            return (self.Values.CreateFileSystem.Failed, [])

    def cim_method_startservice(self, env, object_name):
        """Implements LMI_FileSystemConfigurationService.StartService()

        The StartService method places the Service in the started state.
        Note that the function of this method overlaps with the
        RequestedState property. RequestedState was added to the model to
        maintain a record (such as a persisted value) of the last state
        request. Invoking the StartService method should set the
        RequestedState property appropriately. The method returns an
        integer value of 0 if the Service was successfully started, 1 if
        the request is not supported, and any other number to indicate an
        error. In a subclass, the set of possible return codes could be
        specified using a ValueMap qualifier on the method. The strings to
        which the ValueMap contents are translated can also be specified
        in the subclass as a Values array qualifier. \n\nNote: The
        semantics of this method overlap with the RequestStateChange
        method that is inherited from EnabledLogicalElement. This method
        is maintained because it has been widely implemented, and its
        simple "start" semantics are convenient to use.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method StartService() 
            should be invoked.

        Returns a two-tuple containing the return value (type pywbem.Uint32)
        and a list of CIMParameter objects representing the output parameters

        Output parameters: none

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, 
            unrecognized or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the target CIM Class or instance does not 
            exist in the specified namespace)
        CIM_ERR_METHOD_NOT_AVAILABLE (the CIM Server is unable to honor 
            the invocation request)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_startservice()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #rval = # TODO (type pywbem.Uint32)
        #return (rval, out_params)

    def cim_method_mountfilesystem(self, env, object_name,
                                   param_where=None,
                                   param_theelement=None):
        """Implements LMI_FileSystemConfigurationService.MountFileSystem()

        Mount a filesystem to given location.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method MountFileSystem() 
            should be invoked.
        param_where --  The input parameter Where (type unicode) 
            Mount point.
            
        param_theelement --  The input parameter TheElement (type REF (pywbem.CIMInstanceName(classname='CIM_FileSystem', ...)) 
            File system to mount.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.MountFileSystem)
        and a list of CIMParameter objects representing the output parameters

        Output parameters: none

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, 
            unrecognized or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the target CIM Class or instance does not 
            exist in the specified namespace)
        CIM_ERR_METHOD_NOT_AVAILABLE (the CIM Server is unable to honor 
            the invocation request)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_mountfilesystem()' \
                % self.__class__.__name__)

        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented

        
    class Values(object):
        class DetailedStatus(object):
            Not_Available = pywbem.Uint16(0)
            No_Additional_Information = pywbem.Uint16(1)
            Stressed = pywbem.Uint16(2)
            Predictive_Failure = pywbem.Uint16(3)
            Non_Recoverable_Error = pywbem.Uint16(4)
            Supporting_Entity_in_Error = pywbem.Uint16(5)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 0x8000..

        class RequestedState(object):
            Unknown = pywbem.Uint16(0)
            Enabled = pywbem.Uint16(2)
            Disabled = pywbem.Uint16(3)
            Shut_Down = pywbem.Uint16(4)
            No_Change = pywbem.Uint16(5)
            Offline = pywbem.Uint16(6)
            Test = pywbem.Uint16(7)
            Deferred = pywbem.Uint16(8)
            Quiesce = pywbem.Uint16(9)
            Reboot = pywbem.Uint16(10)
            Reset = pywbem.Uint16(11)
            Not_Applicable = pywbem.Uint16(12)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 32768..65535

        class HealthState(object):
            Unknown = pywbem.Uint16(0)
            OK = pywbem.Uint16(5)
            Degraded_Warning = pywbem.Uint16(10)
            Minor_failure = pywbem.Uint16(15)
            Major_failure = pywbem.Uint16(20)
            Critical_failure = pywbem.Uint16(25)
            Non_recoverable_error = pywbem.Uint16(30)
            # DMTF_Reserved = ..
            # Vendor_Specific = 32768..65535

        class ModifyFileSystem(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            FileSystem_In_Use__cannot_Modify = pywbem.Uint32(6)
            Cannot_satisfy_new_Goal_ = pywbem.Uint32(7)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            # Method_Reserved = 4098..32767
            # Vendor_Specific = 32768..65535
            class InUseOptions(object):
                Do_Not_Execute_Request = pywbem.Uint16(2)
                Wait_for_specified_time__then_Execute_Request_Immediately = pywbem.Uint16(3)
                Try_to_Quiesce_for_specified_time__then_Execute_Request_Immediately = pywbem.Uint16(4)
                # DMTF_Reserved = ..
                # Vendor_Defined = 0x1000..0xFFFF

        class DeleteFileSystem(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed__Unspecified_Reasons = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            FileSystem_in_use__Failed = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            # Method_Parameters_Checked___Job_Started = 0x1000
            # Method_Reserved = 0x1001..0x7FFF
            # Vendor_Specific = 0x8000..
            class InUseOptions(object):
                Do_Not_Delete = pywbem.Uint16(2)
                Wait_for_specified_time__then_Delete_Immediately = pywbem.Uint16(3)
                Attempt_Quiescence_for_specified_time__then_Delete_Immediately = pywbem.Uint16(4)
                # DMTF_Reserved = ..
                # Vendor_Defined = 0x1000..0xFFFF

        class ChangeAffectedElementsAssignedSequence(object):
            Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Error_Occured = pywbem.Uint32(2)
            Busy = pywbem.Uint32(3)
            Invalid_Reference = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            Access_Denied = pywbem.Uint32(6)
            # DMTF_Reserved = 7..32767
            # Vendor_Specified = 32768..65535

        class TransitioningToState(object):
            Unknown = pywbem.Uint16(0)
            Enabled = pywbem.Uint16(2)
            Disabled = pywbem.Uint16(3)
            Shut_Down = pywbem.Uint16(4)
            No_Change = pywbem.Uint16(5)
            Offline = pywbem.Uint16(6)
            Test = pywbem.Uint16(7)
            Defer = pywbem.Uint16(8)
            Quiesce = pywbem.Uint16(9)
            Reboot = pywbem.Uint16(10)
            Reset = pywbem.Uint16(11)
            Not_Applicable = pywbem.Uint16(12)
            # DMTF_Reserved = ..

        class EnabledDefault(object):
            Enabled = pywbem.Uint16(2)
            Disabled = pywbem.Uint16(3)
            Not_Applicable = pywbem.Uint16(5)
            Enabled_but_Offline = pywbem.Uint16(6)
            No_Default = pywbem.Uint16(7)
            Quiesce = pywbem.Uint16(9)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 32768..65535

        class EnabledState(object):
            Unknown = pywbem.Uint16(0)
            Other = pywbem.Uint16(1)
            Enabled = pywbem.Uint16(2)
            Disabled = pywbem.Uint16(3)
            Shutting_Down = pywbem.Uint16(4)
            Not_Applicable = pywbem.Uint16(5)
            Enabled_but_Offline = pywbem.Uint16(6)
            In_Test = pywbem.Uint16(7)
            Deferred = pywbem.Uint16(8)
            Quiesce = pywbem.Uint16(9)
            Starting = pywbem.Uint16(10)
            # DMTF_Reserved = 11..32767
            # Vendor_Reserved = 32768..65535

        class AvailableRequestedStates(object):
            Enabled = pywbem.Uint16(2)
            Disabled = pywbem.Uint16(3)
            Shut_Down = pywbem.Uint16(4)
            Offline = pywbem.Uint16(6)
            Test = pywbem.Uint16(7)
            Defer = pywbem.Uint16(8)
            Quiesce = pywbem.Uint16(9)
            Reboot = pywbem.Uint16(10)
            Reset = pywbem.Uint16(11)
            # DMTF_Reserved = ..

        class Status(object):
            OK = 'OK'
            Error = 'Error'
            Degraded = 'Degraded'
            Unknown = 'Unknown'
            Pred_Fail = 'Pred Fail'
            Starting = 'Starting'
            Stopping = 'Stopping'
            Service = 'Service'
            Stressed = 'Stressed'
            NonRecover = 'NonRecover'
            No_Contact = 'No Contact'
            Lost_Comm = 'Lost Comm'
            Stopped = 'Stopped'

        class CommunicationStatus(object):
            Unknown = pywbem.Uint16(0)
            Not_Available = pywbem.Uint16(1)
            Communication_OK = pywbem.Uint16(2)
            Lost_Communication = pywbem.Uint16(3)
            No_Contact = pywbem.Uint16(4)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 0x8000..

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

        class OperatingStatus(object):
            Unknown = pywbem.Uint16(0)
            Not_Available = pywbem.Uint16(1)
            Servicing = pywbem.Uint16(2)
            Starting = pywbem.Uint16(3)
            Stopping = pywbem.Uint16(4)
            Stopped = pywbem.Uint16(5)
            Aborted = pywbem.Uint16(6)
            Dormant = pywbem.Uint16(7)
            Completed = pywbem.Uint16(8)
            Migrating = pywbem.Uint16(9)
            Emigrating = pywbem.Uint16(10)
            Immigrating = pywbem.Uint16(11)
            Snapshotting = pywbem.Uint16(12)
            Shutting_Down = pywbem.Uint16(13)
            In_Test = pywbem.Uint16(14)
            Transitioning = pywbem.Uint16(15)
            In_Service = pywbem.Uint16(16)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 0x8000..

        class RequestStateChange(object):
            Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown_or_Unspecified_Error = pywbem.Uint32(2)
            Cannot_complete_within_Timeout_Period = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            Invalid_State_Transition = pywbem.Uint32(4097)
            Use_of_Timeout_Parameter_Not_Supported = pywbem.Uint32(4098)
            Busy = pywbem.Uint32(4099)
            # Method_Reserved = 4100..32767
            # Vendor_Specific = 32768..65535
            class RequestedState(object):
                Enabled = pywbem.Uint16(2)
                Disabled = pywbem.Uint16(3)
                Shut_Down = pywbem.Uint16(4)
                Offline = pywbem.Uint16(6)
                Test = pywbem.Uint16(7)
                Defer = pywbem.Uint16(8)
                Quiesce = pywbem.Uint16(9)
                Reboot = pywbem.Uint16(10)
                Reset = pywbem.Uint16(11)
                # DMTF_Reserved = ..
                # Vendor_Reserved = 32768..65535

        class CreateFileSystem(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            StorageExtent_is_not_big_enough_to_satisfy_the_request_ = pywbem.Uint32(6)
            StorageExtent_specified_by_default_cannot_be_created_ = pywbem.Uint32(7)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            # Method_Reserved = 4098..32767
            # Vendor_Specific = 32768..65535

        class StartMode(object):
            Automatic = 'Automatic'
            Manual = 'Manual'

        class PrimaryStatus(object):
            Unknown = pywbem.Uint16(0)
            OK = pywbem.Uint16(1)
            Degraded = pywbem.Uint16(2)
            Error = pywbem.Uint16(3)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 0x8000..

        class MountFileSystem(object):
            Completed_OK = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Failed = pywbem.Uint32(2)
            # Reserved = 3..32767

## end of class LMI_FileSystemConfigurationServiceProvider
    
## get_providers() for associating CIM Class Name to python provider class name
    
def get_providers(env): 
    initAnaconda(False)
    LMI_FileSystemConfigurationService_prov = LMI_FileSystemConfigurationService(env)  
    return {'LMI_FileSystemConfigurationService': LMI_FileSystemConfigurationService_prov}

