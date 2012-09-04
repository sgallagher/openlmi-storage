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

"""Python Provider for LMI_*Pool """

import pywbem
from pywbem.cim_provider2 import CIMProvider2

class WrappedExtent(CIMProvider2):
    """Instrument the CIM class LMI_*Extent"""

    def __init__ (self, env, wrapper):
        logger = env.get_logger()
        logger.log_debug('Initializing provider %s from %s' \
                % (self.__class__.__name__, __file__))
        self.wrapper = wrapper
        super(WrappedExtent, self).__init__()

    def get_instance(self, env, model):
        logger = env.get_logger()
        logger.log_debug('Entering %s.get_instance()' \
                % self.__class__.__name__)
        
        device = self.wrapper.getDevice(model)
        if device is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "Device not found.")
        
        return self.wrapper.getExtentInstance(env, model, device)

    def enum_instances(self, env, model, keys_only):
        logger = env.get_logger()
        logger.log_debug('Entering %s.enum_instances()' \
                % self.__class__.__name__)
        model.path.update({'CreationClassName': None, 'SystemName': None,
            'DeviceID': None, 'SystemCreationClassName': None})
        for model in self.wrapper.enumExtents(env, model, keys_only):
            yield model



    def set_instance(self, env, instance, modify_existing):
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED) # Remove to implement

    def delete_instance(self, env, instance_name):
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED) # Remove to implement
        
    def cim_method_reset(self, env, object_name):
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        
    def cim_method_requeststatechange(self, env, object_name,
                                      param_requestedstate=None,
                                      param_timeoutperiod=None):
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        
    def cim_method_setpowerstate(self, env, object_name,
                                 param_powerstate=None,
                                 param_time=None):
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        
    def cim_method_quiescedevice(self, env, object_name,
                                 param_quiesce=None):
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        
    def cim_method_enabledevice(self, env, object_name,
                                param_enabled=None):
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        
    def cim_method_onlinedevice(self, env, object_name,
                                param_online=None):
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        
    def cim_method_saveproperties(self, env, object_name):
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        
    def cim_method_restoreproperties(self, env, object_name):
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        
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
            Unknown = pywbem.Uint16(0)
            Other = pywbem.Uint16(1)
            VPD83NAA6 = pywbem.Uint16(2)
            VPD83NAA5 = pywbem.Uint16(3)
            VPD83Type2 = pywbem.Uint16(4)
            VPD83Type1 = pywbem.Uint16(5)
            VPD83Type0 = pywbem.Uint16(6)
            SNVM = pywbem.Uint16(7)
            NodeWWN = pywbem.Uint16(8)
            NAA = pywbem.Uint16(9)
            EUI64 = pywbem.Uint16(10)
            T10VID = pywbem.Uint16(11)
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
            _Warning = pywbem.Uint16(4)
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
            Unknown = pywbem.Uint16(0)
            Other = pywbem.Uint16(1)
            VPD83Type3 = pywbem.Uint16(2)
            VPD83Type2 = pywbem.Uint16(3)
            VPD83Type1 = pywbem.Uint16(4)
            VPD80 = pywbem.Uint16(5)
            NodeWWN = pywbem.Uint16(6)
            SNVM = pywbem.Uint16(7)
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

        class Availability(object):
            Other = pywbem.Uint16(1)
            Unknown = pywbem.Uint16(2)
            Running_Full_Power = pywbem.Uint16(3)
            _Warning = pywbem.Uint16(4)
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

## end of class LMI_RAIDCompositeExtentProvider
