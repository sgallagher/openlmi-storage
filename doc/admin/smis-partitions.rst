SMI-S Disk Partition Subprofile
===============================

Profile adjustment
------------------

The Disk Partition Subprofile does not reflect real-world MBR partition tables:

* The profile specifies, there can be up to 4 primary partitions (correct),
  one of them can be extended (correct) and up to 4 logical partitions can be
  instantiated on this extended partition (wrong, number of logical partitions
  is not limited).

* The profile specifies that logical partition metadata is on the beginning of
  the extended partition (see Figure 7 in the profile). In reality, each
  logical partition has its own metadata sector just before the partition. In
  addition, there can be number of empty sectors between the logical partition
  metadata and the partition beginning, which are left as result of alignment
  rules.

As result of this deficiency, some adjustments were necessary:

* The ``LMI_DiskPartition`` representing a logical partition *includes* the
  metadata sector and any alignment sectors.

 * ``NumberOfBlocks`` property *includes* the metadata and any alignment
   sectors.
 * ``ConsumableBlocks`` includes only the real usable data on partition.

.. figure:: pic/partitions.png

   Correct overview of logical partitions.

GPT partition tables do not have these issues and are generally preferred over
MBR ones.

Implementation
--------------
All mandatory classes and methods are implemented.

TODO

.. warning:: Mandatory indications are not implemented.

   Anaconda does not provide such functionality and it would be very CPU-intensive
   to periodically scan for new/deleted partitions.
