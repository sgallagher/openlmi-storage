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

import os
import ConfigParser

class SettingManager(object):
    """
        Class, which manages all persistent, transient and preconfigured
        LMI_*Setting instances.
        
        Note: LMI_*Setting instances, which represent actual configuration
        of some element are *not* managed by this class!
        
        It should be enough to have only one instance of this class.
        
        Settings must be removed using special methods of this class.
        
        Preconfigured settings are stored in /etc/openlmi/storage/setting/
        directory. Each LMI_*Setting class has its own file. Name of the
        file is the same as name of the class.
        Each file has ini structure. Each section represents one LMI_*Setting
        instance, with key=value pairs. Name of the ini section is the same
        as InstanceID of the setting.
        
        Persistent settings have the same structure, but they are stored in
        /var/lib/openlmi-storage/settings/ directory.
    """

    def __init__(self, storage_configuration):
        """
            Create new SettingManager.
        """
        # hash classname -> settings
        #   settings = hash setting_id -> Setting
        self.classes = {}
        self.config = storage_configuration
        # hash classname -> last generated unique ID (integer)
        self.ids = {}

    def get_settings(self, classname):
        """
            Return dictionary of all instances of given LMI_*Setting class.
        """
        if not self.classes.has_key(classname):
            self.classes[classname] = {}
        return self.classes[classname]

    def clean(self):
        """
            Remove all persistent and preconfigured settings, leaving
            only transient ones.
        """
        for c in self.classes.values():
            for setting in c.values():
                if (setting.type == Setting.TYPE_PERSISTENT
                        or setting.type == Setting.TYPE_PRECONFIGURED):
                    del(c[setting.id])

    def load(self):
        """
            Load all persistent and preconfigured settings from configuration
            files.
        """
        self.clean()

        # open all preconfigured config files
        self._loadDirectory(self.config.CONFIG_PATH
                    + self.config.SETTINGS_DIR, Setting.TYPE_PRECONFIGURED)
        self._loadDirectory(self.config.PERSISTENT_PATH
                    + self.config.SETTINGS_DIR, Setting.TYPE_PERSISTENT)

    def _loadDirectory(self, directory, setting_type):
        if not os.path.isdir(directory):
            return

        for classname in os.listdir(directory):
            ini = ConfigParser.SafeConfigParser()
            ini.optionxform = str # don't convert to lowercase
            ini.read(directory + classname)
            for sid in ini.sections():
                setting = Setting(setting_type, sid)
                setting.load(ini)
                self._setSetting(classname, setting)

    def _setSetting(self, classname, setting):
        if self.classes.has_key(classname):
            s = self.classes[classname]
            s[setting.id] = setting
        else:
            self.classes[classname] = { setting.id : setting}

    def set_setting(self, classname, setting):
        """
            Add or set setting. If the setting is (or was) persistent, it will
            be immediately stored to disk.
        """
        was_persistent = False
        settings = self.classes.get(classname, None)
        if settings:
            old_setting = settings.get(setting.id, None)
            if old_setting and old_setting.type == Setting.TYPE_PERSISTENT:
                was_persistent = True

        self._setSetting(classname, setting)
        if setting.type == Setting.TYPE_PERSISTENT or was_persistent:
            self._saveClass(classname)

    def delete_setting(self, classname, setting):
        """
            Remove a setting. If the setting was persistent, it will
            be immediately removed from disk.
        """
        settings = self.classes.get(classname, None)
        if settings:
            old_setting = settings.get(setting.id, None)
            if old_setting:
                del(settings[setting.id])
                if old_setting.type == Setting.TYPE_PERSISTENT:
                    self._saveClass(classname)

    def save(self):
        """
            Save all persistent settings to configuration files.
            Create the persistent directory if it does not exist.
        """
        for classname in self.classes.keys():
            self._saveClass(classname)

    def _saveClass(self, classname):
        ini = ConfigParser.SafeConfigParser()
        ini.optionxform = str # don't convert to lowercase
        for setting in self.classes[classname].values():
            if setting.type != Setting.TYPE_PERSISTENT:
                continue
            setting.save(ini)

        finaldir = self.config.PERSISTENT_PATH + self.config.SETTINGS_DIR
        if not os.path.isdir(finaldir):
            os.makedirs(finaldir)
        with open(finaldir + classname, 'w') as configfile:
            ini.write(configfile)

    def allocate_id(self, classname):
        """
            Return new unique InstanceID for given LMI_*Setting class.
        """
        if not self.ids.has_key(classname):
            self.ids[classname] = 1

        i = self.ids[classname]
        settings = self.get_settings(classname)
        while settings.has_key("LMI:" + classname + ":" + str(i)):
            i = i + 1

        self.ids[classname] = i + 1
        return "LMI:" + classname + ":" + str(i)


class Setting(object):
    """
        This class represents generic LMI_*Setting properties.
        Every instance has name, type and properties (key-value pairs).
        The value must be string!
    """

    # setting with ChangeableType = Persistent
    TYPE_PERSISTENT = 1
    # setting with ChangeableType = Transient
    TYPE_TRANSIENT = 2
    # setting with ChangeableType = Fixed, preconfigured by system admin
    TYPE_PRECONFIGURED = 3
    # setting with ChangeableType = Fixed, current configuration of real
    # managed element, usually associated to it
    TYPE_CONFIGURATION = 4

    def __init__(self, setting_type=None, setting_id=None):
        self.type = setting_type
        self.id = setting_id
        self.properties = {}

    def load(self, config):
        """
            Load setting with self.id from given ini file
            (ConfigParser instance).
        """
        self.properties = {}
        for (key, value) in config.items(self.id):
            if value == "":
                value = None
            self.properties[key] = value



    def save(self, config):
        """
            Save setting with self.id to given ini file
            (ConfigParser instance).
        """
        config.add_section(self.id)
        for (key, value) in self.properties.items():
            if value is None:
                value = ""
            config.set(self.id, key, value)

    def __getitem__(self, key):
        return self.properties[key]

    def __setitem__(self, key, value):
        self.properties[key] = value

    def items(self):
        """
            Return all (key, value) properties.
        """
        return self.properties.items()
