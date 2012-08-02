#!/usr/bin/python

import sys
import re

reg_parse = re.compile(r"\[([^\]]+)\]\s+"
"provider: ([^\s]+)\s+"
"location: (\w+)\s+"
"type: ([^\n]+)\s+"
"namespace: ([^\n]+)")

Types = {
    'instance': '2',
    'association': '3',
    'indication': '4',
    'method': '5',
    'consumer': '6',
    'instanceQuery': '7'
}

def define_module(location):
    return """instance of PG_ProviderModule
{
    Name = "%(location)s";
    Location = "%(location)s";
    Vendor = "RedHat";
    Version = "0.0.1";
    InterfaceType = "CMPI";
    InterfaceVersion = "2.0.0";
    ModuleGroupName = "cura-providers";
};
""" % { 'location': location }

def getTypes(types):
    l = []
    for key, value in Types.items():
        if key in types:
            l.append(value)
    return ",".join(l)

def define_capability(location, provider, cls, types):
    return """instance of PG_Provider
{
    Name = "%(provider)s";
    ProviderModuleName = "%(location)s";
};

instance of PG_ProviderCapabilities
{
   ProviderModuleName = "%(location)s";
   ProviderName = "%(provider)s";
   CapabilityID = "%(class)s";
   ClassName = "%(class)s";
   Namespaces = { "root/cimv2" };
   ProviderType = { %(types)s };
   SupportedProperties = NULL;
   SupportedMethods = NULL;
};
""" % { 'location': location, 'provider': provider, 'class': cls, 'types': getTypes(types) }

modules_defined = {}
for record in reg_parse.findall(sys.stdin.read()):
    cls, provider, location, types, namespace = record

    if location not in modules_defined:
        print define_module(location)
        modules_defined[location] = True

    print define_capability(location, provider, cls, types)
