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


from common import *
from DeviceWrapper import DeviceWrapper
import pyanaconda.storage.devices
import pywbem

class LVWrapper(DeviceWrapper):
    """
        Wrapper for Anaconda logical volume devices, i.e.
        pyanaconda.storage.devices.LVMLogicalVolumeDevices.

        This wrapper is special, it creates only StorageExtent instances and no
        StoragePools. In addition, all logical volumes are automatically
        CIM_LogicalDisks.

        The logical volumes are wrapped only because to be able to create
        additional storage layer (e.g. encryption) on top of them. The
        WrapperManager and all Wrapper* providers are then able to create
        appropriate BasedOn classes.

        For each Anaconda LVMLogicalVolumeDevice, following CIM instances are
        created:

        - one LMI_LVLogicalDisk
        - one LMI_LVLogicalDiskBasedOn association to its volume group
        - one LMI_LVAllocatedFromStoragePool association to pool of its volume
          group.
    """

    def __init__(self):
        super(LVWrapper, self).__init__('LV')

    @property
    def extentClassName(self):
        """
            CIM class name of device's CIM_StorageExtent class.

            This property is overriden to have LMI_LVLogicalDisk as name of
            LV's StorageExtent class. Vanilla DeviceWrapper would provide
            LMI_LVExtent.
        """
        return 'LMI_' + self.prefix + 'LogicalDisk'

    @property
    def basedOnClassName(self):
        """
            CIM class name of device's CIM_BasedOn class.

            This property is overriden to have LMI_LVLogicalDiskBasedOn as
            name of LV's BasedOn class. Vanilla DeviceWrapper would provide
            LMI_LVExtentBasedOn.
        """
        return 'LMI_' + self.prefix + 'LogicalDiskBasedOn'

    def enumDevices(self):
        """
            Enumerate all LVMLogicalVolumeDevices known to Anaconda.
            StorageExtent and all necessary associations
            will be created for each of them.
        """
        for array in storage.lvs:
            yield array

    def enumBaseDevices(self, device):
        """
            Enumerate parent devices of given Anaconda LVMLogicalVolumeDevice.
            BasedOn and AllocatedFrom association will be created to each of them.

            :param device: Instance of LVMLogicalVolumeDevice, whose parent
                devices (i.e. physical volumes) should be returned.
        """
        yield device.vg

    def getExtentInstance(self, env, model, device):
        """
            Fill instance of LMI_LVLogicalDisk for given
            LVMLogicalVolumeDevice.
        """
        params = self.getParameters(device)
        #model['Access'] = self.Values.Access.<VAL>
        #model['AdditionalAvailability'] = [self.Values.AdditionalAvailability.<VAL>,]
        #model['Availability'] = self.Values.Availability.<VAL>
        #model['AvailableRequestedStates'] = [self.Values.AvailableRequestedStates.<VAL>,]
        #model['BlockSize'] = pywbem.Uint64()
        #model['Caption'] = ''
        #model['ClientSettableUsage'] = [pywbem.Uint16(),]
        #model['CommunicationStatus'] = self.Values.CommunicationStatus.<VAL>
        #model['ConsumableBlocks'] = pywbem.Uint64()
        #model['DataOrganization'] = self.Values.DataOrganization.<VAL>
        model['DataRedundancy'] = params['DataRedundancyDefault']
        #model['DeltaReservation'] = pywbem.Uint8()
        #model['Description'] = ''
        #model['DetailedStatus'] = self.Values.DetailedStatus.<VAL>
        model['ElementName'] = device.name
        #model['EnabledDefault'] = self.Values.EnabledDefault.Enabled
        #model['EnabledState'] = self.Values.EnabledState.Not_Applicable
        #model['ErrorCleared'] = bool()
        #model['ErrorDescription'] = ''
        #model['ErrorMethodology'] = ''
        model['ExtentDiscriminator'] = ['SNIA:Pool Component', 'SNIA:Composite']
        #model['ExtentInterleaveDepth'] = pywbem.Uint64()
        model['ExtentStatus'] = pywbem.CIMProperty(name='ExtentStatus', value=[], type='uint16', array_size=0, is_array=True)
        model['ExtentStripeLength'] = params['ExtentStripeLengthDefault']
        #model['Generation'] = pywbem.Uint64()
        #model['HealthState'] = self.Values.HealthState.<VAL>
        #model['IdentifyingDescriptions'] = ['',]
        #model['InstallDate'] = pywbem.CIMDateTime()
        #model['InstanceID'] = ''
        #model['IsBasedOnUnderlyingRedundancy'] = bool()
        #model['IsComposite'] = bool(True)
        #model['IsConcatenated'] = bool()
        #model['LastErrorCode'] = pywbem.Uint32()
        #model['LocationIndicator'] = self.Values.LocationIndicator.<VAL>
        #model['MaxQuiesceTime'] = pywbem.Uint64()
        #model['Name'] = array.path
        #model['NameFormat'] = self.Values.NameFormat.<VAL>
        #model['NameNamespace'] = self.Values.NameNamespace.<VAL>
        model['NoSinglePointOfFailure'] = params['NoSinglePointOfFailure']
        # TODO: calculate size
        #model['NumberOfBlocks'] = pywbem.Uint64()
        #model['OperatingStatus'] = self.Values.OperatingStatus.<VAL>
        #model['OperationalStatus'] = [self.Values.OperationalStatus.<VAL>,]
        #model['OtherEnabledState'] = ''
        #model['OtherIdentifyingInfo'] = ['',]
        #model['OtherNameFormat'] = ''
        #model['OtherNameNamespace'] = ''
        #model['OtherUsageDescription'] = ''
        model['PackageRedundancy'] = params['PackageRedundancyDefault']
        #model['PowerManagementCapabilities'] = [self.Values.PowerManagementCapabilities.<VAL>,]
        #model['PowerManagementSupported'] = bool()
        #model['PowerOnHours'] = pywbem.Uint64()
        #model['PrimaryStatus'] = self.Values.PrimaryStatus.<VAL>
        model['Primordial'] = params['Primordial']
        #model['Purpose'] = ''
        #model['RequestedState'] = self.Values.RequestedState.Not_Applicable
        #model['SequentialAccess'] = bool()
        #model['Status'] = self.Values.Status.<VAL>
        #model['StatusDescriptions'] = ['',]
        #model['StatusInfo'] = self.Values.StatusInfo.<VAL>
        #model['TimeOfLastStateChange'] = pywbem.CIMDateTime()
        #model['TotalPowerOnHours'] = pywbem.Uint64()
        #model['TransitioningToState'] = self.Values.TransitioningToState.Not_Applicable
        #model['Usage'] = self.Values.Usage.<VAL>
        return model

    def enumAllocatedFroms(self, env, model, keys_only):
        """
            Enumerate all LMI_LVAllocatedFromStoragePool instances.

            :param env: Provider Environment (pycimmb.ProviderEnvironment).
            :param model: A template of the pywbem.CIMInstances to be generated.
            :param keys_only:  boolean. True if only the key properties should be
                set on the generated instances.

            Usually, the  AllocatedFrom association is pool -> underlying pool
            but for LVLogicalDisk it's from Extent -> underlying pool
            (because it's LogicalDisk). Therefore this method must be
            overridden.
        """
        for device in self.enumDevices():
            base = device.vg
            extentName = self.getExtentName(device)
            dependentWrapper = wrapperManager.getWrapperForDevice(base)
            basePool = dependentWrapper.getPoolName(base)
            if extentName is None or basePool is None:
                continue
            model['Dependent'] = extentName
            model['Antecedent'] = basePool
            if keys_only:
                yield model
            else:
                yield self.getAllocatedFromInstance(env, model, device, base)

    def getAllocatedFromInstance(self, env, model, device, base):
        """
            Fill instance of LMI_LVAllocatedFromStoragePool for given
            LVMLogicalVolumeDevice.
        """
        model['SpaceConsumed'] = pywbem.Uint64(device.vgSpaceUsed)
        return model

    def getBasedOnInstance(self, env, model, device, base):
        """
            Fill instance of LMI_LVLogicalDiskBasedOn for given
            LVMLogicalVolumeDevice.
        """
        #model['BlockSize'] = pywbem.Uint64()
        #model['EndingAddress'] = pywbem.Uint64()
        #model['LBAMappingIncludesCheckData'] = bool()
        #model['LBAsMappedByDecrementing'] = bool()
        #model['NumberOfBlocks'] = pywbem.Uint64()
        model['OrderIndex'] = pywbem.Uint16(1)
        #model['StartingAddress'] = pywbem.Uint64()
        #model['UnitsBeforeCheckDataInterleave'] = pywbem.Uint64()
        #model['UnitsOfCheckData'] = pywbem.Uint64()
        #model['UnitsOfUserData'] = pywbem.Uint64()
        #model['UserDataStripeDepth'] = pywbem.Uint64()
        return model

    def getPoolId(self, device):
        """
            Return StoragePool.InstanceID for given Anaconda device.
            There is no pool for logical volumes, therefore return None.
        """
        return None

    def getPoolName(self, device):
        """
            Return CIMInstanceName of StoragePool for given Anaconda device.

            :param device: Concrete Anaconda storage device, whose StoragePool's
                CIMInstanceName should be returned.

            There is no pool for logical volumes, therefore return None.
        """
        return None

    def enumPools(self,  env, model, keys_only):
        """
            Enumerate all StoragePools.
            There is no pool for logical volumes, therefore return empty list.
        """
        return []

    def getPoolInstance(self, env, model, device):
        """
            Fill and return a CIMInstance of StoragePool for given Anaconda
            device.

            There is no pool for logical volumes, therefore throw an exception.
        """
        raise  pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED, 'LVM does not have a pool.')

    def getCapabilitiesId(self, device):
        """
            Return StorageCapabilities.InstanceID for given Anaconda device.

            There is no pool for logical volumes, therefore return None.
        """
        return None

    def getCapabilitiesName(self, device):
        """
            Return CIMInstanceName of StorageCapabilities for given Anaconda
            device.

            There is no pool for logical volumes, therefore return None.
        """
        return None

    def enumCapabilities(self, env, model, keys_only):
        """
            Enumerate all StorageCapabilities.

            There is no pool for logical volumes, therefore return empty list.
        """
        return []

    def getCapabilitiesInstance(self, env, model, device):
        """
            Fill and return a CIMInstance of StorageCapabilities for given
            Anaconda device.

            There is no pool for logical volumes, therefore throw an exception.
        """
        raise  pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED, 'LVM does not have a pool.')

    def enumAssociatedExtents(self, env, model, keys_only):
        """
            Enumerate all AssociatedComponentExtents.

            There is no pool for logical volumes, therefore return empty list.
        """
        return []

    def getAssociatedExtentInstance(self, env, model, device):
        """
            Fill and return a CIMInstance of AssociatedComponentExtent
            for given Anaconda device.

            There is no pool for logical volumes, therefore throw an exception.
        """
        raise  pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED, 'LVM does not have a pool.')

    def enumElementCapabilities(self, env, model, keys_only):
        """
            Enumerate all ElementCapabilities.

            There is no pool for logical volumes, therefore return empty list.
        """
        return []

    def getElementCapabilitiesInstance(self, env, model, device):
        """
            Fill and return a CIMInstance of ElementCapabilities
            for given Anaconda device.

            There is no pool for logical volumes, therefore throw an exception.
        """
        raise  pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED, 'LVM does not have a pool.')

    def wrapsDevice(self, device):
        """
            Return True, if given Anaconda device is managed by this wrapper,
            i.e. if it is LVMLogicalVolumeDevice.

            :param device: Device to examine.
        """
        if isinstance(device, pyanaconda.storage.devices.LVMLogicalVolumeDevice):
            return True
        return False

    def getParameters(self, device):
        """
            Return capabilities of given LVMLogicalVolumeDevice.

            :param device: LVMLogicalVolumeDevice to examine.

            Only simple logical volumes are supported for now, no redundancy,
            thin pools or other fancy stuff.
        """
        
        # start with parameters of parent volume group
        parentWrapper = wrapperManager.getWrapperForDevice(device.vg)
        params = parentWrapper.getParameters(device.vg)
        params['LMIAllocationType'] = pywbem.Uint16(0)
        
        # add common parameters like name and size
        params.update(super(LVWrapper, self).getParameters(device))
        return params
        
    def canCreatePool(self, devices, setting, size = None, name = None):
        """
            LogicalVolume is not a pool, therefore this wrapper cannot
            create any.
                        
            :param devices: Array of Anaconda storage devices representing
                 input StoragePools and StorageExtents.
            :param setting: Instance of LMI_StorageSetting.
            :param size: Expected size of the resulting device.
            :param name: Expected name of the resulting device.
            
            The input parameters are taken from
            LMI_StorageConfigurationService.CreateOrModifyStoragePool
        """
        return 0

    def destroyLogicalDisk(self, device):
        """
            Destroy given logical volume.
            
            :param device; Anaconda storage device, representing the
                logical volume.
        """
        if device.format.type is not None:
            action = pyanaconda.storage.deviceaction.ActionDestroyFormat(device)
            storage.devicetree.registerAction(action)
            action.execute()
            storage.devicetree._actions = []
            
        print device
        action = pyanaconda.storage.deviceaction.ActionDestroyDevice(device)
        storage.devicetree.registerAction(action)
        action.execute()
        storage.devicetree._actions = []
        return self.DESTROY_COMPLETED_OK
