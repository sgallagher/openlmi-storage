FILES=extent-inherit.svg \
    pool-inherit.svg
    
HOST="https://localhost:5989"
TOPDIR=../../..
MOFS=$(TOPDIR)/mof/base.mof \
    $(TOPDIR)/mof/filesystems.mof \
    $(TOPDIR)/mof/luks.mof \
    $(TOPDIR)/mof/partitions.mof \
    $(TOPDIR)/mof/storage.mof

all: $(FILES)

clean:
	-rm -rf $(FILES)

%.svg: %.uml ../plantuml.cfg
	plantuml -config ../plantuml.cfg -Tsvg $<

extent-inherit.uml: $(MOFS)
	class2uml.py -s '(CIM_|SNIA_).*' -A -u $(HOST) `cat $(MOFS) | grep "^/*class" | cut -d ' ' -f 2 | egrep "LMI.*StorageExtent|Partition$$" ` >$@

pool-inherit.uml: $(MOFS)
	class2uml.py -s '(CIM_|SNIA_).*' -A -u $(HOST) `cat $(MOFS) | grep "^/*class" | cut -d ' ' -f 2 | egrep "LMI.*StoragePool"` >$@
