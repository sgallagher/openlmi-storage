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

"""Python Provider for LMI_DiskPartition

Instruments the CIM class LMI_DiskPartition

"""

from wrapper.common import *
import pywbem
from pywbem.cim_provider2 import CIMProvider2
import pyanaconda.storage.devices
import util.partitioning

class LMI_DiskPartition(CIMProvider2):
    """Instrument the CIM class LMI_DiskPartition 

    A logical partition.
    
    """

    def __init__ (self, env):
        logger = env.get_logger()
        logger.log_debug('Initializing provider %s from %s' \
                % (self.__class__.__name__, __file__))

    def get_instance(self, env, model, partition = None):
        """Return an instance.

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        model -- A template of the pywbem.CIMInstance to be returned.  The 
            key properties are set on this instance to correspond to the 
            instanceName that was requested.  The properties of the model
            are already filtered according to the PropertyList from the 
            request.  Only properties present in the model need to be
            given values.  If you prefer, you can set all of the 
            values, and the instance will be filtered for you. 

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, unrecognized 
            or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the CIM Class does exist, but the requested CIM 
            Instance does not exist in the specified namespace)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.get_instance()' \
                % self.__class__.__name__)

        if (model['SystemName'] != LMI_SYSTEM_NAME
                or model['SystemCreationClassName'] != LMI_SYSTEM_CLASS_NAME
                or model['CreationClassName'] != 'LMI_DiskPartition'):
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "Wrong keys.")

        # find the partition with given name
        if partition is None:
            partition = storage.devicetree.getDeviceByPath(model['DeviceID'])
            if partition is None:
                raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "DeviceID not found.")
            if  not isinstance(partition, pyanaconda.storage.devices.PartitionDevice):
                raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "DeviceID is not a partition.")
            if partition.disk.format.labelType != util.partitioning.LABEL_MBR:
                raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "DeviceID is not a MBR partition.")

        #model['Access'] = self.Values.Access.<VAL> # TODO 
        #model['AdditionalAvailability'] = [self.Values.AdditionalAvailability.<VAL>,] # TODO 
        #model['Allocatable'] = bool() # TODO 
        #model['Availability'] = self.Values.Availability.<VAL> # TODO 
        #model['AvailableRequestedStates'] = [self.Values.AvailableRequestedStates.<VAL>,] # TODO 
        model['BlockSize'] = pywbem.Uint64(partition.partedDevice.sectorSize)
        if partition.bootable:
            model['Bootable'] = True
        else:
            model['Bootable'] = False
        #model['Caption'] = '' # TODO 
        #model['ClientSettableUsage'] = [pywbem.Uint16(),] # TODO 
        #model['CommunicationStatus'] = self.Values.CommunicationStatus.<VAL> # TODO 
        #model['ConsumableBlocks'] = pywbem.Uint64() # TODO 
        #model['DataOrganization'] = self.Values.DataOrganization.<VAL> # TODO 
        #model['DataRedundancy'] = pywbem.Uint16() # TODO 
        #model['DeltaReservation'] = pywbem.Uint8() # TODO 
        #model['Description'] = '' # TODO 
        #model['DetailedStatus'] = self.Values.DetailedStatus.<VAL> # TODO 
        #model['ElementName'] = '' # TODO 
        model['EnabledDefault'] = self.Values.EnabledDefault.Enabled
        model['EnabledState'] = self.Values.EnabledState.Enabled
        #model['ErrorCleared'] = bool() # TODO 
        #model['ErrorDescription'] = '' # TODO 
        #model['ErrorMethodology'] = '' # TODO 
        #model['Extendable'] = bool() # TODO 
        #model['ExtentDiscriminator'] = ['',] # TODO 
        #model['ExtentInterleaveDepth'] = pywbem.Uint64() # TODO 
        #model['ExtentStatus'] = [self.Values.ExtentStatus.<VAL>,] # TODO 
        #model['ExtentStripeLength'] = pywbem.Uint64() # TODO 
        #model['Generation'] = pywbem.Uint64() # TODO 
        #model['HealthState'] = self.Values.HealthState.<VAL> # TODO 
        #model['IdentifyingDescriptions'] = ['',] # TODO 
        #model['InstallDate'] = pywbem.CIMDateTime() # TODO 
        #model['InstanceID'] = '' # TODO 
        #model['IsBasedOnUnderlyingRedundancy'] = bool() # TODO 
        model['IsComposite'] = False
        #model['IsConcatenated'] = bool() # TODO 
        #model['LastErrorCode'] = pywbem.Uint32() # TODO 
        #model['LocationIndicator'] = self.Values.LocationIndicator.<VAL> # TODO 
        #model['MaxQuiesceTime'] = pywbem.Uint64() # TODO 
        model['Name'] = partition.path
        model['NameFormat'] = self.Values.NameFormat.OS_Device_Name
        model['NameNamespace'] = self.Values.NameNamespace.OS_Device_Namespace
        #model['NoSinglePointOfFailure'] = bool() # TODO
        if partition.isLogical:
            model['NumberOfBlocks'] = pywbem.Uint64(
                                    partition.partedPartition.geometry.end
                                    - util.partitioning.getLogicalPartitionStart(partition)
                                    + 1)
        else:
            model['NumberOfBlocks'] = pywbem.Uint64(partition.partedPartition.getLength())
        #model['OperatingStatus'] = self.Values.OperatingStatus.<VAL> # TODO 
        model['OperationalStatus'] = [self.Values.OperationalStatus.OK]
        #model['OtherEnabledState'] = '' # TODO 
        #model['OtherIdentifyingInfo'] = ['',] # TODO 
        #model['OtherNameFormat'] = '' # TODO 
        #model['OtherNameNamespace'] = '' # TODO 
        #model['OtherUsageDescription'] = '' # TODO 
        #model['PackageRedundancy'] = pywbem.Uint16() # TODO 
        #model['PartitionSubtype'] = self.Values.PartitionSubtype.<VAL> # TODO
        if partition.isLogical:
            model['PartitionType'] = self.Values.PartitionType.Logical
        elif partition.isExtended:
            model['PartitionType'] = self.Values.PartitionType.Extended
        elif partition.isPrimary:
            model['PartitionType'] = self.Values.PartitionType.Primary

        #model['PowerManagementCapabilities'] = [self.Values.PowerManagementCapabilities.<VAL>,] # TODO 
        #model['PowerManagementSupported'] = bool() # TODO 
        #model['PowerOnHours'] = pywbem.Uint64() # TODO
        model['PrimaryPartition'] = bool(partition.isPrimary or partition.isExtended)
        #model['PrimaryStatus'] = self.Values.PrimaryStatus.<VAL> # TODO 
        model['Primordial'] = False # TODO: really 
        #model['Purpose'] = '' # TODO 
        model['RequestedState'] = self.Values.RequestedState.Not_Applicable
        #model['SequentialAccess'] = bool() # TODO 
        #model['Signature'] = '' # TODO 
        #model['SignatureAlgorithm'] = '' # TODO 
        #model['SignatureState'] = self.Values.SignatureState.<VAL> # TODO 
        #model['Status'] = self.Values.Status.<VAL> # TODO 
        #model['StatusDescriptions'] = ['',] # TODO 
        #model['StatusInfo'] = self.Values.StatusInfo.<VAL> # TODO 
        #model['TimeOfLastStateChange'] = pywbem.CIMDateTime() # TODO 
        #model['TotalPowerOnHours'] = pywbem.Uint64() # TODO 
        model['TransitioningToState'] = self.Values.TransitioningToState.Not_Applicable
        #model['Usage'] = self.Values.Usage.<VAL> # TODO 
        return model

    def enum_instances(self, env, model, keys_only):
        """Enumerate instances.

        The WBEM operations EnumerateInstances and EnumerateInstanceNames
        are both mapped to this method. 
        This method is a python generator

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        model -- A template of the pywbem.CIMInstances to be generated.  
            The properties of the model are already filtered according to 
            the PropertyList from the request.  Only properties present in 
            the model need to be given values.  If you prefer, you can 
            always set all of the values, and the instance will be filtered 
            for you. 
        keys_only -- A boolean.  True if only the key properties should be
            set on the generated instances.

        Possible Errors:
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.enum_instances()' \
                % self.__class__.__name__)

        # Prime model.path with knowledge of the keys, so key values on
        # the CIMInstanceName (model.path) will automatically be set when
        # we set property values on the model. 
        model.path.update({'CreationClassName': None, 'SystemName': None,
            'DeviceID': None, 'SystemCreationClassName': None})

        partitions = storage.partitions
        for p in partitions:
            if p.disk.format.labelType != util.partitioning.LABEL_MBR:
                continue
            
            model['SystemName'] = LMI_SYSTEM_NAME
            model['SystemCreationClassName'] = LMI_SYSTEM_CLASS_NAME
            model['CreationClassName'] = 'LMI_DiskPartition'
            model['DeviceID'] = p.path
            if keys_only:
                yield model
            else:
                try:
                    yield self.get_instance(env, model, p)
                except pywbem.CIMError, (num, msg):
                    if num not in (pywbem.CIM_ERR_NOT_FOUND,
                                   pywbem.CIM_ERR_ACCESS_DENIED):
                        raise

    def set_instance(self, env, instance, modify_existing):
        """Return a newly created or modified instance.

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        instance -- The new pywbem.CIMInstance.  If modifying an existing 
            instance, the properties on this instance have been filtered by 
            the PropertyList from the request.
        modify_existing -- True if ModifyInstance, False if CreateInstance

        Return the new instance.  The keys must be set on the new instance. 

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_NOT_SUPPORTED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, unrecognized 
            or otherwise incorrect parameters)
        CIM_ERR_ALREADY_EXISTS (the CIM Instance already exists -- only 
            valid if modify_existing is False, indicating that the operation
            was CreateInstance)
        CIM_ERR_NOT_FOUND (the CIM Instance does not exist -- only valid 
            if modify_existing is True, indicating that the operation
            was ModifyInstance)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.set_instance()' \
                % self.__class__.__name__)
        # TODO create or modify the instance
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED) # Remove to implement
        return instance

    def delete_instance(self, env, instance_name):
        """Delete an instance.

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        instance_name -- A pywbem.CIMInstanceName specifying the instance 
            to delete.

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_NOT_SUPPORTED
        CIM_ERR_INVALID_NAMESPACE
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, unrecognized 
            or otherwise incorrect parameters)
        CIM_ERR_INVALID_CLASS (the CIM Class does not exist in the specified 
            namespace)
        CIM_ERR_NOT_FOUND (the CIM Class does exist, but the requested CIM 
            Instance does not exist in the specified namespace)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.delete_instance()' \
                % self.__class__.__name__)

        if (instance_name['SystemName'] != LMI_SYSTEM_NAME
                or instance_name['SystemCreationClassName'] != LMI_SYSTEM_CLASS_NAME
                or instance_name['CreationClassName'] != 'LMI_DiskPartition'):
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "Wrong keys.")

        # find the partition with given name
        partition = storage.devicetree.getDeviceByPath(instance_name['DeviceID'])
        if partition is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "DeviceID not found.")
        if  not isinstance(partition, pyanaconda.storage.devices.PartitionDevice):
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "DeviceID is not a partition.")
        if partition.disk.format.labelType != util.partitioning.LABEL_MBR:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "DeviceID is not a MBR partition.")
        util.partitioning.deletePartition(partition)

    def cim_method_reset(self, env, object_name):
        """Implements LMI_DiskPartition.Reset()

        Requests a reset of the LogicalDevice. The return value should be 0
        if the request was successfully executed, 1 if the request is not
        supported, and some other value if an error occurred. In a
        subclass, the set of possible return codes could be specified,
        using a ValueMap qualifier on the method. The strings to which the
        ValueMap contents are \'translated\' can also be specified in the
        subclass as a Values array qualifier.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method Reset() 
            should be invoked.

        Returns a two-tuple containing the return value (type pywbem.Uint32)
        and a list of CIMParameter objects representing the output parameters

        Output parameters: none

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

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_reset()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        rval = None# TODO (type pywbem.Uint32)
        return (rval, out_params)

    def cim_method_requeststatechange(self, env, object_name,
                                      param_requestedstate = None,
                                      param_timeoutperiod = None):
        """Implements LMI_DiskPartition.RequestStateChange()

        Requests that the state of the element be changed to the value
        specified in the RequestedState parameter. When the requested
        state change takes place, the EnabledState and RequestedState of
        the element will be the same. Invoking the RequestStateChange
        method multiple times could result in earlier requests being
        overwritten or lost. \nA return code of 0 shall indicate the state
        change was successfully initiated. \nA return code of 3 shall
        indicate that the state transition cannot complete within the
        interval specified by the TimeoutPeriod parameter. \nA return code
        of 4096 (0x1000) shall indicate the state change was successfully
        initiated, a ConcreteJob has been created, and its reference
        returned in the output parameter Job. Any other return code
        indicates an error condition.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method RequestStateChange() 
            should be invoked.
        param_requestedstate --  The input parameter RequestedState (type pywbem.Uint16 self.Values.RequestStateChange.RequestedState) 
            The state requested for the element. This information will be
            placed into the RequestedState property of the instance if the
            return code of the RequestStateChange method is 0 (\'Completed
            with No Error\'), or 4096 (0x1000) (\'Job Started\'). Refer to
            the description of the EnabledState and RequestedState
            properties for the detailed explanations of the RequestedState
            values.
            
        param_timeoutperiod --  The input parameter TimeoutPeriod (type pywbem.CIMDateTime) 
            A timeout period that specifies the maximum amount of time that
            the client expects the transition to the new state to take.
            The interval format must be used to specify the TimeoutPeriod.
            A value of 0 or a null parameter indicates that the client has
            no time requirements for the transition. \nIf this property
            does not contain 0 or null and the implementation does not
            support this parameter, a return code of \'Use Of Timeout
            Parameter Not Supported\' shall be returned.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.RequestStateChange)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...)) 
            May contain a reference to the ConcreteJob created to track the
            state transition initiated by the method invocation.
            

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

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_requeststatechange()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('job', type='reference', 
        #                   value=pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))] # TODO
        rval = None# TODO (type pywbem.Uint32 self.Values.RequestStateChange)
        return (rval, out_params)

    def cim_method_setpowerstate(self, env, object_name,
                                 param_powerstate = None,
                                 param_time = None):
        """Implements LMI_DiskPartition.SetPowerState()

        Note: The use of this method has been deprecated. Instead, use the
        SetPowerState method in the associated PowerManagementService
        class. Deprecated description: Sets the power state of the Device.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method SetPowerState() 
            should be invoked.
        param_powerstate --  The input parameter PowerState (type pywbem.Uint16 self.Values.SetPowerState.PowerState) 
            The power state to set.
            
        param_time --  The input parameter Time (type pywbem.CIMDateTime) 
            Time indicates when the power state should be set, either as a
            regular date-time value or as an interval value (where the
            interval begins when the method invocation is received).
            

        Returns a two-tuple containing the return value (type pywbem.Uint32)
        and a list of CIMParameter objects representing the output parameters

        Output parameters: none

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

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_setpowerstate()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        rval = None# TODO (type pywbem.Uint32)
        return (rval, out_params)

    def cim_method_quiescedevice(self, env, object_name,
                                 param_quiesce = None):
        """Implements LMI_DiskPartition.QuiesceDevice()

        Note: The use of this method has been deprecated in lieu of the
        more general RequestStateChange method that directly overlaps with
        the functionality provided by this method. \nDeprecated
        description: Requests that the LogicalDevice cleanly cease all
        activity ("Quiesce" input parameter=TRUE) or resume activity
        (=FALSE). For this method to quiesce a Device, that Device should
        have an Availability (or Additional Availability) of "Running/Full
        Power" (value=3) and an EnabledStatus/StatusInfo of "Enabled". For
        example, if quiesced, a Device can then be taken offline for
        diagnostics, or disabled for power off and hot swap. For the
        method to "unquiesce" a Device, that Device should have an
        Availability (or AdditionalAvailability) of "Quiesced" (value=21)
        and an EnabledStatus or StatusInfo of "Enabled". In this case, the
        Device would be returned to an "Enabled" and "Running/Full Power"
        status. \nThe return code of the method should indicate the
        success or failure of the quiesce. It should return 0 if
        successful, 1 if the request is not supported at all, 2 if the
        request is not supported due to the current state of the Device,
        and some other value if any other error occurred. In a subclass,
        the set of possible return codes could be specified, using a
        ValueMap qualifier on the method. The strings to which the
        ValueMap contents are \'translated\' can also be specified in the
        subclass as a Values array qualifier.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method QuiesceDevice() 
            should be invoked.
        param_quiesce --  The input parameter Quiesce (type bool) 
            If set to TRUE, then cleanly cease all activity. If FALSE,
            resume activity.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32)
        and a list of CIMParameter objects representing the output parameters

        Output parameters: none

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

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_quiescedevice()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        rval = None# TODO (type pywbem.Uint32)
        return (rval, out_params)

    def cim_method_enabledevice(self, env, object_name,
                                param_enabled = None):
        """Implements LMI_DiskPartition.EnableDevice()

        Note: The use of this method has been deprecated in lieu of the
        more general RequestStateChange method that directly overlaps with
        the functionality provided by this method. \nDeprecated
        description: Requests that the LogicalDevice be enabled ("Enabled"
        input parameter=TRUE) or disabled (=FALSE). If successful, the
        StatusInfo or EnabledState properties of the Device should reflect
        the desired state (enabled or disabled). Note that this function
        overlaps with the RequestedState property. RequestedState was
        added to the model to maintain a record (for example, a persisted
        value) of the last state request. Invoking the EnableDevice method
        should set the RequestedState property appropriately. \nThe return
        code should be 0 if the request was successfully executed, 1 if
        the request is not supported, and some other value if an error
        occurred. In a subclass, the set of possible return codes could be
        specified by using a ValueMap qualifier on the method. The strings
        to which the ValueMap contents are \'translated\' can also be
        specified in the subclass as a Values array qualifier.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method EnableDevice() 
            should be invoked.
        param_enabled --  The input parameter Enabled (type bool) 
            If TRUE, enable the device. If FALSE, disable the device.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32)
        and a list of CIMParameter objects representing the output parameters

        Output parameters: none

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

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_enabledevice()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        rval = None# TODO (type pywbem.Uint32)
        return (rval, out_params)

    def cim_method_onlinedevice(self, env, object_name,
                                param_online = None):
        """Implements LMI_DiskPartition.OnlineDevice()

        Note: The use of this method has been deprecated in lieu of the
        more general RequestStateChange method that directly overlaps with
        the functionality provided by this method. \nDeprecated
        description: Requests that the LogicalDevice be brought online
        ("Online" input parameter=TRUE) or taken offline (=FALSE).
        "Online" indicates that the Device is ready to accept requests,
        and is operational and fully functioning. In this case, the
        Availability property of the Device would be set to a value of 3
        ("Running/Full Power"). "Offline" indicates that a Device is
        powered on and operational, but is not processing functional
        requests. In an offline state, a Device might be capable of
        running diagnostics or generating operational alerts. For example,
        when the "Offline" button is pushed on a Printer, the Device is no
        longer available to process print jobs, but it could be available
        for diagnostics or maintenance. \nIf this method is successful,
        the Availability and AdditionalAvailability properties of the
        Device should reflect the updated status. If a failure occurs when
        you try to bring the Device online or offline, it should remain in
        its current state. The request, if unsuccessful, should not leave
        the Device in an indeterminate state. When bringing a Device back
        "Online" from an "Offline" mode, the Device should be restored to
        its last "Online" state, if at all possible. Only a Device that
        has an EnabledState or StatusInfo of "Enabled" and has been
        configured can be brought online or taken offline. \nOnlineDevice
        should return 0 if successful, 1 if the request is not supported
        at all, 2 if the request is not supported due to the current state
        of the Device, and some other value if any other error occurred.
        In a subclass, the set of possible return codes could be
        specified, using a ValueMap qualifier on the method. The strings
        to which the ValueMap contents are \'translated\' can also be
        specified in the subclass as a Values array qualifier. \nNote that
        the function of this method overlaps with the RequestedState
        property. RequestedState was added to the model to maintain a
        record (for example, a persisted value) of the last state request.
        Invoking the OnlineDevice method should set the RequestedState
        property appropriately.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method OnlineDevice() 
            should be invoked.
        param_online --  The input parameter Online (type bool) 
            If TRUE, take the device online. If FALSE, take the device
            offline.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32)
        and a list of CIMParameter objects representing the output parameters

        Output parameters: none

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

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_onlinedevice()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        rval = None# TODO (type pywbem.Uint32)
        return (rval, out_params)

    def cim_method_saveproperties(self, env, object_name):
        """Implements LMI_DiskPartition.SaveProperties()

        Note: The use of this method is deprecated. Its function is handled
        more generally by the ConfigurationData subclass of SettingData.
        \nDeprecated description: Requests that the Device capture its
        current configuration, setup or state information, or both in a
        backing store. \nThe information returned by this method could be
        used at a later time (using the RestoreProperties method) to
        return a Device to its present "condition". This method might not
        be supported by all Devices. The method should return 0 if
        successful, 1 if the request is not supported, and some other
        value if any other error occurred. In a subclass, the set of
        possible return codes could be specified, using a ValueMap
        qualifier on the method. The strings to which the ValueMap
        contents are \'translated\' can also be specified in the subclass
        as a Values array qualifier.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method SaveProperties() 
            should be invoked.

        Returns a two-tuple containing the return value (type pywbem.Uint32)
        and a list of CIMParameter objects representing the output parameters

        Output parameters: none

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

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_saveproperties()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        rval = None# TODO (type pywbem.Uint32)
        return (rval, out_params)

    def cim_method_restoreproperties(self, env, object_name):
        """Implements LMI_DiskPartition.RestoreProperties()

        Note: The use of this method is deprecated. Its function is handled
        more generally by the ConfigurationData subclass of SettingData.
        \nRequests that the Device re-establish its configuration, setup
        or state information, or both from a backing store. The
        information would have been captured at an earlier time (using the
        SaveProperties method). This method might not be supported by all
        Devices. The method should return 0 if successful, 1 if the
        request is not supported, and some other value if any other error
        occurred. In a subclass, the set of possible return codes could be
        specified using a ValueMap qualifier on the method. The strings to
        which the ValueMap contents are \'translated\' can also be
        specified in the subclass as a Values array qualifier.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method RestoreProperties() 
            should be invoked.

        Returns a two-tuple containing the return value (type pywbem.Uint32)
        and a list of CIMParameter objects representing the output parameters

        Output parameters: none

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

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_restoreproperties()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        rval = None# TODO (type pywbem.Uint32)
        return (rval, out_params)

    class Values(object):
        class RequestedState(object):
            Unknown = pywbem.Uint16(0)
            Enabled = pywbem.Uint16(2)
            Disabled = pywbem.Uint16(3)
            Shut_Down = pywbem.Uint16(4)
            No_Change = pywbem.Uint16(5)
            Offline = pywbem.Uint16(6)
            Test = pywbem.Uint16(7)
            Deferred = pywbem.Uint16(8)
            Quiesce = pywbem.Uint16(9)
            Reboot = pywbem.Uint16(10)
            Reset = pywbem.Uint16(11)
            Not_Applicable = pywbem.Uint16(12)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 32768..65535

        class HealthState(object):
            Unknown = pywbem.Uint16(0)
            OK = pywbem.Uint16(5)
            Degraded_Warning = pywbem.Uint16(10)
            Minor_failure = pywbem.Uint16(15)
            Major_failure = pywbem.Uint16(20)
            Critical_failure = pywbem.Uint16(25)
            Non_recoverable_error = pywbem.Uint16(30)
            # DMTF_Reserved = ..
            # Vendor_Specific = 32768..65535

        class Access(object):
            Unknown = pywbem.Uint16(0)
            Readable = pywbem.Uint16(1)
            Writeable = pywbem.Uint16(2)
            Read_Write_Supported = pywbem.Uint16(3)
            Write_Once = pywbem.Uint16(4)

        class CommunicationStatus(object):
            Unknown = pywbem.Uint16(0)
            Not_Available = pywbem.Uint16(1)
            Communication_OK = pywbem.Uint16(2)
            Lost_Communication = pywbem.Uint16(3)
            No_Contact = pywbem.Uint16(4)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 0x8000..

        class Usage(object):
            Other = pywbem.Uint16(1)
            Unrestricted = pywbem.Uint16(2)
            Reserved_for_ComputerSystem__the_block_server_ = pywbem.Uint16(3)
            Reserved_by_Replication_Services = pywbem.Uint16(4)
            Reserved_by_Migration_Services = pywbem.Uint16(5)
            Local_Replica_Source = pywbem.Uint16(6)
            Remote_Replica_Source = pywbem.Uint16(7)
            Local_Replica_Target = pywbem.Uint16(8)
            Remote_Replica_Target = pywbem.Uint16(9)
            Local_Replica_Source_or_Target = pywbem.Uint16(10)
            Remote_Replica_Source_or_Target = pywbem.Uint16(11)
            Delta_Replica_Target = pywbem.Uint16(12)
            Element_Component = pywbem.Uint16(13)
            Reserved_as_Pool_Contributor = pywbem.Uint16(14)
            Composite_Volume_Member = pywbem.Uint16(15)
            Composite_LogicalDisk_Member = pywbem.Uint16(16)
            Reserved_for_Sparing = pywbem.Uint16(17)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 32768..65535

        class DetailedStatus(object):
            Not_Available = pywbem.Uint16(0)
            No_Additional_Information = pywbem.Uint16(1)
            Stressed = pywbem.Uint16(2)
            Predictive_Failure = pywbem.Uint16(3)
            Non_Recoverable_Error = pywbem.Uint16(4)
            Supporting_Entity_in_Error = pywbem.Uint16(5)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 0x8000..

        class PartitionSubtype(object):
            Empty___Microsoft = pywbem.Uint16(0)
            DOS_12_bit_FAT = pywbem.Uint16(1)
            XENIX_root = pywbem.Uint16(2)
            XENIX_usr = pywbem.Uint16(3)
            DOS_16_bit_FAT = pywbem.Uint16(4)
            DOS_Extended = pywbem.Uint16(5)
            DOS_16_bit_FAT____32MB_ = pywbem.Uint16(6)
            OS_2_HPFS___Win_NTFS___QNX_Ver_2___Adv_UNIX = pywbem.Uint16(7)
            AIX_Boot___OS__2___Dell__Array____Commodore_DOS = pywbem.Uint16(8)
            AIX_Data__Coherent = pywbem.Uint16(9)
            OS_2_Boot_Manager = pywbem.Uint16(10)
            x32_bit_FAT = pywbem.Uint16(11)
            x32_bit_FAT = pywbem.Uint16(12)
            Microsoft_16_bit_FAT = pywbem.Uint16(14)
            Microsoft_DOS_Extended = pywbem.Uint16(15)
            OPUS___OS_2_2_0 = pywbem.Uint16(16)
            OS_2__MOSS__Inactive_Type_1 = pywbem.Uint16(17)
            Compaq_Diagnostics_Partition___Microsoft = pywbem.Uint16(18)
            OS_2__MOSS__Inactive_Type_4 = pywbem.Uint16(20)
            OS_2__MOSS__Inactive_Type_6 = pywbem.Uint16(22)
            OS_2__MOSS__Inactive_Type_7 = pywbem.Uint16(23)
            OS_2__MOSS__Inactive_Type_B = pywbem.Uint16(27)
            OS_2__MOSS__Inactive_Type_C = pywbem.Uint16(28)
            Microsoft = pywbem.Uint16(33)
            Microsoft = pywbem.Uint16(35)
            Microsoft = pywbem.Uint16(36)
            Microsoft = pywbem.Uint16(38)
            Microsoft = pywbem.Uint16(49)
            Microsoft = pywbem.Uint16(51)
            Microsoft = pywbem.Uint16(52)
            OS_2_Logical_Volume_Manager = pywbem.Uint16(53)
            Microsoft = pywbem.Uint16(54)
            OS_2_JFS_Log = pywbem.Uint16(55)
            PowerQuest = pywbem.Uint16(60)
            VENIX_80286___Series_1_Disk = pywbem.Uint16(64)
            Personal_RISC_Boot = pywbem.Uint16(65)
            Veritas = pywbem.Uint16(66)
            Veritas = pywbem.Uint16(67)
            OnTrack_Disk_Manager_Read_Only_DOS = pywbem.Uint16(80)
            OnTrack_Disk_Manager_Read_Write_DOS = pywbem.Uint16(81)
            CPM___Microport_System_V_386___OnTrack_Disk_Mgr___Microsoft = pywbem.Uint16(82)
            OnTrack_Disk_Manager = pywbem.Uint16(83)
            OnTrack_Disk_Manager_Non_DOS = pywbem.Uint16(84)
            Micro_House_EZ_Drive_Non_DOS = pywbem.Uint16(85)
            Golden_Bow_Vfeature___Microsoft = pywbem.Uint16(86)
            Storage_Dimensions_SpeedStor___Microsoft = pywbem.Uint16(97)
            UNIX___AT_T_System_V_386___SCO_UNIX = pywbem.Uint16(99)
            Novell_NetWare___Speedstore = pywbem.Uint16(100)
            Novell_NetWare = pywbem.Uint16(101)
            Novell_NetWare = pywbem.Uint16(102)
            Novell = pywbem.Uint16(103)
            Novell = pywbem.Uint16(104)
            Novell = pywbem.Uint16(105)
            Microsoft = pywbem.Uint16(113)
            Microsoft = pywbem.Uint16(115)
            Microsoft = pywbem.Uint16(116)
            PC_IX_IBM = pywbem.Uint16(117)
            Microsoft = pywbem.Uint16(118)
            QNX_POSIX = pywbem.Uint16(119)
            QNX_POSIX__Secondary_ = pywbem.Uint16(120)
            QNX_POSIX__Secondary_ = pywbem.Uint16(121)
            Minix____1_4a____Linux___Microsoft = pywbem.Uint16(128)
            Minix____1_4b____Microsoft = pywbem.Uint16(129)
            Linux_Swap___Prime = pywbem.Uint16(130)
            Linux_Native___Apple = pywbem.Uint16(131)
            System_Hibernation_for_APM = pywbem.Uint16(132)
            Microsoft = pywbem.Uint16(134)
            HPFS_FT_mirror = pywbem.Uint16(135)
            Amoeba___Microsoft = pywbem.Uint16(147)
            Amoeba_BBT___Microsoft = pywbem.Uint16(148)
            Microsoft = pywbem.Uint16(161)
            Microsoft = pywbem.Uint16(163)
            Microsoft = pywbem.Uint16(164)
            BSD_386 = pywbem.Uint16(165)
            Microsoft = pywbem.Uint16(166)
            Microsoft = pywbem.Uint16(177)
            Microsoft = pywbem.Uint16(179)
            Microsoft = pywbem.Uint16(180)
            Microsoft = pywbem.Uint16(182)
            BSDI_fs___Microsoft = pywbem.Uint16(183)
            BSDI_Swap___Microsoft = pywbem.Uint16(184)
            Microsoft = pywbem.Uint16(193)
            Microsoft = pywbem.Uint16(196)
            Microsoft = pywbem.Uint16(198)
            Syrinx___HPFS_FT_Disabled_Mirror = pywbem.Uint16(199)
            CP_M_86 = pywbem.Uint16(216)
            Digital_Research_CPM_86___Concurrent_DOS___OUTRIGGER = pywbem.Uint16(219)
            SpeedStor_12_bit_FAT_Extended = pywbem.Uint16(225)
            DOS_Read_Only___Storage_Dimensions = pywbem.Uint16(227)
            SpeedStor_16_bit_FAT_Extended = pywbem.Uint16(228)
            Microsoft = pywbem.Uint16(229)
            Microsoft = pywbem.Uint16(230)
            Intel = pywbem.Uint16(239)
            OS_2_Raw_Data = pywbem.Uint16(240)
            Storage_Dimensions = pywbem.Uint16(241)
            DOS__Secondary_ = pywbem.Uint16(242)
            Microsoft = pywbem.Uint16(243)
            SpeedStor_Large___Storage_Dimensions = pywbem.Uint16(244)
            Microsoft = pywbem.Uint16(246)
            Lan_Step___SpeedStor___IBM_PS_2_IML = pywbem.Uint16(254)
            Bad_Block_Tables = pywbem.Uint16(255)
            Unknown = pywbem.Uint16(65535)

        class TransitioningToState(object):
            Unknown = pywbem.Uint16(0)
            Enabled = pywbem.Uint16(2)
            Disabled = pywbem.Uint16(3)
            Shut_Down = pywbem.Uint16(4)
            No_Change = pywbem.Uint16(5)
            Offline = pywbem.Uint16(6)
            Test = pywbem.Uint16(7)
            Defer = pywbem.Uint16(8)
            Quiesce = pywbem.Uint16(9)
            Reboot = pywbem.Uint16(10)
            Reset = pywbem.Uint16(11)
            Not_Applicable = pywbem.Uint16(12)
            # DMTF_Reserved = ..

        class DataOrganization(object):
            Other = pywbem.Uint16(0)
            Unknown = pywbem.Uint16(1)
            Fixed_Block = pywbem.Uint16(2)
            Variable_Block = pywbem.Uint16(3)
            Count_Key_Data = pywbem.Uint16(4)

        class NameFormat(object):
            Other = pywbem.Uint16(1)
            OS_Device_Name = pywbem.Uint16(12)

        class AvailableRequestedStates(object):
            Enabled = pywbem.Uint16(2)
            Disabled = pywbem.Uint16(3)
            Shut_Down = pywbem.Uint16(4)
            Offline = pywbem.Uint16(6)
            Test = pywbem.Uint16(7)
            Defer = pywbem.Uint16(8)
            Quiesce = pywbem.Uint16(9)
            Reboot = pywbem.Uint16(10)
            Reset = pywbem.Uint16(11)
            # DMTF_Reserved = ..

        class LocationIndicator(object):
            Unknown = pywbem.Uint16(0)
            On = pywbem.Uint16(2)
            Off = pywbem.Uint16(3)
            Not_Supported = pywbem.Uint16(4)

        class PartitionType(object):
            Unknown = pywbem.Uint16(0)
            Primary = pywbem.Uint16(1)
            Extended = pywbem.Uint16(2)
            Logical = pywbem.Uint16(3)

        class Status(object):
            OK = 'OK'
            Error = 'Error'
            Degraded = 'Degraded'
            Unknown = 'Unknown'
            Pred_Fail = 'Pred Fail'
            Starting = 'Starting'
            Stopping = 'Stopping'
            Service = 'Service'
            Stressed = 'Stressed'
            NonRecover = 'NonRecover'
            No_Contact = 'No Contact'
            Lost_Comm = 'Lost Comm'
            Stopped = 'Stopped'

        class EnabledDefault(object):
            Enabled = pywbem.Uint16(2)
            Disabled = pywbem.Uint16(3)
            Not_Applicable = pywbem.Uint16(5)
            Enabled_but_Offline = pywbem.Uint16(6)
            No_Default = pywbem.Uint16(7)
            Quiesce = pywbem.Uint16(9)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 32768..65535

        class EnabledState(object):
            Unknown = pywbem.Uint16(0)
            Other = pywbem.Uint16(1)
            Enabled = pywbem.Uint16(2)
            Disabled = pywbem.Uint16(3)
            Shutting_Down = pywbem.Uint16(4)
            Not_Applicable = pywbem.Uint16(5)
            Enabled_but_Offline = pywbem.Uint16(6)
            In_Test = pywbem.Uint16(7)
            Deferred = pywbem.Uint16(8)
            Quiesce = pywbem.Uint16(9)
            Starting = pywbem.Uint16(10)
            # DMTF_Reserved = 11..32767
            # Vendor_Reserved = 32768..65535

        class AdditionalAvailability(object):
            Other = pywbem.Uint16(1)
            Unknown = pywbem.Uint16(2)
            Running_Full_Power = pywbem.Uint16(3)
            xWarning = pywbem.Uint16(4)
            In_Test = pywbem.Uint16(5)
            Not_Applicable = pywbem.Uint16(6)
            Power_Off = pywbem.Uint16(7)
            Off_Line = pywbem.Uint16(8)
            Off_Duty = pywbem.Uint16(9)
            Degraded = pywbem.Uint16(10)
            Not_Installed = pywbem.Uint16(11)
            Install_Error = pywbem.Uint16(12)
            Power_Save___Unknown = pywbem.Uint16(13)
            Power_Save___Low_Power_Mode = pywbem.Uint16(14)
            Power_Save___Standby = pywbem.Uint16(15)
            Power_Cycle = pywbem.Uint16(16)
            Power_Save___Warning = pywbem.Uint16(17)
            Paused = pywbem.Uint16(18)
            Not_Ready = pywbem.Uint16(19)
            Not_Configured = pywbem.Uint16(20)
            Quiesced = pywbem.Uint16(21)

        class StatusInfo(object):
            Other = pywbem.Uint16(1)
            Unknown = pywbem.Uint16(2)
            Enabled = pywbem.Uint16(3)
            Disabled = pywbem.Uint16(4)
            Not_Applicable = pywbem.Uint16(5)

        class PowerManagementCapabilities(object):
            Unknown = pywbem.Uint16(0)
            Not_Supported = pywbem.Uint16(1)
            Disabled = pywbem.Uint16(2)
            Enabled = pywbem.Uint16(3)
            Power_Saving_Modes_Entered_Automatically = pywbem.Uint16(4)
            Power_State_Settable = pywbem.Uint16(5)
            Power_Cycling_Supported = pywbem.Uint16(6)
            Timed_Power_On_Supported = pywbem.Uint16(7)

        class PrimaryStatus(object):
            Unknown = pywbem.Uint16(0)
            OK = pywbem.Uint16(1)
            Degraded = pywbem.Uint16(2)
            Error = pywbem.Uint16(3)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 0x8000..

        class SetPowerState(object):
            class PowerState(object):
                Full_Power = pywbem.Uint16(1)
                Power_Save___Low_Power_Mode = pywbem.Uint16(2)
                Power_Save___Standby = pywbem.Uint16(3)
                Power_Save___Other = pywbem.Uint16(4)
                Power_Cycle = pywbem.Uint16(5)
                Power_Off = pywbem.Uint16(6)

        class NameNamespace(object):
            Other = pywbem.Uint16(1)
            OS_Device_Namespace = pywbem.Uint16(8)

        class OperationalStatus(object):
            Unknown = pywbem.Uint16(0)
            Other = pywbem.Uint16(1)
            OK = pywbem.Uint16(2)
            Degraded = pywbem.Uint16(3)
            Stressed = pywbem.Uint16(4)
            Predictive_Failure = pywbem.Uint16(5)
            Error = pywbem.Uint16(6)
            Non_Recoverable_Error = pywbem.Uint16(7)
            Starting = pywbem.Uint16(8)
            Stopping = pywbem.Uint16(9)
            Stopped = pywbem.Uint16(10)
            In_Service = pywbem.Uint16(11)
            No_Contact = pywbem.Uint16(12)
            Lost_Communication = pywbem.Uint16(13)
            Aborted = pywbem.Uint16(14)
            Dormant = pywbem.Uint16(15)
            Supporting_Entity_in_Error = pywbem.Uint16(16)
            Completed = pywbem.Uint16(17)
            Power_Mode = pywbem.Uint16(18)
            Relocating = pywbem.Uint16(19)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 0x8000..

        class OperatingStatus(object):
            Unknown = pywbem.Uint16(0)
            Not_Available = pywbem.Uint16(1)
            Servicing = pywbem.Uint16(2)
            Starting = pywbem.Uint16(3)
            Stopping = pywbem.Uint16(4)
            Stopped = pywbem.Uint16(5)
            Aborted = pywbem.Uint16(6)
            Dormant = pywbem.Uint16(7)
            Completed = pywbem.Uint16(8)
            Migrating = pywbem.Uint16(9)
            Emigrating = pywbem.Uint16(10)
            Immigrating = pywbem.Uint16(11)
            Snapshotting = pywbem.Uint16(12)
            Shutting_Down = pywbem.Uint16(13)
            In_Test = pywbem.Uint16(14)
            Transitioning = pywbem.Uint16(15)
            In_Service = pywbem.Uint16(16)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 0x8000..

        class RequestStateChange(object):
            Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown_or_Unspecified_Error = pywbem.Uint32(2)
            Cannot_complete_within_Timeout_Period = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            Invalid_State_Transition = pywbem.Uint32(4097)
            Use_of_Timeout_Parameter_Not_Supported = pywbem.Uint32(4098)
            Busy = pywbem.Uint32(4099)
            # Method_Reserved = 4100..32767
            # Vendor_Specific = 32768..65535
            class RequestedState(object):
                Enabled = pywbem.Uint16(2)
                Disabled = pywbem.Uint16(3)
                Shut_Down = pywbem.Uint16(4)
                Offline = pywbem.Uint16(6)
                Test = pywbem.Uint16(7)
                Defer = pywbem.Uint16(8)
                Quiesce = pywbem.Uint16(9)
                Reboot = pywbem.Uint16(10)
                Reset = pywbem.Uint16(11)
                # DMTF_Reserved = ..
                # Vendor_Reserved = 32768..65535

        class ExtentStatus(object):
            Other = pywbem.Uint16(0)
            Unknown = pywbem.Uint16(1)
            None_Not_Applicable = pywbem.Uint16(2)
            Broken = pywbem.Uint16(3)
            Data_Lost = pywbem.Uint16(4)
            Dynamic_Reconfig = pywbem.Uint16(5)
            Exposed = pywbem.Uint16(6)
            Fractionally_Exposed = pywbem.Uint16(7)
            Partially_Exposed = pywbem.Uint16(8)
            Protection_Disabled = pywbem.Uint16(9)
            Readying = pywbem.Uint16(10)
            Rebuild = pywbem.Uint16(11)
            Recalculate = pywbem.Uint16(12)
            Spare_in_Use = pywbem.Uint16(13)
            Verify_In_Progress = pywbem.Uint16(14)
            In_Band_Access_Granted = pywbem.Uint16(15)
            Imported = pywbem.Uint16(16)
            Exported = pywbem.Uint16(17)
            Relocating = pywbem.Uint16(18)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 32768..65535

        class SignatureState(object):
            Unknown = '0'
            Unimplemented = '1'
            Uninitialized = '2'
            Calculated_by_Operating_System = '3'
            Calculated_by_a_Media_Manager = '4'
            Assigned_by_Owning_Application = '5'

        class Availability(object):
            Other = pywbem.Uint16(1)
            Unknown = pywbem.Uint16(2)
            Running_Full_Power = pywbem.Uint16(3)
            xWarning = pywbem.Uint16(4)
            In_Test = pywbem.Uint16(5)
            Not_Applicable = pywbem.Uint16(6)
            Power_Off = pywbem.Uint16(7)
            Off_Line = pywbem.Uint16(8)
            Off_Duty = pywbem.Uint16(9)
            Degraded = pywbem.Uint16(10)
            Not_Installed = pywbem.Uint16(11)
            Install_Error = pywbem.Uint16(12)
            Power_Save___Unknown = pywbem.Uint16(13)
            Power_Save___Low_Power_Mode = pywbem.Uint16(14)
            Power_Save___Standby = pywbem.Uint16(15)
            Power_Cycle = pywbem.Uint16(16)
            Power_Save___Warning = pywbem.Uint16(17)
            Paused = pywbem.Uint16(18)
            Not_Ready = pywbem.Uint16(19)
            Not_Configured = pywbem.Uint16(20)
            Quiesced = pywbem.Uint16(21)

## end of class LMI_LogicalMBRPartitionProvider

## get_providers() for associating CIM Class Name to python provider class name

def get_providers(env):
    initAnaconda(False)
    LMI_logicalmbrpartition_prov = LMI_DiskPartition(env)
    return {'LMI_DiskPartition': LMI_logicalmbrpartition_prov}
