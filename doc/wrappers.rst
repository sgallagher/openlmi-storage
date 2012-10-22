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

#. Add appripriate CIM classes to LMI_Storage.mof file.
#. Implement a subclass of the DeviceWrapper. Override appropriate methods -
   look at RAIDWrapper as an example.
#. Add initialization of the wrapper instance to LMI_Wrappers.py. This python
   module serves as entry point from CIMOM.
#. Register your new CIM classes in your CIMOM. LMI_Wrappers.py should be used
   as the provider. E.g. this registration code can be used for SFCB:

  .. parsed-literal::
    [LMI_AssociatedVGComponentExtent]
       provider: LMI_Wrappers
       location: pyCmpiProvider
       type: instance association
       namespace: root/cimv2
       unload: never
    [LMI_VGAllocatedFromStoragePool]
       provider: LMI_Wrappers
       location: pyCmpiProvider
       type: instance association
       namespace: root/cimv2
       unload: never
    [LMI_VGCompositeExtentBasedOn]
       provider: LMI_Wrappers
       location: pyCmpiProvider
       type: instance association
       namespace: root/cimv2
       unload: never
    [LMI_VGCompositeExtent]
       provider: LMI_Wrappers
       location: pyCmpiProvider
       type: instance method
       namespace: root/cimv2
       unload: never
    [LMI_VGPool]
       provider: LMI_Wrappers
       location: pyCmpiProvider
       type: instance method
       namespace: root/cimv2
       unload: never
    [LMI_VGStorageCapabilities]
       provider: LMI_Wrappers
       location: pyCmpiProvider
       type: instance method
       namespace: root/cimv2
       unload: never
    [LMI_VGStorageElementCapabilities]
       provider: LMI_Wrappers
       location: pyCmpiProvider
       type: instance association
       namespace: root/cimv2
       unload: never

