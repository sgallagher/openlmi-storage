SMI-S Block Services Package
============================

This package is core of SMI-S. It describes how devices (disks) are grouped
together into pools with different capabilities and even hierarchy of pools can
be built.

    A StoragePool is a storage element; its storage capacity has a given set
    of capabilities. Those ‘StorageCapabilities’ indicate the 'Quality of
    Service' requirements that can be applied to objects created from the
    StoragePool.

Storage on Linux does not use pool concept except Volume Groups, therefore we
allow to create storage devices directly from other storage devices, e.g.
create MD RAID from partitions.

Primordial pool
---------------
At the lowest level of hierarchy of SMI-S storage pools are primordial devices
and pools.

    A primordial StoragePool is a type of StoragePool that contains
    unformatted, unprepared, or unassigned capacity. Storage capacity is drawn
    from the primordial StoragePool to create concrete StoragePools. A
    primordial StoragePool aggregates storage capacity not assigned to a
    concrete StoragePool. StorageVolumes and LogicalDisks are allocated from
    concrete StoragePools.

    At least one primordial StoragePool shall always exists on the block
    storage system to represent the unallocated storage on the storage device.

In SMI-S world, a storage system consists of *raw disks* or similar block
devices. These are put into the primordial pool and further allocated as
needed.

On Linux, we have disks and partitions. If *disks* were primordial, we would not
have any possibility to partition them. Therefore it seems it's the best to
have **disk partitions and  unpartitioned disks as primordial**.

.. note:: Anaconda does not support unpartitioned disks, therefore only
   partitions are primordial for now.

.. figure:: pic/primordial.png

   Instance diagram of primordial pool with three partitions.

.. warning:: This probably violates SMI-S, only raw disk devices should be
   primordial. In addition, the hierarchy is quite ugly and complicated.

Logical disks
-------------
In SMI-S, only LogicalDisks instances can be used by the OS. I.e. if an admin
wants to build a filesystem e.g. on RAIDCompositeExtent, in SMI-S it's
necessary to allocate a LogicalDisk from it.

We find this approach useless and we don't allocate LogicalDisks for devices,
which can be used by the OS. In fact, any block device can be used by the OS,
therefore it would make sense to make ``LMI_StorageExtent`` as subclass of
``CIM_LogicalDisk``.

Implementation
--------------
TODO

.. warning:: Mandatory indications are **not** implemented.

