# Cura Storage Provider
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

"""Python Provider for LMI_StorageConfigurationService

Instruments the CIM class LMI_StorageConfigurationService

"""

from wrapper.common import *
import pywbem
from pywbem.cim_provider2 import CIMProvider2

class LMI_StorageConfigurationService(CIMProvider2):
    """Instrument the CIM class LMI_StorageConfigurationService 

    This service allows the active management of a Storage Server. It
    allows jobs to be started for the creation, modification and deletion
    of storage objects (StoragePools, StorageVolumes and LogicalDisks).
    
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
        

        if (model['SystemName'] != LMI_SYSTEM_NAME
                or model['SystemCreationClassName'] != LMI_SYSTEM_CLASS_NAME
                or model['CreationClassName'] != 'LMI_StorageConfigurationService'
                or model['Name'] != 'StorageConfigurationService'):
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, 'Wrong keys.')

        #model['AvailableRequestedStates'] = [self.Values.AvailableRequestedStates.<VAL>,] # TODO 
        #model['Caption'] = '' # TODO 
        #model['CommunicationStatus'] = self.Values.CommunicationStatus.<VAL> # TODO 
        #model['Description'] = '' # TODO 
        #model['DetailedStatus'] = self.Values.DetailedStatus.<VAL> # TODO 
        #model['ElementName'] = '' # TODO 
        model['EnabledDefault'] = self.Values.EnabledDefault.Enabled 
        #model['EnabledState'] = self.Values.EnabledState.Not_Applicable # TODO 
        #model['Generation'] = pywbem.Uint64() # TODO 
        model['HealthState'] = self.Values.HealthState.OK 
        #model['InstallDate'] = pywbem.CIMDateTime() # TODO 
        #model['InstanceID'] = '' # TODO 
        #model['OperatingStatus'] = self.Values.OperatingStatus.<VAL> # TODO 
        model['OperationalStatus'] = [self.Values.OperationalStatus.OK,] 
        #model['OtherEnabledState'] = '' # TODO 
        #model['PrimaryOwnerContact'] = '' # TODO 
        #model['PrimaryOwnerName'] = '' # TODO 
        #model['PrimaryStatus'] = self.Values.PrimaryStatus.<VAL> # TODO 
        #model['RequestedState'] = self.Values.RequestedState.Not_Applicable # TODO 
        #model['Started'] = bool() # TODO 
        #model['StartMode'] = self.Values.StartMode.<VAL> # TODO 
        #model['Status'] = self.Values.Status.<VAL> # TODO 
        #model['StatusDescriptions'] = ['',] # TODO 
        #model['TimeOfLastStateChange'] = pywbem.CIMDateTime() # TODO 
        #model['TransitioningToState'] = self.Values.TransitioningToState.Not_Applicable # TODO 
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
        model['CreationClassName'] = 'LMI_StorageConfigurationService'    
        model['Name'] = 'StorageConfigurationService'
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
        
    def cim_method_deletestoragepool(self, env, object_name,
                                     param_pool=None):
        """Implements LMI_StorageConfigurationService.DeleteStoragePool()

        Start a job to delete a StoragePool. The freed space is returned
        source StoragePools (indicated by AllocatedFrom StoragePool) or
        back to underlying storage extents. If 0 is returned, the function
        completed successfully, and no ConcreteJob was required. If
        4096/0x1000 is returned, a ConcreteJob will be started to delete
        the StoragePool. A reference to the Job is returned in the Job
        parameter.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method DeleteStoragePool() 
            should be invoked.
        param_pool --  The input parameter Pool (type REF (pywbem.CIMInstanceName(classname='CIM_StoragePool', ...)) 
            Reference to the pool to delete.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.DeleteStoragePool)
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
        logger.log_debug('Entering %s.cim_method_deletestoragepool()' \
                % self.__class__.__name__)

        if not param_pool:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'InPool parameter is mandatory.')
        
        wrapper = wrapperManager.getWrapperForInstance(param_pool)
        if wrapper is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Cannot find InPool.')
        device = wrapper.getDevice(param_pool)
        if device is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Cannot find InPool.')
        
        ret = wrapper.destroyPool(device)
        out_params = [] 
        return (ret, out_params)
        
    def cim_method_createormodifyelementfromelements(self, env, object_name,
                                                     param_inelements,
                                                     param_elementtype,
                                                     param_elementname=None,
                                                     param_goal=None,
                                                     param_theelement=None,
                                                     param_size=None):
        """Implements LMI_StorageConfigurationService.CreateOrModifyElementFromElements()

        Start a job to create (or modify) a specified storage element from
        specified input StorageExtents. The created or modified storage
        element can be a StorageExtent, StorageVolume, LogicalDisk, or
        StoragePool. An input list of InElements must be specified. The
        GetAvailableExtents method can be used to get a list of valid
        extents that can be used to achieve a desired goal. Validity of
        the extents is determined by the implementation. As an input
        parameter, Size specifies the desired size of the element. As an
        output parameter, it specifies the size achieved. Space is taken
        from the input InElements. The desired Settings for the element
        are specified by the Goal parameter. If the size of Extents passed
        is less than the size requested, then the capacity is drawn from
        the extents in the order, left to right, that the Extents were
        specified. The partial consumption of an Extent is represented by
        an Extent for the capacity used and an Extent for the capacity not
        used. If the Size is NULL, then a configuration using all Extents
        passed will be attempted. If the requested size cannot be created,
        no action will be taken, and the Return Value will be 4097/0x1001.
        Also, the output value of Size is set to the nearest possible
        size. If 0 is returned, the function completed successfully and no
        ConcreteJob instance was required. If 4096/0x1000 is returned, a
        ConcreteJob will be started to create the element. The Job\'s
        reference will be returned in the output parameter Job.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method CreateOrModifyElementFromElements() 
            should be invoked.
        param_elementname --  The input parameter ElementName (type unicode) 
            A end user relevant name for the element being created. If
            NULL, then a system-supplied default name can be used. The
            value will be stored in the \'ElementName\' property for the
            created element. If not NULL, this parameter will supply a new
            name when modifying an existing element.
            
        param_goal --  The input parameter Goal (type REF (pywbem.CIMInstanceName(classname='CIM_ManagedElement', ...)) 
            The requirements for the element to maintain. If set to a null
            value, the default configuration associated with the Service
            will be used. This parameter should be a reference to a
            Setting, SettingData, or Profile appropriate to the element
            being created. If not NULL, this parameter will supply a new
            Goal when modifying an existing element.
            
        param_theelement --  The input parameter TheElement (type REF (pywbem.CIMInstanceName(classname='CIM_LogicalElement', ...)) 
            As an input parameter: if null, creates a new element. If not
            null, then the method modifies the specified element. As an
            output parameter, it is a reference to the resulting element.
            
        param_inelements --  The input parameter InElements (type REF (pywbem.CIMInstanceName(classname='CIM_StorageExtent', ...)) (Required)
            Array of references to storage element instances that are used
            to create or modify TheElement.
            
        param_elementtype --  The input parameter ElementType (type pywbem.Uint16 self.Values.CreateOrModifyElementFromElements.ElementType) (Required)
            Enumeration indicating the type of element being created or
            modified. If the input parameter TheElement is specified when
            the operation is a \'modify\', this type value must match the
            type of that instance. The actual CIM class of the created
            TheElement can be vendor-specific, but it must be a derived
            class of the appropriate CIM class -- i.e., CIM_StorageVolume,
            CIM_StorageExtent, CIM_LogicalDisk, or CIM_StoragePool.
            
        param_size --  The input parameter Size (type pywbem.Uint64) 
            As an input parameter Size specifies the desired size. If not
            NULL, this parameter will supply a new size when modifying an
            existing element. As an output parameter Size specifies the
            size achieved.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.CreateOrModifyElementFromElements)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...)) 
            Reference to the job (may be null if job completed).
            
        TheElement -- (type REF (pywbem.CIMInstanceName(classname='CIM_LogicalElement', ...)) 
            As an input parameter: if null, creates a new element. If not
            null, then the method modifies the specified element. As an
            output parameter, it is a reference to the resulting element.
            
        Size -- (type pywbem.Uint64) 
            As an input parameter Size specifies the desired size. If not
            NULL, this parameter will supply a new size when modifying an
            existing element. As an output parameter Size specifies the
            size achieved.
            

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
        logger.log_debug('Entering %s.cim_method_createormodifyelementfromelements()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('job', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))] # TODO
        #out_params+= [pywbem.CIMParameter('theelement', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_LogicalElement', ...))] # TODO
        #out_params+= [pywbem.CIMParameter('size', type='uint64', 
        #                   value=pywbem.Uint64())] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.CreateOrModifyElementFromElements)
        #return (rval, out_params)
        
    def cim_method_stopservice(self, env, object_name):
        """Implements LMI_StorageConfigurationService.StopService()

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
        
    def cim_method_createreplicationbuffer(self, env, object_name,
                                           param_host,
                                           param_targetpool=None,
                                           param_targetelement=None):
        """Implements LMI_StorageConfigurationService.CreateReplicationBuffer()

        Create (or start a job to create) a replication buffer that buffers
        asynchronous write operations for remote mirror pairs. The buffer
        is an instance of CIM_Memory with an AssociatedMemory association
        to a hosting system or to a replication network pipe. The buffer
        element may be created based on a StorageExtent, in a pool or in a
        manner opaque to a client. If 0 is returned, the function
        completed successfully and no ConcreteJob instance is created. If
        0x1000 is returned, a ConcreteJob is started, a reference to which
        is returned in the Job output parameter. A return value of 1
        indicates the method is not supported. All other values indicate
        some type of error condition. \n\nIf Job Completed with No Error
        (0) is returned, the function completed successfully and a
        ConcreteJob instance is not created. \n\nIf Method Parameters
        Checked - Job Started (0x1000) is returned, a ConcreteJob is
        started, a reference to which is returned in the Job output
        parameter. \n\nA return value of Not Supported (1) indicates the
        method is not supported. \n\nAll other values indicate some type
        of error condition.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method CreateReplicationBuffer() 
            should be invoked.
        param_targetpool --  The input parameter TargetPool (type REF (pywbem.CIMInstanceName(classname='CIM_StoragePool', ...)) 
            Reference to a container pool for the buffer element.
            
        param_targetelement --  The input parameter TargetElement (type REF (pywbem.CIMInstanceName(classname='CIM_StorageExtent', ...)) 
            Reference to a component extent for the buffer element.
            
        param_host --  The input parameter Host (type REF (pywbem.CIMInstanceName(classname='CIM_ManagedElement', ...)) (Required)
            The hosting system or replication pipe that will be antecedent
            to the created buffer.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.CreateReplicationBuffer)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...)) 
            Reference to the job (may be null if the task completed).
            
        ReplicaBuffer -- (type REF (pywbem.CIMInstanceName(classname='CIM_Memory', ...)) 
            Reference to the created replica buffer element.
            

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
        logger.log_debug('Entering %s.cim_method_createreplicationbuffer()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('job', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))] # TODO
        #out_params+= [pywbem.CIMParameter('replicabuffer', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_Memory', ...))] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.CreateReplicationBuffer)
        #return (rval, out_params)
        
    def cim_method_createreplica(self, env, object_name,
                                 param_sourceelement,
                                 param_elementname=None,
                                 param_targetpool=None,
                                 param_targetsettinggoal=None,
                                 param_copytype=None):
        """Implements LMI_StorageConfigurationService.CreateReplica()

        Start a job to create a new storage object which is a replica of
        the specified source storage object. (SourceElement). Note that
        using the input paramter, CopyType, this function can be used to
        instantiate the replica, and to create an ongoing association
        between the source and replica. If 0 is returned, the function
        completed successfully and no ConcreteJob instance is created. If
        4096/0x1000 is returned, a ConcreteJob is started, a reference to
        which is returned in the Job output parameter.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method CreateReplica() 
            should be invoked.
        param_elementname --  The input parameter ElementName (type unicode) 
            A end user relevant name for the element being created. If
            NULL, then a system supplied default name can be used. The
            value will be stored in the \'ElementName\' property for the
            created element.
            
        param_targetpool --  The input parameter TargetPool (type REF (pywbem.CIMInstanceName(classname='CIM_StoragePool', ...)) 
            The underlying storage for the target element (the replica)
            will be drawn from TargetPool if specified, otherwise the
            allocation is implementation specific.
            
        param_sourceelement --  The input parameter SourceElement (type REF (pywbem.CIMInstanceName(classname='CIM_LogicalElement', ...)) (Required)
            The source storage object which may be a StorageVolume or
            storage object.
            
        param_targetsettinggoal --  The input parameter TargetSettingGoal (type REF (pywbem.CIMInstanceName(classname='CIM_StorageSetting', ...)) 
            The definition for the StorageSetting to be maintained by the
            target storage object (the replica).
            
        param_copytype --  The input parameter CopyType (type pywbem.Uint16 self.Values.CreateReplica.CopyType) 
            CopyType describes the type of copy that will be made. Values
            are: \nAsync: Create and maintain an asynchronous copy of the
            source. \nSync: Create and maintain a synchronized copy of the
            source. \nUnSyncAssoc: Create an unsynchronized copy and
            maintain an association to the source. \nUnSyncUnAssoc: Create
            unassociated copy of the source element.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.CreateReplica)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...)) 
            Reference to the job (may be null if job completed).
            
        TargetElement -- (type REF (pywbem.CIMInstanceName(classname='CIM_LogicalElement', ...)) 
            Reference to the created target storage element (i.e., the
            replica).
            

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
        logger.log_debug('Entering %s.cim_method_createreplica()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('job', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))] # TODO
        #out_params+= [pywbem.CIMParameter('targetelement', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_LogicalElement', ...))] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.CreateReplica)
        #return (rval, out_params)
        
    def cim_method_changeaffectedelementsassignedsequence(self, env, object_name,
                                                          param_managedelements,
                                                          param_assignedsequence):
        """Implements LMI_StorageConfigurationService.ChangeAffectedElementsAssignedSequence()

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
        
    def cim_method_getelementsbasedonusage(self, env, object_name,
                                           param_usage=None,
                                           param_elementtype=None,
                                           param_thepool=None,
                                           param_criteria=None):
        """Implements LMI_StorageConfigurationService.GetElementsBasedOnUsage()

        Allows retrieving elements that meet the specified Usage. The
        criteria can be "available only", "in use only", or both.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method GetElementsBasedOnUsage() 
            should be invoked.
        param_usage --  The input parameter Usage (type pywbem.Uint16) 
            The specific Usage to be retrieved.
            
        param_elementtype --  The input parameter ElementType (type pywbem.Uint16 self.Values.GetElementsBasedOnUsage.ElementType) 
            Enumeration indicating the type of elements to get.
            
        param_thepool --  The input parameter ThePool (type REF (pywbem.CIMInstanceName(classname='CIM_StoragePool', ...)) 
            Limit the search for the elements that satisfy the criteria to
            this StoragePool only. If null, all appropriate StoragePools
            will be considered.
            
        param_criteria --  The input parameter Criteria (type pywbem.Uint16 self.Values.GetElementsBasedOnUsage.Criteria) 
            Specifies whether to retrieve all elements, available elements
            only, or the elements that are in use.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.GetElementsBasedOnUsage)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        TheElements -- (type REF (pywbem.CIMInstanceName(classname='CIM_ManagedSystemElement', ...)) 
            Array of references to storage element instances retrieved.
            

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
        logger.log_debug('Entering %s.cim_method_getelementsbasedonusage()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('theelements', type='reference', 
        #                   value=[pywbem.CIMInstanceName(classname='CIM_ManagedSystemElement', ...),])] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.GetElementsBasedOnUsage)
        #return (rval, out_params)
        
    def cim_method_createelementsfromstoragepool(self, env, object_name,
                                                 param_size,
                                                 param_elementcount,
                                                 param_elementnames=None,
                                                 param_goal=None,
                                                 param_inpool=None,
                                                 param_elementtype=None):
        """Implements LMI_StorageConfigurationService.CreateElementsFromStoragePool()

        Start a job to create (or modify) a specified elements (for example
        StorageVolumes or StorageExtents) from a StoragePool. One of the
        parameters for this method is Size. As an input parameter, Size
        specifies the desired size of the element. As an output parameter,
        it specifies the size achieved. Space is taken from the input
        StoragePool. The desired settings for the element are specified by
        the Goal parameter. If the requested size cannot be created, no
        action will be taken, and the Return Value will be 4097/0x1001.
        Also, the output value of Size is set to the nearest possible
        size. If 0 is returned, the function completed successfully and no
        ConcreteJob instance was required. If 4096/0x1000 is returned, a
        ConcreteJob will be started to create the element. The Job\'s
        reference will be returned in the output parameter Job. If the
        number of elements created is less than the number of elements
        requested, the return value will be 4098/0x1002.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method CreateElementsFromStoragePool() 
            should be invoked.
        param_size --  The input parameter Size (type pywbem.Uint64) (Required)
            As an input parameter Size specifies the desired size for each
            element created. As an output parameter Size specifies the
            size achieved.
            
        param_elementnames --  The input parameter ElementNames (type [unicode,]) 
            One or more user relevant names for the element being created.
            If NULL, then system supplied default names may be used. The
            value will be stored in the "ElementName" property for the
            created element.
            
        param_goal --  The input parameter Goal (type REF (pywbem.CIMInstanceName(classname='CIM_ManagedElement', ...)) 
            The requirements for the element to maintain. If set to a null
            value, the default configuration from the source pool will be
            used. This parameter should be a reference to a Setting or
            Profile appropriate to the element being created.
            
        param_inpool --  The input parameter InPool (type REF (pywbem.CIMInstanceName(classname='CIM_StoragePool', ...)) 
            The Pool from which to create the elements. If not supplied,
            system locates an appropriate pool.
            
        param_elementcount --  The input parameter ElementCount (type pywbem.Uint64) (Required)
            Count of elements to create.
            
        param_elementtype --  The input parameter ElementType (type pywbem.Uint16 self.Values.CreateElementsFromStoragePool.ElementType) 
            Enumeration indicating the type of element being created.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.CreateElementsFromStoragePool)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Size -- (type pywbem.Uint64) (Required)
            As an input parameter Size specifies the desired size for each
            element created. As an output parameter Size specifies the
            size achieved.
            
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...)) 
            Reference to the job (may be null if job completed).
            
        TheElements -- (type REF (pywbem.CIMInstanceName(classname='CIM_LogicalElement', ...)) 
            Reference to the resulting elements.
            

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
        logger.log_debug('Entering %s.cim_method_createelementsfromstoragepool()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('size', type='uint64', 
        #                   value=pywbem.Uint64())] # TODO
        #out_params+= [pywbem.CIMParameter('job', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))] # TODO
        #out_params+= [pywbem.CIMParameter('theelements', type='reference', 
        #                   value=[pywbem.CIMInstanceName(classname='CIM_LogicalElement', ...),])] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.CreateElementsFromStoragePool)
        #return (rval, out_params)
        
    def cim_method_assignstorageresourceaffinity(self, env, object_name,
                                                 param_resourcetype,
                                                 param_storageresources,
                                                 param_storageprocessor=None):
        """Implements LMI_StorageConfigurationService.AssignStorageResourceAffinity()

        Start a job to assign affinity of a StoragePool(s) or
        StorageVolume(s) to a storage processor. At the conclusion of the
        operation, the resource will be a member of the
        StorageResourceLoadGroup with the primary affinity for the
        specified storage processor. Support for this method is indicated
        by the presence of an instance of
        StorageServerAsymmetryCapabilites in which the property
        StorageResourceAffinityAssignable is \'true\'. If 0 is returned,
        the function completed successfully and no ConcreteJob instance
        was required. If 4096/0x1000 is returned, a job will be started to
        assign the element. The Job\'s reference will be returned in the
        output parameter Job.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method AssignStorageResourceAffinity() 
            should be invoked.
        param_resourcetype --  The input parameter ResourceType (type pywbem.Uint16 self.Values.AssignStorageResourceAffinity.ResourceType) (Required)
            Enumeration indicating the type of resource being assigned or
            modified. .
            
        param_storageprocessor --  The input parameter StorageProcessor (type REF (pywbem.CIMInstanceName(classname='CIM_ComputerSystem', ...)) 
            Reference to the storage processor to which to assign the
            resource.
            
        param_storageresources --  The input parameter StorageResources (type REF (pywbem.CIMInstanceName(classname='CIM_LogicalElement', ...)) (Required)
            Array of references to storage resource instances to be
            assigned.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.AssignStorageResourceAffinity)
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
        logger.log_debug('Entering %s.cim_method_assignstorageresourceaffinity()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('job', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.AssignStorageResourceAffinity)
        #return (rval, out_params)
        
    def cim_method_createormodifyelementfromstoragepool(self, env, object_name,
                                                        param_elementname=None,
                                                        param_goal=None,
                                                        param_inpool=None,
                                                        param_theelement=None,
                                                        param_elementtype=None,
                                                        param_size=None):
        """Implements LMI_StorageConfigurationService.CreateOrModifyElementFromStoragePool()

        Start a job to create (or modify) a specified element (for example
        a StorageVolume or StorageExtent) from a StoragePool. One of the
        parameters for this method is Size. As an input parameter, Size
        specifies the desired size of the element. As an output parameter,
        it specifies the size achieved. Space is taken from the input
        StoragePool. The desired settings for the element are specified by
        the Goal parameter. If the requested size cannot be created, no
        action will be taken, and the Return Value will be 4097/0x1001.
        Also, the output value of Size is set to the nearest possible
        size. If 0 is returned, the function completed successfully and no
        ConcreteJob instance was required. If 4096/0x1000 is returned, a
        ConcreteJob will be started to create the element. The Job\'s
        reference will be returned in the output parameter Job.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method CreateOrModifyElementFromStoragePool() 
            should be invoked.
        param_elementname --  The input parameter ElementName (type unicode) 
            A end user relevant name for the element being created. If
            NULL, then a system supplied default name can be used. The
            value will be stored in the \'ElementName\' property for the
            created element. If not NULL, this parameter will supply a new
            name when modifying an existing element.
            
        param_goal --  The input parameter Goal (type REF (pywbem.CIMInstanceName(classname='CIM_ManagedElement', ...)) 
            The requirements for the element to maintain. If set to a null
            value, the default configuration from the source pool will be
            used. This parameter should be a reference to a Setting or
            Profile appropriate to the element being created. If not NULL,
            this parameter will supply a new Goal when modifying an
            existing element.
            
        param_inpool --  The input parameter InPool (type REF (pywbem.CIMInstanceName(classname='CIM_StoragePool', ...)) 
            The Pool from which to create the element. This parameter must
            be set to null if the input parameter TheElement is specified
            (in the case of a \'modify\' operation).
            
        param_theelement --  The input parameter TheElement (type REF (pywbem.CIMInstanceName(classname='CIM_LogicalElement', ...)) 
            As an input parameter: if null, creates a new element. If not
            null, then the method modifies the specified element. As an
            output parameter, it is a reference to the resulting element.
            
        param_elementtype --  The input parameter ElementType (type pywbem.Uint16 self.Values.CreateOrModifyElementFromStoragePool.ElementType) 
            Enumeration indicating the type of element being created or
            modified. If the input parameter TheElement is specified when
            the operation is a \'modify\', this type value must match the
            type of that instance.
            
        param_size --  The input parameter Size (type pywbem.Uint64) 
            As an input parameter Size specifies the desired size. If not
            NULL, this parameter will supply a new size when modifying an
            existing element. As an output parameter Size specifies the
            size achieved.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.CreateOrModifyElementFromStoragePool)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...)) 
            Reference to the job (may be null if job completed).
            
        TheElement -- (type REF (pywbem.CIMInstanceName(classname='CIM_LogicalElement', ...)) 
            As an input parameter: if null, creates a new element. If not
            null, then the method modifies the specified element. As an
            output parameter, it is a reference to the resulting element.
            
        Size -- (type pywbem.Uint64) 
            As an input parameter Size specifies the desired size. If not
            NULL, this parameter will supply a new size when modifying an
            existing element. As an output parameter Size specifies the
            size achieved.
            

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
        logger.log_debug('Entering %s.cim_method_createormodifyelementfromstoragepool()' \
                % self.__class__.__name__)

        # This method can only create LogicalDisks from a pool
        
        # basic checks
        if param_elementtype != self.Values.CreateOrModifyElementFromStoragePool.ElementType.LogicalDisk:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, "Only LogicalDisks can be created.")
        if param_theelement:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, "Element modification is not supported.")
        
        # get a setting (if used)
        setting = None
        if param_goal:
            setting = settingManager.getSetting(param_goal['InstanceID'])
            if not setting:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, "Cannot find Goal setting.")
        
        # get the pool
        if not param_inpool:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, "InPool must be specified.")
        wrapper = wrapperManager.getWrapperForInstance(param_inpool)
        device = wrapper.getDevice(param_inpool)
        if device is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, "Cannot find InPool.")
        
        size = param_size
        
        (ret, element, size) = wrapper.createLogicalDisk(device, setting, size, name=param_elementname)
        outsize = pywbem.CIMParameter('Size', type='uint64', value = pywbem.Uint64(size))
        outparams = [outsize,]
        if element is not None:
            outparams.append(pywbem.CIMParameter('TheElement', type='reference', value = element))
        return (ret, outparams)
        
    def cim_method_createormodifyreplicationpipe(self, env, object_name,
                                                 param_targetsystem,
                                                 param_sourcesystem,
                                                 param_goal=None,
                                                 param_pipeelementname=None,
                                                 param_replicationpipe=None,
                                                 param_sourceendpoint=None,
                                                 param_targetendpoint=None):
        """Implements LMI_StorageConfigurationService.CreateOrModifyReplicationPipe()

        This method establishes a peer-to-peer connection identified by a
        NetworkPipe element and two ProtocolEndpoint elements created by
        the method provider. The NetworkPipe is associated to a special
        peer-to-peer Network element. The provider will verify that two
        systems are capable of a peer relationship. If endpoints are
        assigned to the pipe, the same number of source and target
        endpoints must be supplied by the client to form a set of endpoint
        pairs. If ReplicationPipe is not supplied as an input parameter, a
        new pipe is created. If a pipe is supplied, a new set of endpoints
        is assigned to the existing pipe. \n\nIf Success (0) is returned,
        the function completed successfully. \n\nA return value of Not
        Supported (1) indicates the method is not supported. \n\nA return
        value of Busy (0x1000) indicates the method is not supported.
        \n\nAll other values indicate some type of error condition.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method CreateOrModifyReplicationPipe() 
            should be invoked.
        param_goal --  The input parameter Goal (type pywbem.CIMInstance(classname='CIM_SettingData', ...)) 
            The setting properties to be maintained for the peer-to-peer
            connection.
            
        param_pipeelementname --  The input parameter PipeElementName (type unicode) 
            A user-friendly name for the element created.
            
        param_replicationpipe --  The input parameter ReplicationPipe (type REF (pywbem.CIMInstanceName(classname='CIM_NetworkPipe', ...)) 
            Reference to the created or modified NetworkPipe.
            
        param_targetsystem --  The input parameter TargetSystem (type REF (pywbem.CIMInstanceName(classname='CIM_ComputerSystem', ...)) (Required)
            One of the two peer systems participating in the established
            peer-to-peer connection. If the provider supports
            uni-directional connections, this must identify the system
            hosting replica target elements.
            
        param_sourcesystem --  The input parameter SourceSystem (type REF (pywbem.CIMInstanceName(classname='CIM_ComputerSystem', ...)) (Required)
            One of the two peer systems participating in the established
            peer-to-peer connection. If the provider supports
            uni-directional connections, this must identify the system
            hosting replica source elements.
            
        param_sourceendpoint --  The input parameter SourceEndpoint (type REF (pywbem.CIMInstanceName(classname='CIM_ProtocolEndpoint', ...)) 
            References to source system endpoints/ports assigned to the
            pipe. If a new pipe is created, this is the initial set of
            endpoints assigned. If an existing pipe is modified, this set
            replaces the previous set. The list must be null if a provider
            does not allow the client to manage port assignment.
            
        param_targetendpoint --  The input parameter TargetEndpoint (type REF (pywbem.CIMInstanceName(classname='CIM_ProtocolEndpoint', ...)) 
            References to target system endpoints/ports assigned to the
            pipe. If a new pipe is created, this is the initial set of
            endpoints assigned. If an existing pipe is modified, this set
            replaces the previous set. The list must be null if a provider
            does not allow the client to manage port assignment.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.CreateOrModifyReplicationPipe)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        ReplicationPipe -- (type REF (pywbem.CIMInstanceName(classname='CIM_NetworkPipe', ...)) 
            Reference to the created or modified NetworkPipe.
            

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
        logger.log_debug('Entering %s.cim_method_createormodifyreplicationpipe()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('replicationpipe', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_NetworkPipe', ...))] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.CreateOrModifyReplicationPipe)
        #return (rval, out_params)
        
    def cim_method_createormodifystoragepool(self, env, object_name,
                                             param_elementname=None,
                                             param_goal=None,
                                             param_inpools=None,
                                             param_inextents=None,
                                             param_pool=None,
                                             param_size=None):
        """Implements LMI_StorageConfigurationService.CreateOrModifyStoragePool()

        Starts a job to create (or modify) a StoragePool. The StoragePool
        will be (or must be) scoped to the same System as this Service.
        One of the parameters for this method is Size. As an input
        parameter, Size specifies the desired size of the pool. As an
        output parameter, it specifies the size achieved. Space is taken
        from either or both of the specified input StoragePools and
        StorageExtents (InPools and InExtents). The capability
        requirements that the Pool must support are defined using the Goal
        parameter. If the requested pool size cannot be created, no action
        will be taken, the Return Value will be 4097/0x1001, and the
        output value of Size will be set to the nearest possible size. If
        0 is returned, then the task completed successfully and the use of
        ConcreteJob was not required. If the task will take some time to
        complete, a ConcreteJob will be created and its reference returned
        in the output parameter Job.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method CreateOrModifyStoragePool() 
            should be invoked.
        param_elementname --  The input parameter ElementName (type unicode) 
            A end user relevant name for the pool being created. If NULL,
            then a system supplied default name can be used. The value
            will be stored in the \'ElementName\' property for the created
            pool. If not NULL, this parameter will supply a new name when
            modifying an existing pool.
            
        param_goal --  The input parameter Goal (type REF (pywbem.CIMInstanceName(classname='CIM_StorageSetting', ...)) 
            Reference to an instance of StorageSetting that defines the
            desired capabilities of the StoragePool. If set to a null
            value, the default configuration from the source pool will be
            used. If not NULL, this parameter will supply a new Goal
            setting when modifying an existing pool.
            
        param_inpools --  The input parameter InPools (type [unicode,]) 
            Array of strings containing representations of references to
            CIM_StoragePool instances, that are used to create the Pool or
            modify the source pools.
            
        param_inextents --  The input parameter InExtents (type [unicode,]) 
            Array of strings containing representations of references to
            CIM_StorageExtent instances, that are used to create the Pool
            or modify the source extents.
            
        param_pool --  The input parameter Pool (type REF (pywbem.CIMInstanceName(classname='CIM_StoragePool', ...)) 
            As an input parameter: if null, creates a new StoragePool. If
            not null, modifies the referenced Pool. When returned, it is a
            reference to the resulting StoragePool.
            
        param_size --  The input parameter Size (type pywbem.Uint64) 
            As an input parameter this specifies the desired pool size in
            bytes. As an output parameter this specifies the size
            achieved.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.CreateOrModifyStoragePool)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...)) 
            Reference to the job (may be null if job completed).
            
        Pool -- (type REF (pywbem.CIMInstanceName(classname='CIM_StoragePool', ...)) 
            As an input parameter: if null, creates a new StoragePool. If
            not null, modifies the referenced Pool. When returned, it is a
            reference to the resulting StoragePool.
            
        Size -- (type pywbem.Uint64) 
            As an input parameter this specifies the desired pool size in
            bytes. As an output parameter this specifies the size
            achieved.
            

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
        logger.log_debug('Entering %s.cim_method_createormodifystoragepool()' \
                % self.__class__.__name__)

        # THE ultimate function to create various storage elements - RAID, LVM, ...
        # check the parameters first
        if param_pool:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Pool modification is not supported.')
        
        # collect input devices
        devices = set()
        if param_inextents:
            for extent in param_inextents:
                dev = wrapperManager.getDevice(extent)
                if dev:
                    devices.add(dev)
        if param_inpools:
            for pool in param_inpools:
                dev = wrapperManager.getDevice(pool)
                # insert all *unused* devices from given pools
                if dev == wrapperManager.PRIMORDIAL_POOL_DEVICE:
                    # add all free devices, i.e. unused partitions, from the primordial pool
                    for part in storage.partitions:
                        if not (logicalDiskManager.isUsed(part) or logicalDiskManager.isExposed(part)):
                            devices.add(part)
                elif not (logicalDiskManager.isUsed(dev) or logicalDiskManager.isExposed(dev)): 
                    devices.add(dev)

        # get a setting (if used)
        setting = None
        if param_goal:
            setting = settingManager.getSetting(param_goal['InstanceID'])
            if not setting:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Cannot find Goal setting.')

        (ret, element, size) = wrapperManager.createPool(list(devices), setting, param_size, param_elementname)
        
        outsize = pywbem.CIMParameter('Size', type='uint64', value = pywbem.Uint64(size))
        outparams = [outsize,]
        if element is not None:
            outparams.append(pywbem.CIMParameter('Pool', type='reference', value = element))
        return (ret, outparams)
        
    def cim_method_attachreplica(self, env, object_name,
                                 param_sourceelement,
                                 param_targetelement=None,
                                 param_copytype=None):
        """Implements LMI_StorageConfigurationService.AttachReplica()

        Create (or start a job to create) a StorageSynchronized
        relationship between two existing storage objects. Note that using
        the input parameter, CopyType, this function can be used to to
        create an ongoing association between the source and replica. If 0
        is returned, the function completed successfully and no
        ConcreteJob instance is created. If 0x1000 is returned, a
        ConcreteJob is started, a reference to which is returned in the
        Job output parameter. A return value of 1 indicates the method is
        not supported. All other values indicate some type of error
        condition.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method AttachReplica() 
            should be invoked.
        param_sourceelement --  The input parameter SourceElement (type REF (pywbem.CIMInstanceName(classname='CIM_ManagedElement', ...)) (Required)
            The source storage object which may be a StorageVolume or other
            storage object.
            
        param_targetelement --  The input parameter TargetElement (type REF (pywbem.CIMInstanceName(classname='CIM_ManagedElement', ...)) 
            Reference to the target storage element (i.e., the replica).
            
        param_copytype --  The input parameter CopyType (type pywbem.Uint16 self.Values.AttachReplica.CopyType) 
            CopyType describes the type of Synchronized relationship that
            will be created. Values are: \nAsync: Create and maintain an
            asynchronous copy of the source. \nSync: Create and maintain a
            synchronized copy of the source. \nUnSyncAssoc: Create an
            unsynchronized copy and maintain an association to the source.
            \nUnSyncUnAssoc: Create unassociated copy of the source
            element.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.AttachReplica)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...)) 
            Reference to the job (may be null if the task completed).
            

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
        logger.log_debug('Entering %s.cim_method_attachreplica()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('job', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.AttachReplica)
        #return (rval, out_params)
        
    def cim_method_returntostoragepool(self, env, object_name,
                                       param_theelement=None):
        """Implements LMI_StorageConfigurationService.ReturnToStoragePool()

        Start a job to delete an element previously created from a
        StoragePool. The freed space is returned to the source
        StoragePool. If 0 is returned, the function completed successfully
        and no ConcreteJob was required. If 4096/0x1000 is returned, a
        ConcreteJob will be started to delete the element. A reference to
        the Job is returned in the Job parameter.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method ReturnToStoragePool() 
            should be invoked.
        param_theelement --  The input parameter TheElement (type REF (pywbem.CIMInstanceName(classname='CIM_LogicalElement', ...)) 
            Reference to the element to return to the StoragePool.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.ReturnToStoragePool)
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
        logger.log_debug('Entering %s.cim_method_returntostoragepool()' \
                % self.__class__.__name__)
        
        wrapper = wrapperManager.getWrapperForInstance(param_theelement)
        if wrapper is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Cannot find theElement.')
        
        device = wrapper.getDevice(param_theelement)
        if device is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Cannot find theElement.')
            
        ret = wrapper.destroyLogicalDisk(device)
            
        out_params = []
        return (ret, out_params)
        
    def cim_method_attachormodifyreplica(self, env, object_name,
                                         param_copytype,
                                         param_sourceelement,
                                         param_targetelement,
                                         param_goal=None,
                                         param_replicationpipe=None):
        """Implements LMI_StorageConfigurationService.AttachOrModifyReplica()

        Create (or start a job to create) a StorageSynchronized mirror
        relationship between two storage elements. The target element may
        be a local or a remote storage element. A remote mirror pair may
        be scoped by a peer-to-peer connection modeled as a NetworkPipe
        between peers. \n\nIf Job Completed with No Error (0) is returned,
        the function completed successfully and a ConcreteJob instance is
        not created. \n\nIf Method Parameters Checked - Job Started
        (0x1000) is returned, a ConcreteJob is started, a reference to
        which is returned in the Job output parameter. \n\nA return value
        of Not Supported (1) indicates the method is not supported.
        \n\nAll other values indicate some type of error condition.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method AttachOrModifyReplica() 
            should be invoked.
        param_goal --  The input parameter Goal (type pywbem.CIMInstance(classname='CIM_SettingData', ...)) 
            The StorageSetting properties to be created or modified for the
            target element.
            
        param_copytype --  The input parameter CopyType (type pywbem.Uint16 self.Values.AttachOrModifyReplica.CopyType) (Required)
            CopyType describes the type of Synchronized relationship that
            will be created. Values are: Async: Create and maintain an
            asynchronous copy of the source. Sync: Create and maintain a
            synchronized copy of the source. UnSyncAssoc: Create an
            unsynchronized copy and maintain an association to the source
            element. \nUnSyncUnAssoc: Create an unassociated copy of the
            source element. \nUnSyncAssoc and UnSyncUnAssoc are not
            supported for remote mirror replicas.
            
        param_sourceelement --  The input parameter SourceElement (type REF (pywbem.CIMInstanceName(classname='CIM_ManagedElement', ...)) (Required)
            The source storage element which may be a StorageVolume,
            StorageExtent, LogicalFile, FileSystem, CommonDatabase, or any
            other storage object. For this reason, the type is made very
            generic.
            
        param_replicationpipe --  The input parameter ReplicationPipe (type REF (pywbem.CIMInstanceName(classname='CIM_NetworkPipe', ...)) 
            The NetworkPipe element that scopes the remote mirror pair. If
            the value is null, remote mirrors do not require a
            pre-established connection.
            
        param_targetelement --  The input parameter TargetElement (type REF (pywbem.CIMInstanceName(classname='CIM_ManagedElement', ...)) (Required)
            Reference to the target storage element (i.e., the replica).
            The target storage element which may be a StorageVolume,
            StorageExtent, LogicalFile, FileSystem, CommonDatabase, or any
            other storage object. For this reason, the type is made very
            generic.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.AttachOrModifyReplica)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...)) 
            Reference to the job (may be null if the task completed).
            

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
        logger.log_debug('Entering %s.cim_method_attachormodifyreplica()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('job', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.AttachOrModifyReplica)
        #return (rval, out_params)
        
    def cim_method_returnelementstostoragepool(self, env, object_name,
                                               param_theelements,
                                               param_options=None):
        """Implements LMI_StorageConfigurationService.ReturnElementsToStoragePool()

        Start a job to delete elements previously created from
        StoragePools. The freed space is returned to the source
        StoragePool. If 0 is returned, the function completed successfully
        and no ConcreteJob was required. If 4096/0x1000 is returned, a
        ConcreteJob will be started to delete the element. A reference to
        the Job is returned in the Job parameter.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method ReturnElementsToStoragePool() 
            should be invoked.
        param_options --  The input parameter Options (type pywbem.Uint16 self.Values.ReturnElementsToStoragePool.Options) 
            Additional options. \nContinue on nonexistent element: if the
            method encounters a non-existent element in the list of
            elements supplied, the method continues to delete the
            remaining elements. Return error on nonexistent element: if
            the method encounters a non-existent element in the list of
            elements supplied, the method returns an error.
            
        param_theelements --  The input parameter TheElements (type REF (pywbem.CIMInstanceName(classname='CIM_LogicalElement', ...)) (Required)
            References to the elements to return to the StoragePool.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.ReturnElementsToStoragePool)
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
        logger.log_debug('Entering %s.cim_method_returnelementstostoragepool()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('job', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.ReturnElementsToStoragePool)
        #return (rval, out_params)
        
    def cim_method_requeststatechange(self, env, object_name,
                                      param_requestedstate=None,
                                      param_timeoutperiod=None):
        """Implements LMI_StorageConfigurationService.RequestStateChange()

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
        
    def cim_method_startservice(self, env, object_name):
        """Implements LMI_StorageConfigurationService.StartService()

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
        
    def cim_method_modifysynchronization(self, env, object_name,
                                         param_operation=None,
                                         param_synchronization=None):
        """Implements LMI_StorageConfigurationService.ModifySynchronization()

        Modify (or start a job to modify) the synchronization association
        between two storage objects. If 0 is returned, the function
        completed successfully and no ConcreteJob instance was created. If
        0x1000 is returned, a ConcreteJob was started and a reference to
        this Job is returned in the Job output parameter. A return value
        of 1 indicates the method is not supported. All other values
        indicate some type of error condition.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method ModifySynchronization() 
            should be invoked.
        param_operation --  The input parameter Operation (type pywbem.Uint16 self.Values.ModifySynchronization.Operation) 
            Operation describes the type of modification to be made to the
            replica. Values are: \nDetach: \'Forget\' the synchronization
            between two storage objects. Start to treat the objects as
            independent. \nFracture: Suspend the synchronization between
            two storage objects using Sync or Async replication. \nThe
            association and (typically) changes are remembered to allow a
            fast resynchronization. This may be used during a backup cycle
            to allow one of the objects to be copied while the other
            remains in production. \nResync Replica: Re-establish the
            synchronization of a Sync or Async replication. This will
            negate the action of a previous Fracture operation. Recreate a
            Point In Time image for an UnSyncAssoc replication. \nRestore
            from Replica: Renew the contents of the original storage
            object from a replica. \nPrepare: Get the link ready for a
            Resync operation to take place. Some implementations will
            require this operation to be invoked to keep the Resync
            operation as fast as possible. May start the copy engine.
            \nUnprepare: Clear a prepared state if a Prepare is not to be
            followed by a Resync operation. \nQuiesce: Some applications
            require notification so that they can ready the link for an
            operation. For example flush any cached data or buffered
            changes. The copy engine is stopped for UnSyncAssoc
            replications. \nUnquiesce: Take the link from the quiesced
            state (without executing the intended operation. \nStart Copy:
            initiate a full background copy of the source to the
            UnSyncAssoc replica. Replica enters Frozen state when copy
            operation is completed. \nStop Copy: stop the background copy
            previously started. Reset To Sync: Change the CopyType of the
            association to Sync (e.g., from the Async CopyType). \nReset
            To Async: Change the CopyType of the association to Async
            (e.g., from the Sync CopyType).
            
        param_synchronization --  The input parameter Synchronization (type REF (pywbem.CIMInstanceName(classname='CIM_StorageSynchronized', ...)) 
            The referenced to the StorageSynchronized association
            describing the storage source/replica relationship.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.ModifySynchronization)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...)) 
            Reference to the job (may be null if the task completed).
            

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
        logger.log_debug('Entering %s.cim_method_modifysynchronization()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('job', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.ModifySynchronization)
        #return (rval, out_params)
        
    def cim_method_scsiscan(self, env, object_name,
                            param_job=None):
        """Implements LMI_StorageConfigurationService.ScsiScan()

        This method requests that the system rescan SCSI devices for
        changes in their configuration. If called on a general-purpose
        host, the changes are reflected in the list of devices available
        to applications (for example, the UNIX \'device tree\'. This
        method may also be used on a storage appliance to force rescanning
        of attached SCSI devices. \n\nThis operation can be disruptive;
        optional parameters allow the caller to limit the scan to a single
        or set of SCSI device elements. All parameters are optional; if
        parameters other Job are passed in as null, a full scan is
        invoked.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method ScsiScan() 
            should be invoked.
        param_job --  The input parameter Job (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...)) 
            Reference to the job (may be null if job completed).
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.ScsiScan)
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
        logger.log_debug('Entering %s.cim_method_scsiscan()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('job', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.ScsiScan)
        #return (rval, out_params)
        
    def cim_method_requestusagechange(self, env, object_name,
                                      param_usagevalue=None,
                                      param_operation=None,
                                      param_theelement=None,
                                      param_otherusagedescription=None):
        """Implements LMI_StorageConfigurationService.RequestUsageChange()

        Allows a client to request the Usage to be set if the client has
        access to the element supplied and the request is valid.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method RequestUsageChange() 
            should be invoked.
        param_usagevalue --  The input parameter UsageValue (type pywbem.Uint16) 
            Applicable requested usage/restriction -- see the appropriate
            Usage ValueMap.
            
        param_operation --  The input parameter Operation (type pywbem.Uint16 self.Values.RequestUsageChange.Operation) 
            The action to perform.
            
        param_theelement --  The input parameter TheElement (type REF (pywbem.CIMInstanceName(classname='CIM_LogicalElement', ...)) 
            The storage element to modify.
            
        param_otherusagedescription --  The input parameter OtherUsageDescription (type unicode) 
            New description text. Applicable when the usage value includes
            "Other".
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.RequestUsageChange)
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
        logger.log_debug('Entering %s.cim_method_requestusagechange()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('job', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.RequestUsageChange)
        #return (rval, out_params)

    def cim_method_createraid(self, env, object_name,
                              param_raidtype=None,
                              param_inextents=None):
        """Implements LMI_StorageConfigurationService.CreateRaid()

        Create RAID with given local disks and format it as ext3. This
        function creates GPT partition table on the disks and creates one
        huge partition on each of them. The partitions are then added to
        RAID array.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method CreateRaid() 
            should be invoked.
        param_raidtype --  The input parameter RaidType (type pywbem.Uint16 self.Values.CreateRaid.RaidType) 
            Desired RAID type.
            
        param_inextents --  The input parameter InExtents (type [unicode,]) 
            Array of strings containing representations of references to
            LMI_LocalDiskExtent instances, that are used to create the
            Pool or modify the source extents.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.CreateRaid)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Disk -- (type REF (pywbem.CIMInstanceName(classname='CIM_LogicalDisk', ...)) 
            Created LogicalDisk.
            
        FilesyStem -- (type REF (pywbem.CIMInstanceName(classname='CIM_LocalFileSystem', ...)) 
            Created filesystem.
            

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
        logger.log_debug('Entering %s.cim_method_createraid()' \
                % self.__class__.__name__)
        
        cliconn = env.get_cimom_handle()

        # create GPT partition table on them, i.e. call
        # LMI_DiskPartitionConfigurationService.SetPartitionStyle(disk, partitionStyle) 
        # - get reference to LMI_DiskPartitionConfigurationService instance
        partServices = cliconn.EnumerateInstanceNames(ns=LMI_NAMESPACE, cn='LMI_DiskPartitionConfigurationService')
        partService = partServices.next()

        # - create reference to PartitionStyle we want to create
        partStyle = pywbem.CIMInstanceName(classname='LMI_DiskPartitionConfigurationCapabilities', namespace=LMI_NAMESPACE, keybindings = {'InstanceID':'GPT'})

        for disk in param_inextents:
            # - call partService.SetPartitionStyle(disk)
            (ret, outparams) = cliconn.InvokeMethod(partService, 'SetPartitionStyle', Extent = disk, PartitionStyle = partStyle)
            print 'SetPartitionStyle(', disk['DeviceID'], ')=', ret

        # create one huge partition on the disks, i.e. call
        # LMI_DiskPartitionConfigurationService.CreateOrModifyPartition(disk)
        for disk in param_inextents: 
            # - call partService.SetPartitionStyle(disk)
            (ret, outparams) = cliconn.InvokeMethod(partService, 'CreateOrModifyPartition', Extent = disk)
            print 'CreateOrModifyPartition(', disk['DeviceID'], ')=', ret

        # create RAID out of them, i.e. call
        # LMI_StorageConfigurationService.CreateOrModifyStoragePool(settings, pool)
        # - find the primordial pool
        pool = cliconn.EnumerateInstanceNames(ns = LMI_NAMESPACE, cn='LMI_PrimordialPool').next()
        # - find the LMI_StorageConfigurationService
        storageService = cliconn.EnumerateInstanceNames(ns = LMI_NAMESPACE, cn='LMI_StorageConfigurationService').next()
        # - find appropriate setting
        if param_raidtype == self.Values.CreateRaid.RaidType.RAID0:
            settingName = 'STATIC:RAID0'
        elif param_raidtype == self.Values.CreateRaid.RaidType.RAID1:
            settingName = 'STATIC:RAID1'
        elif param_raidtype == self.Values.CreateRaid.RaidType.RAID5:
            settingName = 'STATIC:RAID5'
        else:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Invalid RaidType')
        setting = pywbem.CIMInstanceName(classname = 'LMI_StorageSetting', namespace = LMI_NAMESPACE, keybindings = {'InstanceID' : 'STATIC:RAID0'})
        (ret, outparams) = cliconn.InvokeMethod(storageService, 'CreateOrModifyStoragePool', Goal = setting, InPools = [pool])
        print 'CreateOrModifyStoragePool()=', ret
        print 'created pool:', outparams['Pool']
        myRaidPool = outparams['Pool']
        
        # allocate LogicalDisk out of the pool, i.e. call
        # LMI_StorageConfigurationService.CreateOrModifyElementFromStoragePool(pool)
        (ret, outparams) = cliconn.InvokeMethod(storageService, 'CreateOrModifyElementFromStoragePool', InPool = myRaidPool, ElementType = pywbem.Uint16(4)) # 4 = create LogicalDisk
        print 'CreateOrModifyElementFromStoragePool()=', ret
        print 'created element:', outparams['TheElement']
        myRaidDisk = outparams['TheElement']

        # create a filesystem on the RAID, i.e. call
        # LMI_FileSystemConfigurationService.CreateFileSystem
        # - find the LMI_FileSystemConfigurationService
        fsService = cliconn.EnumerateInstanceNames(ns = LMI_NAMESPACE, cn='LMI_FileSystemConfigurationService').next()
        (ret, outparams) = cliconn.InvokeMethod(fsService, 'CreateFileSystem', InExtent = myRaidDisk)
        print 'LMI_FileSystemConfigurationService()=', ret
        myFs = outparams['TheElement']

        out_params = [
                pywbem.CIMParameter('disk', type='reference', value = myRaidDisk),
                pywbem.CIMParameter('filesystem', type='reference', value = myFs)
        ]
        rval = self.Values.CreateRaid.Completed_OK
        return (rval, out_params)
     
    class Values(object):
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

        class AttachReplica(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unspecified_Error = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            # Method_Parameters_Checked___Job_Started = 0x1000
            # Method_Reserved = 0x1001..0x7FFF
            # Vendor_Specific = 0x8000..0xFFFF
            class CopyType(object):
                Async = pywbem.Uint16(2)
                Sync = pywbem.Uint16(3)
                UnSyncAssoc = pywbem.Uint16(4)
                UnSyncUnAssoc = pywbem.Uint16(5)
                # DMTF_Reserved = ..
                # Vendor_Specific = 0x8000..0xFFFF

        class CommunicationStatus(object):
            Unknown = pywbem.Uint16(0)
            Not_Available = pywbem.Uint16(1)
            Communication_OK = pywbem.Uint16(2)
            Lost_Communication = pywbem.Uint16(3)
            No_Contact = pywbem.Uint16(4)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 0x8000..

        class CreateOrModifyReplicationPipe(object):
            Success = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unspecified_Error = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            # DMTF_Reserved = ..
            # Busy = 0x1000
            # Method_Reserved = 0x1001..0x7FFF
            # Vendor_Specific = 0x8000..0xFFFF

        class CreateOrModifyStoragePool(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            Size_Not_Supported = pywbem.Uint32(4097)
            # Method_Reserved = 4098..32767
            # Vendor_Specific = 32768..65535

        class DetailedStatus(object):
            Not_Available = pywbem.Uint16(0)
            No_Additional_Information = pywbem.Uint16(1)
            Stressed = pywbem.Uint16(2)
            Predictive_Failure = pywbem.Uint16(3)
            Non_Recoverable_Error = pywbem.Uint16(4)
            Supporting_Entity_in_Error = pywbem.Uint16(5)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 0x8000..

        class AttachOrModifyReplica(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unspecified_Error = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            # Method_Parameters_Checked___Job_Started = 0x1000
            # Method_Reserved = 0x1001..0x7FFF
            # Vendor_Specific = 0x8000..0xFFFF
            class CopyType(object):
                Async = pywbem.Uint16(2)
                Sync = pywbem.Uint16(3)
                UnSyncAssoc = pywbem.Uint16(4)
                UnSyncUnAssoc = pywbem.Uint16(5)
                # DMTF_Reserved = 6..4095
                # Vendor_Specific = 0x1000..0xFFFF

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

        class CreateOrModifyElementFromStoragePool(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            Size_Not_Supported = pywbem.Uint32(4097)
            # Method_Reserved = 4098..32767
            # Vendor_Specific = 32768..65535
            class ElementType(object):
                Unknown = pywbem.Uint16(0)
                Reserved = pywbem.Uint16(1)
                StorageVolume = pywbem.Uint16(2)
                StorageExtent = pywbem.Uint16(3)
                LogicalDisk = pywbem.Uint16(4)
                ThinlyProvisionedStorageVolume = pywbem.Uint16(5)
                ThinlyProvisionedLogicalDisk = pywbem.Uint16(6)
                # DMTF_Reserved = ..
                # Vendor_Specific = 32768..65535

        class PrimaryStatus(object):
            Unknown = pywbem.Uint16(0)
            OK = pywbem.Uint16(1)
            Degraded = pywbem.Uint16(2)
            Error = pywbem.Uint16(3)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 0x8000..

        class DeleteStoragePool(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            # Method_Reserved = 4097..32767
            # Vendor_Specific = 32768..65535

        class ScsiScan(object):
            Success = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            # DMTF_Reserved = 6..4095
            Invalid_connection_type = pywbem.Uint32(4096)
            Invalid_Initiator = pywbem.Uint32(4097)
            No_matching_target_found = pywbem.Uint32(4098)
            No_matching_LUs_found = pywbem.Uint32(4099)
            Prohibited_by_name_binding_configuration = pywbem.Uint32(4100)
            # DMTF_Reserved = ..
            # Vendor_Specific = 32768..65535
            class ConnectionType(object):
                Other = pywbem.Uint16(1)
                Fibre_Channel = pywbem.Uint16(2)
                Parallel_SCSI = pywbem.Uint16(3)
                SSA = pywbem.Uint16(4)
                IEEE_1394 = pywbem.Uint16(5)
                RDMA = pywbem.Uint16(6)
                iSCSI = pywbem.Uint16(7)
                SAS = pywbem.Uint16(8)
                ADT = pywbem.Uint16(9)

        class CreateOrModifyElementFromElements(object):
            Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            Size_Not_Supported = pywbem.Uint32(4097)
            # Method_Reserved = 4098..32767
            # Vendor_Specific = 32768..65535
            class ElementType(object):
                Unknown = pywbem.Uint16(0)
                Reserved = pywbem.Uint16(1)
                Storage_Volume = pywbem.Uint16(2)
                Storage_Extent = pywbem.Uint16(3)
                Storage_Pool = pywbem.Uint16(4)
                Logical_Disk = pywbem.Uint16(5)
                ThinlyProvisionedStorageVolume = pywbem.Uint16(6)
                ThinlyProvisionedLogicalDisk = pywbem.Uint16(7)
                # DMTF_Reserved = ..
                # Vendor_Specific = 32768..65535

        class CreateReplicationBuffer(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unspecified_Error = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            # Method_Parameters_Checked___Job_Started = 0x1000
            # Method_Reserved = 0x1001..0x7FFF
            # Vendor_Specific = 0x8000..0xFFFF

        class GetElementsBasedOnUsage(object):
            Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            # DMTF_Reserved = ..
            # Vendor_Specific = 32768..65535
            class ElementType(object):
                Unknown = pywbem.Uint16(0)
                StorageVolume = pywbem.Uint16(2)
                StorageExtent = pywbem.Uint16(3)
                StoragePool = pywbem.Uint16(4)
                Logical_Disk = pywbem.Uint16(5)
                # DMTF_Reserved = ..
                # Vendor_Specific = 32768..65535
            class Criteria(object):
                Unknown = pywbem.Uint16(0)
                All = pywbem.Uint16(2)
                Available_Only = pywbem.Uint16(3)
                In_Use_Only = pywbem.Uint16(4)
                # DMTF_Reserved = ..
                # Vendor_Specific = 32768..65535

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

        class StartMode(object):
            Automatic = 'Automatic'
            Manual = 'Manual'

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

        class CreateReplica(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            # Method_Reserved = 4097..32767
            # Vendor_Specific = 32768..65535
            class CopyType(object):
                Async = pywbem.Uint16(2)
                Sync = pywbem.Uint16(3)
                UnSyncAssoc = pywbem.Uint16(4)
                UnSyncUnAssoc = pywbem.Uint16(5)
                # DMTF_Reserved = ..
                # Vendor_Specific = 32768..65535

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

        class ReturnToStoragePool(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            # Method_Reserved = 4097..32767
            # Vendor_Specific = 32768..65535

        class AssignStorageResourceAffinity(object):
            Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            Size_Not_Supported = pywbem.Uint32(4097)
            # Method_Reserved = 4098..32767
            # Vendor_Specific = 32768..65535
            class ResourceType(object):
                StorageVolume = pywbem.Uint16(2)
                StoragePool = pywbem.Uint16(3)

        class CreateElementsFromStoragePool(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            Size_Not_Supported = pywbem.Uint32(4097)
            Partially_Completed_Operation = pywbem.Uint32(4098)
            # Method_Reserved = 4099..32767
            # Vendor_Specific = 32768..65535
            class ElementType(object):
                Unknown = pywbem.Uint16(0)
                Reserved = pywbem.Uint16(1)
                StorageVolume = pywbem.Uint16(2)
                StorageExtent = pywbem.Uint16(3)
                LogicalDisk = pywbem.Uint16(4)
                ThinlyProvisionedStorageVolume = pywbem.Uint16(5)
                ThinlyProvisionedLogicalDisk = pywbem.Uint16(6)
                # DMTF_Reserved = ..
                # Vendor_Specific = 32768..65535

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

        class ReturnElementsToStoragePool(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            # Method_Reserved = 4097..32767
            # Vendor_Specific = 32768..65535
            class Options(object):
                Continue_on_nonexistent_element = pywbem.Uint16(2)
                Return_error_on_nonexistent_element = pywbem.Uint16(3)
                # DMTF_Reserved = ..
                # Vendor_Specific = 32768..65535

        class ModifySynchronization(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unspecified_Error = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            # Method_Parameters_Checked___Job_Started = 0x1000
            # Method_Reserved = 0x1001..0x7FFF
            # Vendor_Specific = 0x8000..0xFFFF
            class Operation(object):
                DMTF_Reserved = pywbem.Uint16(0)
                DMTF_Reserved = pywbem.Uint16(1)
                Detach = pywbem.Uint16(2)
                Fracture = pywbem.Uint16(3)
                Resync_Replica = pywbem.Uint16(4)
                Restore_from_Replica = pywbem.Uint16(5)
                Prepare = pywbem.Uint16(6)
                Unprepare = pywbem.Uint16(7)
                Quiesce = pywbem.Uint16(8)
                Unquiesce = pywbem.Uint16(9)
                Reset_To_Sync = pywbem.Uint16(10)
                Reset_To_Async = pywbem.Uint16(11)
                Start_Copy = pywbem.Uint16(12)
                Stop_Copy = pywbem.Uint16(13)
                # DMTF_Reserved = ..
                # Vendor_Specific = 0x8000..0xFFFF

        class RequestUsageChange(object):
            Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            Not_Authorized = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            # Method_Reserved = 4097..32767
            # Vendor_Specific = 32768..65535
            class Operation(object):
                Set = pywbem.Uint16(2)
                Modify__Other__description_only = pywbem.Uint16(3)
                # DMTF_Reserved = ..
                # Vendor_Specific = 32768..65535

        class CreateRaid(object):
            Completed_OK = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Failed = pywbem.Uint32(2)
            # Reserved = 3..32767
            class RaidType(object):
                RAID0 = pywbem.Uint16(0)
                RAID1 = pywbem.Uint16(1)
                RAID5 = pywbem.Uint16(5)
                
## end of class LMI_StorageConfigurationServiceProvider
    
## get_providers() for associating CIM Class Name to python provider class name
    
def get_providers(env): 
    initAnaconda(False)
    LMI_storageconfigurationservice_prov = LMI_StorageConfigurationService(env)  
    return {'LMI_StorageConfigurationService': LMI_storageconfigurationservice_prov} 
