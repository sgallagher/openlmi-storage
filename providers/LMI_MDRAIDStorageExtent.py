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
import cmpi_logging
from DeviceProvider import DeviceProvider

class LMI_MDRAIDStorageExtent(ExtentProvider):
    """
        Provider of LMI_MDRAIDStorageExtent class.
    """

    @cmpi_logging.trace_method
    def __init__(self, *args, **kwargs):
        super(LMI_MDRAIDStorageExtent, self).__init__(
                'LMI_MDRAIDStorageExtent', *args, **kwargs)


    @cmpi_logging.trace_method

    def provides_device(self, device):
        """
            Returns True, if this class is provider for given Anaconda
            StorageDevice class.
        """
        if  isinstance(device, pyanaconda.storage.devices.MDRaidArrayDevice):
            return True
        return False

    @cmpi_logging.trace_method
    def enumerate_devices(self):
        """
            Enumerate all StorageDevices, that this provider provides.
        """
        for device in self.storage.mdarrays:
            yield device

    @cmpi_logging.trace_method
    def get_redundancy(self, device):
        """
            Returns redundancy characteristics for given Anaconda StorageDevice.
        """
        parents = self.get_base_devices(device)
        # find all parents and get their redundancy
        redundancies = map(self._find_redundancy, parents)
        if device.level in [0, 1, 5, 6, DeviceProvider.Redundancy.LINEAR]:
            final_redundancy = DeviceProvider.Redundancy.get_common_redundancy_list(redundancies, device.level)
        else:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Unsupported raid type: " + str(device.level))

        return final_redundancy

    @cmpi_logging.trace_method
    def get_instance(self, env, model, device=None):
        """
            Add MD RAID-specific properties.
        """
        model = super(LMI_MDRAIDStorageExtent, self).get_instance(
                env, model, device)
        if not device:
            device = self._get_device(model)
        model['UUID'] = device.uuid
        return model
