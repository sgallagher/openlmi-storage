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

from BasedOnProvider import BasedOnProvider
import pywbem
import parted

class LMI_PartitionBasedOn(BasedOnProvider):
    """
        Implementation of BasedOn class.
    """
    def __init__(self, *args, **kwargs):
        super(LMI_PartitionBasedOn, self).__init__(*args, **kwargs)


    def enumerateDevices(self):
        """
            Enumerate all devices, which are in this association as
            Dependent ones, i.e. all devices, which do not have any
            specialized BasedOn class
        """
        return self.storage.partitions
    
    def getLogicalPartitionStart(self, device, base):
        """
            Return starting address of logical's partition metadata.
            TODO: This method probably belongs to PartitionConfigurationService
        """
        part = base.partedPartition.nextPartition()
        metadata = None
        while part is not None:
            if (part.type & parted.PARTITION_LOGICAL
                        and part.type & parted.PARTITION_METADATA):
                metadata = part
            if part.path == device.path:
                break
            part = part.nextPartition()
        
        if not part:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, 'Cannot find the partition on the disk: ' +  device.path)
        if not metadata:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, 'Cannot find metadata for the partition: ' + device.path)
        return metadata.geometry.start

    def getMBRInstance(self, model, device, base):
        # primary partitions are simple
        if device.isPrimary or device.isExtended:
            return self.getGPTInstance(model, device, base)
        
        # now the logical ones
        sectorSize = device.partedDevice.sectorSize
        # startaddress is relative to the beginning of the extended partition
        baseStart = base.partedPartition.geometry.start * sectorSize
        # find the metadata
        start = self.getLogicalPartitionStart(device, base) * sectorSize
        end = device.partedPartition.geometry.end * sectorSize
        
        model['OrderIndex'] = pywbem.Uint16(device.partedPartition.number)
        model['StartingAddress'] = pywbem.Uint64(start - baseStart)
        model['EndingAddress'] = pywbem.Uint64(end - baseStart)
        return model

    def getGPTInstance(self, model, device, base):
        sectorSize = device.partedDevice.sectorSize
        model['OrderIndex'] = pywbem.Uint16(device.partedPartition.number)
        model['StartingAddress'] = pywbem.Uint64(device.partedPartition.geometry.start * sectorSize)
        model['EndingAddress'] = pywbem.Uint64(device.partedPartition.geometry.end * sectorSize)
        return model
        
    def get_instance(self, env, model, device=None, base=None):
        model = super(LMI_PartitionBasedOn, self).get_instance(env, model, device, base)
        
        if not device:
            device = self.manager.getDeviceForName(model['Dependent'])
        if not base:
            base = self.manager.getDeviceForName(model['Antecedent'])
        
        if device.isLogical:
            model = self.getMBRInstance(model, device, base)
        elif base.format.labelType == 'msdos':
            model = self.getMBRInstance(model, device, base)
        elif base.format.labelType == 'gpt':
            model = self.getGPTInstance(model, device, base)
        return model
            
        
        
