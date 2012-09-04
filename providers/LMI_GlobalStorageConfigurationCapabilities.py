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

"""Python Provider for LMI_GlobalStorageConfigurationCapabilities

Instruments the CIM class LMI_GlobalStorageConfigurationCapabilities

"""

import pywbem
from pywbem.cim_provider2 import CIMProvider2

class LMI_GlobalStorageConfigurationCapabilities(CIMProvider2):
    """Instrument the CIM class LMI_GlobalStorageConfigurationCapabilities 

    A subclass of Capabilities that defines the Capabilities of a
    StorageConfigurationService. An instance of
    StorageConfigurationCapabilities is associated with a
    StorageConfigurationService using ElementCapabilities. The properties
    in this class specify the envelope of capabilites for storage
    configuration in the context of the Service or Pool with which the
    instance is associated. These properties correspond to the properties
    of the same base names in StorageSetting and StorageSettingWithHints
    when either is used as a goal parameter to the
    StorageConfigurationService methods (CreateOrModifyStoragePool,
    CreateOrModifyElementFromStoragePool, or
    CreateOrModifyElementFromElements).
    
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
        

        if model['InstanceID'] != 'GlobalStorageConfigurationSettings':
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, 'Wrong keys.')
            
        #model['Caption'] = '' # TODO 
        #model['ClientSettableElementUsage'] = [self.Values.ClientSettableElementUsage.<VAL>,] # TODO 
        #model['ClientSettablePoolUsage'] = [self.Values.ClientSettablePoolUsage.<VAL>,] # TODO 
        #model['Description'] = '' # TODO 
        model['ElementName'] = 'GlobalStorageConfigurationSettings'
        #model['Generation'] = pywbem.Uint64() # TODO 
        #model['InitialReplicationState'] = self.Values.InitialReplicationState.<VAL> # TODO 
        #model['MaximumElementCreateCount'] = pywbem.Uint64() # TODO 
        #model['MaximumElementDeleteCount'] = pywbem.Uint64(0) # TODO 
        #model['MultipleElementCreateFeatures'] = [self.Values.MultipleElementCreateFeatures.<VAL>,] # TODO 
        #model['MultipleElementDeleteFeatures'] = [self.Values.MultipleElementDeleteFeatures.<VAL>,] # TODO 
        model['SupportedAsynchronousActions'] = pywbem.CIMProperty(name='SupportedAsynchronousActions', value=[], type='uint16', array_size=0, is_array=True)
        #model['SupportedCopyTypes'] = [self.Values.SupportedCopyTypes.<VAL>,] # TODO 
        model['SupportedStorageElementFeatures'] = [
                self.Values.SupportedStorageElementFeatures.Single_InPool, # to allocate a LogicalDisk
                self.Values.SupportedStorageElementFeatures.Multiple_InPools, # to allocate a RAID or a LVM
                self.Values.SupportedStorageElementFeatures.LogicalDisk_Creation, # to allocate a LogicalDisk
                self.Values.SupportedStorageElementFeatures.InElements, # only full elements can be allocated
        ]
        model['SupportedStorageElementTypes'] = [self.Values.SupportedStorageElementTypes.LogicalDisk]
        #model['SupportedStorageElementUsage'] = [self.Values.SupportedStorageElementUsage.<VAL>,] # TODO 
        model['SupportedStoragePoolFeatures'] = [
                self.Values.SupportedStoragePoolFeatures.Single_InPool,
                self.Values.SupportedStoragePoolFeatures.Multiple_InPools,
                self.Values.SupportedStoragePoolFeatures.Storage_Pool_Capacity_Expansion, # for LVM
                self.Values.SupportedStoragePoolFeatures.Storage_Pool_Capacity_Reduction, # for LVM
        ]
        #model['SupportedStoragePoolUsage'] = [self.Values.SupportedStoragePoolUsage.<VAL>,] # TODO 
        model['SupportedSynchronousActions'] = [
                self.Values.SupportedSynchronousActions.Storage_Pool_Creation,
                self.Values.SupportedSynchronousActions.Storage_Pool_Deletion,
                self.Values.SupportedSynchronousActions.Storage_Pool_Modification, # Modify LVM
                self.Values.SupportedSynchronousActions.Storage_Element_from_Element_Creation,
        ]
        #model['ThinProvisionedClientSettableReserve'] = bool(False) # TODO 
        #model['ThinProvisionedDefaultReserve'] = pywbem.Uint64(0) # TODO 
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
        model.path.update({'InstanceID': None})
        
        model['InstanceID'] = 'GlobalStorageConfigurationSettings'
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
        
    def cim_method_creategoalsettings(self, env, object_name,
                                      param_supportedgoalsettings=None,
                                      param_templategoalsettings=None):
        """Implements LMI_GlobalStorageConfigurationCapabilities.CreateGoalSettings()

        Method to create a set of supported SettingData elements, from two
        sets of SettingData elements, provided by the caller. \nCreateGoal
        should be used when the SettingData instances that represents the
        goal will not persist beyond the execution of the client and where
        those instances are not intended to be shared with other,
        non-cooperating clients. \nBoth TemplateGoalSettings and
        SupportedGoalSettings are represented as strings containing
        EmbeddedInstances of a CIM_SettingData subclass. These embedded
        instances do not exist in the infrastructure supporting this
        method but are maintained by the caller/client. \nThis method
        should return CIM_Error(s) representing that a single named
        property of a setting (or other) parameter (either reference or
        embedded object) has an invalid value or that an invalid
        combination of named properties of a setting (or other) parameter
        (either reference or embedded object) has been requested. \nIf the
        input TemplateGoalSettings is NULL or the empty string, this
        method returns a default SettingData element that is supported by
        this Capabilities element. \nIf the TemplateGoalSettings specifies
        values that cannot be supported, this method shall return an
        appropriate CIM_Error and should return a best match for a
        SupportedGoalSettings. \nThe client proposes a goal using the
        TemplateGoalSettings parameter and gets back Success if the
        TemplateGoalSettings is exactly supportable. It gets back
        "Alternative Proposed" if the output SupportedGoalSettings
        represents a supported alternative. This alternative should be a
        best match, as defined by the implementation. \nIf the
        implementation is conformant to a RegisteredProfile, then that
        profile may specify the algorithms used to determine best match. A
        client may compare the returned value of each property against the
        requested value to determine if it is left unchanged, degraded or
        upgraded. \n\nOtherwise, if the TemplateGoalSettings is not
        applicable an "Invalid Parameter" error is returned. \n\nWhen a
        mutually acceptable SupportedGoalSettings has been achieved, the
        client may use the contained SettingData instances as input to
        methods for creating a new object ormodifying an existing object.
        Also the embedded SettingData instances returned in the
        SupportedGoalSettings may be instantiated via CreateInstance,
        either by a client or as a side-effect of the execution of an
        extrinsic method for which the returned SupportedGoalSettings is
        passed as an embedded instance.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method CreateGoalSettings() 
            should be invoked.
        param_supportedgoalsettings --  The input parameter SupportedGoalSettings (type pywbem.CIMInstance(classname='CIM_SettingData', ...)) 
            SupportedGoalSettings are elements of class CIM_SettingData, or
            a derived class. \nAt most, one instance of each SettingData
            subclass may be supplied. \nAll SettingData instances provided
            by this property are interpreted as a set, relative to this
            Capabilities instance. \n\nTo enable a client to provide
            additional information towards achieving the
            TemplateGoalSettings, an input set of SettingData instances
            may be provided. If not provided, this property shall be set
            to NULL on input.. Note that when provided, what property
            values are changed, and how, is implementation dependent and
            may be the subject of other standards. \nIf provided, the
            input SettingData instances must be ones that the
            implementation is able to support relative to the
            ManagedElement associated via ElementCapabilities. Typically,
            the input SettingData instances are created by a previous
            instantiation of CreateGoalSettings. \nIf the input
            SupportedGoalSettings is not supported by the implementation,
            then an "Invalid Parameter" (5) error is returned by this
            call. In this case, a corresponding CIM_ERROR should also be
            returned. \nOn output, this property is used to return the
            best supported match to the TemplateGoalSettings. \nIf the
            output SupportedGoalSettings matches the input
            SupportedGoalSettings, then the implementation is unable to
            improve further towards meeting the TemplateGoalSettings.
            
        param_templategoalsettings --  The input parameter TemplateGoalSettings (type pywbem.CIMInstance(classname='CIM_SettingData', ...)) 
            If provided, TemplateGoalSettings are elements of class
            CIM_SettingData, or a derived class, that is used as the
            template to be matched. . \nAt most, one instance of each
            SettingData subclass may be supplied. \nAll SettingData
            instances provided by this property are interpreted as a set,
            relative to this Capabilities instance. \nSettingData
            instances that are not relevant to this instance are ignored.
            \nIf not provided, it shall be set to NULL. In that case, a
            SettingData instance representing the default settings of the
            associated ManagedElement is used.
            

        Returns a two-tuple containing the return value (type pywbem.Uint16 self.Values.CreateGoalSettings)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        SupportedGoalSettings -- (type pywbem.CIMInstance(classname='CIM_SettingData', ...)) 
            SupportedGoalSettings are elements of class CIM_SettingData, or
            a derived class. \nAt most, one instance of each SettingData
            subclass may be supplied. \nAll SettingData instances provided
            by this property are interpreted as a set, relative to this
            Capabilities instance. \n\nTo enable a client to provide
            additional information towards achieving the
            TemplateGoalSettings, an input set of SettingData instances
            may be provided. If not provided, this property shall be set
            to NULL on input.. Note that when provided, what property
            values are changed, and how, is implementation dependent and
            may be the subject of other standards. \nIf provided, the
            input SettingData instances must be ones that the
            implementation is able to support relative to the
            ManagedElement associated via ElementCapabilities. Typically,
            the input SettingData instances are created by a previous
            instantiation of CreateGoalSettings. \nIf the input
            SupportedGoalSettings is not supported by the implementation,
            then an "Invalid Parameter" (5) error is returned by this
            call. In this case, a corresponding CIM_ERROR should also be
            returned. \nOn output, this property is used to return the
            best supported match to the TemplateGoalSettings. \nIf the
            output SupportedGoalSettings matches the input
            SupportedGoalSettings, then the implementation is unable to
            improve further towards meeting the TemplateGoalSettings.
            

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
        logger.log_debug('Entering %s.cim_method_creategoalsettings()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('supportedgoalsettings', type='string', 
        #                   value=[pywbem.CIMInstance(classname='CIM_SettingData', ...),])] # TODO
        #rval = # TODO (type pywbem.Uint16 self.Values.CreateGoalSettings)
        #return (rval, out_params)
        
    class Values(object):
        class SupportedStorageElementTypes(object):
            StorageVolume = pywbem.Uint16(2)
            StorageExtent = pywbem.Uint16(3)
            LogicalDisk = pywbem.Uint16(4)
            ThinlyProvisionedStorageVolume = pywbem.Uint16(5)
            ThinlyProvisionedLogicalDisk = pywbem.Uint16(6)
            ThinlyProvisionedAllocatedStoragePool = pywbem.Uint16(7)
            ThinlyProvisionedQuotaStoragePool = pywbem.Uint16(8)
            ThinlyProvisionedLimitlessStoragePool = pywbem.Uint16(9)
            # DMTF_Reserved = ..
            # Vendor_Specific = 0x8000..0xFFFF

        class SupportedStorageElementUsage(object):
            Other = pywbem.Uint16(1)
            Unrestricted = pywbem.Uint16(2)
            Reserved_for_ComputerSystem__the_block_server_ = pywbem.Uint16(3)
            Reserved_by_Replication_Services = pywbem.Uint16(4)
            Reserved_by_Migration_Services = pywbem.Uint16(5)
            Local_Replica_Source = pywbem.Uint16(6)
            Remote_Replica_Source = pywbem.Uint16(7)
            Local_Replica_Target = pywbem.Uint16(8)
            Remote_Replica_Target = pywbem.Uint16(9)
            Local_Replica_Source_or_Target = pywbem.Uint16(10)
            Remote_Replica_Source_or_Target = pywbem.Uint16(11)
            Delta_Replica_Target = pywbem.Uint16(12)
            Element_Component = pywbem.Uint16(13)
            Reserved_as_Pool_Contributor = pywbem.Uint16(14)
            Composite_Volume_Member = pywbem.Uint16(15)
            Composite_LogicalDisk_Member = pywbem.Uint16(16)
            Reserved_for_Sparing = pywbem.Uint16(17)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 32768..65535

        class SupportedStoragePoolUsage(object):
            Other = pywbem.Uint16(1)
            Unrestricted = pywbem.Uint16(2)
            Reserved_for_ComputerSystem__the_block_server_ = pywbem.Uint16(3)
            Reserved_as_a_Delta_Replica_Container = pywbem.Uint16(4)
            Reserved_for_Migration_Services = pywbem.Uint16(5)
            Reserved_for_Local_Replication_Services = pywbem.Uint16(6)
            Reserved_for_Remote_Replication_Services = pywbem.Uint16(7)
            Reserved_for_Sparing = pywbem.Uint16(8)
            Used_as_source_for_Relocation_Service = pywbem.Uint16(9)
            Used_as_target_for_Relocation_Service = pywbem.Uint16(10)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 32768..65535

        class SupportedStoragePoolFeatures(object):
            InExtents = pywbem.Uint16(2)
            Single_InPool = pywbem.Uint16(3)
            Multiple_InPools = pywbem.Uint16(4)
            Storage_Pool_QoS_Change = pywbem.Uint16(5)
            Storage_Pool_Capacity_Expansion = pywbem.Uint16(6)
            Storage_Pool_Capacity_Reduction = pywbem.Uint16(7)
            # DMTF_Reserved = ..
            # Vendor_Specific = 0x8000..0xFFFF

        class InitialReplicationState(object):
            Initialized = pywbem.Uint16(2)
            Prepared = pywbem.Uint16(3)
            Synchronized = pywbem.Uint16(4)
            # DMTF_Reserved = ..
            # Vendor_Specific = 0x8000..0xFFFF

        class SupportedCopyTypes(object):
            Async = pywbem.Uint16(2)
            Sync = pywbem.Uint16(3)
            UnSyncAssoc = pywbem.Uint16(4)
            UnSyncUnAssoc = pywbem.Uint16(5)
            # DMTF_Reserved = ..
            # Vendor_Specific = 0x8000..0xFFFF

        class ClientSettablePoolUsage(object):
            Other = pywbem.Uint16(1)
            Unrestricted = pywbem.Uint16(2)
            Reserved_for_ComputerSystem__the_block_server_ = pywbem.Uint16(3)
            Reserved_as_a_Delta_Replica_Container = pywbem.Uint16(4)
            Reserved_for_Migration_Services = pywbem.Uint16(5)
            Reserved_for_Local_Replication_Services = pywbem.Uint16(6)
            Reserved_for_Remote_Replication_Services = pywbem.Uint16(7)
            Reserved_for_Sparing = pywbem.Uint16(8)
            Used_as_source_for_Relocation_Service = pywbem.Uint16(9)
            Used_as_target_for_Relocation_Service = pywbem.Uint16(10)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 32768..65535

        class SupportedStorageElementFeatures(object):
            StorageExtent_Creation = pywbem.Uint16(2)
            StorageVolume_Creation = pywbem.Uint16(3)
            StorageExtent_Modification = pywbem.Uint16(4)
            StorageVolume_Modification = pywbem.Uint16(5)
            Single_InPool = pywbem.Uint16(6)
            Multiple_InPools = pywbem.Uint16(7)
            LogicalDisk_Creation = pywbem.Uint16(8)
            LogicalDisk_Modification = pywbem.Uint16(9)
            InElements = pywbem.Uint16(10)
            Storage_Element_QoS_Change = pywbem.Uint16(11)
            Storage_Element_Capacity_Expansion = pywbem.Uint16(12)
            Storage_Element_Capacity_Reduction = pywbem.Uint16(13)
            StorageVolume_To_StoragePool_Relocation = pywbem.Uint16(14)
            StoragePool_To_StoragePool_Relocation = pywbem.Uint16(15)
            StorageVolume_To_StorageExtent_Relocation = pywbem.Uint16(16)
            StoragePool_To_StorageExtent_Relocation = pywbem.Uint16(17)
            LogicalDisk_To_StorageExtent_Relocation = pywbem.Uint16(18)
            # DMTF_Reserved = ..
            # Vendor_Specific = 0x8000..0xFFFF

        class SupportedAsynchronousActions(object):
            Storage_Pool_Creation = pywbem.Uint16(2)
            Storage_Pool_Deletion = pywbem.Uint16(3)
            Storage_Pool_Modification = pywbem.Uint16(4)
            Storage_Element_Creation = pywbem.Uint16(5)
            Storage_Element_Return = pywbem.Uint16(6)
            Storage_Element_Modification = pywbem.Uint16(7)
            Replica_Creation = pywbem.Uint16(8)
            Replica_Modification = pywbem.Uint16(9)
            Replica_Attachment = pywbem.Uint16(10)
            SCSI_Scan = pywbem.Uint16(11)
            Storage_Element_from_Element_Creation = pywbem.Uint16(12)
            Storage_Element_from_Element_Modification = pywbem.Uint16(13)
            Element_Usage_Modification = pywbem.Uint16(14)
            StoragePool_Usage_Modification = pywbem.Uint16(15)
            Storage_Resource_Affinity_Assignment = pywbem.Uint16(16)
            StorageVolume_To_StoragePool_Relocation = pywbem.Uint16(17)
            StoragePool_To_StoragePool_Relocation = pywbem.Uint16(18)
            StorageVolume_To_StorageExtent_Relocation = pywbem.Uint16(19)
            StoragePool_To_StorageExtent_Relocation = pywbem.Uint16(20)
            LogicalDisk_To_StorageExtent_Relocation = pywbem.Uint16(21)
            Multiple_Storage_Element_Creation = pywbem.Uint16(22)
            Multiple_Storage_Element_Return = pywbem.Uint16(23)
            # DMTF_Reserved = ..

        class CreateGoalSettings(object):
            Success = pywbem.Uint16(0)
            Not_Supported = pywbem.Uint16(1)
            Unknown = pywbem.Uint16(2)
            Timeout = pywbem.Uint16(3)
            Failed = pywbem.Uint16(4)
            Invalid_Parameter = pywbem.Uint16(5)
            Alternative_Proposed = pywbem.Uint16(6)
            # DMTF_Reserved = ..
            # Vendor_Specific = 32768..65535

        class MultipleElementDeleteFeatures(object):
            Continue_on_nonexistent_element = pywbem.Uint16(2)
            Return_error_on_nonexistent_element = pywbem.Uint16(3)
            # DMTF_Reserved = ..
            # Vendor_Specific = 0x8000..0xFFFF

        class ClientSettableElementUsage(object):
            Other = pywbem.Uint16(1)
            Unrestricted = pywbem.Uint16(2)
            Reserved_for_ComputerSystem__the_block_server_ = pywbem.Uint16(3)
            Reserved_by_Replication_Services = pywbem.Uint16(4)
            Reserved_by_Migration_Services = pywbem.Uint16(5)
            Local_Replica_Source = pywbem.Uint16(6)
            Remote_Replica_Source = pywbem.Uint16(7)
            Local_Replica_Target = pywbem.Uint16(8)
            Remote_Replica_Target = pywbem.Uint16(9)
            Local_Replica_Source_or_Target = pywbem.Uint16(10)
            Remote_Replica_Source_or_Target = pywbem.Uint16(11)
            Delta_Replica_Target = pywbem.Uint16(12)
            Element_Component = pywbem.Uint16(13)
            Reserved_as_Pool_Contributor = pywbem.Uint16(14)
            Composite_Volume_Member = pywbem.Uint16(15)
            Composite_LogicalDisk_Member = pywbem.Uint16(16)
            Reserved_for_Sparing = pywbem.Uint16(17)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 32768..65535

        class MultipleElementCreateFeatures(object):
            Single_instance_creation_indication = pywbem.Uint16(2)
            # DMTF_Reserved = ..
            # Vendor_Specific = 0x8000..0xFFFF

        class SupportedSynchronousActions(object):
            Storage_Pool_Creation = pywbem.Uint16(2)
            Storage_Pool_Deletion = pywbem.Uint16(3)
            Storage_Pool_Modification = pywbem.Uint16(4)
            Storage_Element_Creation = pywbem.Uint16(5)
            Storage_Element_Return = pywbem.Uint16(6)
            Storage_Element_Modification = pywbem.Uint16(7)
            Replica_Creation = pywbem.Uint16(8)
            Replica_Modification = pywbem.Uint16(9)
            Replica_Attachment = pywbem.Uint16(10)
            SCSI_Scan = pywbem.Uint16(11)
            Storage_Element_from_Element_Creation = pywbem.Uint16(12)
            Storage_Element_from_Element_Modification = pywbem.Uint16(13)
            Element_Usage_Modification = pywbem.Uint16(14)
            StoragePool_Usage_Modification = pywbem.Uint16(15)
            Storage_Resource_Affinity_Assignment = pywbem.Uint16(16)
            StorageVolume_To_StoragePool_Relocation = pywbem.Uint16(17)
            StoragePool_To_StoragePool_Relocation = pywbem.Uint16(18)
            StorageVolume_To_StorageExtent_Relocation = pywbem.Uint16(19)
            StoragePool_To_StorageExtent_Relocation = pywbem.Uint16(20)
            LogicalDisk_To_StorageExtent_Relocation = pywbem.Uint16(21)
            Multiple_Storage_Element_Creation = pywbem.Uint16(22)
            Multiple_Storage_Element_Return = pywbem.Uint16(23)
            # DMTF_Reserved = ..

## end of class LMI_GlobalStorageConfigurationCapabilitiesProvider
    
## get_providers() for associating CIM Class Name to python provider class name
    
def get_providers(env): 
    LMI_globalstorageconfigurationcapabilities_prov = LMI_GlobalStorageConfigurationCapabilities(env)  
    return {'LMI_GlobalStorageConfigurationCapabilities': LMI_globalstorageconfigurationcapabilities_prov} 
