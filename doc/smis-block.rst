SMI-S Block Services Package
============================

This package is core of SMI-S. It describes how devices (disks) are grouped
together into pools with different capabilities and even hierarchy of pools
can be built. Logical disks (=storage elements, usable by OS) are then
allocated from these pools.

    A StoragePool is a storage element; its storage capacity has a given set
    of capabilities. Those ‘StorageCapabilities’ indicate the 'Quality of
    Service' requirements that can be applied to objects created from the
    StoragePool.

Primordial pool
----------------
At the lowest level of hierarchy of SMI-S storage pools are primordial devices
and pools.

    A primordial StoragePool is a type of StoragePool that contains
    unformatted, unprepared, or unassigned capacity. Storage capacity is drawn
    from the primordial StoragePool to create concrete StoragePools. A
    primordial StoragePool aggregates storage capacity not assigned to a
    concrete StoragePool. StorageVolumes and LogicalDisks are allocated from
    concrete StoragePools.

    At least one primordial StoragePool shall always exists on the block storage
    system to represent the unallocated storage on the storage device.

In SMI-S world, a storage system consists of *raw disks* or similar block
devices. These are put into the primordial pool and further allocated as needed. 

On Linux, we have disks and partitions. If *disks* were primordial, we would not
have any possibility to partition them. Therefore it seems it's the best to have
**disk partitions and  unpartitioned disks as primordial**.

This gets even more complicated with implementation of Disk Partition
Subprofile – only the top LogicalDisk is primordial. That's why the top
LogicalDisk is named as ``LMI_PartitionExtent`` and should not be used directly.

.. note:: Anaconda does not support unpartitioned disks, therefore only
   partitions are primordial for now.

.. figure:: pic/primordial.png

   Instance diagram of primordial pool with three partitions.

.. warning:: This probably violates SMI-S, only raw disk devices should be
   primordial. In addition, the hierarchy is quite ugly and complicated.

Pool hierarchy
--------------
SMI-S is based on building of hierarchy of storage pools, each pool adding
some storage capability (e.g. RAID1 redundancy). At the top level, LogicalDisks
are allocated from the pools and these LogicalDisks are then usable by OS, e.g.
for filesystems.

This model fairly describes our Linux storage  - we have storage layers too,
various kernel devices can be stacked on
top of each other. E.g. a logical volume is allocated from a volume group, which
is based on top of RAID1, which is built on top
of two partitions, which are primordial in our model.

Therefore we can model our storage layers - LVM, VG, crypto, RAID, ... - as
StoragePools, allocated from underlying storage layers (= other StoragePools).

In SMI-S, StoragePools represent generic storage block, which can be
arbitrarily allocated - e.g. several LogicalDisks can be allocated from one
StoragePool. On Linux, we cannot divide e.g. RAID volume into several disks, at
least not without a volume group in between. Therefore it's possible to use the
RAID volume only as whole.

.. note:: Allocating StoragePools as whole is *probably* supported by SMI-S, but
   it's somewhat weird and against SMI-S idea.

Some storage pools, e.g. volume groups, can be allocated arbitrarily.

.. figure:: pic/raidlvm.png

   Instance diagram of LVM on top of RAID.

.. note:: This example is completely artificial, RAID built on top of two
   partitions on the same disks is not very useful, it just shows the principle
   of layering storage pools and appropriate associated extents.

Admin can create new layer (e.g. RAID or volume group) in the pool hierarchy using
``LMI_StorageConfigurationService.CreateOrModifyStoragePool()``, providing
either list of base StorageExtents or StoragePools or both.

Logical disks
-------------
In SMI-S, only LogicalDisks instances can be used by the OS. I.e. if an
admin wants to build a filesystem e.g. on RAIDCompositeExtent, in
SMI-S it's necessary to allocate a LogicalDisk from it. As we already covered in
the previous section, the RAIDCompositeExtent must be allocated as whole, it's
not possible to allocate only part of it without a volume group on top of the
RAID. The resulting LogicalDisk represents the same storage capacity as the
underlying RAID /dev/md0, it's just artificial object to satisfy the SMI-S
standard.

.. figure:: pic/raid.png

   Instance diagram of LogicalDisk allocated from RAID.

LogicalDisks are allocated using
``StorageConfigurationService.CreateOrMofifyElementFromStoragePool()``. This
allocated LogicalDisk is persistent, i.e. it survives OpenLMI restart.

If an admin creates a filesystem on /dev/md0 directly, not using SMI-S,
appropriate LogicalDisk automatically appears between the RAIDCompositeExtent
and the LocalFilesystem.

