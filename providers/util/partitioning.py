# OpenLMI Storage Provider
#
# Copyright (C) 2012 Red Hat, Inc.  All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
    Support functions for partitioning.
"""

from wrapper.common import storage
import parted
import pyanaconda.storage
import pywbem

TYPE_MBR = 'MBR'
TYPE_EMBR = 'EMBR'
TYPE_GPT = 'GPT'
LABEL_MBR = 'msdos'
LABEL_GPT = 'gpt'    
GPT_SIZE = 34

def getLogicalPartitionStart(partition):
    """ Return starting sector of logical partition metadata."""
    disk = partition.disk
    ext = disk.format.partedDisk.getExtendedPartition()
    if not ext:
        raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, 'Cannot find extended partition.')
    
    metadata = None
    part = ext.nextPartition()
    while part is not None:
        if (part.type & parted.PARTITION_LOGICAL
                and part.type & parted.PARTITION_METADATA):
            metadata = part 
        if part.path == partition.path:
            break
        part = part.nextPartition()
    
    print 'partition', part, 'metadata', metadata
    if not part:
        raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, 'Cannot find the partition on the disk.')
    if not metadata:
        raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, 'Cannot find metadata for the partition.')
    
    return metadata.geometry.start

def deletePartition(partition):
    # I get errors when using
    #action = pyanaconda.storage.deviceaction.ActionDestroyDevice(partition)
    #storage.devicetree.registerAction(action)
    #action.execute()
    #storage.devicetree._actions = []
    #
    # Because:
    # - execute() calls devicetree._removeDevice
    #    -> it calls 
    #        part.disk.format.removePartition(part.partedPartition)
    #
    # - execute calls part->destroy()
    #    -> it calls again part.disk.format.removePartition(part.partedPartition)

    # TODO: fix Anaconda to reliably remove partitions.
    # dirty hack
    storage.devicetree._removeDevice(partition)
    partition.disk.format.commit()
    partition.partedDevice.removeFromCache()

def createPartition(partition):
    action = pyanaconda.storage.deviceaction.ActionCreateDevice(partition)
    storage.devicetree.registerAction(action)
    pyanaconda.storage.partitioning.doPartitioning(storage=storage)
    # patched Anaconda is needed for this to work
    partition.disk.format.resetPartedDisk()
    action.execute()
    storage.devicetree._actions = []
    
def createMBR(disk):
    if storage.deviceDeps(disk):
        raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, 'Previous partition table must be empty.')
    fmt = pyanaconda.storage.formats.getFormat('disklabel', labelType=LABEL_MBR)
    action = pyanaconda.storage.deviceaction.ActionCreateFormat(disk, fmt)
    storage.devicetree.registerAction(action)
    action.execute()
    
def createGPT(disk):
    if storage.deviceDeps(disk):
        raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, 'Previous partition table must be empty.')
    fmt = pyanaconda.storage.formats.getFormat('disklabel', labelType=LABEL_GPT)
    action = pyanaconda.storage.deviceaction.ActionCreateFormat(disk, fmt)
    storage.devicetree.registerAction(action)
    action.execute()
