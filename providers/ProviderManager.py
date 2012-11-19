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
        
        The providers must be registered by addProvider().
        The providers must be subclasses of DeviceProvider class.
    """
        
    def __init__(self):
        self.providers = []
        
    def addProvider(self, provider):
        """
            Add new provider to the manager.
        """
        self.providers.append(provider)
    
    def getProviderForName(self, objectName):
        """
            Return provider for given CIM InstanceName.
            Return None if no such provider is registered.
        """
        for p in self.providers:
            if p.providesName(objectName):
                return p
        return None

    def getDeviceForName(self, objectName):
        """
            Return Anaconda StorageDevice for given CIM InstanceName.
            Return None if no device exist.
        """
        p = self.getProviderForName(objectName)
        if p:
            return p.getDeviceForName(objectName)
        return None
        
    def getProviderForDevice(self, device):
        """
            Return provider for given Anaconda StorageDevice.
            Return None if no such provider is registered.
        """
        for p in self.providers:
            if p.providesDevice(device):
                return p
        return None
    
    def getNameForDevice(self, device):
        """
            Return CIM InstanceName for given Anaconda StorageDevice.
            Return None if no device exist.
        """
        p = self.getProviderForDevice(device)
        if p:
            return p.getNameForDevice(device)
        return None