In other words, OpenLMI shows a LogicalDisk for all block devices previously exposed
by ``StorageConfigurationService.CreateOrModifyElementFromStoragePool()`` and
for all devices with filesystems.

LogicalDisks allocated from a volume group, i.e. logical volumes, are
different - they are represented as instances of ``LMI_LVLogicalDisk`` class
and can be used as input extents for creating a new StoragePool (e.g. to have
dm-crypt based on a logical volume or even RAID on top of a logical volume).


Logical disks on partitions
^^^^^^^^^^^^^^^^^^^^^^^^^^^
SMI-S requests that a LogicalDisk
must be allocated from a concrete storage pool. Therefore it is not possible
to directly allocate a partition from the primordial storage pool.
There must be a concrete storage pool in between.

.. figure:: pic/exposed-partition-smis.png

   SMI-S instance diagram of LogicalDisk allocated from disk partition.

This adds completely useless additional layer to the model, therefore we
decided to skip this concrete pool and if a disk partition is used by the OS
(i.e. there is a filesystem on it), it's allocated directly from the primordial
storage pool.

.. figure:: pic/exposed-partition-openlmi.png

   OpenLMI instance diagram of LogicalDisk allocated from disk partition.

.. warning:: This primordial pool usage contradicts SMI-S Block Services Package
   It would not be difficult to add the concrete pool though, it's just few
   additional classes.

Implementation
--------------
Most of the mandatory SMI-S classes are implemented, but not all mandatory
methods. Only RAID and LVM is implemented for now.

Mapping:

=============================================== =================================================
SMI-S                                           OpenLMI
=============================================== =================================================
CIM_AllocatedFromStoragePool                    LMI_RAIDAllocatedFromStoragePool
                                                LMI_LVAllocatedFromStoragePool
                                                LMI_VGAllocatedFromStoragePool
                                                LMI_LogicalDiskAllocatedFromStoragePool
CIM_ElementCapabilities                         LMI_RAIDStorageElementCapabilities
                                                LMI_PrimordialStorageElementCapabilities
                                                LMI_VGStorageElementCapabilities
                                                LMI_GlobalStorageConfigurationElementCapabilities
CIM_ElementSettingData                          *not yet implemented*
CIM_HostedStoragePool                           LMI_HostedStoragePool
CIM_LogicalDisk                                 LMI_LogicalDisk
                                                LMI_LVLogicalDisk
CIM_StorageCapabilities                         LMI_StorageCapabilities
                                                LMI_VGStorageCapabilities
                                                LMI_RAIDStorageCapabilities
                                                LMI_PrimordialStorageCapabilities
CIM_StorageConfigurationService                 LMI_StorageConfigurationService
CIM_StorageConfigurationCapabilities            LMI_GlobalStorageConfigurationCapabilities
CIM_StoragePool                                 LMI_RAIDPool
                                                LMI_PrimordialPool
                                                LMI_VGPool
CIM_StorageSetting                              LMI_StorageSetting
CIM_StorageSettingsAssociatedToCapabilities     *not yet implemented*
CIM_StorageSettingsGeneratedFromCapabilities    *not yet implemented*
CIM_SystemDevice                                LMI_SystemDevice
=============================================== =================================================

Methods:

======================================= =========================================== ================
Class                                        Status
======================================= =========================================== ================
StorageCapabilities                     CreateSetting                               done
  ...                                   GetSupportedStripeLengths                   TODO? (optional)
  ...                                   GetSupportedStripeLengthRange               TODO? (optional)
  ...                                   GetSupportedStripeDepths                    N/A? (optional)
  ...                                   GetSupportedStripeDepthRange                N/A? (optional)
  ...                                   GetSupportedParityLayouts                   N/A? (optional)
