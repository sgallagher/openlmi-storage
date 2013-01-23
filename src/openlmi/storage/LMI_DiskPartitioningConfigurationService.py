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

from openlmi.storage.ServiceProvider import ServiceProvider
from openlmi.storage.LMI_DiskPartitionConfigurationSetting \
        import LMI_DiskPartitionConfigurationSetting
import pywbem
import pyanaconda.storage.formats
import openlmi.storage.util.partitioning as partitioning
import openlmi.storage.util.units as units
import parted
import openlmi.storage.cmpi_logging as cmpi_logging

class LMI_DiskPartitionConfigurationService(ServiceProvider):
    """
        LMI_DiskPartitionConfigurationService provider implementation.
    """
    @cmpi_logging.trace_method
    def __init__(self, *args, **kwargs):
        super(LMI_DiskPartitionConfigurationService, self).__init__(
                "LMI_DiskPartitionConfigurationService", *args, **kwargs)

    @cmpi_logging.trace_method
    def get_instance(self, env, model):
        model = super(LMI_DiskPartitionConfigurationService, self).get_instance(
                env, model)
        model['PartitioningSchemes'] = self.Values.PartitioningSchemes.Volumes_may_be_partitioned_or_treated_as_whole
        return model

    @cmpi_logging.trace_method
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

    @cmpi_logging.trace_method
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

        cmpi_logging.log_storage_call("CREATE DISKLABEL",
                {'label': label, 'device': device.path})

        fmt = pyanaconda.storage.formats.getFormat('disklabel', labelType=label)
        action = pyanaconda.storage.deviceaction.ActionCreateFormat(device, fmt)
        partitioning.do_storage_action(self.storage, action)

        return self.Values.SetPartitionStyle.Success


    @cmpi_logging.trace_method

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
                if goal and int(goal['PartitionType']) != LMI_DiskPartitionConfigurationSetting.Values.PartitionType.Logical:
                    raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                            "Only Goal with PartitionType == Logical can be created on this device.")
                # don't forget to adjust their start/end addresses
                address_shift = partitioning.get_logical_partition_start(device)
                # create logical partitions on the disk, not on the extended partition
                device = device.parents[0]
            (minstart, maxend) = partitioning.get_available_sectors(device)
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

    @cmpi_logging.trace_method
    def _modify_partition(self, partition, goal, start, end):
        """
            Modify partition to given goal, start and end.
            Start and End can be 0, which means no change.
            Return (retval, partition).
        """
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                "Partition modification is not supported.")


    @cmpi_logging.trace_method
    def _lmi_modify_partition(self, partition, goal, size):
        """
            Modify partition to given goal and size.
            Size can be Null, which means no change.
            Return (retval, partition, size).
        """
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                "Partition modification is not supported.")

    @cmpi_logging.trace_method
    def _get_max_partition_size(self, device, partition_type):
        """
            Return maximum partition size on given device, in bytes.
            Partition_type must be parted constant.
        """
        if not isinstance(device.format, pyanaconda.storage.formats.disklabel.DiskLabel):
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                "Cannot find partition table on the extent.")
        parted_disk = device.format.partedDisk
        geom = pyanaconda.storage.partitioning.getBestFreeSpaceRegion(
                parted_disk,
                partition_type,
                1,
                grow=True)
        if geom is None:
            return 0
        return geom.getLength()



    @cmpi_logging.trace_method
    def _create_partition(self, device, goal, start, end):
        """
            Create partition on given device with  given goal, start and end.
            Return (retval, partition).
        """
        # TODO: wait for anaconda to implement start/end sectors
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                "CreateOrModifyPartition is not supported, use LMI_CreateOrModifyPartition instead.")

    @cmpi_logging.trace_method
    def _lmi_create_partition(self, device, goal, size):
        """
            Create partition on given device with  given goal and size.
            Size can be null, which means the largest possible size.
            Return (retval, partition, size).
        """
        bootable = None
        part_type = None
        hidden = None
        primary = False

        # check goal and set appropriate partition parameters
        if goal:
            bootable = goal['Bootable']
            if int(goal['PartitionType']) == LMI_DiskPartitionConfigurationSetting.Values.PartitionType.Extended:
                if device.format.labelType != "msdos":
                    raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                            "Goal.PartitionType cannot be Extended for this Extent.")
                part_type = parted.PARTITION_EXTENDED
                primary = True
            elif int(goal['PartitionType']) == LMI_DiskPartitionConfigurationSetting.Values.PartitionType.Primary:
                part_type = parted.PARTITION_NORMAL
                primary = True
            elif int(goal['PartitionType']) == LMI_DiskPartitionConfigurationSetting.Values.PartitionType.Logical:
                if device.format.labelType != "msdos":
                    raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                            "Goal.PartitionType cannot be Logical for this Extent.")
                part_type = parted.PARTITION_LOGICAL
            hidden = goal['Hidden']

        # check size and grow it if necessary
        if size is None:
            grow = True
            size = 1
        else:
            # check maximum size
            if part_type is None:
                if not isinstance(device.format, pyanaconda.storage.formats.disklabel.DiskLabel):
                    raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                            "Cannot find partition table on the extent.")
                max_primary = self._get_max_partition_size(device, parted.PARTITION_NORMAL)
                max_logical = 0
                if device.format.extendedPartition is not None:
                    max_logical = self._get_max_partition_size(device, parted.PARTITION_LOGICAL)
                else:
                    if (device.format.labelType == 'msdos'
                            and len(device.format.partitions) > 3):
                        # There is no extended partition and the new one
                        # will be logical
                        # -> reserve 2 MB for extended partition metadata
                        max_primary = max_primary - 2 * units.MEGABYTE
                max_partition = max(max_primary, max_logical)
            else:
                max_partition = self._get_max_partition_size(device, part_type)
            # convert from sectors to bytes
            max_partition = max_partition * device.partedDevice.sectorSize
            if max_partition < size:
                return (self.Values.LMI_CreateOrModifyPartition.Size_Not_Supported, None, max_partition)
            # Ok, the partition will fit. Continue.
            grow = False
            size = size / units.MEGABYTE

        args = {
                'parents': [device],
                'size': size,
                'partType': part_type,
                'bootable': bootable,
                'grow': grow,
                'primary': primary
        }
        cmpi_logging.log_storage_call("CREATE PARTITION", args)

        partition = self.storage.newPartition(**args)
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
        partitioning.do_storage_action(self.storage, action)
        size = partition.size * units.MEGABYTE

        return (self.Values.LMI_CreateOrModifyPartition.Job_Completed_with_No_Error, partition, size)

    @cmpi_logging.trace_method
    def cim_method_lmi_createormodifypartition(self, env, object_name,
                                               param_partition=None,
                                               param_goal=None,
                                               param_extent=None,
                                               param_size=None):
        """
            Implements LMI_DiskPartitionConfigurationService.LMI_CreateOrModifyPartition()

            Create new partition on given extent.Partition modification is not
            yet supported.The implementation will select the best space to fit
            the partition, with all alignment rules etc. \nIf no Size
            parameter is provided, the largest possible partition is
            created.\nIf no Goal is provided and GPT partition is requested,
            normal partition is created. If no Goal is provided and MS-DOS
            partition is requested and there is extended partition already on
            the device, a logical partition is created. If there is no
            extended partition on the device and there are at most two primary
            partitions on the device, primary partition is created. If there
            is no extended partition and three primary partitions already
            exist, new extended partition with all remaining space is created
            and a logical partition with requested size is created.
        
            Keyword arguments:
            env -- Provider Environment (pycimmb.ProviderEnvironment)
            object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
                specifying the object on which the method LMI_CreateOrModifyPartition() 
                should be invoked.
            param_partition --  The input parameter Partition (type REF (pywbem.CIMInstanceName(classname='CIM_GenericDiskPartition', ...)) 
                A reference an existing partition instance to modify or null to
                request a new partition.
            
            param_goal --  The input parameter Goal (type REF (pywbem.CIMInstanceName(classname='LMI_DiskPartitionConfigurationSetting', ...)) 
                Setting to be applied to created/modified partition.
        
            param_extent --  The input parameter extent (type REF (pywbem.CIMInstanceName(classname='CIM_StorageExtent', ...)) 
                A reference to the underlying extent the partition is base on.
        
            param_size --  The input parameter Size (type pywbem.Uint64) 
                Requested size of the partition to create. If null when
                creating a partition, the larges possible partition is
                created.On output, the achieved size is returned.
        """
        # check parameters
        self.check_instance(object_name)

        if not param_partition and not param_extent:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    "Either Partition or extent parameter must be present.")

        # check goal
        if param_goal:
            instance_id = param_goal['InstanceID']

            goal = self.provider_manager.get_setting_for_id(
                    instance_id, "LMI_DiskPartitionConfigurationSetting")
            if not goal:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                        "LMI_DiskPartitionConfigurationSetting Goal does not found.")
            # TODO: remove when bug #891861 is fixed
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                     "Goal parameter is not supported.")
        else:
            goal = None

        # check extent:
        if param_extent:
            device = self.provider_manager.get_device_for_name(param_extent)
            if not device:
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                        "Cannot find the Extent.")
            if isinstance(device, pyanaconda.storage.devices.PartitionDevice):
                if goal and int(goal['PartitionType']) != LMI_DiskPartitionConfigurationSetting.Values.PartitionType.Logical:
                    raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                            "Only Goal with PartitionType == Logical can be created on this device.")
                device = device.parents[0]
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

        if modify:
            (retval, partition, size) = self._lmi_modify_partition(
                    partition, goal, param_size)
        else:
            (retval, partition, size) = self._lmi_create_partition(
                    device, goal, param_size)

        out_params = []
        if partition:
            partition_name = self.provider_manager.get_name_for_device(partition)
            out_params.append(pywbem.CIMParameter('partition', type='reference',
                           value=partition_name))
        if size:
            out_params.append(pywbem.CIMParameter('size', type='uint64',
                           value=pywbem.Uint64(size)))

        return (retval, out_params)



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

        class LMI_CreateOrModifyPartition(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            Size_Not_Supported = pywbem.Uint32(4097)
            # Method_Reserved = 4098..32767
            # Vendor_Specific = 32768..65535
