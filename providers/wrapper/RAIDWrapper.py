# Cura Storage Provider
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

class RAIDWrapper(DeviceWrapper):
    """
        Wrapper for Anaconda MD RAID devices, i.e.
        pyanaconda.storage.devices.MDRaidArrayDevice.

        This class can be taken as example of DeviceWrapper implementation.

        For each Anaconda MDRaidArrayDevice, following CIM instances are
        created:

        - one Cura_RAIDPool
        - one Cura_RAIDCompositeExtent with Cura_AssociatedRAIDComponentExtent
          association to its Cura_RaidPool
        - one Cura_RAIDStorageCapabilities with
          Cura_RAIDStorageElementCapabilities association to Cura_RaidPool
        - one or more Cura_RAIDCompositeExtentBasedOn associations to all RAID
          members.
        - one or more Cura_RAIDAllocatedFromStoragePool associations to all RAID
          members.
    """

    def __init__(self):
        super(RAIDWrapper, self).__init__('RAID')

    @property
    def extentClassName(self):
        """
            CIM class name of device's CIM_StorageExtent class.

            This property is overriden to have Cura_RAIDCompositeExtent as name of
            RAID's StorageExtent class. Vanilla DeviceWrapper would provide
            Cura_RAIDExtent.
        """
        return 'Cura_' + self.prefix + 'CompositeExtent'

    @property
    def basedOnClassName(self):
        """
            CIM class name of device's CIM_BasedOn class.

            This property is overriden to have Cura_RAIDCompositeExtentBasedOn as
            name of RAID's BasedOn class. Vanilla DeviceWrapper would provide
            Cura_RAIDExtentBasedOn.
        """
        return 'Cura_' + self.prefix + 'CompositeExtentBasedOn'

    def enumDevices(self):
        """
            Enumerate all MDRaidArrayDevices  known to Anaconda. StorageExtent,
            StoragePool and StorageCapabilities and all necessary associations
            will be created for each of them.
        """
        for array in storage.mdarrays:
            yield array

    def enumBaseDevices(self, device):
        """
            Enumerate parent devices of given Anaconda MDRaidArrayDevice.
            BasedOn and AllocatedFrom association will be created to each of them.

            :param device: Instance of MDRaidArrayDevice, whose parent devices
                (i.e. RAID members) should be returned.
        """
        for base in device.devices:
            yield base

    def getPoolInstance(self, env, model, device):
        """
            Fill instance of Cura_RAIDPool for given MDRaidArrayDevice.
        """
        if device.partedDevice:
            size = device.partedDevice.length * device.partedDevice.sectorSize
        else:
            size = None

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
        model['ElementName'] = device.path
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
        if logicalDiskManager.isExposed(device) or logicalDiskManager.isUsed(device):
            model['RemainingManagedSpace'] = pywbem.Uint64(0)
        else:
            if size:
                model['RemainingManagedSpace'] = pywbem.Uint64(size)
            else:
                model['RemainingManagedSpace'] = pywbem.Uint64(0)
        #model['Reserved'] = pywbem.Uint64()
        #model['ResourceSubType'] = ''
        #model['ResourceType'] = self.Values.ResourceType.<VAL>
        #model['SpaceLimit'] = pywbem.Uint64()
        #model['SpaceLimitDetermination'] = self.Values.SpaceLimitDetermination.<VAL>
        #model['Status'] = self.Values.Status.<VAL>
        #model['StatusDescriptions'] = ['',]
        #model['ThinProvisionMetaDataSpace'] = pywbem.Uint64()
        if size:
            model['TotalManagedSpace'] = pywbem.Uint64(size)
        model['Usage'] = WrappedPool.Values.Usage.Unrestricted
        return model

    def getExtentInstance(self, env, model, device):
        """
            Fill instance of Cura_RAIDCompositeExtent for given
            MDRaidArrayDevice.
        """
        params = self.getParameters(device)
        print "device:", device, ":",params, "\n\n\n"
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

    def getAllocatedFromInstance(self, env, model, device, base):
        """
            Fill instance of Cura_RAIDAllocatedFromStoragePool for given
            MDRaidArrayDevice.
        """
        model['SpaceConsumed'] = pywbem.Uint64(device.partedDevice.sectorSize * device.partedDevice.length)
        return model

    def getBasedOnInstance(self, env, model, device, base):
        """
            Fill instance of Cura_RAIDCompositeExtentBasedOn for given
            MDRaidArrayDevice.
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
        #model['UserDataStripeDepth'] = pywbem.Uint64() # TODO - missing support in Anaconda
        return model

    def wrapsDevice(self, device):
        """
            Return True, if given Anaconda device is managed by this wrapper,
            i.e. if it is MDRaidArrayDevice.

            :param device: Device to examine.
        """
        if isinstance(device, pyanaconda.storage.devices.MDRaidArrayDevice):
            return True
        return False

    def getParameters(self, device):
        """
            Return capabilities of given MDRaidArrayDevice.

            :param device: MDRaidArrayDevice to examine.
        """
        devcount = len(device.parents)
        
        params = self.calculateCommonBaseParams(device)
        params.update(super(RAIDWrapper, self).getParameters(device))
        
        devcount = len(device.devices)
        if device.level == 0:
            params.update({
                'ExtentStripeLengthDefault': pywbem.Uint16(devcount),
                'CuraAllocationType' : pywbem.Uint16(1),
        })
        elif device.level == 1:
            # RAID1
            # - DataRedundancy = sum of underlying DataRedundancy
            # - PackageRedundancy = how many devices can fail = all underlying
            #   devices but one can fail
            params['DataRedundancyMin'] = pywbem.Uint16(0)
            params['DataRedundancyMax'] = pywbem.Uint16(0)
            params['DataRedundancyDefault'] = pywbem.Uint16(0)
            params['PackageRedundancyMin'] = pywbem.Uint16(0)
            params['PackageRedundancyMax'] = pywbem.Uint16(0)
            params['PackageRedundancyDefault'] = pywbem.Uint16(0)
            params['ExtentStripeLengthDefault'] = pywbem.Uint16(0)
            for base in device.parents:
                baseWrapper = wrapperManager.getWrapperForDevice(base)
                baseParams = baseWrapper.getParameters(base)
                params['DataRedundancyMin'] = pywbem.Uint16(params['DataRedundancyMin'] + baseParams['DataRedundancyDefault'])
                params['DataRedundancyMax'] = pywbem.Uint16(params['DataRedundancyMax'] + baseParams['DataRedundancyDefault'])
                params['DataRedundancyDefault'] = pywbem.Uint16(params['DataRedundancyDefault'] + baseParams['DataRedundancyDefault'])
                params['PackageRedundancyMin'] = pywbem.Uint16(params['PackageRedundancyMin'] + baseParams['PackageRedundancyDefault'] + 1)
                params['PackageRedundancyMax'] = pywbem.Uint16(params['PackageRedundancyMax'] + baseParams['PackageRedundancyDefault'] + 1)
                params['PackageRedundancyDefault'] = pywbem.Uint16(params['PackageRedundancyDefault'] + baseParams['PackageRedundancyDefault'] + 1)
                params['ExtentStripeLengthDefault'] =  pywbem.Uint16(params['ExtentStripeLengthDefault'] + baseParams['ExtentStripeLengthDefault'])
            params['PackageRedundancyMin'] = pywbem.Uint16(params['PackageRedundancyMin'] - 1)
            params['PackageRedundancyMax'] = pywbem.Uint16(params['PackageRedundancyMax'] - 1)
            params['PackageRedundancyDefault'] = pywbem.Uint16(params['PackageRedundancyDefault'] - 1)
            
            params.update({
                'NoSinglePointOfFailure': True,
                'NoSinglePointOfFailureDefault': True,
                'IsBasedOnUnderlyingRedundancy': True,
            })
            
        elif device.level == 5:
            # - DataRedundancy = lowest DataRedundancy
            # - PackageRedundancy = how many devices can fail = one component
            #   can fail, i.e. the one with lowest PackageRedundancy can fail
            params['DataRedundancyMin'] = pywbem.Uint16(65535)
            params['DataRedundancyMax'] = pywbem.Uint16(65535)
            params['DataRedundancyDefault'] = pywbem.Uint16(65535)
            params['PackageRedundancyMin'] = pywbem.Uint16(65535)
            params['PackageRedundancyMax'] = pywbem.Uint16(65535)
            params['PackageRedundancyDefault'] = pywbem.Uint16(65535)
            params['ExtentStripeLengthDefault'] = pywbem.Uint16(65535)
            for base in device.partents:
                baseWrapper = wrapperManager.getWrapperForDevice(base)
                baseParams = baseWrapper.getParameters(base)
                params['DataRedundancyMin'] = pywbem.Uint16(min(baseParams['DataRedundancyDefault'], params['DataRedundancyMin']))
                params['DataRedundancyMax'] = pywbem.Uint16(min(baseParams['DataRedundancyDefault'], params['DataRedundancyMax']))
                params['DataRedundancyDefault'] = pywbem.Uint16(min(baseParams['DataRedundancyDefault'], params['DataRedundancyDefault']))
                params['PackageRedundancyMin'] = pywbem.Uint16(min(baseParams['PackageRedundancyDefault']+1, params['PackageRedundancyMin']))
                params['PackageRedundancyMax'] = pywbem.Uint16(min(baseParams['PackageRedundancyDefault']+1, params['PackageRedundancyMax']))
                params['PackageRedundancyDefault'] = pywbem.Uint16(min(baseParams['PackageRedundancyDefault']+1, params['PackageRedundancyDefault']))
                params['ExtentStripeLengthDefault'] =  pywbem.Uint16(params['ExtentStripeLengthDefault'] + baseParams['ExtentStripeLengthDefault'])
            params.update({
                'NoSinglePointOfFailure': True,
                'NoSinglePointOfFailureDefault': True,
                'IsBasedOnUnderlyingRedundancy': True,
                'CuraAllocationType' : pywbem.Uint16(1),
            })
        return params

    def canCreatePool(self, devices, setting, size = None, name = None):
        """
            Check, if the setting are representing RAID device.
                        
            :param devices: Array of Anaconda storage devices representing
                 input StoragePools and StorageExtents.
            :param setting: Instance of Cura_StorageSetting.
            :param size: Expected size of the resulting device.
            :param name: Expected name of the resulting device.
            
            The input parameters are taken from
            Cura_StorageConfigurationService.CreateOrModifyStoragePool
        """
        if not setting:
            # VolumeGroups are created by default
            return 0
        if setting['DataRedundancyGoal'] > 1 or setting['PackageRedundancyGoal'] > 0:
            # Redundant storage is expected - it must be RAID
            return 2
        if not setting.has_key('CuraAllocationType'):
            # VolumeGroups are created by default
            return 0
        if setting['CuraAllocationType'] == DeviceWrapper.ALLOCATION_TYPE_ONE:
            return 2
        return 0

    RAID0 = 'raid0'
    RAID1 = 'raid1'
    RAID5 = 'raid5'

    def createPool(self, devices, setting, size = None, name = None):
        """
            Create new RAID device
            
            :param devices: Array of Anaconda storage devices representing
                 input StoragePools and StorageExtents.
            :param setting: Instance of Cura_StorageSetting.
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
        if name:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'ElementName is not supported for RAID.')

        datar = setting['DataRedundancyGoal']
        pkgr = setting['PackageRedundancyGoal']

        #TODO: check (or remove ExtentStripeLength)
        if datar == 1 and pkgr == 0:
            raidType = self.RAID0
        elif datar == len(devices) and pkgr == len(devices)-1:
            raidType = self.RAID1
        elif datar == 1 and pkgr == 1:
            raidType = self.RAID5
        else:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Cannot find create pool for given settings - PackageRedundancy and DataRedundancy do not match any supported combination.')

        # check sizes
        if raidType == self.RAID0:
            expectedSize = 0
            for dev in devices:
                expectedSize += dev.partedDevice.sectorSize * dev.partedDevice.length
        else: # RAID 1 and 5
            expectedSize = devices[0].partedDevice.sectorSize * devices[0].partedDevice.length
            for dev in devices:
                thisSize = dev.partedDevice.sectorSize * dev.partedDevice.length
                if expectedSize != thisSize:
                    print 'expected:', expectedSize, 'this:', thisSize, 'dev:', dev.path
                    raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'All members of RAID1 or RAID5 must have the same size.')
            if raidType == self.RAID5:
                expectedSize = expectedSize * (len(devices)-1)
        if size and size != expectedSize:
            return (self.CREATE_POOL_SIZE_NOT_SUPPORTED, None, expectedSize)
        
        # create it
        md = storage.newMDArray(level=raidType, parents=devices, memberDevices=len(devices), totalDevices=len(devices))
        action = pyanaconda.storage.deviceaction.ActionCreateDevice(md)
        storage.devicetree.registerAction(action)
        action.execute()
        storage.devicetree._actions = []
        
        element = self.getPoolName(md)
        return (self.CREATE_POOL_COMPLETED, element, expectedSize)


