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

class LMI_LocalFileSystem(LocalFileSystemProvider):
    """
        Generic file system provider for filesystems which do not have
        it's own provider.
    """
    @cmpi_logging.trace_method
    def __init__(self, *args, **kwargs):
        super(LMI_LocalFileSystem, self).__init__(
                classname="LMI_LocalFileSystem",
                device_type=None,
                setting_classname="LMI_FileSystemSetting",
                *args, **kwargs)

    @cmpi_logging.trace_method
    def provides_format(self, fmt):
        if fmt is None:
            return False
        # skip all filesystems
        if not isinstance(fmt, pyanaconda.storage.formats.fs.FS):
            return False
        # skip formats with its own classes
        if (isinstance(fmt, pyanaconda.storage.formats.fs.Ext2FS)
                or isinstance(fmt, pyanaconda.storage.formats.fs.Ext3FS)
                or isinstance(fmt, pyanaconda.storage.formats.fs.Ext4FS)):
            return False

        # skip 'Unknown' format
        if fmt.type is None:
            return False
        return True
