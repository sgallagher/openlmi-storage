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
""" Module for LMI_FileSystemConfigurationService class."""

from openlmi.storage.ServiceProvider import ServiceProvider
import pywbem
import openlmi.storage.cmpi_logging as cmpi_logging

class LMI_FileSystemConfigurationService(ServiceProvider):
    """
        LMI_FileSystemConfigurationService provider implementation.
    """
    @cmpi_logging.trace_method
    def __init__(self, *args, **kwargs):
        super(LMI_FileSystemConfigurationService, self).__init__(
                "LMI_FileSystemConfigurationService", *args, **kwargs)

    def cim_method_lmi_createfilesystem(self, env, object_name,
                                        param_goal=None,
                                        param_elementname=None,
                                        param_theelement=None,
                                        param_inextents=None):
        """Implements LMI_FileSystemConfigurationService.LMI_CreateFileSystem()

        Start a job to create a FileSystem on StorageExtents. If the
        operation completes successfully and did not require a
        long-running ConcreteJob, it will return 0. If 4096/0x1000 is
        returned, a ConcreteJob will be started to create the element. A
        Reference to the ConcreteJob will be returned in the output
        parameter Job. If any other value is returned, the job will not be
        started, and no action will be taken. \nThe parameter TheElement
        will contain a Reference to the FileSystem if this operation
        completed successfully. \nThe StorageExtents to use is specified
        by the InExtents parameter.\nThe desired settings for the
        FileSystem are specified by the Goal parameter. Goal is an element
        of class CIM_FileSystemSetting, or a derived class. Unlike CIM
        standard CreateFileSystem, the parameter is reference to
        CIM_FileSystemSetting stored on the CIMOM.\nA ResidesOnExtent
        association is created between the created FileSystem and the
        StorageExtents used for it.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method LMI_CreateFileSystem() 
            should be invoked.
        param_goal --  The input parameter Goal (type REF (pywbem.CIMInstanceName(classname='CIM_FileSystemSetting', ...)) 
            The requirements for the FileSystem element to maintain. This
            is an element of class CIM_FileSystemSetting, or a derived
            class. This allows the client to specify the properties
            desired for the file system. If NULL, the
            FileSystemConfigurationService will create default filesystem.
            
        param_elementname --  The input parameter ElementName (type unicode) 
            Label of the filesystem being created. If NULL, a
            system-supplied default name can be used. The value will be
            stored in the \'ElementName\' property for the created
            element.
            
        param_theelement --  The input parameter TheElement (type REF (pywbem.CIMInstanceName(classname='CIM_FileSystem', ...)) 
            The newly created FileSystem.
            
        param_inextents --  The input parameter InExtents (type REF (pywbem.CIMInstanceName(classname='CIM_StorageExtent', ...)) 
            The StorageExtents on which the created FileSystem will reside.
            At least one extent must be provided. If the filesystem being
            created supports more than one storage extent (e.g. btrfs),
            more extents can be provided. The filesystem will then reside
            on all of them.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.LMI_CreateFileSystem)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...)) 
            Reference to the job (may be null if job completed).
            
        TheElement -- (type REF (pywbem.CIMInstanceName(classname='CIM_FileSystem', ...)) 
            The newly created FileSystem.
            

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, 
            unrecognized or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the target CIM Class or instance does not 
            exist in the specified namespace)
        CIM_ERR_METHOD_NOT_AVAILABLE (the CIM Server is unable to honor 
            the invocation request)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE)


    class Values(ServiceProvider.Values):
        class LMI_CreateFileSystem(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            StorageExtent_is_not_big_enough_to_satisfy_the_request = \
                    pywbem.Uint32(6)
            StorageExtent_specified_by_default_cannot_be_created = \
                    pywbem.Uint32(7)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            # Method_Reserved = 4098..32767
            # Vendor_Specific = 32768..65535
