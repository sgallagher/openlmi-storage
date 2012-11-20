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
from LMI_StorageExtent import LMI_StorageExtent

import pyanaconda.storage
import pyanaconda.platform
import os

def initAnaconda(env):
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
    
    storage = initAnaconda(env)
    
    providers = {}
    p = LMI_StorageExtent(env, storage = storage, config = config, manager = manager)
    manager.addProvider(p)
    providers['LMI_StorageExtent'] = p
    
    print "providers:", providers
    
    return providers

    