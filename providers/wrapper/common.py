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

"""
 Cura common definitions and constants
"""

import socket
import os
import cPickle
import pywbem

from pyanaconda import anaconda_log
anaconda_log.init()

import pyanaconda.storage
import pyanaconda.platform

CURA_SYSTEM_CLASS_NAME='Linux_ComputerSystem'
CURA_SYSTEM_NAME=socket.getfqdn()
CURA_NAMESPACE='root/cimv2'

__all__ = ['initAnaconda', 'WrapperManager', 'wrapperManager', 'storage', 'CURA_SYSTEM_CLASS_NAME', 'CURA_SYSTEM_NAME', 'CURA_NAMESPACE', 'storage', 'curaConfig', 'settingManager', 'logicalDiskManager', 'initAnaconda']

def initAnaconda(forceReload = False):
    """ (Re-)load Anaconda storage, i.e. re-scan local storage devices.
        'storage' global variable gets new content.
    """

    if not hasattr(initAnaconda, 'initialized') or forceReload:
        print 'Reloading Anaconda'
        pyanaconda.anaconda_log.init()
        # hack to make LVM visible to Anaconda
        os.system('udevadm control --env=ANACONDA=1')
        os.system('udevadm trigger --subsystem-match block')
        os.system('udevadm settle')
        
        # hack to insert RAID modules
        for module in ('raid0', 'raid1', 'raid5', 'raid10'):
            os.system('modprobe ' + module)

        platform = pyanaconda.platform.getPlatform()
        newStorage = pyanaconda.storage.Storage(platform=platform)
        newStorage.devicetree.populate()
        global storage
        storage = newStorage

        # hack to re-create MD arrays, lost during populate()
        # see bug #817064
        for array in storage.mdarrays:
            array.setup()
        initAnaconda.initialized = True


##############################################################################
# WrapperManager
##############################################################################

class WrapperManager(object):
    """ Collection of all DeviceWrappers.
        It can return a DeviceWrapper for given Anaconda device,
        CIMInstance or CIMInstanceName, or wrapper prefix.
        All DeviceWrappers must add themselves to WrapperManager using
        addWrapper().
    """
    PRIMORDIAL_POOL_DEVICE = "1" 
    
    def __init__(self):
        self.wrappers = []
        
    def addWrapper(self, wrapper):
        """ Add a wrapper to the manager.""" 
        self.wrappers.append(wrapper)
        
    def getWrapperForInstance(self, instanceName):
        """ For CIMInstanceName return its DeviceWrapper. """
        className = instanceName.classname
        for w in self.wrappers:
            if (className == w.poolClassName
                    or className == w.extentClassName
                    or className == w.associatedExtentClassName
                    or className == w.allocatedFromClassName
                    or className == w.capabilitiesClassName
                    or className == w.basedOnClassName):
                return w
        return None
    
    def getWrapperForPrefix(self, prefix):
        """ For given prefix return its DeviceManager. """
        for w in self.wrappers:
            if w.prefix == prefix:
                return w
        return None
    
    def getWrapperForDevice(self, device):
        """ For Anaconda device return its wrapper."""
        for w in self.wrappers:
            if w.wrapsDevice(device):
                return w
        return None
    
    def getDevice(self, instanceName):
        """ For CIMInstanceName return anaconda device (or None).
            This is shortcut for
            wrapperManager.getWrapperForInstance(device).getDevice(device).
            Beware, for primordial pools/settings etc. it may return PRIMORDIAL_POOL_DEVICE.
        """
        wrapper = self.getWrapperForInstance(instanceName)
        if wrapper:
            return wrapper.getDevice(instanceName)
        return None
        
    def createPool(self, devices, setting, size = None, name = None):
        """
            Create a StroagePool, i.e. new Anaconda device, for given setting.
            
            This method just finds the best DeviceWrapper for the setting and
            calls its createPool method, which does the real job.
            
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
                
            The input parameters are taken from
            Cura_StorageConfigurationService.CreateOrModifyStoragePool
        """
        highest = None
        highestScore = 0
        for wrapper in self.wrappers:
            score = wrapper.canCreatePool(devices, setting, size, name)
            if score > highestScore:
                highest = wrapper
        if highest:
            return highest.createPool(devices, setting, size, name)
        raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Cannot create any pool for given Cura_StorageSetting.')


##############################################################################
# CuraConfig
##############################################################################

