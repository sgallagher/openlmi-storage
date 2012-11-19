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
import os
import socket

class StorageConfiguration(ConfigParser.SafeConfigParser):
    
    CONFIG_FILE = '/var/lib/openlmi-storage/storage.ini'
    
    defaults = {
        'namespace' : 'root/cimv2',
        'systemclassname' : 'Linux_ComputerSystem'
    }
    def __init__(self, *args, **kwargs):
        ConfigParser.SafeConfigParser.__init__(self, defaults=self.defaults, *args, **kwargs)
        
    def load(self):
        """
            Load configuration from CONFIG_FILE. Create default, if the file
            does not exist.
        """
        if os.path.isfile(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, 'wb') as configfile:
                self.write(configfile)
        if not self.has_section('common'):
            self.add_section('common')
        
    def save(self):
        """
            Save configuration to CONFIG_FILE. Create a directory for it if it
            does not exist.
        """
        d = os.path.dirname(self.CONFIG_FILE)
        if not os.path.isdir(d):
            os.mkdir(d)
        
        with open(self.CONFIG_FILE, 'wb') as configfile:
            self.write(configfile)

    def getNamespace(self):
        return self.get('common', 'namespace')
    namespace = property(getNamespace)
    
    def getSystemClassName(self):
        return self.get('common', 'systemclassname')
    systemClassName = property(getSystemClassName)
    
    def getSystemName(self):
        return socket.getfqdn()
    systemName = property(getSystemName)
