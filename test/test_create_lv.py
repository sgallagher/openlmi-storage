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

from test_base import StorageTestBase, short_tests_only
import unittest
import pywbem

MEGABYTE = 1024 * 1024

class TestCreateLV(StorageTestBase):
    """
        Test CreateOrModifyLV method.
    """

    VG_CLASS = "LMI_VGStoragePool"
    STYLE_GPT = 3
    PARTITION_CLASS = "LMI_GenericDiskPartition"


    def setUp(self):
        """ Find storage service. """
        super(TestCreateLV, self).setUp()
        self.service = self.wbemconnection.EnumerateInstanceNames(
                "LMI_StorageConfigurationService")[0]
        self.part_service = self.wbemconnection.EnumerateInstanceNames(
                "LMI_DiskPartitionConfigurationService")[0]

        vgname = self._create_vg()
        self.vg = self.wbemconnection.GetInstance(vgname)
        self.lvcaps_name = self.wbemconnection.AssociatorNames(vgname,
                AssocClass="LMI_LVElementCapabilities")[0]

    def tearDown(self):
        self._destroy_vg(self.vg.path)
        super(TestCreateLV, self).tearDown()

    def _create_vg(self):
        """
            Create a partition and Volume Group on it and return its
            CIMInstanceName.
        """
        (ret, outparams) = self.wbemconnection.InvokeMethod(
                "CreateOrModifyVG",
                self.service,
                InExtents=self.partition_names[:1],
                ElementName='tstName')
        self.assertEqual(ret, 0)
        return outparams['pool']

    def _destroy_vg(self, vgname):
        """ Destroy VG and its partition. """
        self.wbemconnection.DeleteInstance(vgname)

    def test_create_no_pool(self):
        """ Test CreateOrModifyLV without InPool."""
        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                "CreateOrModifyLV",
                self.service,
                Size=pywbem.Uint64(40 * MEGABYTE))

    def test_create_no_size(self):
        """ Test CreateOrModifyLV without Size."""
        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                "CreateOrModifyLV",
                self.service,
                InPool=self.vg.path)

    def test_create_wrong_size(self):
        """ Test CreateOrModifyLV with wrong Size."""
        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                "CreateOrModifyLV",
                self.service,
                InPool=self.vg.path,
                Size=pywbem.Uint64(0))
