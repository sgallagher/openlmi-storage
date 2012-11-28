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

from ServiceProvider import ServiceProvider
from LMI_DiskPartitionConfigurationSetting import LMI_DiskPartitionConfigurationSetting
import pywbem
import pyanaconda.storage.formats
import util.partitioning
import parted

class LMI_DiskPartitionConfigurationService(ServiceProvider):
    """
        LMI_DiskPartitionConfigurationService provider implementation.
    """
    def __init__(self, *args, **kwargs):
        super(LMI_DiskPartitionConfigurationService, self).__init__(
                "LMI_DiskPartitionConfigurationService", *args, **kwargs)

    def get_instance(self, env, model):
        model = super(LMI_DiskPartitionConfigurationService, self).get_instance(
                env, model)
        model['PartitioningSchemes'] = self.Values.PartitioningSchemes.Volumes_may_be_partitioned_or_treated_as_whole
        return model

    def cim_method_setpartitionstyle(self, env, object_name,
                                     param_extent=None,
                                     param_partitionstyle=None):
        """
            Implements LMI_DiskPartitionConfigurationService.SetPartitionStyle()

            This method installs a partition table on an extent of the
            specified partition style; creating an association between the
            extent and that capabilities instances referenced as method
            parameters. As a side effect, the consumable block size of the
            underlying extent is reduced by the block size of the metadata
            reserved by the partition table and associated metadata. This size
            is in the PartitionTableSize property of the associated
            DiskPartitionConfigurationCapabilities instance.
        """
        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_setpartitionstyle()' \
                % self.__class__.__name__)

        # check parameters here, the real work is done in _setpartitionstyle
        self.check_instance(object_name)

        if not param_extent:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    "Parameter Extent is mandatory.")

        # check the device
        device = self.provider_manager.get_device_for_name(param_extent)
        if not device:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Cannot find the Extent.")
        if isinstance(device, pyanaconda.storage.devices.PartitionDevice):
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                    "Creation of extended partitions is not supported.")
        if self.storage.deviceDeps(device):
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "The Extent is used.")

        # check the capabilities
        capabilities_provider = self.provider_manager.get_capabilities_provider_for_class('LMI_DiskPartitionConfigurationCapabilities')
        if not capabilities_provider:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Cannot find capabilities provider.")
        if param_partitionstyle:
            capabilities = capabilities_provider.get_capabilities_for_id(
                    param_partitionstyle['InstanceID'])
            if not capabilities:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                        "Cannot find capabilities for given PartitionStyle.")
        else:
            # find the default capabilities
            capabilities = capabilities_provider.get_default_capabilities()
            if not capabilities:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                        "Parameter PartitionStyle is mandatory, there is no default PartitionStyle.")

        if capabilities['PartitionStyle'] == capabilities_provider.Values.PartitionStyle.EMBR:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                    "Creation of extended partitions is not supported.")

        retval = self._setpartitionstyle(device, capabilities, capabilities_provider)
        return (retval, [])

    def _setpartitionstyle(self, device, capabilities, capabilities_provider):
        """
            Really set the partition style, all parameters were successfully
            checked.
        """
        if capabilities['PartitionStyle'] == capabilities_provider.Values.PartitionStyle.MBR:
            label = "msdos"
        elif capabilities['PartitionStyle'] == capabilities_provider.Values.PartitionStyle.GPT:
            label = "gpt"
        else:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                    "Unsupported PartitionStyle:"
                    + str(capabilities['PartitionStyle']) + ".")

        fmt = pyanaconda.storage.formats.getFormat('disklabel', labelType=label)
        action = pyanaconda.storage.deviceaction.ActionCreateFormat(device, fmt)
        self.storage.devicetree.registerAction(action)
        action.execute()
        return self.Values.SetPartitionStyle.Success


    def cim_method_createormodifypartition(self, env, object_name,
                                           param_goal=None,
                                           param_partition=None,
                                           param_devicefilename=None,
                                           param_extent=None,
                                           param_startingaddress=None,
                                           param_endingaddress=None):
        """
            Implements LMI_DiskPartitionConfigurationService.CreateOrModifyPartition()

            This method creates a new partition if the Partition parameter is
            null or modifies the partition specified. If the starting and
            ending address parameters are null, the resulting partition will
            occupy the entire underlying extent. If the starting address is
            non-null and the ending address is null, the resulting partition
            will extend to the end of the underlying extent. \n\nIn
            contradiction to SMI-S, no LogicalDisk will be created on the
            partition.\nIf logical partition is being created, it's start/end
            sector must include space for partition metadata and any alignment
            sectors. ConsumableSpace of the logical partition will be reduced
            by these metadata and alignment sectors.\nThe underlying extent
            MUST be associated to a capabilities class describing the
            installed partition style (partition table); this association is
            established using SetPartitionStyle().
        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_createormodifypartition()' \
                % self.__class__.__name__)

        # check parameters
        self.check_instance(object_name)

        if not param_partition and not param_extent:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    "Either Partition or extent parameter must be present.")
        if param_devicefilename:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                    "Parameter DeviceFileName is not supported.")

        # check goal
        if param_goal:
            instance_id = param_goal['InstanceID']

            goal = self.provider_manager.get_setting_for_id(
                    instance_id, "LMI_DiskPartitionConfigurationSetting")
            if not goal:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                        "LMI_DiskPartitionConfigurationSetting Goal does not found.")
        else:
            goal = None

        # check extent:
        address_shift = 0  # needed to adjust logical partitions addresses 
        if param_extent:
            device = self.provider_manager.get_device_for_name(param_extent)
            if not device:
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                        "Cannot find the Extent.")
            if isinstance(device, pyanaconda.storage.devices.PartitionDevice):
                if goal and goal['PartitionType'] != LMI_DiskPartitionConfigurationSetting.Values.PartitionType.Logical:
                    raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                            "Only Goal with PartitionType == Logical can be created on this device.")
                # create logical partitions on the disk, not on the extended partition
                device = device.parents[0]
                # and don't forget to adjust their start/end addresses
                address_shift = util.partitioning.get_logical_partition_start(device)
            (minstart, maxend) = util.partitioning.get_available_sectors(device)
        else:
            device = None

        # check partition
        if param_partition:
            modify = True
            partition = self.provider_manager.get_device_for_name(param_partition)
            if not partition:
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                        "Cannot find the Partition.")
            if not isinstance(device, pyanaconda.storage.devices.PartitionDevice):
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                        "Parameter Partition does not refer to partition.")
            if device:
                # the partition must be on the device
                if device not in partition.parents:
                    raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                            "The Partition does not reside on the Extent.")
        else:
            modify = False

        if param_startingaddress is None:
            if modify:
                start = 0
            else:
                start = minstart
        else:
            start = param_startingaddress + address_shift

        if param_endingaddress is None:
            if modify:
                end = 0
            else:
                end = maxend
        else:
            end = param_endingaddress + address_shift

        if modify:
            (retval, partition) = self._modify_partition(
                    partition, goal, start, end)
        else:
            (retval, partition) = self._create_partition(
                    device, goal, start, end)

        partition_name = self.provider_manager.get_name_for_device(partition)
        out_params = [pywbem.CIMParameter('partition', type='reference',
                           value=partition_name)]
        return (retval, out_params)

    def _modify_partition(self, partition, goal, start, end):
        """
            Modify partition to given goal, start and end.
            Start and End can be 0, which means no change.
            Return (retval, partition).
        """
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                "Partition modification is not supported.")

    def _create_partition(self, device, goal, start, end):
        """
            Create partition on given device with  given goal, start and end.
            Return (retval, partition).
        """
        bootable = None
        part_type = None
        hidden = None
        if goal:
            bootable = goal['Bootable']
            if goal['PartitionType'] == LMI_DiskPartitionConfigurationSetting.Values.PartitionType.Extended:
                if device.format.labelType != "msdos":
                    raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                            "Goal.PartitionType cannot be Extended for this Extent.")
                part_type = parted.PARTITION_EXTENDED
            elif goal['PartitionType'] == LMI_DiskPartitionConfigurationSetting.Values.PartitionType.Primary:
                part_type = parted.PARTITION_NORMAL
            elif goal['PartitionType'] == LMI_DiskPartitionConfigurationSetting.Values.PartitionType.Logical:
                if device.format.labelType != "msdos":
                    raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                            "Goal.PartitionType cannot be Logical for this Extent.")
                part_type = parted.PARTITION_LOGICAL
            hidden = goal['Hidden']

        size = pyanaconda.storage.partitioning.sectorsToSize(
                end - start,
                device.partedDevice.sectorSize)
        partition = self.storage.newPartition(
                #start=start,
                #end=end,
                parents=[device],
                size=size,
                partType=part_type,
                bootable=bootable,
                grow=False)
        partition.disk = device

        if hidden is not None:
            if partition.flagAvailable(parted.PARTITION_HIDDEN):
                if hidden:
                    partition.setFlag(parted.PARTITION_HIDDEN)
            else:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                        "Goal.Hidden cannot be set for this Extent.")

        # finally, do the dirty job
        action = pyanaconda.storage.deviceaction.ActionCreateDevice(partition)
        self.storage.devicetree.registerAction(action)
        pyanaconda.storage.partitioning.doPartitioning(storage=self.storage)
        # patched Anaconda is needed for this to work
        partition.disk.format.resetPartedDisk()
        action.execute()
        self.storage.devicetree._actions = []

        return (self.Values.CreateOrModifyPartition.Success, partition)

    class Values(ServiceProvider.Values):
        class PartitioningSchemes(object):
            No_partitions_allowed = pywbem.Uint16(2)
            Volumes_may_be_partitioned_or_treated_as_whole = pywbem.Uint16(3)
            Volumes_must_be_partitioned = pywbem.Uint16(4)

        class SetPartitionStyle(object):
            Success = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            # DMTF_Reserved = ..
            # Extent_already_has_partition_table = 0x1000
            # Requested_Extent_too_large = 0x1001
            # Style_not_supported_by_Service = 0x1002
            # Method_Reserved = ..
            # Vendor_Specific = 0x8000..

        class CreateOrModifyPartition(object):
            Success = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            # DMTF_Reserved = ..
            # Overlap_Not_Supported = 0x1000
            # No_Available_Partitions = 0x1001
            # Specified_partition_not_on_specified_extent = 0x1002
            # Device_File_Name_not_valid = 0x1003
            # LogicalDisk_with_different_DeviceFileName_exists = 0x1004
            # Method_Reserved = ..
            # Vendor_Specific = 0x8000..
