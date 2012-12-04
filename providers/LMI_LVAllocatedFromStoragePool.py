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

from BaseProvider import BaseProvider
import pywbem
import pyanaconda.storage

class LMI_LVAllocatedFromStoragePool(BaseProvider):
    """
        Implementation of LMI_LVAllocatedFromStoragePool class.
    """
    def __init__(self, *args, **kwargs):
        super(LMI_LVAllocatedFromStoragePool, self).__init__(*args, **kwargs)

    def enum_instances(self, env, model, keys_only):
        """
            Provider implementation of EnumerateInstances intrinsic method.
        """
        model.path.update({'Dependent': None, 'Antecedent': None})

        for device in self.storage.lvs:
            lvprovider = self.provider_manager.get_provider_for_device(device)
            if not lvprovider:
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                        "Cannot find provider for device " + device.path)
            vg = device.vg
            vgprovider = self.provider_manager.get_provider_for_device(vg)
            if not vgprovider:
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                        "Cannot find provider for device " + vg.path)

            model['Dependent'] = lvprovider.get_name_for_device(device)
            model['Antecedent'] = vgprovider.get_name_for_device(vg)
            if keys_only:
                yield model
            else:
                yield self.get_instance(env, model, device, vg)

    def get_instance(self, env, model, device=None, vg=None):
        """
            Provider implementation of GetInstance intrinsic method.
            It just checks if Dependent and Antecedent are related.
        """
        if not device:
            device = self.provider_manager.get_device_for_name(model['Dependent'])
        if not device:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Cannot find Dependent device")

        if not vg:
            vg = self.provider_manager.get_device_for_name(model['Antecedent'])
        if not vg:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Cannot find Antecedent device")

        if not isinstance(device,
                    pyanaconda.storage.devices.LVMLogicalVolumeDevice):
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Dependend device is not logical volume: " + device.path)
        if not isinstance(vg, pyanaconda.storage.devices.LVMVolumeGroupDevice):
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Antecedent device is not volume vroup: " + vg.path)
        if vg != device.vg:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Antecedent is not related to Dependent device")

        return model


    def references(self, env, object_name, model, result_class_name, role,
                   result_role, keys_only):
        """Instrument Associations.

        All four association-related operations (Associators, AssociatorNames, 
        References, ReferenceNames) are mapped to this method. 
        This method is a python generator

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName that defines the source 
            CIM Object whose associated Objects are to be returned.
        model -- A template pywbem.CIMInstance to serve as a model
            of the objects to be returned.  Only properties present on this
            model need to be set. 
        result_class_name -- If not empty, this string acts as a filter on 
            the returned set of Instances by mandating that each returned 
            Instances MUST represent an association between object_name 
            and an Instance of a Class whose name matches this parameter
            or a subclass. 
        role -- If not empty, MUST be a valid Property name. It acts as a 
            filter on the returned set of Instances by mandating that each 
            returned Instance MUST refer to object_name via a Property 
            whose name matches the value of this parameter.
        result_role -- If not empty, MUST be a valid Property name. It acts 
            as a filter on the returned set of Instances by mandating that 
            each returned Instance MUST represent associations of 
            object_name to other Instances, where the other Instances play 
            the specified result_role in the association (i.e. the 
            name of the Property in the Association Class that refers to 
            the Object related to object_name MUST match the value of this 
            parameter).
        keys_only -- A boolean.  True if only the key properties should be
            set on the generated instances.

        The following diagram may be helpful in understanding the role, 
        result_role, and result_class_name parameters.
        +------------------------+                    +-------------------+
        | object_name.classname  |                    | result_class_name |
        | ~~~~~~~~~~~~~~~~~~~~~  |                    | ~~~~~~~~~~~~~~~~~ |
        +------------------------+                    +-------------------+
           |              +-----------------------------------+      |
           |              |  [Association] model.classname    |      |
           | object_name  |  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    |      |
           +--------------+ object_name.classname REF role    |      |
        (CIMInstanceName) | result_class_name REF result_role +------+
                          |                                   |(CIMInstanceName)
                          +-----------------------------------+

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_NOT_SUPPORTED
        CIM_ERR_INVALID_NAMESPACE
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, unrecognized 
            or otherwise incorrect parameters)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        ch = env.get_cimom_handle()

        # If you want to get references for free, implemented in terms 
        # of enum_instances, just leave the code below unaltered.
        if ch.is_subclass(object_name.namespace,
                          sub=object_name.classname,
                          super='CIM_StorageExtent') or \
                ch.is_subclass(object_name.namespace,
                               sub=object_name.classname,
                               super='CIM_StoragePool'):
            return self.simple_refs(env, object_name, model,
                          result_class_name, role, result_role, keys_only)
