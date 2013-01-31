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
""" Module for LocalFileSystemProvider."""

import pywbem
from openlmi.storage.FormatProvider import FormatProvider
import openlmi.storage.cmpi_logging as cmpi_logging

class LocalFileSystemProvider(FormatProvider):
    """
        Abstract provider for local filesystems.
        Each provider must have .device_type property, which represents
        pyanaconda.storage.formats.<DeviceFormat child>.type of format it
        represents.
    """
    @cmpi_logging.trace_method
    def __init__(self, *args, **kwargs):
        super(LocalFileSystemProvider, self).__init__(*args, **kwargs)

    @cmpi_logging.trace_method
    # pylint: disable-msg=W0221
    def get_instance(self, env, model, fmt=None):
        """
            Get instance.
            Subclasses should override this method, the default implementation
            just check if the instance exists.
        """
        if not fmt:
            fmt = self.get_format_for_name(model)
        if not fmt:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Cannot find the format.")

        model['FileSystemType'] = fmt.name
        model['CaseSensitive'] = True
        model['CasePreserved'] = True
        model['PersistenceType'] = self.Values.PersistenceType.Persistent
        if fmt.label:
            model['ElementName'] = fmt.label
        else:
            model['ElementName'] = "dev:" + fmt.device

        return model

    class Values(FormatProvider.Values):
        class PersistenceType(object):
            Unknown = pywbem.Uint16(0)
            Other = pywbem.Uint16(1)
            Persistent = pywbem.Uint16(2)
            Temporary = pywbem.Uint16(3)
            External = pywbem.Uint16(4)
