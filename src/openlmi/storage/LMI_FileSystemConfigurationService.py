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
""" Module for LMI_FileSystemConfigurationService class."""

import blivet.formats
import openlmi.storage.util
from openlmi.storage.JobManager import Job
from openlmi.storage.ServiceProvider import ServiceProvider
import pywbem
import openlmi.common.cmpi_logging as cmpi_logging

class LMI_FileSystemConfigurationService(ServiceProvider):
    """
        LMI_FileSystemConfigurationService provider implementation.
    """
    @cmpi_logging.trace_method
    def __init__(self, *args, **kwargs):
        super(LMI_FileSystemConfigurationService, self).__init__(
                "LMI_FileSystemConfigurationService", *args, **kwargs)
        self.broker = None

    @cmpi_logging.trace_method
    def cim_method_lmi_createfilesystem(self, env, object_name,
                                        param_elementname=None,
                                        param_goal=None,
                                        param_filesystemtype=None,
                                        param_inextents=None):
        """Implements LMI_FileSystemConfigurationService.LMI_CreateFileSystem()

        Start a job to create a FileSystem on StorageExtents. If the
        operation completes successfully and did not require a
        long-running ConcreteJob, it will return 0. If 4096/0x1000 is
        returned, a ConcreteJob will be started to create the element. A
        Reference to the ConcreteJob will be returned in the output
        parameter Job. If any other value is returned, the job will not be
        started, and no action will be taken. \nThe parameter TheElement
        will contain a Reference to the FileSystem if this operation
        completed successfully. \nThe StorageExtents to use is specified
        by the InExtents parameter.\nThe desired settings for the
        FileSystem are specified by the Goal parameter. Goal is an element
        of class CIM_FileSystemSetting, or a derived class. Unlike CIM
        standard CreateFileSystem, the parameter is reference to
        CIM_FileSystemSetting stored on the CIMOM.\nA ResidesOnExtent
        association is created between the created FileSystem and the
        StorageExtents used for it.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method LMI_CreateFileSystem() 
            should be invoked.
        param_elementname --  The input parameter ElementName (type unicode) 
            Label of the filesystem being created. If NULL, a
            system-supplied default name can be used. The value will be
            stored in the \'ElementName\' property for the created
            element.
            
        param_goal --  The input parameter Goal (type REF (pywbem.CIMInstanceName(classname='CIM_FileSystemSetting', ...)) 
            The requirements for the FileSystem element to maintain. This
            is an element of class CIM_FileSystemSetting, or a derived
            class. This allows the client to specify the properties
            desired for the file system. If NULL, the
            FileSystemConfigurationService will create default filesystem.
            
        param_filesystemtype --  The input parameter FileSystemType (type pywbem.Uint16 self.Values.LMI_CreateFileSystem.FileSystemType) 
            Type of file system to create. When NULL, file system type is
            retrieved from Goal parameter, which cannot be NULL.
            
        param_inextents --  The input parameter InExtents (type REF (pywbem.CIMInstanceName(classname='CIM_StorageExtent', ...)) 
            The StorageExtents on which the created FileSystem will reside.
            At least one extent must be provided. If the filesystem being
            created supports more than one storage extent (e.g. btrfs),
            more extents can be provided. The filesystem will then reside
            on all of them.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.LMI_CreateFileSystem)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...)) 
            Reference to the job (may be null if job completed).
            
        TheElement -- (type REF (pywbem.CIMInstanceName(classname='CIM_FileSystem', ...)) 
            The newly created FileSystem.
            

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, 
            unrecognized or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the target CIM Class or instance does not 
            exist in the specified namespace)
        CIM_ERR_METHOD_NOT_AVAILABLE (the CIM Server is unable to honor 
            the invocation request)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """
        self.check_instance(object_name)

        # remember input parameters for Job
        input_arguments = {
                'ElementName' : pywbem.CIMProperty(name='ElementName',
                        type='string',
                        value=param_elementname),
                'Goal' : pywbem.CIMProperty(name='goal',
                        type='reference',
                        value=param_goal),
                'FileSystemType' : pywbem.CIMProperty(name='FileSystemType',
                        type='uint16',
                        value=param_filesystemtype),
                'InExtents': pywbem.CIMProperty(name='FileSystemType',
                        type='reference',
                        is_array=True,
                        value=param_inextents),
        }

        if not param_inextents:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    "Parameter InExtents must be specified.")
        devices = []
        for extent in param_inextents:
            device = self.provider_manager.get_device_for_name(extent)
            if not device:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    "Cannot find block device for InExtent"
                    + extent['DeviceID'])
            devices.append(device)
        if len(devices) > 1:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    "Creation of filesystems on multiple devices is not"
                    " yet supported.")
        if len(devices) < 1:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    "At least one InExtent must be specified")
        # Convert devices to strings, so we can survive if some of them
        # disappears or is changed while the job is queued.
        device_strings = [device.path for device in devices]
        # TODO: check the devices are unused

        goal = self._parse_goal(param_goal, "LMI_FileSystemSetting")
        # TODO: check that goal has supported values

        if not goal and not param_filesystemtype:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    "Either Goal or FileSystemType parameter must be specified")
        if not param_filesystemtype:
            # retrieve fs type from the goal
            param_filesystemtype = int(goal['ActualFileSystemType'])

        # convert fstype to Blivet FS
        types = self.Values.LMI_CreateFileSystem.FileSystemType
        fstypes = {
                types.FAT: 'vfat',
                types.FAT16: 'vfat',
                types.FAT32: 'vfat',
                types.XFS: 'xfs',
                types.EXT2: 'ext2',
                types.EXT3: 'ext3',
                types.EXT4: 'ext4',
                types.BTRFS: 'btrfs',
                types.VFAT: 'vfat'
        }
        fsname = fstypes.get(param_filesystemtype, 'None')
        if not fsname:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                    "Creation of requested filesystem is not supported.")

        # create the format
        fmt = blivet.formats.getFormat(fsname)
        if not fmt:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                    "Creation of requested filesystem is not supported.")

        # prepare job
        job = Job(
                job_manager=self.job_manager,
                job_name="CREATE FS " + fsname + " ON " + device.path,
                input_arguments=input_arguments,
                method_name='LMI_CreateFileSystem',
                affected_elements=param_inextents,
                owning_element=self._get_instance_name())
        job.set_execute_action(self._create_fs,
                job, device_strings, fmt, param_elementname, goal)

        # prepare output arguments
        outparams = [ pywbem.CIMParameter(
                name='job',
                type='reference',
                value=job.get_name())]
        retvals = self.Values.LMI_CreateFileSystem

        # enqueue the job
        self.job_manager.add_job(job)
        return (retvals.Method_Parameters_Checked___Job_Started,
                outparams)

    @cmpi_logging.trace_method
    def _parse_goal(self, param_goal, classname):
        """
            Find Setting for given CIMInstanceName and check, that it is
            of given CIM class. 
            Return None, if no Goal was given.
            Raise CIMError, if the Goal cannot be found.
        """
        if param_goal:
            instance_id = param_goal['InstanceID']
            goal = self.provider_manager.get_setting_for_id(
                instance_id, classname)
            if not goal:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    classname + " Goal does not found.")
        else:
            goal = None
        return goal

    @cmpi_logging.trace_method
    def _create_fs(self, job, device_strings, fmt, label, goal):
        """
            Create a filesystem on given devices. This method is called
            from JobManager worker thread!
        """
        devices = []
        # convert strings back to devices
        for devname in device_strings:
            device = self.storage.devicetree.getDeviceByPath(devname)
            if not device:
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                        "One of the devices disappeared: " + devname)
            devices.append(device)
        action = blivet.ActionCreateFormat(devices[0],
                format=fmt)
        openlmi.storage.util.storage.do_storage_action(
                self.storage, action)
        fmtprovider = self.provider_manager.get_provider_for_format(
                devices[0], fmt)
        outparams = {
            'theelement': fmtprovider.get_name_for_format(devices[0], format)
        }

        ret = self.Values.LMI_CreateFileSystem.Job_Completed_with_No_Error
        job.finish_method(
                Job.STATE_FINISHED_OK,
                return_value=ret,
                return_type=Job.ReturnValueType.Uint32,
                output_arguments=outparams,
                error=None)

    class Values(ServiceProvider.Values):
        class LMI_CreateFileSystem(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            StorageExtent_is_not_big_enough_to_satisfy_the_request_ = \
                    pywbem.Uint32(6)
            StorageExtent_specified_by_default_cannot_be_created_ = \
                    pywbem.Uint32(7)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            # Method_Reserved = 4098..32767
            # Vendor_Specific = 32768..65535
            class FileSystemType(object):
                Unknown = pywbem.Uint16(0)
                UFS = pywbem.Uint16(2)
                HFS = pywbem.Uint16(3)
                FAT = pywbem.Uint16(4)
                FAT16 = pywbem.Uint16(5)
                FAT32 = pywbem.Uint16(6)
                NTFS4 = pywbem.Uint16(7)
                NTFS5 = pywbem.Uint16(8)
                XFS = pywbem.Uint16(9)
                AFS = pywbem.Uint16(10)
                EXT2 = pywbem.Uint16(11)
                EXT3 = pywbem.Uint16(12)
                REISERFS = pywbem.Uint16(13)
                # DMTF_Reserved = ..
                EXT4 = pywbem.Uint16(32769)
                BTRFS = pywbem.Uint16(32770)
                JFS = pywbem.Uint16(32771)
                TMPFS = pywbem.Uint16(32772)
                VFAT = pywbem.Uint16(32773)
