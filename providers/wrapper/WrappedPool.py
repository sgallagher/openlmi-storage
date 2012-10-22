# OpenLMI Storage Provider
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

"""Python Provider for LMI_*Pool"""

import pywbem
from pywbem.cim_provider2 import CIMProvider2

class WrappedPool(CIMProvider2):
    """Instrument the CIM class LMI_*Pool """

    def __init__ (self, env, wrapper):
        logger = env.get_logger()
        logger.log_debug('Initializing provider %s from %s' \
                % (self.__class__.__name__, __file__))
        self.wrapper = wrapper
        super(WrappedPool, self).__init__()

    def get_instance(self, env, model):
        logger = env.get_logger()
        logger.log_debug('Entering %s.get_instance()' \
                % self.__class__.__name__)

        device = self.wrapper.getDevice(model)
        if device is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "InstanceID not found.")
        
        return self.wrapper.getPoolInstance(env, model, device)

    def enum_instances(self, env, model, keys_only):
        logger = env.get_logger()
        logger.log_debug('Entering %s.enum_instances()' \
                % self.__class__.__name__)
                
        model.path.update({'InstanceID': None})
        for model in self.wrapper.enumPools(env, model, keys_only):
            yield model

    def set_instance(self, env, instance, modify_existing):
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED) # Remove to implement

    def delete_instance(self, env, instance_name):
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED) # Remove to implement
        
    def cim_method_getsupportedsizes(self, env, object_name,
                                     param_elementtype=None,
                                     param_goal=None,
                                     param_sizes=None):
        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_getsupportedsizes()' \
                % self.__class__.__name__)

        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        
    def cim_method_getsupportedsizerange(self, env, object_name,
                                         param_minimumvolumesize=None,
                                         param_maximumvolumesize=None,
                                         param_elementtype=None,
                                         param_volumesizedivisor=None,
                                         param_goal=None):
        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_getsupportedsizerange()' \
                % self.__class__.__name__)

        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        
    def cim_method_getavailableextents(self, env, object_name,
                                       param_goal=None):
        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_getavailableextents()' \
                % self.__class__.__name__)

        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        
    class Values(object):
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

        class DetailedStatus(object):
            Not_Available = pywbem.Uint16(0)
            No_Additional_Information = pywbem.Uint16(1)
            Stressed = pywbem.Uint16(2)
            Predictive_Failure = pywbem.Uint16(3)
            Non_Recoverable_Error = pywbem.Uint16(4)
            Supporting_Entity_in_Error = pywbem.Uint16(5)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 0x8000..

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

        class SpaceLimitDetermination(object):
            Allocated = pywbem.Uint16(2)
            Quote = pywbem.Uint16(3)
            Limitless = pywbem.Uint16(4)

        class GetSupportedSizeRange(object):
            Method_completed_OK = pywbem.Uint32(0)
            Method_not_supported = pywbem.Uint32(1)
            Use_GetSupportedSizes_instead = pywbem.Uint32(2)
            Invalid_Element_Type = pywbem.Uint32(3)
            class ElementType(object):
                Storage_Pool = pywbem.Uint16(2)
                Storage_Volume = pywbem.Uint16(3)
                Logical_Disk = pywbem.Uint16(4)
                Thin_Provisioned_Volume = pywbem.Uint16(5)
                Thin_Provisioned_Logical_Disk = pywbem.Uint16(6)

        class ResourceType(object):
            Other = pywbem.Uint16(1)
            Computer_System = pywbem.Uint16(2)
            Processor = pywbem.Uint16(3)
            Memory = pywbem.Uint16(4)
            IDE_Controller = pywbem.Uint16(5)
            Parallel_SCSI_HBA = pywbem.Uint16(6)
            FC_HBA = pywbem.Uint16(7)
            iSCSI_HBA = pywbem.Uint16(8)
            IB_HCA = pywbem.Uint16(9)
            Ethernet_Adapter = pywbem.Uint16(10)
            Other_Network_Adapter = pywbem.Uint16(11)
            I_O_Slot = pywbem.Uint16(12)
            I_O_Device = pywbem.Uint16(13)
            Floppy_Drive = pywbem.Uint16(14)
            CD_Drive = pywbem.Uint16(15)
            DVD_drive = pywbem.Uint16(16)
            Disk_Drive = pywbem.Uint16(17)
            Tape_Drive = pywbem.Uint16(18)
            Storage_Extent = pywbem.Uint16(19)
            Other_storage_device = pywbem.Uint16(20)
            Serial_port = pywbem.Uint16(21)
            Parallel_port = pywbem.Uint16(22)
            USB_Controller = pywbem.Uint16(23)
            Graphics_controller = pywbem.Uint16(24)
            IEEE_1394_Controller = pywbem.Uint16(25)
            Partitionable_Unit = pywbem.Uint16(26)
            Base_Partitionable_Unit = pywbem.Uint16(27)
            Power = pywbem.Uint16(28)
            Cooling_Capacity = pywbem.Uint16(29)
            Ethernet_Switch_Port = pywbem.Uint16(30)
            Logical_Disk = pywbem.Uint16(31)
            Storage_Volume = pywbem.Uint16(32)
            Ethernet_Connection = pywbem.Uint16(33)
            # DMTF_reserved = ..
            # Vendor_Reserved = 0x8000..0xFFFF

        class GetAvailableExtents(object):
            Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            # Method_Reserved = 4098..32767
            # Vendor_Specific = 32768..65535

        class CommunicationStatus(object):
            Unknown = pywbem.Uint16(0)
            Not_Available = pywbem.Uint16(1)
            Communication_OK = pywbem.Uint16(2)
            Lost_Communication = pywbem.Uint16(3)
            No_Contact = pywbem.Uint16(4)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 0x8000..

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

        class Usage(object):
            Other = pywbem.Uint16(1)
            Unrestricted = pywbem.Uint16(2)
            Reserved_for_ComputerSystem__the_block_server_ = pywbem.Uint16(3)
            Reserved_as_a_Delta_Replica_Container = pywbem.Uint16(4)
            Reserved_for_Migration_Services = pywbem.Uint16(5)
            Reserved_for_Local_Replication_Services = pywbem.Uint16(6)
            Reserved_for_Remote_Replication_Services = pywbem.Uint16(7)
            Reserved_for_Sparing = pywbem.Uint16(8)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 32768..65535

        class GetSupportedSizes(object):
            Method_completed_OK = pywbem.Uint32(0)
            Method_not_supported = pywbem.Uint32(1)
            Use_GetSupportedSizes_instead = pywbem.Uint32(2)
            Invalid_Element_Type = pywbem.Uint32(3)
            class ElementType(object):
                Storage_Pool = pywbem.Uint16(2)
                Storage_Volume = pywbem.Uint16(3)
                Logical_Disk = pywbem.Uint16(4)
                Thin_Provisioned_Volume = pywbem.Uint16(5)
                Thin_Provisioned_Logical_Disk = pywbem.Uint16(6)

        class PrimaryStatus(object):
            Unknown = pywbem.Uint16(0)
            OK = pywbem.Uint16(1)
            Degraded = pywbem.Uint16(2)
            Error = pywbem.Uint16(3)
            # DMTF_Reserved = ..
            # Vendor_Reserved = 0x8000..

## end of class LMI_RAIDPoolProvider