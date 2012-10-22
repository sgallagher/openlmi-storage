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

"""Python Provider for LMI_*StorageElementCapabilities"""

import pywbem
from pywbem.cim_provider2 import CIMProvider2

class WrappedStorageElementCapabilities(CIMProvider2):
    """Instrument the CIM class LMI_RAIDStorageElementCapabilities""" 

    def __init__ (self, env, wrapper):
        logger = env.get_logger()
        logger.log_debug('Initializing provider %s from %s' \
                % (self.__class__.__name__, __file__))
        self.wrapper = wrapper
        super(WrappedStorageElementCapabilities, self).__init__()

    def get_instance(self, env, model):
        logger = env.get_logger()
        logger.log_debug('Entering %s.get_instance()' \
                % self.__class__.__name__)
        
        device = self.wrapper.getDevice(model)
        if device is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "Device not found.")
        
        return self.wrapper.getElementCapabilitiesInstance(env, model, device)

    def enum_instances(self, env, model, keys_only):
        logger = env.get_logger()
        logger.log_debug('Entering %s.enum_instances()' \
                % self.__class__.__name__)
                
        model.path.update({'Capabilities': None, 'ManagedElement': None})
        
        for model in self.wrapper.enumElementCapabilities(env, model, keys_only):
            yield model

    def set_instance(self, env, instance, modify_existing):
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED) # Remove to implement

    def delete_instance(self, env, instance_name):
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED) # Remove to implement
        
    def references(self, env, object_name, model, result_class_name, role,
                   result_role, keys_only):
        logger = env.get_logger()
        logger.log_debug('Entering %s.references()' \
                % self.__class__.__name__)
        ch = env.get_cimom_handle()

        # If you want to get references for free, implemented in terms 
        # of enum_instances, just leave the code below unaltered.
        if ch.is_subclass(object_name.namespace, 
                          sub=object_name.classname,
                          super='CIM_Capabilities') or \
                ch.is_subclass(object_name.namespace,
                               sub=object_name.classname,
                               super='CIM_ManagedElement'):
            return self.simple_refs(env, object_name, model,
                          result_class_name, role, result_role, keys_only)
                          
    class Values(object):
        class Characteristics(object):
            Default = pywbem.Uint16(2)
            Current = pywbem.Uint16(3)
            # DMTF_Reserved = ..
            # Vendor_Specific = 32768..65535

## end of class LMI_RAIDStorageElementCapabilitiesProvider
