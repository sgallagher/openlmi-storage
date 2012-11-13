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

"""Python Provider for LMI_PrimaryMBRDiskPartitionConfigurationCapabilities

Instruments the CIM class LMI_PrimaryMBRDiskPartitionConfigurationCapabilities

"""

from wrapper.common import *
import pywbem
from pywbem.cim_provider2 import CIMProvider2
import util.partitioning

class LMI_DiskPartitionConfigurationCapabilities(CIMProvider2):
    """Instrument the CIM class LMI_PrimaryMBRDiskPartitionConfigurationCapabilities 

    POC DiskPartitionConfigurationCapabilities of primary MBR partition
    table. Size of this partition table is fixed.
    
    """

    def __init__ (self, env):
        logger = env.get_logger()
        logger.log_debug('Initializing provider %s from %s' \
                % (self.__class__.__name__, __file__))
        gpt = {'PartitionStyle': self.Values.PartitionStyle.GPT,
                'MaxNumberOfPartitions': pywbem.Uint16(128), # TODO ???
                'MaxCapacity': pywbem.Uint64(2**31-1),
                'OverlapAllowed': False,
                'PartitionTableSize': pywbem.Uint32(2*util.partitioning.GPT_SIZE), # count also the secondary GPT!
                'ElementName': 'GPT'
        }
        
        mbr = {'PartitionStyle': self.Values.PartitionStyle.MBR,
                'ValidSubPartitionStyles': [self.Values.ValidSubPartitionStyles.MBR],
                'MaxNumberOfPartitions': pywbem.Uint16(4),
                'MaxCapacity': pywbem.Uint64(2**31-1),
                'OverlapAllowed': False,
                'PartitionTableSize': pywbem.Uint32(1),
                'ElementName': 'MBR'
        }
        embr = {'PartitionStyle': self.Values.PartitionStyle.MBR,
                'MaxNumberOfPartitions': pywbem.Uint16(65535),
                'MaxCapacity': pywbem.Uint64(2**31-1),
                'OverlapAllowed': False,
                'PartitionTableSize': pywbem.Uint32(1),
                'ElementName': 'ExtendedMBR'
        }
        self.instances = {util.partitioning.TYPE_GPT: gpt, util.partitioning.TYPE_MBR: mbr, util.partitioning.TYPE_EMBR: embr}

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

        instance = self.instances.get(model['InstanceID'], None)
        if not instance:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, 'Wrong InstanceID')

        model.update(instance)
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
        
        for instanceId in self.instances.keys():
            model['InstanceID'] = instanceId
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
        """Implements LMI_PrimaryMBRDiskPartitionConfigurationCapabilities.CreateGoalSettings()

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
        rval = None # TODO (type pywbem.Uint16 self.Values.CreateGoalSettings)
        return (rval, out_params)
        
    class Values(object):
        class ValidSubPartitionStyles(object):
            Other = pywbem.Uint16(1)
            MBR = pywbem.Uint16(2)
            VTOC = pywbem.Uint16(3)
            GPT = pywbem.Uint16(4)

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

        class SupportedSynchronousActions(object):
            SetPartitionStyle = pywbem.Uint16(2)
            CreateOrModifyPartition = pywbem.Uint16(3)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 0x8000..

        class PartitionStyle(object):
            MBR = pywbem.Uint16(2)
            GPT = pywbem.Uint16(3)
            VTOC = pywbem.Uint16(4)

## end of class LMI_PrimaryMBRDiskPartitionConfigurationCapabilitiesProvider
    
## get_providers() for associating CIM Class Name to python provider class name
    
def get_providers(env): 
    initAnaconda(False)
    LMI_diskpartitionconfigurationcapabilities_prov = LMI_DiskPartitionConfigurationCapabilities(env)  
    return {'LMI_DiskPartitionConfigurationCapabilities': LMI_diskpartitionconfigurationcapabilities_prov} 
