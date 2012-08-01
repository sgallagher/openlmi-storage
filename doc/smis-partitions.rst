SMI-S Disk Partition Subprofile
===============================

Profile adjustment
------------------

The Disk Partition Subprofile does not reflect real-world MBR partition tables:

* The profile specifies, there can be up to 4 primary partitions (correct), one
  of them can be extended (correct) and up to 4 logical partitions can be
  instantiated on this extended partition (wrong, number of logical partitions
  is not limited).

* The profile specifies that logical partition metadata is on the beginning of
  the extended partition (see Figure 7 in the profile). In reality, each
  logical partition has its own metadata sector just before the partition. In
  addition, there can be number of empty sectors between the logical partition
  metadata and the partition beginning, which are left as result of alignment
  rules.

As result of this deficiency, some adjustments were necessary:

* The ``Cura_DiskPartition`` representing a logical partition *includes* the
  metadata sector and any alignment sectors.

* The ``Cura_PartitionExtent`` (= ``CIM_LogicalDisk``) allocated from the
  ``Cura_DiskPartition`` includes only the real partition data.

.. figure:: pic/partitions.png

   Correct overview of logical partitions.

GPT partition tables do not have these issues and are generally preferred
over MBR ones.

Implementation
--------------
All mandatory classes and methods are implemented:

=============================================== ==========================================
SMI-S                                           Cura
=============================================== ==========================================
CIM_BasedOn                                     Cura_PartitionBasedOnLocalDiskExtent
CIM_BasedOn                                     Cura_PartitionBasedOnPartition
CIM_DiskPartitionConfigurationCapabilities      Cura_DiskPartitionConfigurationCapabilities
CIM_DiskPartitionConfigurationService           Cura_DiskPartitionConfigurationService
CIM_ElementCapabilities                         Cura_PartitionElementCapabilities
CIM_GenericPartition                            N/A
CIM_HostedService                               Cura_HostedService
CIM_InstalledPartitionTable                     Cura_InstalledParititionTable
CIM_LogicalDisk                                 Cura_PartitionExtent [#1]_
CIM_LogicalDiskBasedOnPartition                 Cura_PartitionExtentBasedOnPartition
CIM_StorageExtent                               Cura_StorageExtent
CIM_SystemDevice                                Cura_SystemDevice
=============================================== ==========================================

.. warning:: Mandatory indications are not implemented.

   Anaconda does not provide such functionality and it would be very CPU-intensive
   to periodically scan for new/deleted partitions.

.. rubric:: Footnotes

.. [#1] This LogicalDisk descendant should not be directly used, see
   :doc:`smis-block`.