class CuraConfig(object):
    """ 
        Persistent configuration of Cura.
        Data are stored in CONFIG_FILE. Data are automatically written on each
        set() call.
    """
    
    CONFIG_FILE = '/var/lib/storage-mgmt/cura.cfg'
    
    # list of config options
    CONFIG_EXPOSED_DISKS = 'exposed'
    CONFIG_PERSISTENT_SETTINGS = 'persistent-settings'
    
    def __init__(self):
        """
            Initialize and load new configuration from CONFIG_FILE.
        """
        self.config = {}
        self.loadConfig()

    def get(self, key, defaultValue):
        """
            Get configuration option.
            
            ;param key: Name of the option.
            :param defaultValue: Default value of the option.
        """
        return self.config.get(key, defaultValue)
    
    def set(self, key, value):
        """
            Set configuration option. The configuration file is immediately
            saved.
            
            ;param key: Name of the option.
            :param value: New value of the option.
        """
        self.config[key] = value
        # let's assume that 'set' is called only occasionally
        self.writeConfig()
    
    def loadConfig(self):
        """
            Load the configuration from CONFIG_FILE. This method should
            not be called directly, configuration is automatically loaded
            during __init__().
        """
        if os.path.isfile(self.CONFIG_FILE):
            f = open(self.CONFIG_FILE, 'r')
            self.config = cPickle.load(f)
            f.close()
        else:
            self.config = {}

    def writeConfig(self):
        """
            Write the configuration to CONFIG_FILE. This method should
            not be called directly, configuration is  automatically saved on
            set() method call.
        """
        # Create new directory for the config file, if needed                 
        d = os.path.dirname(self.CONFIG_FILE)
        if not os.path.isdir(d):
            print 'Creating', d
            os.mkdir(d)
            
        f = open(self.CONFIG_FILE, 'w')
        cPickle.dump(self.config, f)
        f.close()


##############################################################################
# LogicalDiskManager
##############################################################################

class LogicalDiskManager(object):
    """ 
        Collection of exposed LogicalDisks.
        Admin can allocate LogicalDisk from any leaf StorageExtent, i.e. when no
        StorageExtent is based on it.
        Leaf StorageExtents with filesystems have implicitly a LogicalDisk
        associated.
        The list of exposed LogicalDisks is saved in provided configuration.
    """
        
    def __init__(self, config):
        """
            Create new list and load it from given CuraConfig instance.
            
            :param config: CuraConfig to load/save list of instances from/to.
        """
        self.exposedDisks = []
        self.config = config
        
    def isUsed(self, device):
        """
            Tell if the Anaconda device is used by something (e.g. by LVM on it).
            This does *not* cover filesystems!
        """
        return not device.isleaf

    def setExpose(self, device, status):
        """
            Allocate LogicalDisk from given Anaconda device (if status == True).
            Remove LogicalDisk for given Anaconda device if status == False.
            This allocation/removal is persistent, i.e. Cura remembers it in
            its configuration file.
        """
        exposed = self.config.get(CuraConfig.CONFIG_EXPOSED_DISKS, [])
        if status:
            if not device.path in exposed:
                exposed.append(device.path)
        else:
            if device.path in exposed:
                exposed.remove(device.path)
        self.config.set(CuraConfig.CONFIG_EXPOSED_DISKS, exposed)
         
    def isExposed(self, device):
        """
            Tell if the Anaconda device is exposed, i.e. LogicalDisk is
            allocated from it either using SMI-S, i.e. setExpose(), or there
            is a filesystem on it.
        """
        exposed = self.config.get(CuraConfig.CONFIG_EXPOSED_DISKS, [])
        if device.path in exposed:
            if self.isUsed(device):
                # used device cannot be exposed!
                self.setExpose(device, False)
                return False
            else:
                return True

        if self.isUsed(device):
            return False

        # all devices with filesystems are exposed
        if device.format.type != None and isinstance(device.format, pyanaconda.storage.formats.fs.FS):
            return True
        return False



##############################################################################
# SettingManager
##############################################################################

