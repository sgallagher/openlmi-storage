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

class BaseProvider(CIMProvider2):
    """
        CIM Provider for LMI. It adds access to ProviderManager, configuration
        and pyanaconda.storage.Storage instance.

        In addition to CIM provider methods, this class and its subclasses
        can convert CIM InstanceName to Anaconda's StorageDevice instance
        and a vice versa.
    """
    def __init__(self, env, storage, config, manager, setting_manager):
        """
            Initialize the provider.
            Store reference to pyanaconda.storage.Storage.
            Store reference to StorageConfiguration.
            Register at given ProviderManager.
        """
        super(BaseProvider, self).__init__()
        self.storage = storage
        self.config = config
        self.manager = manager
        self.setting_manager = setting_manager
        self.logger = env.get_logger()
        
