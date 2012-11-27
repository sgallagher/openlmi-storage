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

from BaseProvider import BaseProvider
import pywbem

class CapabilitiesProvider(BaseProvider):
    """
        Base class for every LMI_*Capabilities providers.
        It implements get_instance and enum_instances methods.
        
        This class assumes that most LMI_*Capabilities are associated to
        appropriate LMI_*Service and adds support for it.
        
        Of course, LMI_*Capabilities can be associated to different instances
        in subclasses of this provider.
    """

    def __init__(self, classname, *args, **kwargs):
        super(CapabilitiesProvider, self).__init__(*args, **kwargs)
        self.classname = classname

    def create_setting_id(self, myid):
        """
            InstanceID should have format LMI:<classname>:<ID>.
            This method returns string LMI:<classname>:<myid>
        """
        return "LMI:" + self.classname + ":" + myid

    def parse_instance_id(self, instance_id):
        """
            InstanceID should have format LMI:<classname>:<myid>.
            This method checks, that the format is OK and returns the myid.
            It returns None if the format is not OK.
            This method can be used in get_configuration_for_id.
        """
        parts = instance_id.split(":")
        if len(parts) != 3:
            return None
        if parts[0] != "LMI":
            return None
        if parts[1] != self.classname:
            return None
        return parts[2]

    def get_capabilities_for_id(self, instance_id):
        """
            Return dictionary property_name -> value.
            If the capabilities are the default ones, it must have
            '_default' as a property name.
            Return None if there is no such Capabilities instance.
            
            Subclasses can override this method.
        """
        for capabilities in self.enumerate_capabilities():
            if capabilities['InstanceID'] == instance_id:
                return capabilities
        return None

    def enumerate_capabilities(self):
        """
            Return an iterable with all capabilities instances, i.e.
            dictionaries property_name -> value.
            If the capabilities are the default ones, it must have
            '_default' as a property name.
            
            Subclasses must override this method.
        """
        return []

    def create_setting_for_capabilities(self, capabilities):
        """
            Create LMI_*Setting for given capabilities.
            Return CIMInstanceName of the setting or raise CIMError on error. 
            
            Subclasses must override this method.
        """
        return None

    def get_instance(self, env, model, capabilities=None):
        """
            Provider implementation of GetInstance intrinsic method.
        """
        logger = env.get_logger()
        logger.log_debug('Entering %s.get_instance()' \
                % self.__class__.__name__)

        if not capabilities:
            instance_id = model['InstanceID']
            capabilities = self.get_capabilities_for_id(instance_id)
        if not capabilities:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Capabilities not found.")

        # skip _default and other underscore properties
        for (key, value) in capabilities.iteritems():
            if key.startswith("_"):
                continue
            model[key] = value

        return model

    def enum_instances(self, env, model, keys_only):
        """
            Provider implementation of EnumerateInstances intrinsic method.
        """
        logger = env.get_logger()
        logger.log_debug('Entering %s.enum_instances()' \
                % self.__class__.__name__)

        model.path.update({'InstanceID': None})

        for capabilities in self.enumerate_capabilities():
            model['InstanceID'] = capabilities['InstanceID']
            if keys_only:
                yield model
            else:
                yield self.get_instance(env, model, capabilities)

    def is_default(self, capabilities):
        """
            Return True, if the capabilities are the default one, i.e.
            with ElementCapabilities.Characteristics == Default.
        """
        return capabilities.has_key('_default')

    def cim_method_createsetting(self, env, object_name):
        """Implements LMI_DiskPartitionConfigurationCapabilities.CreateSetting()

        Create LMI_DiskPartitionConfigurationSetting applicable to this
        partition table. All properties its will have default values.
        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_createsetting()' \
                % self.__class__.__name__)

        capabilities = self.get_capabilities_for_id(object_name['InstanceID'])
        if not capabilities:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Capabilities not found.")

        setting_name = self.create_setting_for_capabilities(capabilities)

        if not setting_name:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Unknown error when creating setting.")
        out_params = [pywbem.CIMParameter('setting', type='reference',
                value=setting_name)]
        rval = self.Values.CreateSetting.Success
        return (rval, out_params)



    class Values(object):
        class CreateSetting(object):
            Success = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Failed = pywbem.Uint32(2)

class ElementCapabilitiesProvider(BaseProvider):
    """
        Base class for LMI_*ElementCapabilities providers.
        
        If all capabilities instances are associated only with appropriate
        LMI_*Service, this class does not need to be subclasses.
        
        Otherwise, subclasses can associate capabilities to other managed
        elements.
    """
    def __init__(self, classname, capabilities_provider, service_provider,
            *args, **kwargs):
        self.classname = classname
        self.capabilities_provider = capabilities_provider
        self.service_provider = service_provider
        super(ElementCapabilitiesProvider, self).__init__(*args, **kwargs)

    def enumerate_capabilities(self):
        """
            Return iterable with (managed_element_name, capabilities_name),
            where managed_element_name and capabilities_name
            are CIMInstanceName.
            
            By default, all capabilities provided by capabilities_provider
            are associated to service_provider.
            
            Subclasses can override this method if different behavior is
            requested.
        """
        for capabilities in self.capabilities_provider.enumerate_capabilities():
            managed_element_name = pywbem.CIMInstanceName(
                    classname=self.service_provider.classname,
                    namespace=self.config.namespace,
                    keybindings={
                            'CreationClassName': self.service_provider.classname,
                            'Name': self.service_provider.classname,
                            'SystemCreationClassName' : self.config.system_class_name,
                            'SystemName': self.config.system_name
                    })

            capabilities_name = pywbem.CIMInstanceName(
                    classname=self.capabilities_provider.classname,
                    namespace=self.config.namespace,
                    keybindings={'InstanceID' : capabilities['InstanceID']})
            yield (managed_element_name, capabilities_name)

    def enum_instances(self, env, model, keys_only):
        """
            Provider implementation of EnumerateInstances intrinsic method.
        """
        logger = env.get_logger()
        logger.log_debug('Entering %s.enum_instances()' \
                % self.__class__.__name__)

        model.path.update({'Capabilities': None, 'ManagedElement': None})
        for (managed_element, capabilities) in self.enumerate_capabilities():
            model['Capabilities'] = capabilities
            model['ManagedElement'] = managed_element
            if keys_only:
                yield model
            else:
                yield self.get_instance(env, model, capabilities)

    def get_instance(self, env, model, capabilities=None):
        """
            Provider implementation of GetInstance intrinsic method.
        """
        logger = env.get_logger()
        logger.log_debug('Entering %s.get_instance()' \
                % self.__class__.__name__)

        # find the capabilities instance
        if not capabilities:
            for (element_name, capabilities) in self.enumerate_capabilities():
                if (element_name == model['ManagedElement']
                        and capabilities == model['Capabilities']):
                    break
            else:
                raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                        "ElementCapabilities not found.")

        characteristics = [self.Values.Characteristics.Current]
        if self.capabilities_provider.is_default(capabilities):
            characteristics.append(self.Values.Characteristics.Default)

        model['Characteristics'] = characteristics
        return model

    def references(self, env, object_name, model, result_class_name, role,
                   result_role, keys_only):
        """Instrument Associations. """
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
