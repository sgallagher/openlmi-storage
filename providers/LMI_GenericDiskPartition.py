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

class LMI_GenericDiskPartition(ExtentProvider):
    """
        Provider of LMI_GenericDiskPartition class.
    """
    
    def __init__(self, *args, **kwargs):
        super(LMI_GenericDiskPartition, self).__init__('LMI_GenericDiskPartition', *args, **kwargs)


    def provides_device(self, device):
        """
            Returns True, if this class is provider for given Anaconda
            StorageDevice class.
        """
        if  isinstance(device, pyanaconda.storage.devices.PartitionDevice):
            if device.parents[0].format.labelType == 'msdos':
                return False
            return True
        return False
    
    def enumerate_devices(self):
        """
            Enumerate all StorageDevices, that this provider provides.
        """
        for device in self.storage.partitions:
            if self.provides_device(device):
                yield device
