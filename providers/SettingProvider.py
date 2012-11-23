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

import pywbem
from BaseProvider import BaseProvider
from SettingManager import Setting

class SettingProvider(BaseProvider):
    """
        Base of all LMI_*Setting providers.
        Every setting class can have:
            - number of fixed preconfigured instances
            - number of configurable persistent instances
            - number of configurable in-memory (transient) instances
            - instances associated to managed elements
        This class provides all four instance types.
        
        The setting itself is represented by dictionary of key -> value.
        
        Preconfigured instances are stored in /etc/openlmi/storage/settings/<classname>.ini
        Persistent instances are stored in /var/lib/openlmi-storage/settings/<classname>.ini
    """
    def __init__(self, classname, supportedProperties, *args, **kwargs):
        """
            classname = name of CIM class, which we provide
            supportedProperties = hash propertyName -> constructor
                constructor is a function which takes string argument
                and returns CIM value. (i.e. pywbem.Uint16
                or bool or string etc).
        """
        self.classname = classname
        supportedProperties['Caption'] = str
        supportedProperties['ConfigurationName'] = str
        supportedProperties['Description'] = str
        supportedProperties['ChangeableType'] = pywbem.Uint16
        supportedProperties['ElementName'] = str
        
        self.supportedProperties = supportedProperties
        
        super(SettingProvider, self).__init__(*args, **kwargs)

    def enumerateConfigurations(self):
        """
            Enumerate all instances of LMI_*Setting, which are attached 
            to managed elements, i.e. are not transient, persistent nor
            preconfigured.
            
            This method returns iterabe with Setting instances.
            
            Subclasses should override this method.
        """
        return []

    def enum_instances(self, env, model, keys_only):
        """
            Provider implementation of EnumerateInstances intrinsic method.
            Subclasses should not override this method, they should override
            enumerateConfigurations only.
        """
        model.path.update({'InstanceID': None})

        # handle transient, persistent and preconfigured settings
        settings = self.settingManager.getSettings(self.classname)
        for setting in settings.values():
            model['InstanceID'] = setting.id
            if keys_only:
                yield model
            else:
                yield self.get_instance(env, model, setting)

        # handle configurations
        for setting in self.enumerateConfigurations():
            model['InstanceID'] = setting.id
            if keys_only:
                yield model
            else:
                yield self.get_instance(env, model, setting)

    def findInstance(self, instanceId):
        # find the setting in settingManager
        settings = self.settingManager.getSettings(self.classname)
        if settings.has_key(instanceId):
            return settings[instanceId]
            
        # find the setting in configurations
        # TODO: this can be probably optimized
        for s in self.enumerateConfigurations():
            if s.id == instanceId:
                return s
        return None
        
    def get_instance(self, env, model, setting = None):
        """
            Provider implementation of GetInstance intrinsic method.
        """
        if not setting:
            setting = self.findInstance(model['InstanceID'])
            
        if not setting:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "Cannot find setting.")
        
        # convert setting to model using supportedProperties
        for (name, value) in setting.items():
            if value is not None:
                if self.supportedProperties.has_key(name):
                    model[name] = self.supportedProperties[name](value)
        
        if setting.type == Setting.TYPE_CONFIGURATION:
            model['ChangeableType'] = self.SettingProviderValues.ChangeableType.Not_Changeable_Transient
        elif setting.type == Setting.TYPE_PERSISTENT:
            model['ChangeableType'] = self.SettingProviderValues.ChangeableType.Changeable_Persistent
        elif setting.type == Setting.TYPE_PRECONFIGURED:
            model['ChangeableType'] = self.SettingProviderValues.ChangeableType.Not_Changeable_Persistent
        elif setting.type == Setting.TYPE_TRANSIENT:
            model['ChangeableType'] = self.SettingProviderValues.ChangeableType.Changeable_Transient
            
        return model
    
    def stringToBool(self, value):
        if value == 1 or value == "true" or value == "True":
            return True
        elif value == 0 or value == "false" or value == "False":
            return False
        return bool(value)
    
    
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
        
        setting = self.findInstance(instance['InstanceID'])
        if not setting:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "Cannot find setting.")
        
        if not modify_existing:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED, "CreateInstance is not supported.")
        
        if (setting.type == Setting.TYPE_CONFIGURATION
                or setting.type == Setting.TYPE_PRECONFIGURED):
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, "Cannot modify not-changeable setting.")

        for name in instance.iterkeys():
            if name == 'InstanceID':
                continue
            if not self.supportedProperties.has_key(name):
                if instance[name]:
                    raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, "Property is not supported: " + name)
                continue
            if name == 'ChangeableType':
                if setting.type == Setting.TYPE_TRANSIENT:
                    if instance[name] == self.SettingProviderValues.ChangeableType.Changeable_Persistent:
                        # can change only transient -> persistent
                        setting.type = Setting.TYPE_PERSISTENT
                        continue
                    if instance[name] == self.SettingProviderValues.ChangeableType.Changeable_Transient:
                        # ignore transient -> transient
                        continue
                elif ( setting.type == Setting.TYPE_PERSISTENT
                            and instance[name] == self.SettingProviderValues.ChangeableType.Changeable_Persistent):
                    # ignore persistent -> persistent
                    continue

                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, "Cannot modify ChangeableType property to new value.")
            if instance[name] is not None:
                setting[name] = str(instance[name])
            else:
                setting[name] = None
                

        self.settingManager.setSetting(self.classname, setting)
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

        setting = self.findInstance(instance_name['InstanceID'])
        if not setting:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "Cannot find setting.")
                
        if (setting.type == Setting.TYPE_CONFIGURATION
                or setting.type == Setting.TYPE_PRECONFIGURED):
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, "Cannot delete not-changeable setting.")
        
        self.settingManager.deleteSetting(self.classname, setting)
        
    def cim_method_clonesetting(self, env, object_name):
        """Implements LMI_DiskPartitionConfigurationSetting.CloneSetting()

        Create a copy of this instance. The resulting instance will have
        the same class and the same properties as the original instance
        except ChangeableType, which will be set to "Changeable -
        Transient" in the clone, and InstanceID.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method CloneSetting() 
            should be invoked.

        Returns a two-tuple containing the return value (type pywbem.Uint32)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Clone -- (type REF (pywbem.CIMInstanceName(classname='CIM_StorageSetting', ...)) 
            Created copy.
            

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
        logger.log_debug('Entering %s.cim_method_clonesetting()' \
                % self.__class__.__name__)

        setting = self.findInstance(object_name['InstanceID'])
        if not setting:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "Cannot find setting.")

        instanceId = self.settingManager.allocateId(self.classname)
        print "instanceid = ", instanceId
        newSetting = Setting(Setting.TYPE_TRANSIENT, instanceId)
        for (key, value) in setting.items():
            newSetting[key] = value
        self.settingManager.setSetting(self.classname, newSetting)
        
        out_params = []
        out_params+= [pywbem.CIMParameter('clone', type='reference', 
                           value=pywbem.CIMInstanceName(
                                   classname=self.classname,
                                   namespace=self.config.namespace,
                                   keybindings= {'InstanceID' : instanceId}))]
        return (self.SettingProviderValues.CloneSetting.Success, out_params)

    
    class SettingProviderValues(object):
        class ChangeableType(object):
            Not_Changeable_Persistent = pywbem.Uint16(0)
            Changeable_Transient = pywbem.Uint16(1)
            Changeable_Persistent = pywbem.Uint16(2)
            Not_Changeable_Transient = pywbem.Uint16(3)
            
        class CloneSetting(object):
            Success = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Failed = pywbem.Uint32(2)