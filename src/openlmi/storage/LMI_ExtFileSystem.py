# Copyright (C) 2013 Red Hat, Inc.  All rights reserved.
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
""" Module for LMI_LocalFilesystem."""

from openlmi.storage.LocalFileSystemProvider import LocalFileSystemProvider
import openlmi.storage.cmpi_logging as cmpi_logging
import pyanaconda.storage.formats
import pywbem

class LMI_ExtFileSystem(LocalFileSystemProvider):
    """
        Generic file system provider for filesystems which do not have
        it's own provider.
    """
    @cmpi_logging.trace_method
    def __init__(self, *args, **kwargs):
        super(LMI_ExtFileSystem, self).__init__(
                classname="LMI_ExtFileSystem",
                device_type=None,
                setting_classname="LMI_ExtFileSystemSetting",
                *args, **kwargs)

    @cmpi_logging.trace_method
    def provides_format(self, fmt):
        if fmt is None:
            return False
        if isinstance(fmt, pyanaconda.storage.formats.fs.Ext4FS):
            return True
        if isinstance(fmt, pyanaconda.storage.formats.fs.Ext3FS):
            return True
        if isinstance(fmt, pyanaconda.storage.formats.fs.Ext2FS):
            return True
        return False

    @cmpi_logging.trace_method
    # pylint: disable-msg=W0221
    def get_instance(self, env, model, fmt=None):
        """
            Get instance.
            Subclasses should override this method, the default implementation
            just check if the instance exists.
        """
        model = super(LMI_ExtFileSystem, self).get_instance(
                env, model, fmt)
        if not fmt:
            fmt = self.get_format_for_name(model)

        if isinstance(fmt, pyanaconda.storage.formats.fs.Ext2FS):
            model['ExtVersion'] = self.Values.ExtVersion.ext2
        elif isinstance(fmt, pyanaconda.storage.formats.fs.Ext3FS):
            model['ExtVersion'] = self.Values.ExtVersion.ext3
        elif isinstance(fmt, pyanaconda.storage.formats.fs.Ext4FS):
            model['ExtVersion'] = self.Values.ExtVersion.ext4
        return model

    class Values(LocalFileSystemProvider.Values):
        class ExtVersion(object):
            ext2 = pywbem.Uint16(2)
            ext3 = pywbem.Uint16(3)
            ext4 = pywbem.Uint16(4)
