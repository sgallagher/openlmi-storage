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

class LMI_MDRAIDStorageExtent(ExtentProvider):
    """
        Provider of LMI_MDRAIDStorageExtent class.
    """

    def __init__(self, *args, **kwargs):
        super(LMI_MDRAIDStorageExtent, self).__init__(
                'LMI_MDRAIDStorageExtent', *args, **kwargs)


    def provides_device(self, device):
        """
            Returns True, if this class is provider for given Anaconda
            StorageDevice class.
        """
        if  isinstance(device, pyanaconda.storage.devices.MDRaidArrayDevice):
            return True
        return False

    def enumerate_devices(self):
        """
            Enumerate all StorageDevices, that this provider provides.
        """
        for device in self.storage.mdarrays:
            yield device

    def _getRedundancy0(self, a, b):
        """
            Return the combined data redundancy characteristics for
            two devices combined in RAID0.
        """
        # data is spread on all devices -> DataRedundancy is sum of base DataRedundancies
        # PackageRedundancy is the minimum of PackageRedundancies
        data_dedundancy = min(a.data_dedundancy, b.data_dedundancy)
        package_redundancy = min(a.package_redundancy, b.package_redundancy)
        no_single_point_of_failure = a.no_single_point_of_failure and b.no_single_point_of_failure
        stripe_length = a.stripe_length + b.stripe_length

        return self.Redundancy(
                no_single_point_of_failure=no_single_point_of_failure,
                data_dedundancy=data_dedundancy,
                package_redundancy=package_redundancy,
                stripe_length=stripe_length)

    def _getRedundancy1(self, a, b):
        """
            Return the combined data redundancy characteristics for
            two devices combined in RAID1.
        """
        data_dedundancy = a.data_dedundancy + b.data_dedundancy
        package_redundancy = a.package_redundancy + b.package_redundancy
        no_single_point_of_failure = True
        stripe_length = min(a.stripe_length, b.stripe_length)

        return self.Redundancy(
                no_single_point_of_failure=no_single_point_of_failure,
                data_dedundancy=data_dedundancy,
                package_redundancy=package_redundancy,
                stripe_length=stripe_length)

    def _getRedundancy5(self, a, b):
        """
            Return the combined data redundancy characteristics for
            two devices combined in RAID5.
        """
        data_dedundancy = min(a.data_dedundancy, b.data_dedundancy)
        package_redundancy = min(a.package_redundancy, b.package_redundancy)
        no_single_point_of_failure = True
        stripe_length = a.stripe_length + b.stripe_length

        return self.Redundancy(
                no_single_point_of_failure=no_single_point_of_failure,
                data_dedundancy=data_dedundancy,
                package_redundancy=package_redundancy,
                stripe_length=stripe_length)

    def get_redundancy(self, device):
        """
            Returns redundancy characterictics for given Anaconda StorageDevice.
            
            Calculate RAID redundancy.
        """
        parents = self.get_base_devices(device)
        # find all parents and get their redundancy
        redundancies = map(self._findRedundancy, parents)
        if (device.level == 0):
            # iteratively call self._getRedundancy0(r1, r2), ...
            final_redundancy = reduce(self._getRedundancy0, redundancies)

        elif (device.level == 1):
            # DataRedundancy is minimum of all
            # PackageRedundancy - all but one underlying device can fail,
            final_redundancy = reduce(self._getRedundancy1, redundancies)
            final_redundancy.package_redundancy = \
                    final_redundancy.package_redundancy + len(parents) - 1

        elif (device.level == 5):
            # DataRedundancy is minimum of all
            # PackageRedundancy - one whole underlying device can fail
            final_redundancy = reduce(self._getRedundancy5, redundancies)
            final_redundancy.package_redundancy = \
                    final_redundancy.package_redundancy + 1

        else:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Unsupported raid type: " + str(device.level))

        return final_redundancy

    def get_instance(self, env, model, device=None):
        """
            Add MD RAID-specific properties.
        """
        model = super(LMI_MDRAIDStorageExtent, self).get_instance(
                env, model, device)
        if not device:
            device = self._getDevice(model)
        model['UUID'] = device.uuid
        return model
