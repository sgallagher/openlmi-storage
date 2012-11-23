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

class StorageTestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = os.environ.get("LMI_STORAGE_URL", "https://localhost:5989")
        cls.username = os.environ.get("LMI_STORAGE_USERNAME", "root")
        cls.password = os.environ.get("LMI_STORAGE_PASSWORD", "")
        cls.disks = os.environ.get("LMI_STORAGE_DISKS", "").split()

        cls.wbemconnection = pywbem.WBEMConnection(cls.url, (cls.username, cls.password))
        
    def setUp(self):
        self.startUdevMonitor()
        
    def startUdevMonitor(self):
        self.udevContext = pyudev.Context()
        self.udevMonitor = pyudev.Monitor.from_netlink(self.udevContext)
        self.udevMonitor.filter_by('block')
        self.udevObserver = pyudev.MonitorObserver(self.udevMonitor, self.udevEvent)
        self.devices = []
        self.udevObserver.start()

    def stopUdevMonitor(self):
        self.udevObserver.stop()

    def udevEvent(self, action, device):
        if action == 'change':
            return
        
        print "UDEV event:", action, device.device_node
        if action == 'add':
            self.devices.append(device.device_node)
        if action == 'remove':
            if device.device_node in self.devices:
                self.devices.remove(device.device_node)

    def destroyCreated(self):
        """
            Destroy all devices created during the tests as recorded by the
            udev. It returns nr. of removed items.
        """
        count = 0

        # remove them in reverse order        
        while self.devices:
            device = self.devices.pop()
            uDevice = pyudev.Device.from_device_file(self.udevContext, device)
            print "Destroying %s:%s" % (device, uDevice.device_type)
            
            if uDevice.device_type == 'partition':
                count += 1
                self.destroyMBR(uDevice.parent.device_node)
            if uDevice.device_type == 'disk':
                # is it RAID?
                try:
                    if uDevice['MD_LEVEL']:
                        count += 1
                        self.destroyMD(device)
                except KeyError:
                    pass # it's not RATD
                    
            #TODO: add LVM
        return count
                            
        
    def destroyVG(self, vgname):
        """
            Destroy given volume group, not using CIM.
            This method should be called when a test fails and wants to clean
            up its mess.
        """
        return self.logRun(["vgremove", "-f", "/dev/mapper/" + vgname])

    def destroyMD(self, mdDeviceId):
        """
            Destroy given RAID, not using CIM.
            This method should be called when a test fails and wants to clean
            up its mess.
        """
        return self.logRun(["test/tools/mdremove", mdDeviceId])
    
    def destroyMBR(self, diskDeviceId):
        """
            Destroy any partition table on given device.
            This method should be called when a test fails and wants to clean
            up its mess.
        """
        return self.logRun(["test/tools/mbrremove", diskDeviceId])
        
    def restartCIM(self):
        """
            Restart CIMOM
        """
        ret = self.logRun(["systemctl", "restart", "sblim-sfcb.service"])
        time.sleep(1)
        if ret == 0:
            self.wbemconnection = pywbem.WBEMConnection(self.url, (self.username, self.password))
        return ret
        
        
        
    def logRun(self, args):
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
        if self.destroyCreated():
            self.restartCIM()
