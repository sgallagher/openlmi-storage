Device management
=================

The API manages all block devices in
machine's local /dev/ directory, i.e. also remote disks (iSCSI, FcoE, ...), as
long as there is appropriate device in local /dev/.


Device hierarchy
----------------

Each block device is represented by instance of ``CIM_StorageExtent`` or its
subclasss.

.. figure:: pic/extent-inherit.svg

``LMI_StorageExtent`` represents all devices, which do not have any specific
``CIM_StorageExtent`` subclass.

Each volume group is represented by ``LMI_VGStoragePool``.

.. figure:: pic/pool-inherit.svg

Instances of ``LMI_VGStoragePool``, ``CIM_StorageExtent`` and its subclasses
compose an oriented graph of devices on the system. Devices are connected with
these associations or their subclasses:

- ``LMI_BasedOn`` and is subclasses associates a block device to all devices,
  on which it directly depends on, for example a partition is associated to a
  disk, on which it resides, and MD RAID is associated to all underlying
  devices, which compose the RAID.

- ``LMI_AssociatedComponentExtent`` associates volume groups with its physical
  extents.

- ``LMI_LVAllocatedFromStoragePool`` associates logical volumes to their
  volume groups.

.. figure:: pic/raid-lvm-simple.svg

  Example of two logical volumes allocated from volume group created on top of
  MD RAID with three devices.

Device manipulation
-------------------
Block devices cannot be directly manipulated using intrinsic or extrinsic
methods of ``CIM_StorageExtent`` or ``LMI_VGStoragePool``.

The only exception is ``DeleteInstance`` intrinsic method, which removes the
block device. The device must be *unused*, which means it must not be mounted
or used as base of other block devices.

Please appropriate ``ConfigurationService`` to create or modify devices or
volume groups.