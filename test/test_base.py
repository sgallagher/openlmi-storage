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
#
# Base class for all storage tests

import os
import unittest
import pywbem
import subprocess
import pyudev
import time
import socket

class StorageTestBase(unittest.TestCase):
    """
        This is base class of OpenLMI storage tests.
        It monitors all devices created between setUp and tearDown
        and tries to remove them in tearDown.
    """

    SYSTEM_CLASS_NAME = "Linux_ComputerSystem"
    SYSTEM_NAME = socket.getfqdn()
    DISK_CLASS = "LMI_StorageExtent"

    @classmethod
    def setUpClass(cls):
        cls.url = os.environ.get("LMI_CIMOM_URL", "https://localhost:5989")
        cls.username = os.environ.get("LMI_CIMOM_USERNAME", "root")
        cls.password = os.environ.get("LMI_CIMOM_PASSWORD", "")
        cls.disk = os.environ.get("LMI_STORAGE_DISK", "")
        cls.partitions = os.environ.get("LMI_STORAGE_PARTITIONS", "").split()
        cls.cimom = os.environ.get("LMI_CIMOM_BROKER", "sblim-sfcb")
        cls.clean = os.environ.get("LMI_STORAGE_CLEAN", "Yes")
        cls.verbose = os.environ.get("LMI_STORAGE_VERBOSE", None)
        cls.disk_name = pywbem.CIMInstanceName(
                classname=cls.DISK_CLASS,
                namespace="root/cimv2",
                keybindings={
                        'DeviceID': cls.disk,
                        'SystemCreationClassName': cls.SYSTEM_CLASS_NAME,
                        'SystemName': cls.SYSTEM_NAME,
                        'CreationClassName': cls.DISK_CLASS})
        cls.wbemconnection = pywbem.WBEMConnection(cls.url, (cls.username, cls.password))

        # Get the first partition and copy its name for all other partitions
        part = cls.wbemconnection.ExecQuery(
                "WQL", 'select * from CIM_StorageExtent where Name="' + cls.partitions[0] + '"')[0]
        template = part.path
        cls.partition_names = []
        for device_id in cls.partitions:
            name = pywbem.CIMInstanceName(classname=template.classname,
                    namespace=template.namespace,
                    keybindings=template.keybindings)
            name['DeviceID'] = device_id
            cls.partition_names.append(name)

    def setUp(self):
        self.start_udev_monitor()

    def start_udev_monitor(self):
        self.udev_context = pyudev.Context()  # IGNORE:W0201
        self.udev_monitor = pyudev.Monitor.from_netlink(self.udev_context)  # IGNORE:W0201
        self.udev_monitor.filter_by('block')
        self.udev_observer = pyudev.MonitorObserver(self.udev_monitor, self.udev_event)  # IGNORE:W0201
        self.devices = []  # IGNORE:W0201
        self.udev_observer.start()

    def stop_udev_monitor(self):
        self.udev_observer.stop()

    def udev_event(self, action, device):
        if action == 'change':
            return

        if self.verbose:
            print "UDEV event:", action, device.device_node
        if action == 'add':
            self.devices.append(device.device_node)
        if action == 'remove':
            if device.device_node in self.devices:
                self.devices.remove(device.device_node)

    def destroy_created(self):
        """
            Destroy all devices created during the tests as recorded by the
            udev. It returns nr. of removed items.
        """
        count = 0

        # remove them in reverse order
        while self.devices:
            device = self.devices.pop()
            udev_device = pyudev.Device.from_device_file(
                    self.udev_context, device)
            if self.verbose:
                print "Destroying %s:%s" % (device, udev_device.device_type)

            if udev_device.device_type == 'partition':
                count += 1
                self.destroy_mbr(udev_device.parent.device_node)
            if udev_device.device_type == 'disk':
                # is it RAID?
                try:
                    if udev_device['MD_LEVEL']:
                        count += 1
                        self.destroy_md(device)
                except KeyError:
                    pass  # it's not RATD

            # TODO: add LVM
        return count


    def destroy_vg(self, vgname):
        """
            Destroy given volume group, not using CIM.
            This method should be called when a test fails and wants to clean
            up its mess.
        """
        return self.log_run(["vgremove", "-f", "/dev/mapper/" + vgname])

    def destroy_md(self, md_device_id):
        """
            Destroy given RAID, not using CIM.
            This method should be called when a test fails and wants to clean
            up its mess.
        """
        return self.log_run(["test/tools/mdremove", md_device_id])

    def destroy_mbr(self, disk_device_id):
        """
            Destroy any partition table on given device.
            This method should be called when a test fails and wants to clean
            up its mess.
        """
        return self.log_run(["test/tools/mbrremove", disk_device_id])

    def restart_cim(self):
        """
            Restart CIMOM
        """
        ret = self.log_run(["systemctl", "restart", self.cimom])
        time.sleep(1)
        if ret == 0:
            self.wbemconnection = pywbem.WBEMConnection(self.url, (self.username, self.password))
        return ret



    def log_run(self, args):
        """
            Print arguments and run them.
            args must be prepared for subprocess.call()
        """
        print "Running:", " ".join(args)
        return subprocess.call(args)


    def tearDown(self):
        """
            Default teardown. It destroys any devices created since setUp().
            It restarts CIMOM if any devices were destroyed.
            
            Each test should clean after itself!
        """
        # try to destroy everything and restart CIMOM
        self.stop_udev_monitor()
        if self.clean:
            if self.destroy_created():
                self.restart_cim()

    def _check_redundancy(self, extent, setting,
            data_redundancy=None,
            stripe_legtht=None,
            package_redundancy=None,
            parity_layout=None,
            check_parity_layout=False,
            nspof=None
            ):
        """
            Check if redundancy setting of StorageExtent and StorageSetting
            match and have requested values. Assert if not.
            If any value is None, it will not be checked, except parity_layout.
            If check_parity_layout is True, parity_layout will be checked
            against setting['ParityLayout'] even if it is None 
            Both extent and setting must be CIMInstance.
        """
        self.assertEqual(setting['DataRedundancyGoal'], extent['DataRedundancy'])
        self.assertEqual(setting['DataRedundancyMin'], extent['DataRedundancy'])
        self.assertEqual(setting['DataRedundancyMax'], extent['DataRedundancy'])
        self.assertEqual(setting['ExtentStripeLength'], extent['ExtentStripeLength'])
        self.assertEqual(setting['ExtentStripeLengthMin'], extent['ExtentStripeLength'])
        self.assertEqual(setting['ExtentStripeLengthMax'], extent['ExtentStripeLength'])
        self.assertEqual(setting['NoSinglePointOfFailure'], extent['NoSinglePointOfFailure'])
        self.assertEqual(setting['PackageRedundancyGoal'], extent['PackageRedundancy'])
        self.assertEqual(setting['PackageRedundancyMin'], extent['PackageRedundancy'])
        self.assertEqual(setting['PackageRedundancyMax'], extent['PackageRedundancy'])

        if data_redundancy:
            self.assertEqual(extent['DataRedundancy'], data_redundancy)
        if stripe_legtht:
            self.assertEqual(extent['ExtentStripeLength'], stripe_legtht)
        if package_redundancy:
            self.assertEqual(extent['PackageRedundancy'], package_redundancy)
        if check_parity_layout or parity_layout:
            self.assertEqual(setting['ParityLayout'], parity_layout)
        if nspof is not None:
            self.assertEqual(setting['NoSinglePointOfFailure'], nspof)



def short_tests_only():
    """
        Returns True, if only short test should be executed, i.e.
        LMI_STORAGE_SHORT_ONLY is set.
    """
    if os.environ.get("LMI_STORAGE_SHORT_ONLY", None):
        return True
    return False
