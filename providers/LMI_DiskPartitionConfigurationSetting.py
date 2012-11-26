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

import pywbem
from SettingProvider import SettingProvider
from SettingManager import Setting

import parted

class LMI_DiskPartitionConfigurationSetting(SettingProvider):
    """
        Implementation of LMI_DiskPartitionConfigurationSetting
    """

    def __init__(self, *args, **kwargs):
        supported_properties = {
            'Bootable': self.string_to_bool,
            'Hidden': self.string_to_bool,
            'PartitionType': pywbem.Uint16,
        }
        super(LMI_DiskPartitionConfigurationSetting, self).__init__(
                classname="LMI_DiskPartitionConfigurationSetting",
                supported_properties=supported_properties,
                *args, **kwargs)

    def get_configuration_id(self, device):
        return "LMI:" + self.classname + ":" + device.path

    def get_configuration(self, device):
        setting = Setting(Setting.TYPE_CONFIGURATION,
                self.get_configuration_id(device))
        setting['Bootable'] = str(device.bootable)
        flag = device.getFlag(parted.PARTITION_HIDDEN)
        if flag:
            setting['Hidden'] = "True"
        if device.isExtended:
            setting['PartitionType'] = str(self.DiskPartitionValues.PartitionType.Extended)
        elif device.isLogical:
            setting['PartitionType'] = str(self.DiskPartitionValues.PartitionType.Logical)
        elif device.isPrimary:
            setting['PartitionType'] = str(self.DiskPartitionValues.PartitionType.Primary)
        else:
            setting['PartitionType'] = str(self.DiskPartitionValues.PartitionType.Unknown)
        setting['ElementName'] = setting.id
        return setting


    def enumerate_configurations(self):
        """
            Enumerate all instances attached to partitions.
        """
        for device in self.storage.partitions:
            yield self.get_configuration(device)


    class DiskPartitionValues(object):
        class PartitionType(object):
            Unknown = 0
            Primary = 1
            Extended = 2
            Logical = 3
