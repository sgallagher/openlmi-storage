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

class LMI_DiskPartition(ExtentProvider):
    """
        Provider of LMI_DiskPartition class.
    """
    
    def __init__(self, *args, **kwargs):
        super(LMI_DiskPartition, self).__init__('LMI_DiskPartition', *args, **kwargs)


    def providesDevice(self, device):
        """
            Returns True, if this class is provider for given Anaconda
            StorageDevice class.
        """
        if  isinstance(device, pyanaconda.storage.devices.PartitionDevice):
            if device.disk.format.labelType == 'msdos':
                return True
        return False
    
    def getBaseDevices(self, device):
        if device.isPrimary or device.isExtended:
            return super(LMI_DiskPartition, self).getBaseDevices(device)    
        
        # logical partitions depend on the extended partition
        partedExt = device.disk.format.partedDisk.getExtendedPartition()
        if not partedExt:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, 'Cannot find extended partition for device: ' + device.path)
        
        ext = self.storage.devicetree.getDeviceByPath(partedExt.path)
        return [ext,]
        

    def enumerateDevices(self):
        """
            Enumerate all StorageDevices, that this provider provides.
        """
        for device in self.storage.partitions:
            if self.providesDevice(device):
                yield device

    def get_instance(self, env, model, device = None):
        """
            Add partition-specific properties.
        """
        model = super(LMI_DiskPartition, self).get_instance(env, model, device)
        if not device:
            device = self._getDevice(model)
        
        model['PrimaryPartition'] = device.isPrimary
        if device.isPrimary:
            model['PartitionType'] = self.DiskPartitionValues.PartitionType.Primary
        if device.isExtended:
            model['PartitionType'] = self.DiskPartitionValues.PartitionType.Extended
        if device.isLogical:
            model['PartitionType'] = self.DiskPartitionValues.PartitionType.Logical

        return model
        
    class DiskPartitionValues(object):
        class PartitionType(object):
            Unknown = pywbem.Uint16(0)
            Primary = pywbem.Uint16(1)
            Extended = pywbem.Uint16(2)
            Logical = pywbem.Uint16(3)

            
