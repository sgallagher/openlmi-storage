TODO list
=========

Generic

- find better name/place for Cura_Common.StorageFunctions
- write high-level design and documentation
- implement Server Profile

Block Services Package

- Experimental: every pool can have its own StorageConfigurationCapabilities
- add GlobalStorageCapabilities associated with the StorageConfigurationService (basically a copy of PrimordialStorageCapabilities with different InstanceID).
- implement CIM_ElementSettingData
- implement CIM_Setting associations
- implement CIM_Settings for LogicalDisks
- check SMI-S for mandatory methods/properties/classes
- implement all methods !!!
- implement recursive Setting / Capabilities - if LVM is on RAID, it should have appropriate redundancy capabilities

LVM

- implement destruction of logical volumes
- implement modification of LVs and VGs
- implement snapshots - Copy Services Subprofile

Extent Composition Subprofile

- implement Remaining Extents in a pool - deprecated? How is it replaced?
- RAIDCompositeExtentBasedOn - implement UserDataStripeLength
