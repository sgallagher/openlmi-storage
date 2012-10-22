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

"""Python Provider for LMI_StorageSetting

Instruments the CIM class LMI_StorageSetting

"""

from wrapper.common import *
import pywbem
from pywbem.cim_provider2 import CIMProvider2

class LMI_StorageSetting(CIMProvider2):
    """Instrument the CIM class LMI_StorageSetting 

    StorageSetting is roughly equivalent to a Service Level Agreement (SLA)
    It defines the characteristics, qualities of service and goals when
    used in a CreateOrModifyElement FromStoragePool or
    CreateOrModifyStoragePool method in the StorageConfigurationService.
    It specifies a series of properties with Maximum and Minimum values
    that define the (inclusive) bounds that the object should maintain.
    Note that the setting is associated to a StorageVolume or LogicalDisk,
    using ElementSetting. \nThe use of these properties differs depending
    on whether the StorageSetting instance is being used as a goal for a
    configuration operation or being used as a Service Level Agreement for
    a created Volume. In addition the properties fall into two categories:
    The QOS properties(PackageRedundancy, Data Redundancy, &
    NoSinglePointOfFailure) and the Detailed RAID
    properties(ExtentStripeLength, ParityLayout, and UserDataStripeDepth).
    In a Setting used as a goal, the QOS properties are required as a set;
    The Detailed RAID properties(if supported as indicated by the scoping
    StorageCapabilities instance) may be used optionally in any
    combination. The implementation MUST supply it\'s own best practice in
    the case where one or more supported RAID properties are not supplied.
    In this situation the use of StorageSettingWithHints can be useful to
    provide direction to the implementation. \nIn a Setting used as a
    service agreement for a Volume, the QOS properties reflect the Service
    Level Agreement, with goal, min, & max. The actual current service
    level is exposed by corresponding values in StorageExtent. \nThe
    Detailed RAID properties, by contrast, reflect specific values that
    reflect the RAID construction of the Volume. Only the primary values
    are meaningful; Min and Max are set to match. \nCertain StorageSetting
    instances may be classed as "Fixed", by using the "ChangeableType"
    property, indicating the setting is preset. Such settings are used
    when the possible setting variations are low enough to be instantiated
    in their entirety. The StorageCapabilities "CreateSetting" method MAY
    NOT be used to return settings that are not changeable. \nOther
    StorageSetting instances are created using the "CreateSetting" method.
    If the capabilities specifies ranges, then the setting can be used by
    a client to narrow the range to particular values within the range. In
    other words, the capabilities MAY be broad, but the related setting
    MUST be as capable or less capable, that is more narrowly defined,
    before it is used to create or modify resources. \nThese created
    StorageSetting instances MUST have their "ChangeableType" property =
    1, "Changeable - Transient". \nGeneratedSettings MAY not remain after
    the restart or reset of the implementation. They may be deleted by
    implementation at any time. A reasonable minimal time to retain the
    generated transient settings is five minutes, although there is no
    minimal retention time.
    
    """

    SUPPORTED_PROPERTIES = ('Caption', 'ChangeableType',
            'DataRedundancyGoal', 'DataRedundancyMax', 'DataRedundancyMin',
            'ExtentStripeLength',
            'NoSinglePointOfFailure',
            'PackageRedundancyGoal', 'PackageRedundancyMax', 'PackageRedundancyMin',
            'Description', 'ElementName', 'InstanceID', 'LMIAllocationType')

    FIXED_PROPERTIES = { 'SpaceLimit' : 0 }
    
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
        
        instanceId = model['InstanceID']
        setting = settingManager.getSetting(instanceId)
        if not setting:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "Wrong InstanceID")

        model.update(setting)
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
        
        for setting in settingManager.enumerateSettings():
            model.update(settingManager.getSettingName(setting))
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

        if not modify_existing:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED, 'Create not supported.')
        
        instanceId = instance['InstanceID']
        setting = settingManager.getSetting(instanceId)
        if not setting:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, 'Cannot find InstanceID.')
        
        changed = False
        for (name, value) in instance.iteritems():
            if setting.has_key(name) and value == setting[name]:
                continue
            if not setting.has_key(name) and value is None :
                continue
    
            if self.FIXED_PROPERTIES.has_key(name):
                if self.FIXED_PROPERTIES[name] != value:
                    raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Property '+name+' is fixed to ' + str(self.FIXED_PROPERTIES[name]))
                continue
            
            if not name in self.SUPPORTED_PROPERTIES:
                if value:
                    raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Property '+name+' is not supported: ' + str(value))
                # ignore NULL values of unsupported properties
                continue
            
            if name == 'ChangeableType':
                # only some modifications are possible
                print '\n\n Changeable type from ', setting['ChangeableType'], 'to', value
                if not (value == self.Values.ChangeableType.Changeable___Persistent and
                        setting['ChangeableType'] == self.Values.ChangeableType.Changeable___Transient):
                    raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'ChangeableType can be changed only from transient to persistent.')
            
            changed = True
            print 'Changing', name, 'from', setting.get(name, None), 'to', value
            if value is None:
                del setting[name]
            else:
                setting[name] = value
                
        if changed:
            settingManager.setSetting(setting)
                
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

        instanceId = instance_name['InstanceID']
        setting = settingManager.getSetting(instanceId)
        if not setting:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, 'Cannot find InstanceID.')

        settingManager.removeSetting(setting)
        
        
    class Values(object):
        class InitialSynchronization(object):
            Not_Applicable = pywbem.Uint16(0)
            Not_Managed = pywbem.Uint16(1)
            Start = pywbem.Uint16(2)
            Do_Not_Start = pywbem.Uint16(3)
            # DMTF_Reserved = ..
            # Vendor_Specific = 0x8000..

        class ChangeableType(object):
            Fixed___Not_Changeable = pywbem.Uint16(0)
            Changeable___Transient = pywbem.Uint16(1)
            Changeable___Persistent = pywbem.Uint16(2)

        class UseReplicationBuffer(object):
            Not_Applicable = pywbem.Uint16(0)
            Not_Managed = pywbem.Uint16(1)
            Use_Buffer = pywbem.Uint16(2)
            Do_Not_Use_Buffer = pywbem.Uint16(3)
            # DMTF_Reserved = ..
            # Vendor_Specific = 0x8000..

        class Encryption(object):
            Do_Not_Care = pywbem.Uint16(0)
            Not_Supported = pywbem.Uint16(1)
            Supported = pywbem.Uint16(2)

        class StorageExtentInitialUsage(object):
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

        class ThinProvisionedPoolType(object):
            ThinlyProvisionedAllocatedStoragePool = pywbem.Uint16(7)
            ThinlyProvisionedQuotaStoragePool = pywbem.Uint16(8)
            ThinlyProvisionedLimitlessStoragePool = pywbem.Uint16(9)
            # DMTF_Reserved = ..
            # Vendor_Specific = 0x800..0xFFFF

        class FormFactorType(object):
            Do_Not_Care = pywbem.Uint16(0)
            Other = pywbem.Uint16(1)
            Not_Reported = pywbem.Uint16(2)
            _5_25_inch = pywbem.Uint16(3)
            _3_5_inch = pywbem.Uint16(4)
            _2_5_inch = pywbem.Uint16(5)
            _1_8_inch = pywbem.Uint16(6)

        class DiskType(object):
            Do_Not_Care = pywbem.Uint16(0)
            Other = pywbem.Uint16(1)
            Hard_Disk_Drive = pywbem.Uint16(2)
            Solid_State_Drive = pywbem.Uint16(3)

        class ReplicationPriority(object):
            Not_Applicable = pywbem.Uint16(0)
            Not_Managed = pywbem.Uint16(1)
            Low = pywbem.Uint16(2)
            Same = pywbem.Uint16(3)
            High = pywbem.Uint16(4)
            # DMTF_Reserved = ..
            # Vendor_Specific = 0x8000..

        class ParityLayout(object):
            Non_rotated_Parity = pywbem.Uint16(1)
            Rotated_Parity = pywbem.Uint16(2)

        class PortType(object):
            Do_Not_Care = pywbem.Uint16(0)
            other = pywbem.Uint16(1)
            SAS = pywbem.Uint16(2)
            SATA = pywbem.Uint16(3)
            SAS_SATA = pywbem.Uint16(4)
            FC = pywbem.Uint16(5)

        class DataOrganization(object):
            Other = pywbem.Uint16(0)
            Unknown = pywbem.Uint16(1)
            Fixed_Block = pywbem.Uint16(2)
            Variable_Block = pywbem.Uint16(3)
            Count_Key_Data = pywbem.Uint16(4)

        class StoragePoolInitialUsage(object):
            Other = pywbem.Uint16(1)
            Unrestricted = pywbem.Uint16(2)
            Reserved_for_ComputerSystem__the_block_server_ = pywbem.Uint16(3)
            Reserved_as_a_Delta_Replica_Container = pywbem.Uint16(4)
            Reserved_for_Migration_Services = pywbem.Uint16(5)
            Reserved_for_Local_Replication_Services = pywbem.Uint16(6)
            Reserved_for_Remote_Replication_Services = pywbem.Uint16(7)
            Reserved_for_Sparing = pywbem.Uint16(8)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 32768..65535

## end of class LMI_StorageSettingProvider
    
## get_providers() for associating CIM Class Name to python provider class name
    
def get_providers(env): 
    initAnaconda(False)
    LMI_storagesetting_prov = LMI_StorageSetting(env)  
    return {'LMI_StorageSetting': LMI_storagesetting_prov} 
