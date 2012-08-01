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
  CIM Provider base module. This module handles *all* wrapped classes.
"""

from wrapper.common import *
from wrapper.WrappedAllocatedFromStoragePool import WrappedAllocatedFromStoragePool
from wrapper.WrappedExtent import WrappedExtent
from wrapper.WrappedExtentBasedOn import WrappedExtentBasedOn
from wrapper.WrappedPool import WrappedPool
from wrapper.WrappedStorageCapabilities import WrappedStorageCapabilities
from wrapper.WrappedStorageElementCapabilities import WrappedStorageElementCapabilities
from wrapper.WrappedAssociatedComponentExtent import WrappedAssociatedComponentExtent
from wrapper.RAIDWrapper import RAIDWrapper
from wrapper.PrimordialWrapper import PrimordialWrapper
from wrapper.VGWrapper import VGWrapper
from wrapper.LVWrapper import LVWrapper

initialized = False

# initialize (= create and register) all wrappers
def initialize():
    global initialized
    
    if initialized:
        return
    
    wrappers = [RAIDWrapper(),
            PrimordialWrapper(),
            VGWrapper(),
            LVWrapper()]
    for wrapper in wrappers:
            wrapperManager.addWrapper(wrapper)
            
    initialized = True
    
# wrapper -> dictionary for get_providers
def add_providers(env, wrapper):
    cura_raidallocatedfromstoragepool_prov = WrappedAllocatedFromStoragePool(env, wrapper)
    cura_raidcompositeextent_prov = WrappedExtent(env, wrapper)  
    cura_raidcompositeextentbasedon_prov = WrappedExtentBasedOn(env, wrapper)  
    cura_raidpool_prov = WrappedPool(env, wrapper)  
    cura_raidstoragecapabilities_prov = WrappedStorageCapabilities(env, wrapper)  
    cura_raidstorageelementcapabilities_prov = WrappedStorageElementCapabilities(env, wrapper)  
    cura_associatedraidcomponentextent_prov = WrappedAssociatedComponentExtent(env, wrapper)
    return{
            wrapper.allocatedFromClassName: cura_raidallocatedfromstoragepool_prov,
            wrapper.extentClassName: cura_raidcompositeextent_prov,
            wrapper.basedOnClassName: cura_raidcompositeextentbasedon_prov,
            wrapper.poolClassName: cura_raidpool_prov,
            wrapper.capabilitiesClassName: cura_raidstoragecapabilities_prov,
            wrapper.elementCapabilitiesClassName: cura_raidstorageelementcapabilities_prov,
            wrapper.associatedExtentClassName: cura_associatedraidcomponentextent_prov
    }

# cmpi-bindings function to get all providers in this module
def get_providers(env):
    initAnaconda(False)
    
    provs = {}
    
    initialize()
    wrappers = [wrapperManager.getWrapperForPrefix('RAID'),
                wrapperManager.getWrapperForPrefix('VG'),
                wrapperManager.getWrapperForPrefix('LV'),
                wrapperManager.getWrapperForPrefix('Primordial')]
    for wrapper in wrappers:
        provs.update(add_providers(env, wrapper))
    return provs
