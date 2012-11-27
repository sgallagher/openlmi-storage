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

from CapabilitiesProvider import CapabilitiesProvider
from LMI_DiskPartitionConfigurationSetting import LMI_DiskPartitionConfigurationSetting
from SettingManager import Setting
import pywbem

MAXINT64 = pywbem.Uint64((2 << 63) - 1)

class LMI_DiskPartitionConfigurationCapabilities(CapabilitiesProvider):
    """
        LMI_DiskPartitionConfigurationCapabilities provider implementation.
    """

    def __init__(self, *args, **kwargs):
        super(LMI_DiskPartitionConfigurationCapabilities, self).__init__(
                "LMI_DiskPartitionConfigurationCapabilities", *args, **kwargs)

        self.instances = [
            {
                    'InstanceID': 'MBRCapabilities',
                    'SupportedSettings': [
                            self.Values.SupportedSettings.Partition_Type,
                            self.Values.SupportedSettings.Bootable,
                            self.Values.SupportedSettings.Hidden],
                    'PartitionTableSize': pywbem.Uint32(1),
                    'PartitionStyle': self.Values.PartitionStyle.MBR,
                    'ValidSubPartitionStyles': [self.Values.ValidSubPartitionStyles.EMBR],
                    'MaxNumberOfPartitions': pywbem.Uint16(4),
                    'SupportedSynchronousActions': [
                            self.Values.SupportedSynchronousActions.CreateOrModifyPartition,
                            self.Values.SupportedSynchronousActions.SetPartitionStyle],
                    'Caption': "Capabilities of MS-DOS style primary partitions.",
                    'MaxCapacity': MAXINT64,
                    'ElementName': 'MBRCapabilities',
                    'OverlapAllowed' : False,
            },
            {
                    'InstanceID': 'EMBRCapabilities',
                    'SupportedSettings': [
                            self.Values.SupportedSettings.Bootable,
                            self.Values.SupportedSettings.Hidden],
                    'PartitionTableSize': pywbem.Uint32(1),
                    'PartitionStyle': self.Values.PartitionStyle.EMBR,
                    'ValidSubPartitionStyles': pywbem.CIMProperty(
                            name='MaxNumberOfPartitions',
                            value=None,
                            type='uint16',
                            array_size=0,
                            is_array=True),
                    'MaxNumberOfPartitions': pywbem.Uint16(2 << 15 - 1),
                    'SupportedSynchronousActions': [
                            self.Values.SupportedSynchronousActions.CreateOrModifyPartition,
                            self.Values.SupportedSynchronousActions.SetPartitionStyle],
                    'Caption': "Capabilities of MS-DOS style logical partitions.",
                    'MaxCapacity': MAXINT64,
                    'ElementName': 'EMBRCapabilities',
                    'OverlapAllowed' : False,
            },
            {
                    'InstanceID': 'GPTCapabilities',
                    'SupportedSettings': [
                            self.Values.SupportedSettings.Bootable, ],
                    'PartitionTableSize': pywbem.Uint32(68),
                    'PartitionStyle': self.Values.PartitionStyle.GPT,
                    'ValidSubPartitionStyles': pywbem.CIMProperty(
                            name='MaxNumberOfPartitions',
                            value=None,
                            type='uint16',
                            array_size=0,
                            is_array=True),
                    'MaxNumberOfPartitions': pywbem.Uint16(128),
                    'SupportedSynchronousActions': [
                            self.Values.SupportedSynchronousActions.CreateOrModifyPartition,
                            self.Values.SupportedSynchronousActions.SetPartitionStyle],
                    'Caption': "Capabilities of GPT partitions.",
                    'MaxCapacity': MAXINT64,
                    'ElementName': 'GPTCapabilities',
                    'OverlapAllowed' : False,
                    '_default': True,
            },
    ]


    def enumerate_capabilities(self):
        """
            Return an iterable with all capabilities instances, i.e.
            dictionaries property_name -> value.
            If the capabilities are the default ones, it must have
            '_default' as a property name.
        """

        return self.instances

    def create_setting_for_capabilities(self, capabilities):
        """
            Create LMI_*Setting for given capabilities.
            Return CIMInstanceName of the setting or raise CIMError on error.
        """
        setting_id = self.setting_manager.allocate_id(
                'LMI_DiskPartitionConfigurationSetting')
        if not setting_id:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Failed to allocate setting InstanceID")

        setting = Setting(Setting.TYPE_TRANSIENT, setting_id)
        setting['Bootable'] = False
        setting['ElementName'] = 'CreatedFrom' + capabilities['InstanceID']
        setting['Hidden'] = False
        if (capabilities['PartitionStyle'] == self.Values.PartitionStyle.GPT
                or capabilities['PartitionStyle'] == self.Values.PartitionStyle.MBR):
            setting['PartitionType'] = LMI_DiskPartitionConfigurationSetting.Values.PartitionType.Primary
        else:
            setting['PartitionType'] = LMI_DiskPartitionConfigurationSetting.Values.PartitionType.Logical

        self.setting_manager.set_setting('LMI_DiskPartitionConfigurationSetting', setting)

        return pywbem.CIMInstanceName(
                classname='LMI_DiskPartitionConfigurationSetting',
                namespace=self.config.namespace,
                keybindings={'InstanceID': setting_id})





    class Values(CapabilitiesProvider.Values):
        class SupportedSettings(object):
            Partition_Type = pywbem.Uint16(1)
            Bootable = pywbem.Uint16(2)
            Hidden = pywbem.Uint16(3)

        class ValidSubPartitionStyles(object):
            Other = pywbem.Uint16(1)
            MBR = pywbem.Uint16(2)
            VTOC = pywbem.Uint16(3)
            GPT = pywbem.Uint16(4)
            EMBR = pywbem.Uint16(4100)

        class SupportedSynchronousActions(object):
            SetPartitionStyle = pywbem.Uint16(2)
            CreateOrModifyPartition = pywbem.Uint16(3)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 0x8000..

        class PartitionStyle(object):
            MBR = pywbem.Uint16(2)
            GPT = pywbem.Uint16(3)
            VTOC = pywbem.Uint16(4)
            PC98 = pywbem.Uint16(4097)
            SUN = pywbem.Uint16(4098)
            MAC = pywbem.Uint16(4099)
            EMBR = pywbem.Uint16(4100)