# TODO: test this:
#        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
#                "CreateOrModifyLV",
#                self.service,
#                InPool=self.vg.path,
#                Size=pywbem.Uint64(self.vg['TotalManagedSpace'] * 10))

    def test_create_missing_goal(self):
        """ Test CreateOrModifyLV with missing Goal."""
        goal_name = pywbem.CIMInstanceName(
                classname="LMI_LVStorageSetting",
                keybindings={
                        "InstanceID": "LMI:LMI_LVStorageSetting:not-existing"
                })
        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                "CreateOrModifyLV",
                self.service,
                InPool=self.vg.path,
                Size=pywbem.Uint64(40 * MEGABYTE),
                Goal=goal_name)

    def _create_setting(self):
        """
            Create new LMI_LVStorageSetting with default values and return
            its CIMInstance.
        """
        (ret, outparams) = self.wbemconnection.InvokeMethod(
                "CreateLVStorageSetting",
                self.lvcaps_name)
        self.assertEqual(ret, 0)
        setting_name = outparams['setting']
        setting = self.wbemconnection.GetInstance(setting_name)
        return setting

    def test_create_wrong_goal(self):
        """ Test CreateOrModifyLV with wrong Goal."""
        setting = self._create_setting()
        setting['ExtentStripeLengthMin'] = pywbem.Uint16(100)
        self.wbemconnection.ModifyInstance(setting)

        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                "CreateOrModifyLV",
                self.service,
                InPool=self.vg.path,
                Size=pywbem.Uint64(40 * MEGABYTE),
                Goal=setting.path)

        self.wbemconnection.DeleteInstance(setting.path)

    def test_create_no_goal(self):
        """ Test CreateOrModifyLV without any Goal."""
        (retval, outparams) = self.wbemconnection.InvokeMethod(
                "CreateOrModifyLV",
                self.service,
                InPool=self.vg.path,
                Size=pywbem.Uint64(10 * self.vg['ExtentSize']))
        self.assertEqual(retval, 0)
        self.assertEqual(len(outparams), 2)
        self.assertEqual(outparams['Size'], 10 * self.vg['ExtentSize'])

        lv_name = outparams['theelement']
        lv = self.wbemconnection.GetInstance(lv_name)
        vg_setting = self.wbemconnection.Associators(self.vg.path,
                AssocClass="LMI_VGElementSettingData")[0]
        lv_setting = self.wbemconnection.Associators(lv_name,
                AssocClass="LMI_LVElementSettingData")[0]

        self.assertEqual(
                lv['BlockSize'] * lv['NumberOfBlocks'],
                10 * self.vg['ExtentSize'])
        self.assertEqual(
                lv['NoSinglePointOfFailure'],
                lv_setting['NoSinglePointOfFailure'])
        self.assertEqual(
                lv['NoSinglePointOfFailure'],
                vg_setting['NoSinglePointOfFailure'])
        self.assertEqual(
                lv['DataRedundancy'],
                lv_setting['DataRedundancyGoal'])
        self.assertEqual(
                lv['DataRedundancy'],
                vg_setting['DataRedundancyGoal'])
        self.assertEqual(
                lv['PackageRedundancy'],
                lv_setting['PackageRedundancyGoal'])
        self.assertEqual(
                lv['PackageRedundancy'],
                vg_setting['PackageRedundancyGoal'])
        self.assertEqual(
                lv['ExtentStripeLength'],
                lv_setting['ExtentStripeLength'])
        self.assertEqual(
                lv['ExtentStripeLength'],
                vg_setting['ExtentStripeLength'])

        # check vg is reduced
        new_vg = self.wbemconnection.GetInstance(self.vg.path)
        self.assertEqual(
                new_vg['RemainingExtents'],
                self.vg['RemainingExtents'] - 10)
        self.assertEqual(
                new_vg['RemainingManagedSpace'],
                self.vg['RemainingManagedSpace'] - 10 * self.vg['ExtentSize'])

        self.wbemconnection.DeleteInstance(lv_name)

    def test_create_goal_name(self):
        """ Test CreateOrModifyLV with a Goal and elementname."""
        goal = self._create_setting()
        (retval, outparams) = self.wbemconnection.InvokeMethod(
                "CreateOrModifyLV",
                self.service,
                InPool=self.vg.path,
                Size=pywbem.Uint64(10 * self.vg['ExtentSize']),
                Goal=goal.path,
                ElementName="tstNAME")
        self.assertEqual(retval, 0)
        self.assertEqual(len(outparams), 2)
        self.assertEqual(outparams['Size'], 10 * self.vg['ExtentSize'])

        lv_name = outparams['theelement']
        lv = self.wbemconnection.GetInstance(lv_name)
        lv_setting = self.wbemconnection.Associators(lv_name,
                AssocClass="LMI_LVElementSettingData")[0]

        self.assertEqual(lv['ElementName'], "tstNAME")
        self.assertEqual(
                lv['BlockSize'] * lv['NumberOfBlocks'],
                10 * self.vg['ExtentSize'])
        self.assertEqual(
                lv['NoSinglePointOfFailure'],
                lv_setting['NoSinglePointOfFailure'])
        self.assertEqual(
                lv['NoSinglePointOfFailure'],
                goal['NoSinglePointOfFailure'])
        self.assertEqual(
                lv['DataRedundancy'],
                lv_setting['DataRedundancyGoal'])
        self.assertEqual(
                lv['DataRedundancy'],
                goal['DataRedundancyGoal'])
        self.assertEqual(
                lv['PackageRedundancy'],
                lv_setting['PackageRedundancyGoal'])
        self.assertEqual(
                lv['PackageRedundancy'],
                goal['PackageRedundancyGoal'])
        self.assertEqual(
                lv['ExtentStripeLength'],
                lv_setting['ExtentStripeLength'])
        self.assertEqual(
                lv['ExtentStripeLength'],
                goal['ExtentStripeLength'])

        # check vg is reduced
        new_vg = self.wbemconnection.GetInstance(self.vg.path)
        self.assertEqual(
                new_vg['RemainingExtents'],
                self.vg['RemainingExtents'] - 10)
        self.assertEqual(
                new_vg['RemainingManagedSpace'],
                self.vg['RemainingManagedSpace'] - 10 * self.vg['ExtentSize'])

        self.wbemconnection.DeleteInstance(goal.path)
        self.wbemconnection.DeleteInstance(lv_name)

    @unittest.skipIf(short_tests_only(), reason="Skipping long tests.")
    def test_create_10(self):
        """ Test CreateOrModifyLV 10x."""
        lvs = []
        for i in range(10):
            (retval, outparams) = self.wbemconnection.InvokeMethod(
                    "CreateOrModifyLV",
                    self.service,
                    InPool=self.vg.path,
                    Size=pywbem.Uint64(2 * self.vg['ExtentSize']),
                    )
            self.assertEqual(retval, 0)
            self.assertEqual(len(outparams), 2)
            self.assertEqual(outparams['Size'], 2 * self.vg['ExtentSize'])

            lv_name = outparams['theelement']
            lv = self.wbemconnection.GetInstance(lv_name)
            lv_setting = self.wbemconnection.Associators(lv_name,
                    AssocClass="LMI_LVElementSettingData")[0]
            lvs.append(lv)

            self.assertEqual(
                    lv['BlockSize'] * lv['NumberOfBlocks'],
                    2 * self.vg['ExtentSize'])
            self.assertEqual(
                    lv['NoSinglePointOfFailure'],
                    lv_setting['NoSinglePointOfFailure'])
            self.assertEqual(
                    lv['DataRedundancy'],
                    lv_setting['DataRedundancyGoal'])
            self.assertEqual(
                    lv['PackageRedundancy'],
                    lv_setting['PackageRedundancyGoal'])
            self.assertEqual(
                    lv['ExtentStripeLength'],
                    lv_setting['ExtentStripeLength'])

            # check vg is reduced
            new_vg = self.wbemconnection.GetInstance(self.vg.path)
            self.assertEqual(
                    new_vg['RemainingExtents'],
                    self.vg['RemainingExtents'] - (i + 1) * 2)
            self.assertEqual(
                    new_vg['RemainingManagedSpace'],
                    self.vg['RemainingManagedSpace'] - (i + 1) * 2 * self.vg['ExtentSize'])

        for lv in lvs:
            self.wbemconnection.DeleteInstance(lv.path)

if __name__ == '__main__':
    unittest.main()
