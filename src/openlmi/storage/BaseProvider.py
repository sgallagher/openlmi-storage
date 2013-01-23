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

from pywbem.cim_provider2 import CIMProvider2
import openlmi.storage.cmpi_logging as cmpi_logging

class BaseProvider(CIMProvider2):
    """
        CIM Provider for LMI. It adds access to ProviderManager, configuration
        and pyanaconda.storage.Storage instance.

        In addition to CIM provider methods, this class and its subclasses
        can convert CIM InstanceName to Anaconda's StorageDevice instance
        and a vice versa.
    """
    @cmpi_logging.trace_method
    def __init__(self, storage, config, provider_manager, setting_manager,
            *args, **kwargs):
        """
            Initialize the provider.
            Store reference to pyanaconda.storage.Storage.
            Store reference to StorageConfiguration.
            Register at given ProviderManager.
        """
        super(BaseProvider, self).__init__(*args, **kwargs)
        self.storage = storage
        self.config = config
        self.provider_manager = provider_manager
        self.setting_manager = setting_manager

