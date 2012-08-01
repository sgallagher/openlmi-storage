#!/usr/bin/python
# Quick and dirty script, which generates python skeleton for all classes on command line.

import pywbem
import pywbem.cim_provider2
import sys

con = pywbem.WBEMConnection('http://localhost')

for classname in sys.argv[1:]:
    cc = con.GetClass(classname, 'root/cimv2')
    python_code, registration = pywbem.cim_provider2.codegen(cc)

    codefile = open(classname + '.py', 'w')
    codefile.write(python_code)
    codefile.close()

    for line in registration.splitlines()[2:7]:
        print line.replace(' // TODO', '')

