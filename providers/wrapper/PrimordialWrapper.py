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
from DeviceWrapper import DeviceWrapper
from WrappedExtent import WrappedExtent
import pyanaconda.storage.devices
import pywbem

class PrimordialWrapper(DeviceWrapper):
    """
        Wrapper for primordial deivces, i.e. in our implementation all
        Anaconda torage.devices.PartitionDevices.

        This wrapper is special, there is only one StoragePool for all
        these primordial devices, therefore more methods than usual
        need to be overriden.

        For each Anaconda PartitionDevices, following CIM instances are
        created:

        - one LMI_PartitionExtent with LMI_AssociatedPrimordialExtent
          association to its LMI_PrimordialPool
        - one LMI_PartitionExtentBasedOnPartition associations to underlying
          DiskPartition (see :doc:`smis-partitions` for details).

        There is no (StoragePool)AllocatedFrom(StoragePool) association, because
        the primordial pool is the base bool and is not allocated from any pool.

        There is only one instance of LMI_PrimordialPool and
        LMI_PrimordialStorageCapabilities, connected together with
        LMI_PrimordialStorageElementCapabilities association.

        In case there is no partition on the system, an instance of the
        primordial pool must still exist. Therefore special device
        wrapperManager.PRIMORDIAL_POOL_DEVICE is used instead of Anaconda's
        PartitionDevice instance.
    """

    def __init__(self):
        super(PrimordialWrapper, self).__init__('Primordial')

    @property
    def extentClassName(self):
        """
            CIM class name of device's CIM_StorageExtent class.

            The default name is not suitable, this wrapper creates
            LMI_PartitionExtent instances.
        """
        return 'LMI_PartitionExtent'

    @property
    def basedOnClassName(self):
        """
            CIM class name of device's CIM_BasedOn class.

            The default name is not suitable, this wrapper creates
            LMI_PartitionExtentBasedOnPartition instances.
        """
        return 'LMI_PartitionExtentBasedOnPartition'

    @property
    def associatedExtentClassName(self):
        """
            CIM class name of device's CIM_AssociatedComponentExtent class.

            The default name is not suitable, this wrapper creates
            LMI_AssociatedPrimordialExtent instances.
        """
        return 'LMI_AssociatedPrimordialExtent'

    def getPoolId(self, device):
        """
            Return LMI_PrimordialPool.InstanceID for given Anaconda device.

            :param device: Concrete Anaconda storage device, whose InstanceID
                should be returned.

            There is only one primordial pool for all devices, therefore this
            method is overridden.
        """
        return self.prefix + ':Pool:'

    def enumDevices(self):
        """
            Enumerate all primordial devices, i.e. all Anaconda PartitionDevice
            instances.
        """
        for part in storage.partitions:
            yield part

    def enumBaseDevices(self, device):
        """
            Enumerate all Anaconda base devices which are parents of given
            PartitionDevice.

            The primordial pool is not allocated from any other pool, so return
            empty array of base devices so
            (StoragePool)AllocatedFrom(StoragePool) instances won't be created.

            Please notice that enumBasedOns method is overriden in this wrapper,
            therefore LMI_PartitionExtentBasedOnPartition instances will be
            created.

            :param device: Anaconda PartitionDevice to get list of
                parent devices from.
        """
        return []

    def enumPools(self,  env, model, keys_only):
        """
            Enumerate all LMI_PrimordialPools.

            There is only one pool for whole system, therefore only one
            CIMInstance is returned.
        """
        model.update(self.getPoolName(wrapperManager.PRIMORDIAL_POOL_DEVICE).keybindings)
        if keys_only:
            yield model
        else:
            yield self.getPoolInstance(env, model, wrapperManager.PRIMORDIAL_POOL_DEVICE)

    def getPoolInstance(self, env, model, device):
        """
            Fill instance of LMI_PrimordialPool. There is one instance for whole
            system, so we ignore the device parameter.
        """
        # Compute managed space
        total = 0
        remaining = 0
        for part in storage.partitions:
            size = part.partedDevice.sectorSize * part.partedDevice.length
            total += size
            if not (logicalDiskManager.isUsed(part) or logicalDiskManager.isExposed(part)):
                remaining += size

        #model['AllocationUnits'] = ''
        #model['Capacity'] = pywbem.Uint64()
        #model['CapacityInMigratingSource'] = pywbem.Uint64()
        #model['CapacityInMigratingTarget'] = pywbem.Uint64()
        #model['Caption'] = ''
        #model['ClientSettableUsage'] = [pywbem.Uint16(),]
        #model['CommunicationStatus'] = self.Values.CommunicationStatus.<VAL>
        model['ConsumedResourceUnits'] = ''
        #model['CurrentlyConsumedResource'] = pywbem.Uint64()
        #model['Description'] = ''
        #model['DetailedStatus'] = self.Values.DetailedStatus.<VAL>
        #model['ElementName'] = ''
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
        model['PoolID'] = 'PrimordialPool'
        #model['PrimaryStatus'] = self.Values.PrimaryStatus.<VAL>
        model['Primordial'] = True
        model['RemainingManagedSpace'] = pywbem.Uint64(remaining)
        #model['Reserved'] = pywbem.Uint64()
        #model['ResourceSubType'] = ''
        #model['ResourceType'] = self.Values.ResourceType.<VAL>
        #model['SpaceLimit'] = pywbem.Uint64()
        #model['SpaceLimitDetermination'] = self.Values.SpaceLimitDetermination.<VAL>
        #model['Status'] = self.Values.Status.<VAL>
        #model['StatusDescriptions'] = ['',]
        #model['ThinProvisionMetaDataSpace'] = pywbem.Uint64()
        model['TotalManagedSpace'] = pywbem.Uint64(total)
        #model['Usage'] = self.Values.Usage.<VAL>
        return model

    def getExtentInstance(self, env, model, device):
        """
            Fill instance of LMI_PartitionExtent for given Anaconda
            PartitionDevice.
        """
        #model['Access'] = self.Values.Access.<VAL>
        #model['AdditionalAvailability'] = [self.Values.AdditionalAvailability.<VAL>,]
        #model['Availability'] = self.Values.Availability.<VAL>
        #model['AvailableRequestedStates'] = [self.Values.AvailableRequestedStates.<VAL>,]
        model['BlockSize'] = pywbem.Uint64(device.partedDevice.sectorSize)
        #model['Caption'] = ''
        #model['ClientSettableUsage'] = [pywbem.Uint16(),]
        #model['CommunicationStatus'] = self.Values.CommunicationStatus.<VAL>
        #model['ConsumableBlocks'] = pywbem.Uint64()
        #model['DataOrganization'] = self.Values.DataOrganization.<VAL>
        #model['DataRedundancy'] = pywbem.Uint16()
        #model['DeltaReservation'] = pywbem.Uint8()
        #model['Description'] = ''
        #model['DetailedStatus'] = self.Values.DetailedStatus.<VAL>
        #model['ElementName'] = ''
        model['EnabledDefault'] = WrappedExtent.Values.EnabledDefault.Enabled
        model['EnabledState'] = WrappedExtent.Values.EnabledState.Enabled
        #model['ErrorCleared'] = bool()
        #model['ErrorDescription'] = ''
        #model['ErrorMethodology'] = ''
        #model['ExtentDiscriminator'] = ['',]
        #model['ExtentInterleaveDepth'] = pywbem.Uint64()
        #model['ExtentStatus'] = [self.Values.ExtentStatus.<VAL>,]
        #model['ExtentStripeLength'] = pywbem.Uint64()
        #model['Generation'] = pywbem.Uint64()
        #model['HealthState'] = self.Values.HealthState.<VAL>
        #model['IdentifyingDescriptions'] = ['',]
        #model['InstallDate'] = pywbem.CIMDateTime()
        #model['InstanceID'] = ''
        #model['IsBasedOnUnderlyingRedundancy'] = bool()
        model['IsComposite'] = False
        #model['IsConcatenated'] = bool()
        #model['LastErrorCode'] = pywbem.Uint32()
        #model['LocationIndicator'] = self.Values.LocationIndicator.<VAL>
        #model['MaxQuiesceTime'] = pywbem.Uint64()
        model['Name'] = device.path
        model['NameFormat'] = WrappedExtent.Values.NameFormat.OS_Device_Name
        model['NameNamespace'] = WrappedExtent.Values.NameNamespace.OS_Device_Namespace
        model['NoSinglePointOfFailure'] = False
        model['NumberOfBlocks'] = pywbem.Uint64(device.partedPartition.getLength())
        #model['NumExtentsMigrating'] = pywbem.Uint64()
        #model['OperatingStatus'] = self.Values.OperatingStatus.<VAL>
        model['OperationalStatus'] = [WrappedExtent.Values.OperationalStatus.OK]
        #model['OtherEnabledState'] = ''
        #model['OtherIdentifyingInfo'] = ['',]
        #model['OtherNameFormat'] = ''
        #model['OtherNameNamespace'] = ''
        #model['OtherUsageDescription'] = ''
        #model['PackageRedundancy'] = pywbem.Uint16()
        #model['PowerManagementCapabilities'] = [self.Values.PowerManagementCapabilities.<VAL>,]
        #model['PowerManagementSupported'] = bool()
        #model['PowerOnHours'] = pywbem.Uint64()
        #model['PrimaryStatus'] = self.Values.PrimaryStatus.<VAL>
        model['Primordial'] = False # TODO: really ??
        #model['Purpose'] = ''
        model['RequestedState'] = WrappedExtent.Values.RequestedState.Not_Applicable
        #model['SequentialAccess'] = bool()
        #model['Status'] = self.Values.Status.<VAL>
        #model['StatusDescriptions'] = ['',]
        #model['StatusInfo'] = self.Values.StatusInfo.<VAL>
        #model['ThinlyProvisioned'] = bool(False)
        #model['TimeOfLastStateChange'] = pywbem.CIMDateTime()
        #model['TotalPowerOnHours'] = pywbem.Uint64()
        model['TransitioningToState'] = WrappedExtent.Values.TransitioningToState.Not_Applicable
        #model['Usage'] = self.Values.Usage.<VAL>
        return model

    def getAllocatedFromInstance(self, env, model, device, base):
        return model

    def enumBasedOns(self, env, model, keys_only):
        """
            Enumerate LMI_PartitionExtentBasedOnPartition instances. The default
            implementation would try to connect LMI_PartitionExtents with their
            base devices, but since the base device (LMI_DiskPartition) is not
            managed by any wrapper, the default won't help here and we must
            enumerate the instances manually.

            Upcall to CIMOM is used to get all LMI_DiskPartition instances.
        """
        # won't help here and special one is  needed
        ch = env.get_cimom_handle()
        # find all partitions on the system starting with 'Cura'
        partitions = ch.EnumerateInstanceNames(ns = LMI_NAMESPACE, cn='CIM_GenericDiskPartition')
        for partition in partitions:
            if not partition['CreationClassName'].startswith('Cura'):
                continue

            model['Dependent'] = pywbem.CIMInstanceName(classname='LMI_PartitionExtent',
                    namespace=LMI_NAMESPACE,
                    keybindings={'CreationClassName': 'LMI_PartitionExtent',
                                 'DeviceID': partition['DeviceID'],
                                 'SystemCreationClassName': LMI_SYSTEM_CLASS_NAME,
                                 'SystemName': LMI_SYSTEM_NAME
                    })
            model['Antecedent'] = partition
            yield model

    def getBasedOnInstance(self, env, model, device, base):
        """
            Fill instance of LMI_PartitionExtentBasedOnPartition instance for
            given Anaconda PartitionDevice.
        """
        return model

    def getCapabilitiesId(self, device):
        """
            Return LMI_PrimordialStorageCapabilities.InstanceID for given
            PartitionDevice.

            :param device: PartitionDevice, whose InstanceID
                should be returned.

            There is only one primordial pool for all devices, therefore this
            method is overridden and ignores it's parameter.
        """
        return self.prefix + ':Caps:'

    def enumCapabilities(self, env, model, keys_only):
        """
            Enumerate all LMI_PrimordialStorageCapabilities.

            There is only one pool for whole system, therefore only one
            CIMInstance is returned.
        """
        model.update(self.getCapabilitiesName(wrapperManager.PRIMORDIAL_POOL_DEVICE).keybindings)
        if keys_only:
            yield model
        else:
            yield self.getCapabilitiesInstance(env, model, wrapperManager.PRIMORDIAL_POOL_DEVICE)

    def enumElementCapabilities(self, env, model, keys_only):
        """
            Enumerate all LMI_PrimordialStorageElementCapabilities.

            There is only one pool for whole system, therefore only one
            CIMInstance is returned.
        """
        model['ManagedElement'] = self.getPoolName(wrapperManager.PRIMORDIAL_POOL_DEVICE)
        model['Capabilities'] = self.getCapabilitiesName(wrapperManager.PRIMORDIAL_POOL_DEVICE)
        yield model

    def wrapsDevice(self, device):
        """
            Return True, if given Anaconda device is managed by this wrapper,
            i.e. if it is PartitionDevice.

            :param device: Device to examine.
        """
        if isinstance(device, pyanaconda.storage.devices.PartitionDevice):
            return True
        if device == wrapperManager.PRIMORDIAL_POOL_DEVICE:
            return True
        return False

    def getParameters(self, device):
        """
            Return hash of properties to be added to StorageCapabilities or
            StorageSettings or StorageExtent.
        """
        params = {}
        if device != wrapperManager.PRIMORDIAL_POOL_DEVICE:
            params = super(PrimordialWrapper, self).getParameters(device)
        
        count = len(storage.partitions)
        params.update({
                'DataRedundancyMin': pywbem.Uint16(1),
                'DataRedundancyMax': pywbem.Uint16(count),
                'DataRedundancyDefault': pywbem.Uint16(1),
                'PackageRedundancyMin':  pywbem.Uint16(0),
                'PackageRedundancyMax':  pywbem.Uint16(count-1),
                'PackageRedundancyDefault':  pywbem.Uint16(0),
                'NoSinglePointOfFailure': True,
                'NoSinglePointOfFailureDefault': False,
                'IsBasedOnUnderlyingRedundancy': False,
                'ExtentStripeLengthDefault': pywbem.Uint16(1),
                'Primordial' : True
        })
        return params

    def getDevice(self, instanceName):
        """
            Return Anaconda PartitionDevice for given CIMInstanceName.

            We need different method that the DeviceMapper - there can be pools
            without any extents in it, i,e, this method can return
            WrapperManager.PRIMORDIAL_POOL_DEVICE instead of PartitionDevice
            instance.

            :param instanceName: CIMInstanceName of instance to find.
        """
        classname = instanceName.classname
        path = None
        if classname == self.poolClassName or classname == self.capabilitiesClassName:
            try:
                (prefix, infix, path) = instanceName['InstanceID'].split(':')
            except ValueError:
                return None
            if prefix != self.prefix:
                return None
            if classname == self.poolClassName and infix != 'Pool':
                return None
            if classname == self.capabilitiesClassName and infix != 'Caps':
                return None
            if path != '':
                return None
            return wrapperManager.PRIMORDIAL_POOL_DEVICE
        elif classname == self.extentClassName:
            path = instanceName['DeviceID']
            if (instanceName['SystemName'] != LMI_SYSTEM_NAME or
                    instanceName['SystemCreationClassName'] !=LMI_SYSTEM_CLASS_NAME or
                    instanceName['CreationClassName'] != self.extentClassName):
                return None
            return storage.devicetree.getDeviceByPath(path)
        elif classname == self.associatedExtentClassName:
            group = instanceName['GroupComponent']
            part = instanceName['PartComponent']
            groupDevice = self.getDevice(group)
            partDevice = self.getDevice(part)
            if groupDevice != wrapperManager.PRIMORDIAL_POOL_DEVICE:
                return None
            if not self.wrapsDevice(partDevice):
                return None
            return partDevice
        elif classname == self.allocatedFromClassName:
            return None # this pool is not alocated from anything
        elif classname == self.basedOnClassName:
            extent = instanceName['Dependent']
            base = instanceName['Antecedent']
            device = self.getDevice(extent)
            if not self.wrapsDevice(device):
                return None
            return (device, device)
        elif classname == self.elementCapabilitiesClassName:
            managed = instanceName['ManagedElement']
            capabilities = instanceName['Capabilities']
            mdev = self.getDevice(managed)
            cdev = self.getDevice(capabilities)
            if mdev == cdev:
                return mdev
            return None # Managed and Capabilities do not match
        else:
            return None # unsupported classname
        return None # device not found

    def canCreatePool(self, devices, setting, size = None, name = None):
        """
            Check, if this PrimordialWrapper is able to create new pool, i.e.
            new Anaconda storage device, from given devices, setting, size
            and name.
            
            PrimordialWrapper devices are created by
            LMI_PartitionConfigurationService, not by
            StorageConfigurationService.
        """
        return 0

    def createLogicalDisk(self, device, setting, size, name = None):
        """
            Allocate LMI_LogicalDisk from the primordial pool.
            
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
        if not name is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, 'ElementName is not supported for allocation fron this pool.')
        # check the settings
        if not size:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, 'Size must be specified in this pool.')
        if setting:            
            if setting.get('DataRedundancyMin',1) > 1:
                 raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Wrong Goal: DataRedundancy must be 1 in this pool.') 
            if setting.get('ExtentStripeLengthMin',1) > 1:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Wrong Goal: ExtentStripeLengthMin must be 1 in this pool.')
            if setting.get('NoSinglePointOfFailure',False):
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Wrong Goal: NoSinglePointOfFailure must be False in this pool.')
            if setting.get('PackageRedundancyMin',0):
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Wrong Goal: PackageRedundancyMin must be 0 in this pool.')
        
        nearestSize = 0
        theElement = None
        # try to find the element and also the size of nearest available partition
        for part in storage.partitions:
            if logicalDiskManager.isExposed(part) or logicalDiskManager.isUsed(part):
                continue
            deviceSize = part.partedDevice.length * part.partedDevice.sectorSize
            if deviceSize == size:
                theElement = part
                nearestSize = size
                print 'Candidate device:', part.path
                break
            
            if abs(deviceSize - size) < abs(nearestSize - size):
                nearestSize = abs(deviceSize - size)

        if not theElement:
            if nearestSize>0:
                return (self.CREATE_DISK_SIZE_NOT_SUPPORTED, None, nearestSize)
            else:
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, 'No free space in the pool.')
        
        logicalDiskManager.setExpose(theElement, True)
        element = pywbem.CIMInstanceName(classname='LMI_LogicalDisk', namespace=LMI_NAMESPACE,
                    keybindings = {"SystemName" : LMI_SYSTEM_NAME,
                        "SystemCreationClassName" : LMI_SYSTEM_CLASS_NAME,
                        "CreationClassName" : 'LMI_LogicalDisk',
                        "DeviceID" : device.path
                    }) 
        return (self.CREATE_DISK_COMPLETED_OK, element, size)

    def destroyPool(self, device):
        """
            The primordial pool cannot be destroyed.
            
            :param device: The device to destroy.
        """
        raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Cannot destroy primordial Pool.')

