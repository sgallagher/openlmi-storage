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
from WrappedPool import WrappedPool
from DeviceWrapper import DeviceWrapper
import pyanaconda.storage.devices
import pywbem

class VGWrapper(DeviceWrapper):
    """
        Wrapper for Anaconda volume group devices, i.e.
        pyanaconda.storage.devices.LVMVolumeGroupDevices.

        For each Anaconda LVMVolumeGroupDevices, following CIM instances are
        created:

        - one LMI_VGPool
        - one LMI_VGCompositeExtent with LMI_AssociatedVGComponentExtent
          association to its LMI_VGPool
        - one LMI_VGStorageCapabilities with
          LMI_VGStorageElementCapabilities association to LMI_VGPool
        - one or more LMI_VGCompositeExtentBasedOn associations to all physical
          volumes.
        - one or more LMI_VGAllocatedFromStoragePool associations to pools of
          all physical volumes.

        Logical volumes allocated from the volume groups are managed by
        LVWrapper.
    """

    def __init__(self):
        super(VGWrapper, self).__init__('VG')

    @property
    def extentClassName(self):
        """
            CIM class name of device's CIM_StorageExtent class.

            This property is overriden to have LMI_VGCompositeExtent as name of
            VG's StorageExtent class. Vanilla DeviceWrapper would provide
            LMI_VGExtent.
        """
        return 'LMI_' + self.prefix + 'CompositeExtent'

    @property
    def basedOnClassName(self):
        """
            CIM class name of device's CIM_BasedOn class.

            This property is overriden to have LMI_VGCompositeExtentBasedOn as
            name of VG's BasedOn class. Vanilla DeviceWrapper would provide
            LMI_VGExtentBasedOn.
        """
        return 'LMI_' + self.prefix + 'CompositeExtentBasedOn'

    def enumDevices(self):
        """
            Enumerate all LVMVolumeGroupDevices known to Anaconda. StorageExtent,
            StoragePool and StorageCapabilities and all necessary associations
            will be created for each of them.
        """
        for array in storage.vgs:
            yield array

    def enumBaseDevices(self, device):
        """
            Enumerate parent devices of given Anaconda LVMVolumeGroupDevices.
            BasedOn and AllocatedFrom association will be created to each of them.

            :param device: Instance of LVMVolumeGroupDevices, whose parent devices
                (i.e. physical volumes) should be returned.
        """
        for base in device.pvs:
            yield base

    def getPoolInstance(self, env, model, device):
        """
            Fill instance of LMI_VGPool for given LVMVolumeGroupDevices.
        """
        #model['AllocationUnits'] = ''
        #model['Capacity'] = pywbem.Uint64()
        #model['CapacityInMigratingSource'] = pywbem.Uint64()
        #model['CapacityInMigratingTarget'] = pywbem.Uint64()
        #model['Caption'] = ''
        #model['ClientSettableUsage'] = []
        #model['CommunicationStatus'] = self.Values.CommunicationStatus.<VAL>
        #model['ConsumedResourceUnits'] = ''
        #model['CurrentlyConsumedResource'] = pywbem.Uint64()
        #model['Description'] = ''
        #model['DetailedStatus'] = self.Values.DetailedStatus.<VAL>
        model['ElementName'] = device.name
        #model['Generation'] = pywbem.Uint64()
        #model['HealthState'] = self.Values.HealthState.<VAL>
        #model['InstallDate'] = pywbem.CIMDateTime()
        #model['LowSpaceWarningThreshold'] = pywbem.Uint16()
        #model['MaxConsumableResource'] = pywbem.Uint64()
        #model['Name'] = ''
        #model['OperatingStatus'] = self.Values.OperatingStatus.<VAL>
        #model['OperationalStatus'] = [self.Values.OperationalStatus.<VAL>,]
        #model['OtherResourceType'] = ''
        #model['OtherUsageDescription'] = ''
        model['PoolID'] = device.path
        #model['PrimaryStatus'] = self.Values.PrimaryStatus.<VAL>
        model['Primordial'] = bool(False)
        model['RemainingManagedSpace'] = pywbem.Uint64(device.freeExtents * device.peSize * 1024)
        #model['Reserved'] = pywbem.Uint64()
        #model['ResourceSubType'] = ''
        #model['ResourceType'] = self.Values.ResourceType.<VAL>
        #model['SpaceLimit'] = pywbem.Uint64()
        #model['SpaceLimitDetermination'] = self.Values.SpaceLimitDetermination.<VAL>
        #model['Status'] = self.Values.Status.<VAL>
        #model['StatusDescriptions'] = ['',]
        #model['ThinProvisionMetaDataSpace'] = pywbem.Uint64()
        model['TotalManagedSpace'] = pywbem.Uint64(device.extents * device.peSize * 1024)
        model['Usage'] = WrappedPool.Values.Usage.Unrestricted
        return model

    def getExtentInstance(self, env, model, device):
        """
            Fill instance of LMI_VGCompositeExtent for given
            LVMVolumeGroupDevices.
        """
        params = self.getParameters(device)
        #model['Access'] = self.Values.Access.<VAL>
        #model['AdditionalAvailability'] = [self.Values.AdditionalAvailability.<VAL>,]
        #model['Availability'] = self.Values.Availability.<VAL>
        #model['AvailableRequestedStates'] = [self.Values.AvailableRequestedStates.<VAL>,]
        model['BlockSize'] = params['BlockSize']
        #model['Caption'] = ''
        #model['ClientSettableUsage'] = [pywbem.Uint16(),]
        #model['CommunicationStatus'] = self.Values.CommunicationStatus.<VAL>
        model['ConsumableBlocks'] = params['ConsumableBlocks']
        #model['DataOrganization'] = self.Values.DataOrganization.<VAL>
        model['DataRedundancy'] = params['DataRedundancyDefault']
        #model['DeltaReservation'] = pywbem.Uint8()
        #model['Description'] = ''
        #model['DetailedStatus'] = self.Values.DetailedStatus.<VAL>
        #model['ElementName'] = ''
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
        model['NumberOfBlocks'] = params['NumberOfBlocks']
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

    def getAllocatedFromInstance(self, env, model, device, base):
        """
            Fill instance of LMI_VGAllocatedFromStoragePool for given
            LVMVolumeGroupDevices.
        """
        # TODO: is there any metadata?
        # Or sum size of underlying PEs ?
        model['SpaceConsumed'] = pywbem.Uint64(device.extents * device.peSize)
        return model

    def getBasedOnInstance(self, env, model, device, base):
        """
            Fill instance of LMI_VGCompositeExtentBasedOn for given
            LVMVolumeGroupDevices.
        """
        try:
            index = device.devices.index(base)
        except ValueError:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, 'Antecedent DeviceID is not associated to Dependent.')
        #model['BlockSize'] = pywbem.Uint64()
        #model['EndingAddress'] = pywbem.Uint64()
        #model['LBAMappingIncludesCheckData'] = bool()
        #model['LBAsMappedByDecrementing'] = bool()
        #model['NumberOfBlocks'] = pywbem.Uint64()
        model['OrderIndex'] = pywbem.Uint16(index+1)
        #model['StartingAddress'] = pywbem.Uint64()
        #model['UnitsBeforeCheckDataInterleave'] = pywbem.Uint64()
        #model['UnitsOfCheckData'] = pywbem.Uint64()
        #model['UnitsOfUserData'] = pywbem.Uint64()
        #model['UserDataStripeDepth'] = pywbem.Uint64()
        return model

    def wrapsDevice(self, device):
        """
            Return True, if given Anaconda device is managed by this wrapper,
            i.e. if it is LVMVolumeGroupDevices.

            :param device: Device to examine.
        """
        if isinstance(device, pyanaconda.storage.devices.LVMVolumeGroupDevice):
            return True
        return False

    def getParameters(self, device):
        devcount = len(device.pvs)
        params = self.calculateCommonBaseParams(device)
        params.update({
                'LMIAllocationType' : pywbem.Uint16(0),
                'NumberOfBlocks': pywbem.Uint64(device.extents),
                'ConsumableBlocks': pywbem.Uint64(device.extents - device.freeExtents),
                'BlockSize': pywbem.Uint64(device.peSize * 1024),
                'Name': device.path,
                'Primordial': False,
                'ExtentStripeLengthDefault': pywbem.Uint16(devcount)
        })
        return params

    def canCreatePool(self, devices, setting, size = None, name = None):
        """
            Check, if the setting are representing volume group.
                        
            :param devices: Array of Anaconda storage devices representing
                 input StoragePools and StorageExtents.
            :param setting: Instance of LMI_StorageSetting.
            :param size: Expected size of the resulting device.
            :param name: Expected name of the resulting device.
            
            The input parameters are taken from
            LMI_StorageConfigurationService.CreateOrModifyStoragePool
        """
        if not setting:
            return 1 # we can create it, but if someone else wants...
        if setting['DataRedundancyGoal'] != 1 or setting['PackageRedundancyGoal'] != 0:
            # Redundant storage is expected - it must be RAID
            return 0
        if not setting.has_key('LMIAllocationType'):
            # VolumeGroups are created by default
            return 1
        if setting['LMIAllocationType'] == DeviceWrapper.ALLOCATION_TYPE_MULTIPLE:
            return 2
        return 0

    def createPool(self, devices, setting, size = None, name = None):
        """
            Create new volume group.
            
            :param devices: Array of Anaconda storage devices representing
                 input StoragePools and StorageExtents.
            :param setting: Instance of LMI_StorageSetting.
            :param size: Expected size of the resulting device.
            :param name: Expected name of the resulting device.

            Return tuple (return_code, device, size), where
            
            # return_code is pywbem error code, e.g.
                pywbem.CIM_ERR_INVALID_PARAMETER.
            # device is created device or None on error.
            # size is size of the created device or, when input size parameter
                was wrong, nearest size of the device that could be created
                from provided devices.
                
        """
        if setting['DataRedundancyGoal'] != 1:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Only DataRedundancyGoal = 1 is supported with LMIAllocationType = Multiple')
        if setting['PackageRedundancyGoal'] != 0:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Only PackageRedundancyGoal = 0 is supported with LMIAllocationType = Multiple')
        if len(devices) < 1:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'At least one device is required for VG.')
        # check sizes
        expectedSize = 0
        for dev in devices:
            expectedSize += dev.partedDevice.sectorSize * dev.partedDevice.length
        if size and size != expectedSize:
            return (self.CREATE_POOL_SIZE_NOT_SUPPORTED, None, expectedSize)
        
        # Create lvmpv format on the devices (i.e. mark them as PhysicalVolumes)
        for dev in devices:
            fmt = pyanaconda.storage.formats.getFormat('lvmpv')
            action = pyanaconda.storage.deviceaction.ActionCreateFormat(dev, fmt)
            storage.devicetree.registerAction(action)
            action.execute()
            storage.devicetree._actions = []
        
        # Create the VG
        if name:
            vg = storage.newVG(pvs=devices, name=name)
        else:
            vg = storage.newVG(pvs=devices)
        action = pyanaconda.storage.deviceaction.ActionCreateDevice(vg)
        storage.devicetree.registerAction(action)
        action.execute()
        storage.devicetree._actions = []
        
        element = self.getPoolName(vg)
        return (self.CREATE_POOL_COMPLETED, element, expectedSize)

    def createLogicalDisk(self, device, setting, size, name = None):
        """
            Allocate a LogicalVolume from a pool represented by given
            Anaconda device.
            
            :param setting: Instance of LMI_StorageSetting.
            :param device: Anaconda storage device, representing the pool to
                allocate from. The pool is managed by this wrapper.
            :param size: Expected size of the resulting LogicalDisk.
            :param name: Expected name of the resulting LogicalDisk.
            
            Return tuple (return_code, element, size), where
            
            # return_code is DeviceWrapper.CREATE_DISK_*
            # element is CIMInstanceName of created LogicalDisk or None on
                error.
            # size is size of the created LogicalDisk or, when input size
                parameter was wrong, the nearest size of the device that could
                be created from provided pool.

            The input parameters are taken from
            LMI_StorageConfigurationService.CreateOrModifyElementFromStoragePool

        """

        if setting and setting['DataRedundancyGoal'] != 1:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Only DataRedundancyGoal = 1 is supported with VGStoragePool')
        if setting and setting['PackageRedundancyGoal'] != 0:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Only PackageRedundancyGoal = 0 is supported with VGStoragePool')
        if not size:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Size must be specified.')

        if name:
            lv = storage.newLV(vg=device, name=name, size=size/(1024*1024))
        else:
            lv = storage.newLV(vg=device, size=size/(1024*1024))
        action = pyanaconda.storage.deviceaction.ActionCreateDevice(lv)
        storage.devicetree.registerAction(action)
        action.execute()
        storage.devicetree._actions = []
        
        wrapper = wrapperManager.getWrapperForDevice(lv)
        element = wrapper.getExtentName(lv)
        # TODO: calculate size
        return (self.CREATE_DISK_COMPLETED_OK, element, size)
