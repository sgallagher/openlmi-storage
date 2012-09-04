# Anaconda initialization routines
# Useful for python -i anaconda_init.py
#

from pyanaconda import anaconda_log
anaconda_log.init()

import pyanaconda.storage
import pyanaconda.storage.partitioning
import pyanaconda.platform

def commit():
    global storage
    print "storage.devicetree.processActions(dryRun=False)"
    return storage.devicetree.processActions(dryRun=False)

def partition_do():
    pyanaconda.storage.partitioning.doPartitioning(storage=storage)

# set up storage class instance
platform = pyanaconda.platform.getPlatform()
storage = pyanaconda.storage.Storage(platform=platform)

# identify the system's storage devices
storage.devicetree.populate()
for array in storage.mdarrays:
    array.setup()


# now storage.devicetree contains all devices on the system and storage knows about them, e.g.:
# sda1 = storage.devicetree.getDeviceByName('sda1')

print "\n\n***********************"
print "disk = storage.devicetree.getDeviceByName('sda')"
disk = storage.devicetree.getDeviceByName('sda')

