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
    Support functions for filesystems.
"""
import pyanaconda.storage
from wrapper.common import storage
   
def createFilesystem(device, label):
    fmt = pyanaconda.storage.formats.getFormat('ext3')
    fmt.label = label
    action = pyanaconda.storage.deviceaction.ActionCreateFormat(device, fmt)
    storage.devicetree.registerAction(action)
    action.execute()
    storage.devicetree._actions = []
    return device
