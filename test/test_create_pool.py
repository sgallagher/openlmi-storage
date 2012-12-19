#!/usr/bin/python
# -*- Coding:utf-8 -*-
#
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

from test_base import StorageTestBase, short_test_only
import unittest
import pywbem


MEGABYTE = 1024 * 1024

class TestCreatePool(StorageTestBase):
    """
        Test LMI_StorageConfigurationService.CreateOrModifyStoragePool
        (create only).
    """

    DISK_CLASS = "LMI_StorageExtent"
    VG_CLASS = "LMI_VGStoragePool"
    STYLE_EMBR = 4100
    STYLE_MBR = 2
    STYLE_GPT = 3
    PARTITION_CLASS = "LMI_GenericDiskPartition"


    def setUp(self):
        """ Find storage service. """
        super(TestCreatePool, self).setUp()
        self.service = self.wbemconnection.EnumerateInstanceNames(
                "LMI_StorageConfigurationService")[0]
        self.part_service = self.wbemconnection.EnumerateInstanceNames(
                "LMI_DiskPartitionConfigurationService")[0]
        self.capabilities = self.wbemconnection.EnumerateInstanceNames(
                "LMI_VGStorageCapabilities")[0]

    def _prepare_partitions(self, diskname, partition_count):
        """ Create partition table and partitions on given device """
        disk_path = pywbem.CIMInstanceName(
                classname=self.DISK_CLASS,
                keybindings={
                    'DeviceID': diskname,
                    'SystemCreationClassName': self.SYSTEM_CLASS_NAME,
                    'SystemName': self.SYSTEM_NAME,
                    'CreationClassName': self.DISK_CLASS})

        caps = pywbem.CIMInstanceName(
                classname="LMI_DiskPartitionConfigurationCapabilities",
                keybindings={
                        'InstanceID': "LMI:LMI_DiskPartitionConfigurationCapabilities:GPT"
                })
        (retval, outparams) = self.wbemconnection.InvokeMethod(
                "SetPartitionStyle",
                self.part_service,
                Extent=disk_path,
                PartitionStyle=caps)
        self.assertEqual(retval, 0)
        disk = self.wbemconnection.GetInstance(disk_path)
        offset = 2048  # first usable sector
        size = disk['NumberOfBlocks']
        size = size - 2 * offset  # reserve also some space at the end
        partition_size = size / partition_count
        partitions = []
        for i in range(partition_count):
            (retval, outparams) = self.wbemconnection.InvokeMethod(
                "CreateOrModifyPartition",
                self.part_service,
                extent=disk_path,
                StartingAddress=pywbem.Uint64(offset + i * partition_size),
                EndingAddress=pywbem.Uint64(offset + (i + 1) * partition_size))
            self.assertEqual(retval, 0)
            partitions.append(outparams['partition'])
        return partitions

    def _destroy_partitions(self, partitions):
        """ Delete partitions """
        for part in partitions:
            self.wbemconnection.DeleteInstance(part)

    def _get_disk_size(self, diskname):
        """ Return size of given disk, in bytes."""
        disk_path = pywbem.CIMInstanceName(
                classname=self.DISK_CLASS,
                keybindings={
                    'DeviceID': diskname,
                    'SystemCreationClassName': self.SYSTEM_CLASS_NAME,
                    'SystemName': self.SYSTEM_NAME,
                    'CreationClassName': self.DISK_CLASS})
        disk = self.wbemconnection.GetInstance(disk_path)
        return disk['NumberOfBlocks'] * disk['BlockSize']

    def test_create_1pv(self):
        """ Test CreateOrModifyStoragePool with one PV."""
        partitions = self._prepare_partitions(self.disks[0], 1)
        (ret, outparams) = self.wbemconnection.InvokeMethod(
                "CreateOrModifyStoragePool",
                self.service,
                InExtents=partitions,
                ElementName='myCRAZYname')
        self.assertEqual(ret, 0)
        self.assertEqual(len(outparams), 2)
        self.assertAlmostEqual(
                outparams['size'],
                self._get_disk_size(self.disks[0]),
                delta=50 * MEGABYTE)
        vgname = outparams['pool']
        vg = self.wbemconnection.GetInstance(vgname)
        self.assertEqual(vg['TotalManagedSpace'], outparams['size'])
        self.assertEqual(vg['PoolID'], 'myCRAZYname')
        self.assertEqual(vg['ElementName'], 'myCRAZYname')
        self.assertNotEqual(vg['UUID'], '')
        self.assertNotEqual(vg['UUID'], None)
        self.assertEqual(vg['ExtentSize'], 4 * MEGABYTE)
        self.assertEqual(
                vg['ExtentSize'] * vg['TotalExtents'],
                vg['TotalManagedSpace'])
        self.assertEqual(
                vg['ExtentSize'] * vg['RemainingExtents'],
                vg['RemainingManagedSpace'])

        self.wbemconnection.DeleteInstance(vgname)
        self._destroy_partitions(partitions)

    @unittest.skipIf(short_test_only(), "Running short tests only.")
    def test_create_10pv(self):
        """ Test CreateOrModifyStoragePool with 10 PVs."""
        partitions = self._prepare_partitions(self.disks[0], 10)
        (ret, outparams) = self.wbemconnection.InvokeMethod(
                "CreateOrModifyStoragePool",
                self.service,
                InExtents=partitions)
        self.assertEqual(ret, 0)
        self.assertEqual(len(outparams), 2)
        self.assertAlmostEqual(
                outparams['size'],
                self._get_disk_size(self.disks[0]),
                delta=50 * MEGABYTE)
        vg = outparams['pool']

        self.wbemconnection.DeleteInstance(vg)
        self._destroy_partitions(partitions)

    @unittest.skipIf(short_test_only(), "Running short tests only.")
    def test_create_10vg(self):
        """ Test CreateOrModifyStoragePool with 10 VGs."""
        partitions = self._prepare_partitions(self.disks[0], 10)
        vgs = []
        for part in partitions:
            (ret, outparams) = self.wbemconnection.InvokeMethod(
                    "CreateOrModifyStoragePool",
                    self.service,
                    InExtents=[part])
            self.assertEqual(ret, 0)
            self.assertEqual(len(outparams), 2)
            vg = outparams['pool']
            vgs.append(vg)

        for vg in vgs:
            self.wbemconnection.DeleteInstance(vg)
        self._destroy_partitions(partitions)

    def test_create_unknown_setting(self):
        """ Test CreateOrModifyStoragePool with non-existing setting."""
        partitions = self._prepare_partitions(self.disks[0], 1)

        goal = pywbem.CIMInstanceName(
                classname=" LMI_VGStorageSetting",
                keybindings={
                        'InstanceID' : 'LMI:LMI_VGStorageSetting:not-existing'
                })
        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                    "CreateOrModifyStoragePool",
                    self.service,
                    InExtents=partitions,
                    Goal=goal
                    )
        self._destroy_partitions(partitions)

    def test_create_wrong_setting_class(self):
        """ Test CreateOrModifyStoragePool with non-existing setting."""
        partitions = self._prepare_partitions(self.disks[0], 1)

        goal = pywbem.CIMInstanceName(
                classname=" LMI_LVStorageSetting",
                keybindings={
                        'InstanceID' : 'LMI:LMI_LVStorageSetting:not-existing'
                })
        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                    "CreateOrModifyStoragePool",
                    self.service,
                    InExtents=partitions,
                    Goal=goal
                    )
        self._destroy_partitions(partitions)

    def test_create_wrong_inpools(self):
        """ Test CreateOrModifyStoragePool with InPools param."""
        partitions = self._prepare_partitions(self.disks[0], 1)

        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                    "CreateOrModifyStoragePool",
                    self.service,
                    InExtents=partitions,
                    InPools=partitions
                    )
        self._destroy_partitions(partitions)

    def test_create_wrong_size(self):
        """ Test CreateOrModifyStoragePool with Size param."""
        partitions = self._prepare_partitions(self.disks[0], 1)

        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                    "CreateOrModifyStoragePool",
                    self.service,
                    InExtents=partitions,
                    Size=pywbem.Uint64(1 * MEGABYTE)
                    )
        self._destroy_partitions(partitions)

    def _create_setting(self):
        """ Create a VGStorageSetting and return CIMInstance of it."""
        (retval, outparams) = self.wbemconnection.InvokeMethod(
                "CreateSetting",
                self.capabilities)
        self.assertEqual(retval, 0)
        self.assertEqual(len(outparams), 1)

        setting_name = outparams['newsetting']
        setting = self.wbemconnection.GetInstance(setting_name)
        return setting

    def _delete_setting(self, setting_name):
        """ Delete given setting. """
        self.wbemconnection.DeleteInstance(setting_name)

    def test_create_default_setting(self):
        """
            Test CreateOrModifyStoragePool with default setting from 
            VGStroageCapabilities.CreateSetting.
        """
        partitions = self._prepare_partitions(self.disks[0], 1)
        goal = self._create_setting()

        (ret, outparams) = self.wbemconnection.InvokeMethod(
                    "CreateOrModifyStoragePool",
                    self.service,
                    InExtents=partitions,
                    Goal=goal.path
                    )

        self.assertEqual(ret, 0)
        self.assertEqual(len(outparams), 2)
        self.assertAlmostEqual(
                outparams['size'],
                self._get_disk_size(self.disks[0]),
                delta=50 * MEGABYTE)
        vgname = outparams['pool']
        vg = self.wbemconnection.GetInstance(vgname)
        self.assertEqual(vg['TotalManagedSpace'], outparams['size'])
        self.assertNotEqual(vg['ElementName'], '')
        self.assertNotEqual(vg['ElementName'], None)
        self.assertNotEqual(vg['UUID'], '')
        self.assertNotEqual(vg['UUID'], None)
        self.assertEqual(vg['ExtentSize'], 4 * MEGABYTE)
        self.assertEqual(
                vg['ExtentSize'] * vg['TotalExtents'],
                vg['TotalManagedSpace'])
        self.assertEqual(
                vg['ExtentSize'] * vg['RemainingExtents'],
                vg['RemainingManagedSpace'])

        # check it has a setting associated
        settings = self.wbemconnection.Associators(
                vgname,
                AssocClass="LMI_VGElementSettingData")
        self.assertEqual(len(settings), 1)
        setting = settings[0]
        self.assertEqual(setting['ExtentSize'], goal['ExtentSize'])
        self.assertEqual(setting['DataRedundancyGoal'], goal['DataRedundancyGoal'])
        self.assertLessEqual(setting['DataRedundancyMax'], goal['DataRedundancyMax'])
        self.assertGreaterEqual(setting['DataRedundancyMin'], goal['DataRedundancyMin'])
        self.assertEqual(setting['ExtentStripeLength'], goal['ExtentStripeLength'])
        self.assertLessEqual(setting['ExtentStripeLengthMax'], goal['ExtentStripeLengthMax'])
        self.assertGreaterEqual(setting['ExtentStripeLengthMin'], goal['ExtentStripeLengthMin'])
        self.assertEqual(setting['NoSinglePointOfFailure'], goal['NoSinglePointOfFailure'])
        self.assertEqual(setting['PackageRedundancyGoal'], goal['PackageRedundancyGoal'])
        self.assertLessEqual(setting['PackageRedundancyMax'], goal['PackageRedundancyMax'])
        self.assertGreaterEqual(setting['PackageRedundancyMin'], goal['PackageRedundancyMin'])

        self.wbemconnection.DeleteInstance(vgname)
        self._delete_setting(goal.path)
        self._destroy_partitions(partitions)

    def test_create_setting_2m(self):
        """
            Test CreateOrModifyStoragePool with 2MiB ExtentSize.
        """
        partitions = self._prepare_partitions(self.disks[0], 1)
        goal = self._create_setting()
        goal['ExtentSize'] = pywbem.Uint64(2 * MEGABYTE)
        self.wbemconnection.ModifyInstance(goal)

        (ret, outparams) = self.wbemconnection.InvokeMethod(
                    "CreateOrModifyStoragePool",
                    self.service,
                    InExtents=partitions,
                    Goal=goal.path
                    )
        self.assertEqual(ret, 0)
        self.assertEqual(len(outparams), 2)
        self.assertAlmostEqual(
                outparams['size'],
                self._get_disk_size(self.disks[0]),
                delta=50 * MEGABYTE)
        vgname = outparams['pool']
        vg = self.wbemconnection.GetInstance(vgname)
        self.assertEqual(vg['TotalManagedSpace'], outparams['size'])
        self.assertNotEqual(vg['ElementName'], '')
        self.assertNotEqual(vg['ElementName'], None)
        self.assertNotEqual(vg['UUID'], '')
        self.assertNotEqual(vg['UUID'], None)
        self.assertEqual(vg['ExtentSize'], 2 * MEGABYTE)
        self.assertEqual(
                vg['ExtentSize'] * vg['TotalExtents'],
                vg['TotalManagedSpace'])
        self.assertEqual(
                vg['ExtentSize'] * vg['RemainingExtents'],
                vg['RemainingManagedSpace'])

        # check it has a setting associated
        settings = self.wbemconnection.Associators(
                vgname,
                AssocClass="LMI_VGElementSettingData")
        self.assertEqual(len(settings), 1)
        setting = settings[0]
        self.assertEqual(setting['ExtentSize'], goal['ExtentSize'])
        self.assertEqual(setting['DataRedundancyGoal'], goal['DataRedundancyGoal'])
        self.assertLessEqual(setting['DataRedundancyMax'], goal['DataRedundancyMax'])
        self.assertGreaterEqual(setting['DataRedundancyMin'], goal['DataRedundancyMin'])
        self.assertEqual(setting['ExtentStripeLength'], goal['ExtentStripeLength'])
        self.assertLessEqual(setting['ExtentStripeLengthMax'], goal['ExtentStripeLengthMax'])
        self.assertGreaterEqual(setting['ExtentStripeLengthMin'], goal['ExtentStripeLengthMin'])
        self.assertEqual(setting['NoSinglePointOfFailure'], goal['NoSinglePointOfFailure'])
        self.assertEqual(setting['PackageRedundancyGoal'], goal['PackageRedundancyGoal'])
        self.assertLessEqual(setting['PackageRedundancyMax'], goal['PackageRedundancyMax'])
        self.assertGreaterEqual(setting['PackageRedundancyMin'], goal['PackageRedundancyMin'])

        self.wbemconnection.DeleteInstance(vgname)
        self._delete_setting(goal.path)
        self._destroy_partitions(partitions)

    def test_create_setting_64k(self):
        """
            Test CreateOrModifyStoragePool with 64k ExtentSize.
        """
        partitions = self._prepare_partitions(self.disks[0], 1)
        goal = self._create_setting()
        goal['ExtentSize'] = pywbem.Uint64(64 * 1024)
        self.wbemconnection.ModifyInstance(goal)

        (ret, outparams) = self.wbemconnection.InvokeMethod(
                    "CreateOrModifyStoragePool",
                    self.service,
                    InExtents=partitions,
                    Goal=goal.path
                    )
        self.assertEqual(ret, 0)
        self.assertEqual(len(outparams), 2)
        self.assertAlmostEqual(
                outparams['size'],
                self._get_disk_size(self.disks[0]),
                delta=50 * MEGABYTE)
        vgname = outparams['pool']
        vg = self.wbemconnection.GetInstance(vgname)
        self.assertEqual(vg['TotalManagedSpace'], outparams['size'])
        self.assertNotEqual(vg['ElementName'], '')
        self.assertNotEqual(vg['ElementName'], None)
        self.assertNotEqual(vg['UUID'], '')
        self.assertNotEqual(vg['UUID'], None)
        self.assertEqual(vg['ExtentSize'], 64 * 1024)
        self.assertEqual(
                vg['ExtentSize'] * vg['TotalExtents'],
                vg['TotalManagedSpace'])
        self.assertEqual(
                vg['ExtentSize'] * vg['RemainingExtents'],
                vg['RemainingManagedSpace'])

        # check it has a setting associated
        settings = self.wbemconnection.Associators(
                vgname,
                AssocClass="LMI_VGElementSettingData")
        self.assertEqual(len(settings), 1)
        setting = settings[0]
        self.assertEqual(setting['ExtentSize'], goal['ExtentSize'])
        self.assertEqual(setting['DataRedundancyGoal'], goal['DataRedundancyGoal'])
        self.assertLessEqual(setting['DataRedundancyMax'], goal['DataRedundancyMax'])
        self.assertGreaterEqual(setting['DataRedundancyMin'], goal['DataRedundancyMin'])
        self.assertEqual(setting['ExtentStripeLength'], goal['ExtentStripeLength'])
        self.assertLessEqual(setting['ExtentStripeLengthMax'], goal['ExtentStripeLengthMax'])
        self.assertGreaterEqual(setting['ExtentStripeLengthMin'], goal['ExtentStripeLengthMin'])
        self.assertEqual(setting['NoSinglePointOfFailure'], goal['NoSinglePointOfFailure'])
        self.assertEqual(setting['PackageRedundancyGoal'], goal['PackageRedundancyGoal'])
        self.assertLessEqual(setting['PackageRedundancyMax'], goal['PackageRedundancyMax'])
        self.assertGreaterEqual(setting['PackageRedundancyMin'], goal['PackageRedundancyMin'])

        self.wbemconnection.DeleteInstance(vgname)
        self._delete_setting(goal.path)
        self._destroy_partitions(partitions)

if __name__ == '__main__':
    unittest.main()