class SettingManager(object):
    """ Collection of StoreageSettings, both persistent and temporary. """
    SETTING_CHANGEABLE_PERSISTENT = 2 # see DMTF documentation of CIM_StorageSetting
    staticSettings = [
            {
                    'Caption' : 'RAID0',
                    'ChangeableType' : pywbem.Uint16(0),
                    'DataRedundancyGoal': pywbem.Uint16(1),
                    'DataRedundancyMax': pywbem.Uint16(1),
                    'DataRedundancyMin': pywbem.Uint16(1),
                    'NoSinglePointOfFailure': False,
                    'PackageRedundancyGoal': pywbem.Uint16(0),
                    'PackageRedundancyMax': pywbem.Uint16(0),
                    'PackageRedundancyMin': pywbem.Uint16(0),
                    'Description': 'Setting for RAID0 with unlimited number of underlying StorageExtents.',
                    'ElementName': 'STATIC:RAID0',
                    'InstanceID': 'STATIC:RAID0',
                    'CuraAllocationType': pywbem.Uint16(1)
            },
            {
                    'Caption' : 'RAID1 for 2 disks',
                    'ChangeableType' : pywbem.Uint16(0),
                    'DataRedundancyGoal': pywbem.Uint16(2),
                    'DataRedundancyMax': pywbem.Uint16(2),
                    'DataRedundancyMin': pywbem.Uint16(2),
                    'NoSinglePointOfFailure': True,
                    'PackageRedundancyGoal': pywbem.Uint16(1),
                    'PackageRedundancyMax': pywbem.Uint16(1),
                    'PackageRedundancyMin': pywbem.Uint16(1),
                    'Description': 'Setting for RAID1 with two disks.',
                    'ElementName': 'STATIC:RAID1',
                    'InstanceID': 'STATIC:RAID1',
                    'CuraAllocationType': pywbem.Uint16(1)
            },
            {
                    'Caption' : 'RAID5 for 3 disks',
                    'ChangeableType' : pywbem.Uint16(0),
                    'DataRedundancyGoal': pywbem.Uint16(1),
                    'DataRedundancyMax': pywbem.Uint16(1),
                    'DataRedundancyMin': pywbem.Uint16(1),
                    'NoSinglePointOfFailure': True,
                    'PackageRedundancyGoal': pywbem.Uint16(1),
                    'PackageRedundancyMax': pywbem.Uint16(1),
                    'PackageRedundancyMin': pywbem.Uint16(1),
                    'Description': 'Setting for RAID5 with three disks.',
                    'ElementName': 'STATIC:RAID5',
                    'InstanceID': 'STATIC:RAID5',
                    'CuraAllocationType': pywbem.Uint16(1)
            },
            {
                    'Caption' : 'Volume Group',
                    'ChangeableType' : pywbem.Uint16(0),
                    'DataRedundancyGoal': pywbem.Uint16(1),
                    'DataRedundancyMax': pywbem.Uint16(1),
                    'DataRedundancyMin': pywbem.Uint16(1),
                    'NoSinglePointOfFailure': False,
                    'PackageRedundancyGoal': pywbem.Uint16(0),
                    'PackageRedundancyMax': pywbem.Uint16(0),
                    'PackageRedundancyMin': pywbem.Uint16(0),
                    'Description': 'Setting for Volume Group.',
                    'ElementName': 'STATIC:VG',
                    'InstanceID': 'STATIC:VG',
                    'CuraAllocationType': pywbem.Uint16(0)
            }
    ]
    
    def __init__(self, myCuraConfig):
        self.settings = {}
        
        # prevent writeConfig writing anything, we don't want
        # setSetting to write anything.
        self.config = None
        
        # add persistent settings
        persistentSettings = myCuraConfig.get(CuraConfig.CONFIG_PERSISTENT_SETTINGS, {})
        for s in persistentSettings.values():
            self.setSetting(s)
        # add static settings
        for s in self.staticSettings:
            self.setSetting(s)

        # now restore writeConfig functionality            
        self.config = myCuraConfig
            
        self.reserevedId = []
        self.lastId = 1
       

    def setSetting(self, setting):
        """ Change a setting. If the setting is persistent, it's written
            immediately to config file.
        """
        instanceId = setting['InstanceID']
        self.settings[instanceId] = setting
        self.writeConfig()

    def getSetting(self, instanceId):
        """ Return setting with given ID or None if it does not exist.
        """
        return self.settings.get(instanceId, None)

    def enumerateSettings(self):
        """ Return generator of all settings.
        """
        return self.settings.itervalues()

    def getSettingName(self, setting):
        """ Return CIMInstanceName for given setting.
        """
        return pywbem.CIMInstanceName(classname='Cura_StorageSetting',
                        namespace = CURA_NAMESPACE,
                        keybindings = {
                                'InstanceID' : setting['InstanceID'],
                        })

    def removeSetting(self, setting):
        """ Remove given setting. If the setting was persistent, it's
            immediately removed from the config file.
        """
        instanceId = setting['InstanceID']
        del self.settings[instanceId]
        self.writeConfig()
    
    def writeConfig(self):
        if self.config is None:
            return
        # store persistent settings
        persistent = {}
        for s in self.enumerateSettings():
            if s['ChangeableType'] == self.SETTING_CHANGEABLE_PERSISTENT:
                instanceId = s['InstanceID']
                persistent[instanceId] = s
        self.config.set(CuraConfig.CONFIG_PERSISTENT_SETTINGS, persistent)
    
    def generateId(self):
        """ Return free InstanceID. This ID is reserved and won't be returned by
            subsequent call to this function.
        """
        i = self.lastId
        while self.settings.has_key(str(i)) and (i in self.reserevedId):
            i = i + 1
        self.reserevedId.append(i)
        return str(i)

# global objects
curaConfig = CuraConfig()
wrapperManager = WrapperManager()
settingManager = SettingManager(curaConfig)
logicalDiskManager = LogicalDiskManager(curaConfig)

storage = None
initAnaconda()
