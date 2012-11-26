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

from DeviceProvider import DeviceProvider
import pywbem
import pyanaconda.storage

MEGABYTE = 1024 * 1024

class LMI_VGStoragePool(DeviceProvider):
    """
        Provider of LMI_VGStoragePool.
    """
    def __init__(self, *args, **kwargs):
        super(LMI_VGStoragePool, self).__init__(*args, **kwargs)

    def provides_name(self, object_name):
        """
            Returns True, if this class is provider for given CIM InstanceName.
        """

        instance_id = object_name['InstanceID']
        parts = instance_id.split(":")
        if len(parts) != 3:
            return False
        if parts[0] != "LMI":
            return False
        if parts[1] != "VG":
            return False
        return True

    def provides_device(self, device):
        """
            Returns True, if this class is provider for given Anaconda
            StorageDevice class.
        """
        if  isinstance(device, pyanaconda.storage.devices.LVMVolumeGroupDevice):
            return True
        return False

    def get_device_for_name(self, object_name):
        """
            Returns Anaconda StorageDevice for given CIM InstanceName or
            None if no device is found.
        """
        if self.provides_name(object_name):
            instance_id = object_name['InstanceID']
            parts = instance_id.split(":")
            vgname = parts[2]
            for vg in self.storage.vgs:
                if vg.name == vgname:
                    return vg
            return None

    def get_name_for_device(self, device):
        """
            Returns CIM InstanceName for given Anaconda StorageDevice.
            None if no device is found.
        """
        vgname = device.name
        name = pywbem.CIMInstanceName('LMI_VGStoragePool',
                namespace=self.config.namespace,
                keybindings={
                    'InstanceID' : "LMI:VG:" + vgname
                })
        return name

    def get_instance(self, env, model, device=None):
        """
            Provider implementation of GetInstance intrinsic method.
            It fills all VGStoragePool properties.
        """
        if not self.provides_name(model):
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "Wrong keys.")
        if not device:
            device = self.get_device_for_name(model)
        if not device:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "Cannot find the VG.")

        model['Primordial'] = False
        model['ElementName'] = device.name
        model['PoolID'] = device.name

        model['TotalManagedSpace'] = pywbem.Uint64(
                device.extents * device.peSize * MEGABYTE)
        model['RemainingManagedSpace'] = pywbem.Uint64(
                device.freeExtents * device.peSize * MEGABYTE)

        model['ExtentSize'] = pywbem.Uint64(device.peSize * MEGABYTE)
        model['TotalExtents'] = pywbem.Uint64(device.extents)
        model['RemainingExtents'] = pywbem.Uint64(device.freeExtents)
        model['UUID'] = device.uuid

        return model


    def enum_instances(self, env, model, keys_only):
        """Enumerate instances.

        The WBEM operations EnumerateInstances and EnumerateInstanceNames
        are both mapped to this method. 
        This method is a python generator

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        model -- A template of the pywbem.CIMInstances to be generated.  
            The properties of the model are already filtered according to 
            the PropertyList from the request.  Only properties present in 
            the model need to be given values.  If you prefer, you can 
            always set all of the values, and the instance will be filtered 
            for you. 
        keys_only -- A boolean.  True if only the key properties should be
            set on the generated instances.

        Possible Errors:
        CIM_ERR_FAILED (some other unspecified error occurred)

        """
        model.path.update({'InstanceID': None})

        for device in self.storage.vgs:
            name = self.get_name_for_device(device)
            model['InstanceID'] = name['InstanceID']
            if keys_only:
                yield model
            else:
                yield self.get_instance(env, model, device)

    def cim_method_getsupportedsizes(self, env, object_name,
                                     param_elementtype=None,
                                     param_goal=None,
                                     param_sizes=None):
        """Implements LMI_VGStoragePool.GetSupportedSizes() """
        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_getsupportedsizes()' \
                % self.__class__.__name__)
        rval = self.Values.GetSupportedSizes.Use_GetSupportedSizes_instead
        return (rval, [])

    def cim_method_getsupportedsizerange(self, env, object_name,
                                         param_minimumvolumesize=None,
                                         param_maximumvolumesize=None,
                                         param_elementtype=None,
                                         param_volumesizedivisor=None,
                                         param_goal=None):
        """Implements LMI_VGStoragePool.GetSupportedSizeRange()
        param_minimumvolumesize --  The input parameter MinimumVolumeSize (type pywbem.Uint64) 
            The minimum size for a volume/pool in bytes.
            
        param_maximumvolumesize --  The input parameter MaximumVolumeSize (type pywbem.Uint64) 
            The maximum size for a volume/pool in bytes.
            
        param_elementtype --  The input parameter ElementType (type pywbem.Uint16 self.Values.GetSupportedSizeRange.ElementType) 
            The type of element for which supported size ranges are
            reported. The Thin Provision values are only supported when
            the Thin Provisioning Profile is supported; the resulting
            StorageVolues/LogicalDisk shall have ThinlyPprovisioned set to
            true.
            
        param_volumesizedivisor --  The input parameter VolumeSizeDivisor (type pywbem.Uint64) 
            A volume/pool size must be a multiple of this value which is
            specified in bytes.
            
        param_goal --  The input parameter Goal (type REF (pywbem.CIMInstanceName(classname='CIM_StorageSetting', ...)) 
            The StorageSetting for which supported size ranges should be
            reported for.

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.GetSupportedSizeRange)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        MinimumVolumeSize -- (type pywbem.Uint64) 
            The minimum size for a volume/pool in bytes.
            
        MaximumVolumeSize -- (type pywbem.Uint64) 
            The maximum size for a volume/pool in bytes.
            
        VolumeSizeDivisor -- (type pywbem.Uint64) 
            A volume/pool size must be a multiple of this value which is
            specified in bytes.
            
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

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_getsupportedsizerange()' \
                % self.__class__.__name__)

        if not self.provides_name(object_name):
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "Wrong keys.")
        device = self.get_device_for_name(object_name)
        if not device:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "Cannot find the VG.")

        # we support only logical disks for now (should be StorageExtent)
        if (param_elementtype
                and param_elementtype != self.Values.GetSupportedSizeRange.ElementType.Logical_Disk):
            ret = self.Values.GetSupportedSizeRange.Invalid_Element_Type
            return (ret, [])

        # TODO: check Goal setting!

        extent_size = long(device.peSize * MEGABYTE)
        available_size = long(device.peSize * device.freeExtents * MEGABYTE)

        out_params = []
        out_params += [pywbem.CIMParameter('minimumvolumesize', type='uint64',
                           value=pywbem.Uint64(extent_size))]
        out_params += [pywbem.CIMParameter('maximumvolumesize', type='uint64',
                           value=pywbem.Uint64(available_size))]
        out_params += [pywbem.CIMParameter('volumesizedivisor', type='uint64',
                           value=pywbem.Uint64(extent_size))]
        rval = pywbem.Uint32(
            self.Values.GetSupportedSizeRange.Method_completed_OK)
        return (rval, out_params)



    class Values(DeviceProvider.Values):
        class GetSupportedSizeRange(object):
            Method_completed_OK = pywbem.Uint32(0)
            Method_not_supported = pywbem.Uint32(1)
            Use_GetSupportedSizes_instead = pywbem.Uint32(2)
            Invalid_Element_Type = pywbem.Uint32(3)
            class ElementType(object):
                Storage_Pool = pywbem.Uint16(2)
                Storage_Volume = pywbem.Uint16(3)
                Logical_Disk = pywbem.Uint16(4)
                Thin_Provisioned_Volume = pywbem.Uint16(5)
                Thin_Provisioned_Logical_Disk = pywbem.Uint16(6)

        class GetSupportedSizes(object):
            Method_completed_OK = pywbem.Uint32(0)
            Method_not_supported = pywbem.Uint32(1)
            Use_GetSupportedSizes_instead = pywbem.Uint32(2)
            Invalid_Element_Type = pywbem.Uint32(3)
            class ElementType(object):
                Storage_Pool = pywbem.Uint16(2)
                Storage_Volume = pywbem.Uint16(3)
                Logical_Disk = pywbem.Uint16(4)
                Thin_Provisioned_Volume = pywbem.Uint16(5)
                Thin_Provisioned_Logical_Disk = pywbem.Uint16(6)
