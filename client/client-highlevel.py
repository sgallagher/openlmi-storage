#!/usr/bin/python
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

# Demo of SMI-S functionality.
# Prerequisites:
#   - at least three /dev/sd* disk exist
#   - all of them have empty partition table
#   - raid1, raid0 and raid5 modules are in kernel ('modprobe raid5')
#
# The demo
#   - installs new GPT partition table to all /dev/sd* devices
#   - creates one partition on each of them
#   - adds these partitions to one RAID<level>
#   - creates ext3 filesystem on it

import sys
import pywbem
import time

# Parse command line arguments
if len(sys.argv) < 4:
    print 'Usage: %s <address> <namespace> <raid level> [user] [password]' % sys.argv[0]
    print 'Example: %s http://localhost:5988 root/cimv2 5 root redhat' % sys.argv[0]
    print
    print 'BEWARE! It can destroy your data!'
    sys.exit(1)

addr = sys.argv[1]
namespace = sys.argv[2]
level = sys.argv[3]
user = None
password = None
if len(sys.argv) > 4:
    user = sys.argv[4]
if len(sys.argv) > 5:
    password = sys.argv[5]

# Connect to a CIM server
cliconn = pywbem.WBEMConnection(addr, (user, password))
cliconn.default_namespace = namespace

# Get all /dev/sd* disks
disks = cliconn.ExecQuery('WQL', 'SELECT * FROM LMI_LocalDiskExtent WHERE DeviceID LIKE "/dev/sd%"')


# create GPT partition table on them, i.e. call
# LMI_DiskPartitionConfigurationService.SetPartitionStyle(disk, partitionStyle) 
# - get reference to LMI_DiskPartitionConfigurationService instance
partServices = cliconn.EnumerateInstanceNames('LMI_DiskPartitionConfigurationService')
partService = partServices[0]

# - get reference to PartitionStyle we want to create
partStyle = cliconn.ExecQuery('WQL', 'SELECT * FROM LMI_DiskPartitionConfigurationCapabilities WHERE InstanceID = "GPT"')[0]

for disk in disks:
    # - call partService.SetPartitionStyle(disk)
    (ret, outparams) = cliconn.InvokeMethod('SetPartitionStyle', partService, Extent = disk.path, PartitionStyle = partStyle.path)
    print 'SetPartitionStyle(', disk['DeviceID'], ')=', ret

# create one huge partition on the disks, i.e. call
# LMI_DiskPartitionConfigurationService.CreateOrModifyPartition(disk)
for disk in disks: 
    # - call partService.SetPartitionStyle(disk)
    (ret, outparams) = cliconn.InvokeMethod('CreateOrModifyPartition', partService, Extent = disk.path)
    print 'CreateOrModifyPartition(', disk['DeviceID'], ')=', ret

# create RAID out of them, i.e. call
# LMI_StorageConfigurationService.CreateOrModifyStoragePool(settings, pool)
# - find the primordial pool
pool = cliconn.EnumerateInstanceNames('LMI_PrimordialPool')[0]
# - find the LMI_StorageConfigurationService
storageService = cliconn.EnumerateInstanceNames('LMI_StorageConfigurationService')[0]
# - find (or create) appropriate setting
setting = cliconn.ExecQuery('WQL', 'SELECT * FROM LMI_StorageSetting WHERE InstanceID = "STATIC:RAID%s"' % level)[0]
(ret, outparams) = cliconn.InvokeMethod('CreateOrModifyStoragePool', storageService, Goal = setting.path, InPools = [pool])
print 'CreateOrModifyStoragePool()=', ret
print 'created pool:', outparams['Pool']
myRaidPool = outparams['Pool']

# allocate LogicalDisk out of the pool, i.e. call
# LMI_StorageConfigurationService.CreateOrModifyElementFromStoragePool(pool)
(ret, outparams) = cliconn.InvokeMethod('CreateOrModifyElementFromStoragePool', storageService, InPool = myRaidPool, ElementType = pywbem.Uint16(4)) # 4 = create LogicalDisk
print 'CreateOrModifyElementFromStoragePool()=', ret
print 'created element:', outparams['TheElement']
myRaidDisk = outparams['TheElement']

# create a filesystem on the RAID, i.e. call
# LMI_FileSystemConfigurationService.CreateFileSystem
# - find the LMI_FileSystemConfigurationService
fsService = cliconn.EnumerateInstanceNames('LMI_FileSystemConfigurationService')[0]
(ret, outparams) = cliconn.InvokeMethod('CreateFileSystem', fsService, InExtent = myRaidDisk)
print 'LMI_FileSystemConfigurationService()=', ret
