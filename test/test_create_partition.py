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

from test_base import StorageTestBase
import unittest
import pywbem

class TestCreatePartition(StorageTestBase):
    """
        Test LMI_DiskPartitionConfigurationService.CreateOrModifyPartition
        with different parameters.
        
        As consequence, it tests also:
        - LMI_DiskPartitionConfigurationCapabilities.CreateSetting.
        - Setting modify / delete.
        - DeleteInstance on partitions.
        - SetPartitionStyle.
    """

    DISK_CLASS = "LMI_StorageExtent"
    MBR_CLASS = "LMI_DiskPartition"
    GPT_CLASS = "LMI_GenericDiskPartition"

    STYLE_EMBR = 4100
    STYLE_MBR = 2
    STYLE_GPT = 3

    def setUp(self):
        """ Prepare for test."""
        super(TestCreatePartition, self).setUp()
        self.service = self.wbemconnection.EnumerateInstanceNames(
                "LMI_DiskPartitionConfigurationService")[0]
        self.diskname = pywbem.CIMInstanceName(
                classname=self.DISK_CLASS,
                keybindings={
                        'DeviceID': self.disks[0],
                        'SystemCreationClassName': self.SYSTEM_CLASS_NAME,
                        'SystemName': self.SYSTEM_NAME,
                        'CreationClassName': self.DISK_CLASS})


    def _check_name(self, partname, classname):
        """ Check that CIMInstanceName represents a partition. """
        self.assertEqual(partname['SystemName'], self.SYSTEM_NAME)
        self.assertEqual(partname['SystemCreationClassName'], self.SYSTEM_CLASS_NAME)
        self.assertEqual(partname['CreationClassName'], classname)

    def _get_capabilities_name(self, style):
        """
            Return CIMInstanceName with partition capabilities representing
            given partition style.
        """
        if style == self.STYLE_EMBR:
            style_name = "EMBR"
        elif style == self.STYLE_MBR:
            style_name = "MBR"
        elif style == self.STYLE_GPT:
            style_name = "GPT"

        return pywbem.CIMInstanceName(
                classname="LMI_DiskPartitionConfigurationCapabilities",
                keybindings={
                        'InstanceID': "LMI:LMI_DiskPartitionConfigurationCapabilities:" + style_name
                })

    def _create_setting(self, style):
        """
            Create new partition configuration setting instance of given
            PartitionStryle and return its CIMInstance.
        """
        capabilities = self._get_capabilities_name(style)
        if not capabilities:
            return None
        (retval, outparams) = self.wbemconnection.InvokeMethod(
                "CreateSetting", capabilities)
        self.assertEqual(retval, 0)
        self.assertEqual(len(outparams), 1)
        return self.wbemconnection.GetInstance(outparams['setting'])

    def _delete_setting(self, setting):
        """ Delete Setting with given CIMInstanceName."""
        self.wbemconnection.DeleteInstance(setting)


    def _set_partition_style(self, style):
        """ Create partition table on self.diskname with given style."""
        caps = self._get_capabilities_name(style)
        (retval, outparams) = self.wbemconnection.InvokeMethod(
                "SetPartitionStyle",
                self.service,
                Extent=self.diskname,
                PartitionStyle=caps)
        self.assertEqual(retval, 0)
        self.assertDictEqual(outparams, {})

    def test_err_no_params(self):
        """ Try CreateOrModifyPartition with no parameters -> error."""
        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                "CreateOrModifyPartition",
                self.service)

    def test_err_device_file_name(self):
        """ Try CreateOrModifyPartition with DeviceFileName -> error."""
        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                "CreateOrModifyPartition",
                self.service,
                extent=self.diskname,
                DeviceFileName="blabla")

    def test_err_wrong_goal(self):
        """ Try CreateOrModifyPartition with unknown goal InstanceId -> error."""
        goal = pywbem.CIMInstanceName(
                classname="LMI_DiskPartitionConfigurationSetting",
                keybindings={'InstanceID':'not_existing'})
        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                "CreateOrModifyPartition",
                self.service,
                extent=self.diskname,
                Goal=goal)

    def test_err_wrong_extent(self):
        """ Try CreateOrModifyPartition with unknown extent DeviceID -> error."""
        diskname = pywbem.CIMInstanceName(
                classname=self.DISK_CLASS,
                keybindings={
                        'DeviceID': '/dev/does/not/exist',
                        'SystemCreationClassName': self.SYSTEM_CLASS_NAME,
                        'SystemName': self.SYSTEM_NAME,
                        'CreationClassName': self.DISK_CLASS})
        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                "CreateOrModifyPartition",
                self.service,
                extent=diskname)

    def test_err_wrong_goal_style_gpt(self):
        """
            Try CreateOrModifyPartition with goal not corresponding to
            GPT partition table style.-> error.
        """
        # create GPT partition table
        self._set_partition_style(self.STYLE_GPT)

        # try Hidden
        goal = self._create_setting(self.STYLE_GPT)
        goal['Hidden'] = True
        self.wbemconnection.ModifyInstance(goal)
        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                "CreateOrModifyPartition",
                self.service,
                extent=self.diskname,
                Goal=goal.path)
        self._delete_setting(goal.path)

        # try Extended partition
        goal = self._create_setting(self.STYLE_GPT)
        goal['PartitionType'] = pywbem.Uint16(2)
        self.wbemconnection.ModifyInstance(goal)
        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                "CreateOrModifyPartition",
                self.service,
                extent=self.diskname,
                Goal=goal)

        # try logical partition
        goal['PartitionType'] = pywbem.Uint16(3)
        self.wbemconnection.ModifyInstance(goal)
        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                "CreateOrModifyPartition",
                self.service,
                extent=self.diskname,
                Goal=goal.path)

        self._delete_setting(goal.path)

    def test_gpt_maximum(self):
        """
            Try CreateOrModifyPartition on GPT partition table without
            any start/end addresses.
        """
        # create GPT partition table
        self._set_partition_style(self.STYLE_GPT)
        goal = self._create_setting(self.STYLE_GPT)
        (retval, outparams) = self.wbemconnection.InvokeMethod(
                "CreateOrModifyPartition",
                self.service,
                extent=self.diskname,
                Goal=goal.path)
        self.assertEqual(retval, 0)
        self.assertIn("partition", outparams)

        partition = outparams['partition']
        disk_instance = self.wbemconnection.GetInstance(self.diskname)
        partition_instance = self.wbemconnection.GetInstance(partition)

        self.assertAlmostEqual(
                disk_instance['NumberOfBlocks'],
                partition_instance['NumberOfBlocks'],
                delta=2 * 1024 * 10) # 10 megabytes

        # second call must fail
        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                "CreateOrModifyPartition",
                self.service,
                extent=self.diskname,
                Goal=goal)

        # check based on
        basedons = self.wbemconnection.References(
                partition,
                ResultClass="LMI_PartitionBasedOn")
        self.assertEqual(len(basedons), 1)
        basedon = basedons[0]
        self.assertEqual(basedon['Antecedent'], self.diskname)
        self.assertEqual(basedon['Dependent'], partition)
        self.assertAlmostEqual(
                basedon['StartingAddress'], 0, delta=2 * 1024 * 2) # 2 megabytes
        self.assertAlmostEqual(
                basedon['EndingAddress'],
                disk_instance['NumberOfBlocks'],
                delta=4 * 1024 * 2) # 4 megabytes

        # check based on
        basedons = self.wbemconnection.References(
                partition,
                ResultClass="LMI_PartitionBasedOn")
        self.assertEqual(len(basedons), 1)
        basedon = basedons[0]
        self.assertEqual(basedon['Antecedent'], self.diskname)
        self.assertEqual(basedon['Dependent'], partition)
        self.assertAlmostEqual(
                basedon['StartingAddress'], 0, delta=2 * 1024 * 2) # 2 megabytes
        self.assertAlmostEqual(
                basedon['EndingAddress'],
                disk_instance['NumberOfBlocks'],
                delta=4 * 1024 * 2) # 4 megabytes

        self._delete_setting(goal.path)
        self.wbemconnection.DeleteInstance(partition)

    def test_mbr_maximum(self):
        """
            Try CreateOrModifyPartition on MBR partition table without
            any start/end addresses.
        """
        # create MBR partition table
        self._set_partition_style(self.STYLE_MBR)
        goal = self._create_setting(self.STYLE_MBR)
        (retval, outparams) = self.wbemconnection.InvokeMethod(
                "CreateOrModifyPartition",
                self.service,
                extent=self.diskname,
                Goal=goal.path)
        self.assertEqual(retval, 0)
        self.assertIn("partition", outparams)

        partition = outparams['partition']
        disk_instance = self.wbemconnection.GetInstance(self.diskname)
        partition_instance = self.wbemconnection.GetInstance(partition)

        self.assertAlmostEqual(
                disk_instance['NumberOfBlocks'],
                partition_instance['NumberOfBlocks'],
                delta=2 * 1024 * 10) # 10 megabytes

        # check based on
        basedons = self.wbemconnection.References(
                partition,
                ResultClass="LMI_PartitionBasedOn")
        self.assertEqual(len(basedons), 1)
        basedon = basedons[0]
        self.assertEqual(basedon['Antecedent'], self.diskname)
        self.assertEqual(basedon['Dependent'], partition)
        self.assertAlmostEqual(
                basedon['StartingAddress'], 0, delta=2 * 1024 * 2) # 2 megabytes
        self.assertAlmostEqual(
                basedon['EndingAddress'],
                disk_instance['NumberOfBlocks'],
                delta=4 * 1024 * 2) # 4 megabytes

        # second call must fail
        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                "CreateOrModifyPartition",
                self.service,
                extent=self.diskname,
                Goal=goal)

        self._delete_setting(goal.path)
        self.wbemconnection.DeleteInstance(partition)

    def test_gpt_positions(self):
        """
            Try CreateOrModifyPartition on GPT partition table with
            start/end addresses.
        """
        partition_start = 35 # beware of GPT table size
        partition_size = 1025 * 2 * 10 # 10 MB
        partition_count = 20
        partitions = []
        # create GPT partition table
        self._set_partition_style(self.STYLE_GPT)
        goal = self._create_setting(self.STYLE_GPT)

        for i in xrange(partition_count):
            pstart = partition_start + partition_size * i
            pend = partition_start + partition_size * (i + 1) - 1
            (retval, outparams) = self.wbemconnection.InvokeMethod(
                    "CreateOrModifyPartition",
                    self.service,
                    extent=self.diskname,
                    StartingAddress=pywbem.Uint64(pstart),
                    EndingAddress=pywbem.Uint64(pend),

                    Goal=goal.path)
            self.assertEqual(retval, 0)
            self.assertIn("partition", outparams)

            partition = outparams['partition']
            partitions.append(partition)

            partition_instance = self.wbemconnection.GetInstance(partition)
            self.assertEqual(
                    partition_size,
                    partition_instance['NumberOfBlocks'])

            # check based on
            basedons = self.wbemconnection.References(
                    partition,
                    ResultClass="LMI_PartitionBasedOn")
            self.assertEqual(len(basedons), 1)
            basedon = basedons[0]
            self.assertEqual(basedon['Antecedent'], self.diskname)
            self.assertEqual(basedon['Dependent'], partition)
            self.assertEqual(
                    basedon['StartingAddress'],
                    pstart)
            self.assertEqual(
                    basedon['EndingAddress'],
                    pend)

        self._delete_setting(goal.path)

        for partition in partitions:
            self.wbemconnection.DeleteInstance(partition)

    def test_mbr_positions(self):
        """
            Try CreateOrModifyPartition on MBR partition table with
            start/end addresses.
        """
        partition_start = 1 # beware of MBR table size
        partition_size = 1025 * 2 * 10 # 10 MB
        partition_count = 4
        partitions = []
        # create MBR partition table
        self._set_partition_style(self.STYLE_MBR)
        goal = self._create_setting(self.STYLE_MBR)

        for i in xrange(partition_count):
            pstart = partition_start + partition_size * i
            pend = partition_start + partition_size * (i + 1) - 1
            (retval, outparams) = self.wbemconnection.InvokeMethod(
                    "CreateOrModifyPartition",
                    self.service,
                    extent=self.diskname,
                    StartingAddress=pywbem.Uint64(pstart),
                    EndingAddress=pywbem.Uint64(pend),

                    Goal=goal.path)
            self.assertEqual(retval, 0)
            self.assertIn("partition", outparams)

            partition = outparams['partition']
            partitions.append(partition)

            partition_instance = self.wbemconnection.GetInstance(partition)
            self.assertEqual(
                    partition_size,
                    partition_instance['NumberOfBlocks'])

            # check based on
            basedons = self.wbemconnection.References(
                    partition,
                    ResultClass="LMI_PartitionBasedOn")
            self.assertEqual(len(basedons), 1)
            basedon = basedons[0]
            self.assertEqual(basedon['Antecedent'], self.diskname)
            self.assertEqual(basedon['Dependent'], partition)
            self.assertEqual(
                    basedon['StartingAddress'],
                    pstart)
            self.assertEqual(
                    basedon['EndingAddress'],
                    pend)

        self._delete_setting(goal.path)

        for partition in partitions:
            self.wbemconnection.DeleteInstance(partition)

    def test_logical_positions(self):
        """
            Try CreateOrModifyPartition on MBR partition table with
            start/end addresses and logical partitions.
        """
        partition_start = 1 # beware of MBR table size
        partition_size = 1025 * 2 * 10 # 10 MB
        partition_count = 20
        partitions = []
        # create MBR partition table and one huge Extended partition
        self._set_partition_style(self.STYLE_MBR)
        goal = self._create_setting(self.STYLE_MBR)
        goal['PartitionType'] = pywbem.Uint16(2) # Extended
        self.wbemconnection.ModifyInstance(goal)
        (retval, outparams) = self.wbemconnection.InvokeMethod(
                "CreateOrModifyPartition",
                self.service,
                extent=self.diskname,
                Goal=goal.path)
        self.assertEqual(retval, 0)
        self.assertIn("partition", outparams)
        extended_partition = outparams['partition']

        # create partition_count logical partitions on it
        goal['PartitionType'] = pywbem.Uint16(3) # Logical
        self.wbemconnection.ModifyInstance(goal)
        for i in xrange(partition_count):
            pstart = partition_start + partition_size * i
            pend = partition_start + partition_size * (i + 1) - 1
            (retval, outparams) = self.wbemconnection.InvokeMethod(
                    "CreateOrModifyPartition",
                    self.service,
                    extent=extended_partition,
                    StartingAddress=pywbem.Uint64(pstart),
                    EndingAddress=pywbem.Uint64(pend),
                    Goal=goal.path)
            self.assertEqual(retval, 0)
            self.assertIn("partition", outparams)

            partition = outparams['partition']
            partitions.append(partition)

            partition_instance = self.wbemconnection.GetInstance(partition)
            self.assertEqual(
                    partition_size,
                    partition_instance['NumberOfBlocks'])

            # check based on
            basedons = self.wbemconnection.References(
                    partition,
                    ResultClass="LMI_PartitionBasedOn")
            self.assertEqual(len(basedons), 1)
            basedon = basedons[0]
            self.assertEqual(basedon['Antecedent'], extended_partition)
            self.assertEqual(basedon['Dependent'], partition)
            self.assertEqual(
                    basedon['StartingAddress'],
                    pstart)
            self.assertEqual(
                    basedon['EndingAddress'],
                    pend)

        self._delete_setting(goal.path)

        for partition in partitions:
            self.wbemconnection.DeleteInstance(partition)
        self.wbemconnection.DeleteInstance(extended_partition)

    # TODO: test partition modification

if __name__ == '__main__':
    unittest.main()
