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

"""Python Provider for Cura_StorageCapabilities

Instruments the CIM class Cura_StorageCapabilities

"""

import pywbem
from pywbem.cim_provider2 import CIMProvider2
from common import *

class WrappedStorageCapabilities(CIMProvider2):
    """Instrument the CIM class Cura_*Capabilities""" 

    def __init__ (self, env, wrapper):
        logger = env.get_logger()
        logger.log_debug('Initializing provider %s from %s' \
                % (self.__class__.__name__, __file__))
        self.wrapper = wrapper
        super(WrappedStorageCapabilities, self).__init__()

    def get_instance(self, env, model):
        logger = env.get_logger()
        logger.log_debug('Entering %s.get_instance()' \
                % self.__class__.__name__)
        
        device = self.wrapper.getDevice(model)
        if device is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "Device not found.")
        
        return self.wrapper.getCapabilitiesInstance(env, model, device)

    def enum_instances(self, env, model, keys_only):
        logger = env.get_logger()
        logger.log_debug('Entering %s.enum_instances()' \
                % self.__class__.__name__)
                
        model.path.update({'InstanceID': None})
        
        for model in self.wrapper.enumCapabilities(env, model, keys_only):
            yield model




    def set_instance(self, env, instance, modify_existing):
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED) # Remove to implement

    def delete_instance(self, env, instance_name):
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED) # Remove to implement
        
    def cim_method_getsupportedstripelengths(self, env, object_name):
        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_getsupportedstripelengths()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        #out_params = []
        #out_params+= [pywbem.CIMParameter('stripelengths', type='uint16', 
        #                   value=[pywbem.Uint16(),])] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.GetSupportedStripeLengths)
        #return (rval, out_params)
        
    def cim_method_getsupportedparitylayouts(self, env, object_name):
        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_getsupportedparitylayouts()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        #out_params = []
        #out_params+= [pywbem.CIMParameter('paritylayout', type='uint16', 
        #                   value=[self.Values.GetSupportedParityLayouts.ParityLayout.<VAL>,])] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.GetSupportedParityLayouts)
        #return (rval, out_params)
        
    def cim_method_getsupportedstripedepthrange(self, env, object_name):
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        
    def cim_method_creategoalsettings(self, env, object_name,
                                      param_supportedgoalsettings=None,
                                      param_templategoalsettings=None):
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        
    def cim_method_getsupportedstripelengthrange(self, env, object_name):
        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_getsupportedstripelengthrange()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        #out_params = []
        #out_params+= [pywbem.CIMParameter('stripelengthdivisor', type='uint32', 
        #                   value=pywbem.Uint32())] # TODO
        #out_params+= [pywbem.CIMParameter('minimumstripelength', type='uint16', 
        #                   value=pywbem.Uint16())] # TODO
        #out_params+= [pywbem.CIMParameter('maximumstripelength', type='uint16', 
        #                   value=pywbem.Uint16())] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.GetSupportedStripeLengthRange)
        #return (rval, out_params)
        
    def cim_method_getsupportedstripedepths(self, env, object_name):
        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_getsupportedstripedepths()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        #out_params = []
        #out_params+= [pywbem.CIMParameter('stripedepths', type='uint64', 
        #                   value=[pywbem.Uint64(),])] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.GetSupportedStripeDepths)
        #return (rval, out_params)
        
    def cim_method_createsetting(self, env, object_name,
                                 param_settingtype=None):
        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_createsetting()' \
                % self.__class__.__name__)

        # find the capabilities
        device = self.wrapper.getDevice(object_name)
        if not device:
            pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND)
        
        paramsName = self.wrapper.getCapabilitiesName(device)
        params = self.wrapper.getCapabilitiesInstance(env, paramsName, device)

        i = settingManager.generateId()
        setting = {
                'InstanceID': str(i),
                'ChangeableType': pywbem.Uint16(1), #Cura_StorageSetting.Values.ChangeableType.Changeable___Transient,
                'ElementName': str(i),
                'Caption': '',
                'Description': ''
        }
        if not param_settingtype:
            param_settingtype = self.Values.CreateSetting.SettingType.Default
        
        if param_settingtype == self.Values.CreateSetting.SettingType.Default:
            setting.update({
                    'DataRedundancyMin' : params['DataRedundancyDefault'],
                    'DataRedundancyMax' : params['DataRedundancyDefault'],
                    'DataRedundancyGoal': params['DataRedundancyDefault'],
                    'PackageRedundancyMin': params['PackageRedundancyDefault'],
                    'PackageRedundancyMax': params['PackageRedundancyDefault'],
                    'PackageRedundancyGoal': params['PackageRedundancyDefault'],
                    'ExtentStripeLength' : params['ExtentStripeLengthDefault'],
                    'ExtentStripeLengthMin' : params['ExtentStripeLengthDefault'],
                    'ExtentStripeLengthMax' : params['ExtentStripeLengthDefault']
            })
        elif param_settingtype == self.Values.CreateSetting.SettingType.Goal:
            setting.update({
                    'DataRedundancyMin' : params['DataRedundancyMin'],
                    'DataRedundancyMax' : params['DataRedundancyMax'],
                    'DataRedundancyGoal': params['DataRedundancyDefault'],
                    'PackageRedundancyMin': params[' PackageRedundancyMin'],
                    'PackageRedundancyMax': params[' PackageRedundancyMax'],
                    'PackageRedundancyGoal': params[' PackageRedundancyDefault'],
                    'ExtentStripeLength' : params['ExtentStripeLengthDefault'],
                    'ExtentStripeLengthMin' : params['ExtentStripeLengthDefault'],
                    'ExtentStripeLengthMax' : params['ExtentStripeLengthDefault']
            })
        else:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Unsupported settingtype')
 
        #TODO: store the setting       
        settingManager.setSetting(setting)
        
        newsetting = pywbem.CIMParameter('newsetting', type='reference', 
                           value = settingManager.getSettingName(setting))
        rval = self.Values.CreateSetting.Success
        return (rval, [newsetting, ])
        
    class Values(object):
        class SupportedDataOrganizations(object):
            Other = pywbem.Uint16(0)
            Unknown = pywbem.Uint16(1)
            Fixed_Block = pywbem.Uint16(2)
            Variable_Block = pywbem.Uint16(3)
            Count_Key_Data = pywbem.Uint16(4)

        class ParityLayoutDefault(object):
            Non_Rotated_Parity = pywbem.Uint16(2)
            Rotated_Parity = pywbem.Uint16(3)

        class AvailablePortType(object):
            Unknown = pywbem.Uint16(0)
            other = pywbem.Uint16(1)
            SAS = pywbem.Uint16(2)
            SATA = pywbem.Uint16(3)
            SAS_SATA = pywbem.Uint16(4)
            FC = pywbem.Uint16(5)

        class AvailableDiskType(object):
            Unknown = pywbem.Uint16(0)
            Other = pywbem.Uint16(1)
            Hard_Disk_Drive = pywbem.Uint16(2)
            Solid_State_Drive = pywbem.Uint16(3)

        class Encryption(object):
            Unknown = pywbem.Uint16(0)
            Not_Supported = pywbem.Uint16(1)
            Supported = pywbem.Uint16(2)

        class GetSupportedParityLayouts(object):
            Method_completed_OK = pywbem.Uint32(0)
            Method_not_supported = pywbem.Uint32(1)
            Choice_not_aavailable_for_this_capability = pywbem.Uint32(2)
            class ParityLayout(object):
                Non_Rotated_Parity = pywbem.Uint16(2)
                Rotated_Parity = pywbem.Uint16(3)

        class GetSupportedStripeDepthRange(object):
            Method_completed_OK = pywbem.Uint32(0)
            Method_not_supported = pywbem.Uint32(1)
            Use_GetSupportedStripeDepths_instead = pywbem.Uint32(2)

        class AvailableFormFactorType(object):
            Unknown = pywbem.Uint16(0)
            Other = pywbem.Uint16(1)
            Not_Reported = pywbem.Uint16(2)
            _5_25_inch = pywbem.Uint16(3)
            _3_5_inch = pywbem.Uint16(4)
            _2_5_inch = pywbem.Uint16(5)
            _1_8_inch = pywbem.Uint16(6)

        class GetSupportedStripeDepths(object):
            Method_completed_OK = pywbem.Uint32(0)
            Method_not_supported = pywbem.Uint32(1)
            Use_GetSupportedStripeDepthRange_instead = pywbem.Uint32(2)

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

        class GetSupportedStripeLengthRange(object):
            Method_completed_OK = pywbem.Uint32(0)
            Method_not_supported = pywbem.Uint32(1)
            Choices_not_available_for_this_Capability = pywbem.Uint32(2)
            Use_GetSupportedStripeLengths_instead = pywbem.Uint32(3)

        class GetSupportedStripeLengths(object):
            Method_completed_OK = pywbem.Uint32(0)
            Method_not_supported = pywbem.Uint32(1)
            Choices_not_available_for_this_Capability = pywbem.Uint32(2)
            Use_GetSupportedStripeLengthRange_instead = pywbem.Uint32(3)

        class ElementType(object):
            Unknown = pywbem.Uint16(0)
            Reserved = pywbem.Uint16(1)
            Any_Type = pywbem.Uint16(2)
            StorageVolume = pywbem.Uint16(3)
            StorageExtent = pywbem.Uint16(4)
            StoragePool = pywbem.Uint16(5)
            StorageConfigurationService = pywbem.Uint16(6)
            LogicalDisk = pywbem.Uint16(7)
            StorageTier = pywbem.Uint16(8)

        class CreateSetting(object):
            Success = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unspecified_Error = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            # DMTF_Reserved = ..
            # Vendor_Specific = 32768..65535
            class SettingType(object):
                Default = pywbem.Uint16(2)
                Goal = pywbem.Uint16(3)

## end of class Cura_StorageCapabilitiesProvider
