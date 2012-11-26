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


"""
    This module is the main entry from CIMOM.
    
    All initialization must be done here.
    
    This module instantiates all providers and registers them in CIMOM.
"""

from pyanaconda import anaconda_log
anaconda_log.init()

from StorageConfiguration import StorageConfiguration
from ProviderManager import ProviderManager
from SettingManager import SettingManager

from LMI_StorageExtent import LMI_StorageExtent
from LMI_MDRAIDStorageExtent import LMI_MDRAIDStorageExtent 
from LMI_DiskPartition import LMI_DiskPartition
from LMI_GenericDiskPartition import LMI_GenericDiskPartition
from LMI_LVStorageExtent import LMI_LVStorageExtent
from LMI_VGStoragePool import LMI_VGStoragePool
from LMI_PartitionBasedOn import LMI_PartitionBasedOn
from LMI_MDRAIDBasedOn import LMI_MDRAIDBasedOn
from LMI_LVBasedOn import LMI_LVBasedOn
from LMI_LVAllocatedFromStoragePool import LMI_LVAllocatedFromStoragePool
from LMI_VGAssociatedComponentExtent import LMI_VGAssociatedComponentExtent
from LMI_DiskPartitionConfigurationSetting import LMI_DiskPartitionConfigurationSetting

import pyanaconda.storage
import pyanaconda.platform
import os

def init_anaconda(env):
    logger = env.get_logger()
    
    logger.log_info("Initializing Anaconda")   
    
    os.system('udevadm control --env=ANACONDA=1')
    os.system('udevadm trigger --subsystem-match block')
    os.system('udevadm settle')

    # hack to insert RAID modules
    for module in ('raid0', 'raid1', 'raid5', 'raid10'):
        os.system('modprobe ' + module)

    # set up storage class instance
    platform = pyanaconda.platform.getPlatform()
    storage = pyanaconda.storage.Storage(platform=platform)

    # identify the system's storage devices
    storage.devicetree.populate()
        
    return storage
  
def get_providers(env):
    config = StorageConfiguration()
    config.load()
    
    manager = ProviderManager()
    setting_manager = SettingManager(config)
    setting_manager.load()
    storage = init_anaconda(env)
    
    providers = {}
    
    # common construction options
    opts = {'env': env,
            'storage': storage,
            'config': config,
            'manager': manager,
            'setting_manager': setting_manager}    
    # StorageDevice providers
    p = LMI_StorageExtent(**opts)
    manager.add_provider(p)
    providers['LMI_StorageExtent'] = p

    p = LMI_MDRAIDStorageExtent(**opts)
    manager.add_provider(p)
    providers['LMI_MDRAIDStorageExtent'] = p

    p = LMI_DiskPartition(**opts)
    manager.add_provider(p)
    providers['LMI_DiskPartition'] = p
    
    p = LMI_GenericDiskPartition(**opts)
    manager.add_provider(p)
    providers['LMI_GenericDiskPartition'] = p

    p = LMI_LVStorageExtent(**opts)
    manager.add_provider(p)
    providers['LMI_LVStorageExtent'] = p

    p = LMI_VGStoragePool(**opts)
    manager.add_provider(p)
    providers['LMI_VGStoragePool'] = p

    # settings
    p = LMI_DiskPartitionConfigurationSetting(**opts)
    providers['LMI_DiskPartitionConfigurationSetting'] = p

    # Associations
    p = LMI_PartitionBasedOn(**opts)
    providers['LMI_PartitionBasedOn'] = p

    p = LMI_MDRAIDBasedOn(**opts)
    providers['LMI_MDRAIDBasedOn'] = p

    p = LMI_LVBasedOn(**opts)
    providers['LMI_LVBasedOn'] = p

    p = LMI_LVAllocatedFromStoragePool(**opts)
    providers['LMI_LVAllocatedFromStoragePool'] = p
    
    p = LMI_VGAssociatedComponentExtent(**opts)
    providers['LMI_VGAssociatedComponentExtent'] = p


    print "providers:", providers
    
    return providers

    