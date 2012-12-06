SMI-S profiles
==============

OpenLMI-Storage implements following profiles:

.. toctree::
   :maxdepth: 2

   smis-partitions
   smis-block
   smis-composition

The CIM API follows following principles:

- Each block device is represented by exactly one StorageExtent.
 - For example RAID devices are created using
   ``StorageConfigurationService.CreateOrModifyElementFromElements()``, without
   any pool.
 - No LogicalDisk is created for devices consumed by the OS, i.e. when there
   is filesystem on them.
  - Actually, all block devices can be used by the OS and it might be useful
    to have LMI_StorageExtent as subclass of CIM_LogicalDisk. .. warning:: This
    violates SMI-S, each block device should have a StorageExtent + LogicalDisk
    associated from it to be usable by the OS.
- StoragePool is used for real pool objects - volume groups.
- PrimordialPool is created, it contains unpartitioned disks and disk
  partitions.
 - Nothing can be allocated from it, it just shows unused space.

The implementation is not complete, e.g. mandatory Server Profile is not
implemented at all. The list will get updated.
