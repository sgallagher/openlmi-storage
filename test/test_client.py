# -*- coding: utf-8 -*-

from test_base import StorageTestBase
import pywbem
import unittest

class TestClient(StorageTestBase):
    def __init__(self, *args, **kwargs):
        self.mdName = None
        super(TestClient, self).__init__(*args, **kwargs)
        
    
    def test_client(self):
        
        level = 5 # RAID5
        
        # find all disks
        disks = []
        
        candidates = self.wbemconnection.EnumerateInstanceNames('LMI_LocalDiskExtent')
        for c in candidates:
            if c['DeviceID'] in self.disks:
                disks.append(c)
        
        # create GPT partition table on them, i.e. call
        # LMI_DiskPartitionConfigurationService.SetPartitionStyle(disk, partitionStyle) 
        # - get reference to LMI_DiskPartitionConfigurationService instance
        partServices = self.wbemconnection.EnumerateInstanceNames('LMI_DiskPartitionConfigurationService')
        partService = partServices[0]
        
        # - get reference to PartitionStyle we want to create
        partStyle = self.wbemconnection.ExecQuery('WQL', 'SELECT * FROM LMI_DiskPartitionConfigurationCapabilities WHERE InstanceID = "GPT"')[0]
        
        for disk in disks:
            # - call partService.SetPartitionStyle(disk)
            (ret, outparams) = self.wbemconnection.InvokeMethod('SetPartitionStyle', partService, Extent = disk, PartitionStyle = partStyle.path)
            print 'SetPartitionStyle(', disk['DeviceID'], ')=', ret
        
        # create one huge partition on the disks, i.e. call
        # LMI_DiskPartitionConfigurationService.CreateOrModifyPartition(disk)
        for disk in disks: 
            # - call partService.SetPartitionStyle(disk)
            (ret, outparams) = self.wbemconnection.InvokeMethod('CreateOrModifyPartition', partService, Extent = disk)
            print 'CreateOrModifyPartition(', disk['DeviceID'], ')=', ret
        
        # create RAID out of them, i.e. call
        # LMI_StorageConfigurationService.CreateOrModifyStoragePool(settings, pool)
        # - find the primordial pool
        pool = self.wbemconnection.EnumerateInstanceNames('LMI_PrimordialPool')[0]
        # - find the LMI_StorageConfigurationService
        storageService = self.wbemconnection.EnumerateInstanceNames('LMI_StorageConfigurationService')[0]
        # - find (or create) appropriate setting
        setting = self.wbemconnection.ExecQuery('WQL', 'SELECT * FROM LMI_StorageSetting WHERE InstanceID = "STATIC:RAID%s"' % level)[0]
        (ret, outparams) = self.wbemconnection.InvokeMethod('CreateOrModifyStoragePool', storageService, Goal = setting.path, InPools = [pool])
        print 'CreateOrModifyStoragePool()=', ret
        print 'created pool:', outparams['Pool']
        myRaidPool = outparams['Pool']
        
        # allocate LogicalDisk out of the pool, i.e. call
        # LMI_StorageConfigurationService.CreateOrModifyElementFromStoragePool(pool)
        (ret, outparams) = self.wbemconnection.InvokeMethod('CreateOrModifyElementFromStoragePool', storageService, InPool = myRaidPool, ElementType = pywbem.Uint16(4)) # 4 = create LogicalDisk
        print 'CreateOrModifyElementFromStoragePool()=', ret
        print 'created element:', outparams['TheElement']
        myRaidDisk = outparams['TheElement']
        self.mdName = myRaidDisk['DeviceID']
        
        # create a filesystem on the RAID, i.e. call
        # LMI_FileSystemConfigurationService.CreateFileSystem
        # - find the LMI_FileSystemConfigurationService
        fsService = self.wbemconnection.EnumerateInstanceNames('LMI_FileSystemConfigurationService')[0]
        (ret, outparams) = self.wbemconnection.InvokeMethod('CreateFileSystem', fsService, InExtent = myRaidDisk)
        print 'LMI_FileSystemConfigurationService()=', ret
        
if __name__ == '__main__':
    unittest.main()
