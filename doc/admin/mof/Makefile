all: index.rst

HOST="https://localhost:5989"
TOPDIR=../../..
MOFS=$(TOPDIR)/mof/base.mof \
    $(TOPDIR)/mof/filesystems.mof \
    $(TOPDIR)/mof/luks.mof \
    $(TOPDIR)/mof/partitions.mof \
    $(TOPDIR)/mof/storage.mof

index.rst: $(MOFS)
	class2rst.py -H header.txt -u $(HOST) `cat $(MOFS) | grep "^class" | cut -d ' ' -f 2`
