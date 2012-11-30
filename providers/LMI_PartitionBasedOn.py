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
import util.partitioning

class LMI_PartitionBasedOn(BasedOnProvider):
    """
        Implementation of BasedOn class.
    """
    def __init__(self, *args, **kwargs):
        super(LMI_PartitionBasedOn, self).__init__(*args, **kwargs)


    def enumerate_devices(self):
        """
            Enumerate all devices, which are in this association as
            Dependent ones, i.e. all devices, which do not have any
            specialized BasedOn class
        """
        return self.storage.partitions

    def get_logical_partition_start(self, device):
        """
            Return starting address of logical's partition metadata.
        """
        return util.partitioning.get_logical_partition_start(device)

    def get_mbr_instance(self, model, device, base):
        # primary partitions are simple
        if device.isPrimary or device.isExtended:
            return self.get_gpt_instance(model, device, base)

        # startaddress is relative to the beginning of the extended partition
        base_start = base.partedPartition.geometry.start
        # find the metadata
        start = self.get_logical_partition_start(device)
        end = device.partedPartition.geometry.end

        model['OrderIndex'] = pywbem.Uint16(device.partedPartition.number)
        model['StartingAddress'] = pywbem.Uint64(start - base_start)
        model['EndingAddress'] = pywbem.Uint64(end - base_start)
        return model

    def get_gpt_instance(self, model, device, base):
        model['OrderIndex'] = pywbem.Uint16(device.partedPartition.number)
        model['StartingAddress'] = \
            pywbem.Uint64(device.partedPartition.geometry.start)
        model['EndingAddress'] = \
            pywbem.Uint64(device.partedPartition.geometry.end)
        return model

    def get_instance(self, env, model, device=None, base=None):
        model = super(LMI_PartitionBasedOn, self).get_instance(
                env, model, device, base)

        if not device:
            device = self.provider_manager.get_device_for_name(model['Dependent'])
        if not base:
            base = self.provider_manager.get_device_for_name(model['Antecedent'])

        if device.isLogical:
            model = self.get_mbr_instance(model, device, base)
        elif base.format.labelType == 'msdos':
            model = self.get_mbr_instance(model, device, base)
        elif base.format.labelType == 'gpt':
            model = self.get_gpt_instance(model, device, base)
        return model
