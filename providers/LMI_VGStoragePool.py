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

MEGABYTE = 1024*1024

class LMI_VGStoragePool(DeviceProvider):
    """
        Provider of LMI_VGStoragePool.
    """
    def __init__(self, *args, **kwargs):
        super(LMI_VGStoragePool, self).__init__(*args, **kwargs)

    def providesName(self, objectName):
        """
            Returns True, if this class is provider for given CIM InstanceName.
        """
        
        instanceId = objectName['InstanceID']
        parts = instanceId.split(":")
        if len(parts) != 3:
            return False
        if parts[0] != "LMI":
            return False
        if parts[1] != "VG":
            return False
        return True

    def providesDevice(self, device):
        """
            Returns True, if this class is provider for given Anaconda
            StorageDevice class.
        """
        if  isinstance(device, pyanaconda.storage.devices.LVMVolumeGroupDevice):
            return True
        return False
        
    def getDeviceForName(self, objectName):
        """
            Returns Anaconda StorageDevice for given CIM InstanceName or
            None if no device is found.
        """
        if self.providesName(objectName):
            instanceId = objectName['InstanceID']
            parts = instanceId.split(":")
            vgname = parts[2]
            for vg in self.storage.vgs:
                if vg.name == vgname:
                    return vg
            return None

    def getNameForDevice(self, device):
        """
            Returns CIM InstanceName for given Anaconda StorageDevice.
            None if no device is found.
        """
        vgname = device.name
        name = pywbem.CIMInstanceName('LMI_VGStoragePool',
                namespace = self.config.namespace,
                keybindings = {
                    'InstanceID' : "LMI:VG:" + vgname
                })
        return name
                
    def get_instance(self, env, model, device = None):
        """
            Provider implementation of GetInstance intrinsic method.
            It fills all VGStoragePool properties.
        """
        if not self.providesName(model):
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "Wrong keys.")
        if not device:
            device = self.getDeviceForName(model)
        if not device:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "Cannot find the VG.")
        
        model['Primordial'] = False
        model['ElementName'] = device.name
        model['PoolID'] = device.name

        model['TotalManagedSpace'] = pywbem.Uint64(device.extents * device.peSize * MEGABYTE)
        model['RemainingManagedSpace'] = pywbem.Uint64(device.freeExtents * device.peSize * MEGABYTE)
        
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
            name = self.getNameForDevice(device)
            model['InstanceID'] = name['InstanceID']
            if keys_only:
                yield model
            else:
                yield self.get_instance(env, model, device)

            