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

class ProviderManager(object):
    """
        Simple class containing references to all device providers of Anaconda
        StorageDevice subclasses and all LMI_*Setting providers.
        
        Each StorageDevice subclass should have one CIM provider registered in
        a ProviderManager. The manager can then find a CIM provider for a
        StorageDevice instance and find provider or StorageDevice instance
        for CIM InstanceName.
        
        The same applies to LMI_*Settings - various providers need to get
        Setting for given LMI_*Setting InstanceID.
        
        The major benefit of this manager is to convert Anaconda StorageDevice
        instance to CIM InstanceName and back. Therefore various associations
        can easily get their Antecendent/Dependent InstanceNames.
        
        The device providers must be registered by add_device_provider().
        The device providers must be subclasses of DeviceProvider class.
    """

    def __init__(self):
        self.device_providers = []
        self.setting_providers = []

    def add_device_provider(self, provider):
        """
            Add new device provider to the manager.
        """
        self.device_providers.append(provider)

    def add_setting_provider(self, provider):
        """
            Add new setting provider to the manager.
        """
        self.setting_providers.append(provider)

    def get_device_provider_for_name(self, object_name):
        """
            Return provider for given CIM InstanceName.
            Return None if no such provider is registered.
        """
        for p in self.device_providers:
            if p.provides_name(object_name):
                return p
        return None

    def get_device_for_name(self, object_name):
        """
            Return Anaconda StorageDevice for given CIM InstanceName.
            Return None if no device exist.
        """
        p = self.get_device_provider_for_name(object_name)
        if p:
            return p.get_device_for_name(object_name)
        return None

    def get_provider_for_device(self, device):
        """
            Return provider for given Anaconda StorageDevice.
            Return None if no such provider is registered.
        """
        for p in self.device_providers:
            if p.provides_device(device):
                return p
        return None

    def get_name_for_device(self, device):
        """
            Return CIM InstanceName for given Anaconda StorageDevice.
            Return None if no device exist.
        """
        p = self.get_provider_for_device(device)
        if p:
            return p.get_name_for_device(device)
        return None

    def get_setting_for_id(self, instance_id):
        """
            Return Setting instance for given InstanceID.
            Return None if there is no such instance.
        """
        # parse the instance id
        parts = instance_id.split(":")
        if len(parts) != 3:
            return None
        if parts[0] != "LMI":
            return None
        classname = parts[1]
        for provider in self.setting_providers:
            if provider.setting_classname == classname:
                return provider.find_instance(instance_id)

