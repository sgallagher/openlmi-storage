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

import ConfigParser
import socket
import cmpi_logging

class StorageConfiguration(object):
    """
        OpenLMI configuration file. By default, it resides in
        /etc/opelmi/storage/storage.ini.
        
        There should be only one instance of this class.
    """

    CONFIG_PATH = '/etc/openlmi/storage/'
    CONFIG_FILE = CONFIG_PATH + 'storage.ini'

    PERSISTENT_PATH = '/var/lib/openlmi-storage/'
    SETTINGS_DIR = 'settings/'

    defaults = {
        'namespace' : 'root/cimv2',
        'systemclassname' : 'Linux_ComputerSystem'
    }

    @cmpi_logging.trace
    def __init__(self):
        """ Initialize and load a configuration file."""
        self.config = ConfigParser.SafeConfigParser(defaults=self.defaults)
        self.load()

    @cmpi_logging.trace
    def load(self):
        """
            Load configuration from CONFIG_FILE. The file does not need to
            exist.
        """
        self.config.read(self.CONFIG_FILE)
        if not self.config.has_section('common'):
            self.config.add_section('common')

    @cmpi_logging.trace
    def get_namespace(self):
        """ Return namespace of OpenLMI storage provider."""
        return self.config.get('common', 'namespace')
    namespace = property(get_namespace)

    @cmpi_logging.trace
    def get_system_class_name(self):
        """ Return SystemClassName of OpenLMI storage provider."""
        return self.config.get('common', 'systemclassname')
    system_class_name = property(get_system_class_name)

    @cmpi_logging.trace
    def get_system_name(self):
        """ Return SystemName of OpenLMI storage provider."""
        return socket.getfqdn()
    system_name = property(get_system_name)
