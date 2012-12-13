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

import parted
import pywbem
import pyanaconda.storage
import cmpi_logging

GPT_TABLE_SIZE = 34 * 2  # there are two copies
MBR_TABLE_SIZE = 1

def _align_up(address, alignment):
    return (address / alignment + 1) * alignment

def _align_down(address, alignment):
    return (address / alignment) * alignment

@cmpi_logging.trace_function
def get_logical_partition_start(partition):
    """
        Return starting sector of logical partition metadata, relative to
        extended partition start.
    """
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

@cmpi_logging.trace_function
def get_partition_table_size(device):
    """
        Return size of partition table (in blocks) for given Anaconda
        StorageDevice instance.
    """
    if device.format:
        fmt = device.format
        if fmt.labelType == "gpt":
            return GPT_TABLE_SIZE * 2
        if fmt.labelType == "msdos":
            return MBR_TABLE_SIZE
    return 0

@cmpi_logging.trace_function
def get_available_sectors(device):
    """
        Return (start, end), where start is the first usable sector after
        partition table and end is the last usable sector before any
        partition table copy 
    """
    size = device.partedDevice.length
    if device.format:
        fmt = device.format
        alignment = device.partedDevice.optimumAlignment.grainSize
        if fmt.labelType == "gpt":
            return (
                    _align_up(GPT_TABLE_SIZE, alignment),
                    _align_down(size - GPT_TABLE_SIZE - 1, alignment))
        if fmt.labelType == "msdos":
            return(
                    _align_up(MBR_TABLE_SIZE, alignment),
                    _align_down(size - 1, alignment))

    if isinstance(device, pyanaconda.storage.devices.PartitionDevice):
        if device.isExtended:
            return(
                    _align_up(0, alignment),
                    _align_down(size - 1, alignment))

    return (0, size - 1)

@cmpi_logging.trace_function
def remove_partition(storage, device):
    """
        Remove PartitionDevice from system, i.e. delete a partition.
    """
    action = pyanaconda.storage.deviceaction.ActionDestroyDevice(device)
    do_storage_action(storage, action)

@cmpi_logging.trace_function
def do_storage_action(storage, action):
    """
        Perform Anaconda DeviceAction on given Storage instance.
    """

    cmpi_logging.logger.trace_info("Running action " + str(action))
    cmpi_logging.logger.trace_info("    on device " + repr(action.device))

    do_partitioning = False
    if (isinstance(action.device, pyanaconda.storage.devices.PartitionDevice)
            and isinstance(action, pyanaconda.storage.deviceaction.ActionCreateDevice)):
        do_partitioning = True
    storage.devicetree.registerAction(action)

    try:
        if do_partitioning:
            # this must be called when creating a partition
            cmpi_logging.logger.trace_verbose("Running doPartitioning()")
            pyanaconda.storage.partitioning.doPartitioning(storage=storage)

        storage.devicetree.processActions(dryRun=False)
        if not isinstance(action, pyanaconda.storage.deviceaction.ActionDestroyDevice):
            cmpi_logging.logger.trace_verbose("Result: " + repr(action.device))
    finally:
        storage.reset()
