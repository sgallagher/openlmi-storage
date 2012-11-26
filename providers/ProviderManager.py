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
        Simple class containing references to all providers of Anaconda
        StorageDevice subclasses.
        
        Each StorageDevice subclass should have one CIM provider registered in
        a ProviderManager. The manager can then find a CIM provider for a
        StorageDevice instance and find provider or StorageDevice instance
        for CIM InstanceName.
        
        The major benefit of this manager is to convert Anaconda StorageDevice
        instance to CIM InstanceName and back. Therefore various associations
        can easily get their Antecendent/Dependent InstanceNames.
        
        The providers must be registered by add_provider().
        The providers must be subclasses of DeviceProvider class.
    """

    def __init__(self):
        self.providers = []

    def add_provider(self, provider):
        """
            Add new provider to the manager.
        """
        self.providers.append(provider)

    def get_provider_for_name(self, object_name):
        """
            Return provider for given CIM InstanceName.
            Return None if no such provider is registered.
        """
        for p in self.providers:
            if p.provides_name(object_name):
                return p
        return None

    def get_device_for_name(self, object_name):
        """
            Return Anaconda StorageDevice for given CIM InstanceName.
            Return None if no device exist.
        """
        p = self.get_provider_for_name(object_name)
        if p:
            return p.get_device_for_name(object_name)
        return None

    def get_provider_for_device(self, device):
        """
            Return provider for given Anaconda StorageDevice.
            Return None if no such provider is registered.
        """
        for p in self.providers:
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
