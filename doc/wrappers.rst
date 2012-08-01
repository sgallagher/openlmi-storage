Device Wrapper
==============

.. automodule:: wrapper.DeviceWrapper
   :members:

RAIDWrapper
"""""""""""

.. automodule:: wrapper.RAIDWrapper
   :members:

PrimordialWrapper
"""""""""""""""""

.. automodule:: wrapper.PrimordialWrapper
   :members:

VGWrapper
"""""""""

.. automodule:: wrapper.VGWrapper
   :members:

LVWrapper
"""""""""

.. automodule:: wrapper.LVWrapper
   :members:


Providers
"""""""""
CIM providers classes for all DeviceWrapper subclasses are implemented in
these python modules:

- WrappedExtent.py
- WrappedPool.py
- WrappedStorageCapabilities.py
- WrappedExtentBasedOn.py
- WrappedAllocatedFromStoragePool.py
- WrappedAssociatedComponentExtent.py
- WrappedStorageElementCapabilities.py

To implement new wrapper, following steps are necessary:

#. Add appripriate CIM classes to cura-storage.mof file.
#. Implement a subclass of the DeviceWrapper. Override appropriate methods -
   look at RAIDWrapper as an example.
#. Add initialization of the wrapper instance to Cura_Wrappers.py. This python
   module serves as entry point from CIMOM.
#. Register your new CIM classes in your CIMOM. Cura_Wrappers.py should be used
   as the provider. E.g. this registration code can be used for SFCB:

  .. parsed-literal::
    [Cura_AssociatedVGComponentExtent]
       provider: Cura_Wrappers
       location: pyCmpiProvider
       type: instance association
       namespace: root/cimv2
       unload: never
    [Cura_VGAllocatedFromStoragePool]
       provider: Cura_Wrappers
       location: pyCmpiProvider
       type: instance association
       namespace: root/cimv2
       unload: never
    [Cura_VGCompositeExtentBasedOn]
       provider: Cura_Wrappers
       location: pyCmpiProvider
       type: instance association
       namespace: root/cimv2
       unload: never
    [Cura_VGCompositeExtent]
       provider: Cura_Wrappers
       location: pyCmpiProvider
       type: instance method
       namespace: root/cimv2
       unload: never
    [Cura_VGPool]
       provider: Cura_Wrappers
       location: pyCmpiProvider
       type: instance method
       namespace: root/cimv2
       unload: never
    [Cura_VGStorageCapabilities]
       provider: Cura_Wrappers
       location: pyCmpiProvider
       type: instance method
       namespace: root/cimv2
       unload: never
    [Cura_VGStorageElementCapabilities]
       provider: Cura_Wrappers
       location: pyCmpiProvider
       type: instance association
       namespace: root/cimv2
       unload: never