StorageConfigurationService             CreateOrModifyStoragePool                   done [#1]_ 
  ...                                   DeleteStoragePool                           done? [#2]_
  ...                                   CreateOrModifyElementFromStoragePool        done [#3]_
  ...                                   CreateOrModifyElementFromElements           N/A?
  ...                                   ReturnToStoragePool                         TODO
  ...                                   RequestUsageChange                          N/A?
  ...                                   GetElementsBasedOnUsage                     N/A?
  ...                                   GetSupportedSizes                           TODO
  ...                                   GetSupportedSizeRanges                      TODO
  ...                                   GetAvailableExtents                         TODO
======================================= =========================================== ================

.. warning:: Mandatory indications are **not** implemented.

.. warning:: To distinguish creation of RAID0 and volume group, new property to
   LMI_StorageSetting had to be added. This property tells, if resulting
   StoragePool is to be allocated as whole (=RAID0) or multiple LogicalDisks can
   be allocated from it (=volume group)

.. [#1] With appropriate ``LMI_StorageSetting``, it can create RAID or volume group
   or any other storage layer.
.. [#2] Deletes RAID or volume group (if empty).
.. [#3] Allocates a LogicalDisk, either ``LMI_LogicalDisk`` or
   ``LMI_LVLogicalDisk`` (=logical volume)

Usage
-----

Create RAID or volume group:

#. Acquire LMI_StorageSetting

  * Either find appropriate LMI_StorageSetting, there are some pre-configured
    for most typical RAID types.

  * Or create new setting:

    #. Find appropriate LMI_StorageCapabilities and call its CreateSetting() method.

    #. Modify the setting.

    #. Setting with ChangeableType = Persistent will be saved to disk and will survive OpenLMI restart.

  * For RAID0, use:

    .. parsed-literal::
       DataRedundancyGoal = 1
       PackageRedundancyGoal = 0
       NoSinglePointOfFailure = False
       LMIAllocationType = 1

  * For volume group, use:

    .. parsed-literal::
      DataRedundancyGoal = 1
      NoSinglePointOfFailure = False
      PackageRedundancyGoal = 0
      LMIAllocationType = 0

    (notice that only LMIAllocationType is different to RAID0 setting)

  * For RAID1, use:

    .. parsed-literal::
       DataRedundancyGoal = nr. of devices in the RAID
       NoSinglePointOfFailure = True
       PackageRedundancyGoal = nr. of devices in the RAID - 1
       LMIAllocationType = 1 (or NULL)

  * For RAID5, use:

    .. parsed-literal::
       DataRedundancyGoal = 1
       PackageRedundancyGoal = 1
       PackageRedundancyGoal = 1
       LMIAllocationType = 1 (or NULL)

#. Call LMI_StorageConfigurationService.CreateOrModifyStoragePool with following
   parameters:

   .. parsed-literal::
      ElementName = NULL for RAID, kernel will assign any /dev/mdX 
      ElementName = <name of the volume group> for volume group
      Goal = refrence to your LMI_StorageSetting from previous step
      InPools = list of pools to create the pool from. It can be the primordial
                pool (all unused partitions will be added to the new pool) or any other
                pool (whole device will be added to the new pool).
      InExtents = list of extents to create the pool from. You can e.g. specify
                  explicit parition this way.
      Pool = NULL, pool modification is not supported now
      Size = expected size of the new pool, can be NULL.

   Both InPools and InExtents can be used. All Anaconda devices, represented by
   the pools and extents (i.e. 'union' of both, not 'intersection'), will be
   then used to create the device. The most safe is to use InExtents only - you
   can exactly choose, which partitions will be used.

   Size parameter is only checked, it is not used to select the right devices
   from InPools or InExtents.

   This method is synchronous (for now) and never returns a job.

Delete RAID or volume group:

#. the appropriate StoragePool must be unused, i.e. no device (StoragePool,
   StorageExtent or LogicalDisk) can be allocated from it.

#. Call StorageConfigurationService.DeleteStoragePool().


Allocate a LogicalDisk from a StoragePool:

#. Create LMI_StorageSetting like when creating RAID0

#. Call StorageConfigurationService.CreateOrModifyElementFromStoragePool() with these
   parameters:

   * allocating LMI_LVLolgicalDisk (= logical volume):

     .. parsed-literal::
        ElementName = name of the logical volume
        Goal = the LMI_StorageSetting
        InPool = the pool to allocate from (i.e. reference to LMI_VGPool)
        ElementType = 4
        Size = size of the volume, in bytes

   * allocating LMI_LogicalDisk for a partition from the primordial pool:

     .. parsed-literal::
        ElementName = NULL
        Goal = the LMI_StorageSetting
        InPool = the primordial pool
        ElementType = 4
        Size = size of the partition to allocate

     It is not possible to specify, which partition to allocate! Any partition
     with given size will be allocated.

   * allocating LMI_LogicalDisk from any other StoragePool (e.g. RAIDPool):

     .. parsed-literal::
        ElementName = NULL
        Goal = the LMI_StorageSetting
        InPool = the pool
        ElementType = 4
        Size = size of the pool

     Only whole pool can be allocated!

As alrady noted, LMI_LogicalDisk is artificial object only and represents the
same Linux device as underlying StoragePool (or LMI_PartitionExtent).




