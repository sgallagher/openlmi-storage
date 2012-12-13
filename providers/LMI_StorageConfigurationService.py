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
import pywbem
import pyanaconda.storage
import cmpi_logging
import util

MEGABYTE = 1024 * 1024

class LMI_StorageConfigurationService(ServiceProvider):
    """ Provider of LMI_StorageConfigurationService. """

    @cmpi_logging.trace_method
    def __init__(self, *args, **kwargs):
        print args, kwargs
        super(LMI_StorageConfigurationService, self).__init__(
                classname="LMI_StorageConfigurationService",
                *args, **kwargs)

    @cmpi_logging.trace_method
    def _check_redundancy_setting(self, redundancy, setting):
        """
            Check that DeviceProvider.Redundancy matches Setting.
            Return None if so or string with error message if it does
            not match.
        """
        drmax = setting.get('DataRedundancyMax', None)
        drmin = setting.get('DataRedundancyMin', None)
        drgoal = setting.get('DataRedundancyGoal', None)
        if drmax is not None and drmax < redundancy.data_redundancy:
            return "DataRedundancyMax is too low."
        if drmin is not None and drmin > redundancy.data_redundancy:
            return "DataRedundancyMin is too high."
        if (drmax is None and drmin is None and drgoal is not None
                and drgoal != redundancy.data_redundancy):
            # only goal is set - it must match
            return "DataRedundancyGoal does not match."

        esmax = setting.get('ExtentStripeLengthMax', None)
        esmin = setting.get('ExtentStripeLengthMin', None)
        esgoal = setting.get('ExtentStripeLength', None)
        if esmax is not None and esmax < redundancy.stripe_length:
            return "ExtentStripeLengthMax is too low."
        if esmin is not None and esmin > redundancy.stripe_length:
            return "ExtentStripeLengthMin is too high."
        if (esmax is None and esmin is None and esgoal is not None
                and esgoal != redundancy.stripe_length):
            # only goal is set - it must match
            return "ExtentStripeLength does not match."

        prmax = setting.get('PackageRedundancyMax', None)
        prmin = setting.get('PackageRedundancyMin', None)
        prgoal = setting.get('PackageRedundancyGoal', None)
        if prmax is not None and prmax < redundancy.package_redundancy:
            return "PackageRedundancyMax is too low."
        if prmin is not None and prmin > redundancy.package_redundancy:
            return "PackageRedundancyMin is too high."
        if (prmax is None and prmin is None and prgoal is not None
                and prgoal != redundancy.package_redundancy):
            # only goal is set - it must match
            return "PackageRedundancyGoal does not match."

        nspof = setting.get('NoSinglePointOfFailure', None)
        if nspof is not None and nspof != redundancy.no_single_point_of_failure:
            return "NoSinglePointOfFailure does not match."

        return None

    @cmpi_logging.trace_method
    def _modify_lv(self, device, name, size):
        """
            Really modify the logical volume, all parameters were checked.
        """
        outparams = []
        if name is not None:
            # rename
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                    "Rename of logical volume is not yet supported.")

        if size is not None:
            # resize

            # check PE size
            newsize = device.vg.align(float(size) / MEGABYTE, True)
            oldsize = device.vg.align(device.size, False)
            print "oldszie", oldsize, "newsize", newsize
            if newsize != oldsize:
                action = pyanaconda.storage.deviceaction.ActionResizeDevice(
                        device, newsize)
                util.partitioning.do_storage_action(self.storage, action)
                self.storage.devicetree.processActions(dryRun=False)
                self.storage.reset()

        newsize = device.size * MEGABYTE
        outparams.append(pywbem.CIMParameter(
                name="Size",
                type="uint64",
                value=pywbem.Uint64(newsize)))

        outparams.append(pywbem.CIMParameter(
                name='theelement',
                type='reference',
                value=self.provider_manager.get_name_for_device(device)))
        return (self.Values.CreateOrModifyElementFromStoragePool.Job_Completed_with_No_Error,
                outparams)


    @cmpi_logging.trace_method
    def _create_lv(self, pool, name, size):
        """
            Really create the logical volume, all parameters were checked.
        """
        args = {}
        args['parents'] = [pool]
        args['size'] = pool.align(float(size) / MEGABYTE, True)
        print "size:", args['size']
        if name:
            args['name'] = name
        lv = self.storage.newLV(**args)
        action = pyanaconda.storage.deviceaction.ActionCreateDevice(lv)
        util.partitioning.do_storage_action(self.storage, action)

        newsize = lv.size * MEGABYTE
        outparams = [
                pywbem.CIMParameter(
                        name='theelement',
                        type='reference',
                        value=self.provider_manager.get_name_for_device(lv)),
                pywbem.CIMParameter(
                    name="Size",
                    type="uint64",
                    value=pywbem.Uint64(newsize))
        ]

        return (self.Values.CreateOrModifyElementFromStoragePool.Job_Completed_with_No_Error,
                outparams)

    @cmpi_logging.trace_method
    def cim_method_createormodifylv(self, env, object_name,
                                    param_elementname=None,
                                    param_goal=None,
                                    param_theelement=None,
                                    param_inpool=None,
                                    param_size=None):
        """
            Implements LMI_StorageConfigurationService.CreateOrModifyLV()

            Create or modify Logical Volume. This method is shortcut to
            CreateOrModifyElementFromStoragePool with the right Goal. Lazy
            applications can use this method to create or modify LVs, without
            calculation of the Goal setting.
        """
        self.check_instance(object_name)
        # check parameters

        # goal
        if param_goal:
            instance_id = param_goal['InstanceID']

            goal = self.provider_manager.get_setting_for_id(
                    instance_id, "LMI_LVStorageSetting")
            if not goal:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                        "LMI_LVStorageSetting Goal does not found.")
        else:
            goal = None

        # lv
        if param_theelement:
            device = self.provider_manager.get_device_for_name(param_theelement)
            if not device:
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                        "Cannot find the TheElement device.")
            if not isinstance(device, pyanaconda.storage.devices.LVMLogicalVolumeDevice):
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                        "The TheElement parameter is not LMI_LVStorageExtent.")
        else:
            device = None

        # pool
        if param_inpool:
            pool = self.provider_manager.get_device_for_name(param_inpool)
            if not pool:
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                        "Cannot find the InPool device.")
            if not isinstance(pool, pyanaconda.storage.devices.LVMVolumeGroupDevice):
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                        "The InPool parameter is not LMI_VGStoragePool.")
        else:
            pool = None

        if param_size is not None:
            newsize = param_size
        else:
            newsize = None

        # check if resize is needed
        if newsize and device:
            oldsize = device.vg.align(device.size, False) * MEGABYTE
            if newsize < oldsize:
                raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                        "Shrinking of logical volumes is not supported.")
            if oldsize == newsize:
                # don't need to change the size
                newsize = None

        # check if rename is needed
        if param_elementname and device:
            oldname = device.name
            if oldname == param_elementname:
                # don't need to change the name
                param_elementname = None

        # pool vs goal
        if goal and pool:
            pool_provider = self.provider_manager.get_provider_for_device(pool)
            redundancy = pool_provider.get_redundancy(pool)
            error = self._check_redundancy_setting(redundancy, goal)
            if error:
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                        "The Goal does not match InPool's capabilities: "
                            + error)

        # pool vs theelement
        if pool and device:
            if device.vg != pool:
                raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                        "InPool does not match TheElement's pool, modification of a pool is not supported.")

        if not device and not pool:
                raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                        "Either InPool or TheElement must be specified.")

        if not device and not newsize:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    "Parameter Size must be set when creating a logical volume.")

        if device:
            return self._modify_lv(device, param_elementname, newsize)
        else:
            return self._create_lv(pool, param_elementname, newsize)


    @cmpi_logging.trace_method
    def cim_method_createormodifyelementfromstoragepool(self, env, object_name,
                                                        param_elementname=None,
                                                        param_goal=None,
                                                        param_inpool=None,
                                                        param_theelement=None,
                                                        param_elementtype=None,
                                                        param_size=None):
        """
            Implements LMI_StorageConfigurationService
                            .CreateOrModifyElementFromStoragePool()

            Start a job to create (or modify) a Logical Volume from a
            LMI_StoragePool. One of the parameters for this method is Size. As
            an input parameter, Size specifies the desired size of the
            element. As an output parameter, it specifies the size achieved.
            The Size is rounded to extent size of the Volume Group. Space is
            taken from the input StoragePool. The desired settings for the
            element are specified by the Goal parameter. If the requested size
            cannot be created, no action will be taken, and the Return Value
            will be 4097/0x1001. Also, the output value of Size is set to the
            nearest possible size.  This method supports renaming or resizing
            of a Logical Volume.  If 0 is returned, the function completed
            successfully and no ConcreteJob instance was required. If
            4096/0x1000 is returned, a ConcreteJob will be started to create
            the element. The Job's reference will be returned in the output
            parameter Job.
        """
        if param_elementtype is not None:
            if param_elementtype != self.Values.CreateOrModifyElementFromStoragePool.ElementType.StorageExtent:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                        "The only ElementType is StorageExtent (3).")
        # create LV
        return self.cim_method_createormodifylv(env, object_name,
                param_elementname,
                param_goal,
                param_theelement,
                param_inpool,
                param_size)


    class Values(ServiceProvider.Values):
        class CreateOrModifyElementFromStoragePool(object):
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
            class ElementType(object):
                Unknown = pywbem.Uint16(0)
                Reserved = pywbem.Uint16(1)
                StorageVolume = pywbem.Uint16(2)
                StorageExtent = pywbem.Uint16(3)
                LogicalDisk = pywbem.Uint16(4)
                ThinlyProvisionedStorageVolume = pywbem.Uint16(5)
                ThinlyProvisionedLogicalDisk = pywbem.Uint16(6)
                # DMTF_Reserved = ..
                # Vendor_Specific = 32768..65535

        class CreateOrModifyLV(object):
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
