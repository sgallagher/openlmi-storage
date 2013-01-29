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
    This module is the main entry from openlmi.storage.CIMOM.
    
    All initialization must be done here.
    
    This module instantiates all providers and registers them in CIMOM.
"""

from pyanaconda import anaconda_log
anaconda_log.init()

from openlmi.storage.StorageConfiguration import StorageConfiguration
from openlmi.storage.ProviderManager import ProviderManager
from openlmi.storage.SettingManager import SettingManager

from openlmi.storage.LMI_StorageExtent import LMI_StorageExtent
from openlmi.storage.LMI_MDRAIDStorageExtent import LMI_MDRAIDStorageExtent
from openlmi.storage.LMI_DiskPartition import LMI_DiskPartition
from openlmi.storage.LMI_GenericDiskPartition import LMI_GenericDiskPartition
from openlmi.storage.LMI_LVStorageExtent import LMI_LVStorageExtent
from openlmi.storage.LMI_VGStoragePool import LMI_VGStoragePool
from openlmi.storage.LMI_PartitionBasedOn import LMI_PartitionBasedOn
from openlmi.storage.LMI_MDRAIDBasedOn import LMI_MDRAIDBasedOn
from openlmi.storage.LMI_LVBasedOn import LMI_LVBasedOn
from openlmi.storage.LMI_LVAllocatedFromStoragePool \
        import LMI_LVAllocatedFromStoragePool
from openlmi.storage.LMI_VGAssociatedComponentExtent \
        import LMI_VGAssociatedComponentExtent
from openlmi.storage.LMI_DiskPartitionConfigurationSetting \
        import LMI_DiskPartitionConfigurationSetting
from openlmi.storage.SettingProvider \
        import ElementSettingDataProvider, SettingHelperProvider
from openlmi.storage.LMI_DiskPartitioningConfigurationService \
        import LMI_DiskPartitionConfigurationService
from openlmi.storage.LMI_HostedStorageService \
        import LMI_HostedStorageService
from openlmi.storage.LMI_DiskPartitionConfigurationCapabilities \
        import LMI_DiskPartitionConfigurationCapabilities
from openlmi.storage.CapabilitiesProvider import ElementCapabilitiesProvider
from openlmi.storage.LMI_InstalledPartitionTable \
        import LMI_InstalledPartitionTable
from openlmi.storage.LMI_LVStorageCapabilities \
        import LMI_LVStorageCapabilities, LMI_LVElementCapabilities
from openlmi.storage.LMI_StorageConfigurationService \
        import LMI_StorageConfigurationService
from openlmi.storage.LMI_VGStorageCapabilities import LMI_VGStorageCapabilities
from openlmi.storage.LMI_MDRAIDStorageCapabilities \
        import LMI_MDRAIDStorageCapabilities
from openlmi.storage.LMI_SystemStorageDevice import LMI_SystemStorageDevice
from openlmi.storage.LMI_MDRAIDFormatProvider import LMI_MDRAIDFormatProvider
from openlmi.storage.LMI_PVFormatProvider import LMI_PVFormatProvider
from openlmi.storage.LMI_DataFormatProvider import LMI_DataFormatProvider
from openlmi.storage.FormatProvider import LMI_ResidesOnExtent

import openlmi.storage.cmpi_logging as cmpi_logging
import pyanaconda.storage
import pyanaconda.platform
import os

def init_anaconda():
    """ Initialize Anaconda storage module."""
    cmpi_logging.logger.info("Initializing Anaconda")

    os.system('udevadm control --env=ANACONDA=1')
    os.system('udevadm trigger --subsystem-match block')
    os.system('udevadm settle')

    # hack to insert RAID modules
    for module in ('raid0', 'raid1', 'raid5', 'raid10'):
        os.system('modprobe ' + module)

    # set up storage class instance
    # ugly hack to make it working on both F17 and F18
    try:
        # pylint: disable-msg=E1121
        platform = pyanaconda.platform.getPlatform(None)
    except TypeError:
        # pylint: disable-msg=E1120
        platform = pyanaconda.platform.getPlatform()
    storage = pyanaconda.storage.Storage(platform=platform)

    # identify the system's storage devices
    storage.devicetree.populate()

    return storage

def get_providers(env):
    """
        Called by CIMOM. Initialize OpenLMI and return dictionary of all
        providers we implement.
    """
    # allow **magic here
    # pylint: disable-msg=W0142
    log_manager = cmpi_logging.LogManager(env)

    config = StorageConfiguration()
    config.load()
    log_manager.set_config(config)

    manager = ProviderManager()
    setting_manager = SettingManager(config)
    setting_manager.load()
    storage = init_anaconda()

    providers = {}

    # common construction options
    opts = {'storage': storage,
            'config': config,
            'provider_manager': manager,
            'setting_manager': setting_manager}
    # StorageDevice providers
    provider = LMI_StorageExtent(**opts)
    manager.add_device_provider(provider)
    providers['LMI_StorageExtent'] = provider

    provider = LMI_MDRAIDStorageExtent(**opts)
    manager.add_device_provider(provider)
    providers['LMI_MDRAIDStorageExtent'] = provider
    setting_provider = SettingHelperProvider(
            setting_helper=provider,
            setting_classname="LMI_MDRAIDStorageSetting",
            **opts)
    manager.add_setting_provider(setting_provider)
    providers['LMI_MDRAIDStorageSetting'] = setting_provider
    assoc_provider = ElementSettingDataProvider(
            setting_provider=setting_provider,
            managed_element_classname="LMI_MDRAIDStorageExtent",
            setting_data_classname="LMI_MDRAIDStorageSetting",
            **opts)
    providers['LMI_MDRAIDElementSettingData'] = assoc_provider

    provider = LMI_DiskPartition(**opts)
    manager.add_device_provider(provider)
    providers['LMI_DiskPartition'] = provider

    provider = LMI_GenericDiskPartition(**opts)
    manager.add_device_provider(provider)
    providers['LMI_GenericDiskPartition'] = provider

    provider = LMI_LVStorageExtent(**opts)
    manager.add_device_provider(provider)
    providers['LMI_LVStorageExtent'] = provider
    setting_provider = SettingHelperProvider(
            setting_helper=provider,
            setting_classname="LMI_LVStorageSetting",
            **opts)
    manager.add_setting_provider(setting_provider)
    providers['LMI_LVStorageSetting'] = setting_provider
    assoc_provider = ElementSettingDataProvider(
            setting_provider=setting_provider,
            managed_element_classname="LMI_LVStorageExtent",
            setting_data_classname="LMI_LVStorageSetting",
            **opts)
    providers['LMI_LVElementSettingData'] = assoc_provider

    provider = LMI_VGStoragePool(**opts)
    manager.add_device_provider(provider)
    providers['LMI_VGStoragePool'] = provider
    setting_provider = SettingHelperProvider(
            setting_helper=provider,
            setting_classname="LMI_VGStorageSetting",
            **opts)
    manager.add_setting_provider(setting_provider)
    providers['LMI_VGStorageSetting'] = setting_provider
    assoc_provider = ElementSettingDataProvider(
            setting_provider=setting_provider,
            managed_element_classname="LMI_VGStoragePool",
            setting_data_classname="LMI_VGStorageSetting",
            **opts)
    providers['LMI_VGElementSettingData'] = assoc_provider
    cap_provider = LMI_LVStorageCapabilities(**opts)
    manager.add_capabilities_provider(cap_provider)
    providers['LMI_LVStorageCapabilities'] = cap_provider
    assoc_provider = LMI_LVElementCapabilities(
            "LMI_LVElementCapabilities",
            cap_provider, provider, **opts)
    providers['LMI_LVElementCapabilities'] = assoc_provider

    # settings
    setting_provider = LMI_DiskPartitionConfigurationSetting(
            ** opts)
    manager.add_setting_provider(setting_provider)
    providers['LMI_DiskPartitionConfigurationSetting'] = setting_provider
    assoc_provider = ElementSettingDataProvider(
            setting_provider=setting_provider,
            managed_element_classname="CIM_DiskPartition",
            setting_data_classname="LMI_DiskPartitionConfigurationSetting",
            **opts)
    providers['LMI_DiskPartitionElementSettingData'] = assoc_provider


    # services & capabilities
    service_provider = LMI_StorageConfigurationService(**opts)
    manager.add_service_provider(service_provider)
    providers['LMI_StorageConfigurationService'] = service_provider
    cap_provider = LMI_VGStorageCapabilities(**opts)
    manager.add_capabilities_provider(cap_provider)
    providers['LMI_VGStorageCapabilities'] = cap_provider
    assoc_provider = ElementCapabilitiesProvider(
            "LMI_VGElementCapabilities",
            cap_provider, service_provider, **opts)
    providers['LMI_VGElementCapabilities'] = assoc_provider

    cap_provider = LMI_MDRAIDStorageCapabilities(**opts)
    manager.add_capabilities_provider(cap_provider)
    providers['LMI_MDRAIDStorageCapabilities'] = cap_provider
    assoc_provider = ElementCapabilitiesProvider(
            "LMI_MDRAIDElementCapabilities",
            cap_provider, service_provider, **opts)
    providers['LMI_MDRAIDElementCapabilities'] = assoc_provider


    service_provider = LMI_DiskPartitionConfigurationService(
            ** opts)

    manager.add_service_provider(service_provider)
    providers['LMI_DiskPartitionConfigurationService'] = service_provider

    cap_provider = LMI_DiskPartitionConfigurationCapabilities(
            ** opts)
    manager.add_capabilities_provider(cap_provider)
    providers['LMI_DiskPartitionConfigurationCapabilities'] = cap_provider
    assoc_provider = ElementCapabilitiesProvider(
            "LMI_DiskPartitionElementCapabilities",
            cap_provider, service_provider, **opts)
    providers['LMI_DiskPartitionElementCapabilities'] = assoc_provider


    # Associations
    provider = LMI_PartitionBasedOn(**opts)
    providers['LMI_PartitionBasedOn'] = provider

    provider = LMI_MDRAIDBasedOn(**opts)
    providers['LMI_MDRAIDBasedOn'] = provider

    provider = LMI_LVBasedOn(**opts)
    providers['LMI_LVBasedOn'] = provider

    provider = LMI_LVAllocatedFromStoragePool(**opts)
    providers['LMI_LVAllocatedFromStoragePool'] = provider

    provider = LMI_VGAssociatedComponentExtent(**opts)
    providers['LMI_VGAssociatedComponentExtent'] = provider

    provider = LMI_HostedStorageService(**opts)
    providers['LMI_HostedStorageService'] = provider

    provider = LMI_SystemStorageDevice(**opts)
    providers['LMI_SystemStorageDevice'] = provider

    provider = LMI_InstalledPartitionTable(**opts)
    providers['LMI_InstalledPartitionTable'] = provider

    fmt = LMI_DataFormatProvider(**opts)
    manager.add_format_provider(fmt)
    providers['LMI_DataFormat'] = fmt

    fmt = LMI_MDRAIDFormatProvider(**opts)
    manager.add_format_provider(fmt)
    providers['LMI_MDRAIDFormat'] = fmt

    fmt = LMI_PVFormatProvider(**opts)
    manager.add_format_provider(fmt)
    providers['LMI_PVFormat'] = fmt

    provider = LMI_ResidesOnExtent(**opts)
    providers['LMI_ResidesOnExtent'] = provider

    print "providers:", providers

    return providers

