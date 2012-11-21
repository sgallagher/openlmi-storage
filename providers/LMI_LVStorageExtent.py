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

from ExtentProvider import ExtentProvider
import pyanaconda.storage
import pywbem

class LMI_LVStorageExtent(ExtentProvider):
    """
        Provider of LMI_LVStorageExtent class.
    """
    
    def __init__(self, *args, **kwargs):
        super(LMI_LVStorageExtent, self).__init__('LMI_LVStorageExtent', *args, **kwargs)


    def providesDevice(self, device):
        """
            Returns True, if this class is provider for given Anaconda
            StorageDevice class.
        """
        if  isinstance(device, pyanaconda.storage.devices.LVMLogicalVolumeDevice):
            return True
        return False
    
    def enumerateDevices(self):
        """
            Enumerate all StorageDevices, that this provider provides.
        """
        for device in self.storage.lvs:
            yield device

    def getElementName(self, device):
        return device.lvname

    def get_instance(self, env, model, device = None):
        """
            Add LV-specific properties.
        """
        model = super(LMI_LVStorageExtent, self).get_instance(env, model, device)
        if not device:
            device = self._getDevice(model)
        
        model['UUID'] = device.uuid

        return model
