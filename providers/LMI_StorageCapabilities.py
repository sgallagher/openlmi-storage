# Copyright (C) 2012 Red Hat, Inc.  All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# Authors: Jan Safranek <jsafrane@redhat.com>

"""Python Provider for LMI_StorageCapabilities

Instruments the CIM class LMI_StorageCapabilities

"""

from wrapper.common import settingManager
import pywbem
from pywbem.cim_provider2 import CIMProvider2
from LMI_StorageSetting import LMI_StorageSetting

class LMI_StorageCapabilities(CIMProvider2):
    """Instrument the CIM class LMI_StorageCapabilities 

    This is abstract base class for OpenLMI purposes.
    
    A subclass of Capabilities that defines the Capabilities of a
    StorageService or StoragePool. For example, an instance of
    StorageCapabilities could be associated with either a
    StorageConfigurationService or StoragePool by using
    ElementCapabilities.
    
    """

    def __init__ (self, env, classname):
        logger = env.get_logger()
        logger.log_debug('Initializing provider %s from %s' \
                % (self.__class__.__name__, __file__))
        self.classname = classname
        self.lastSettingId = 0

    def _get_instance(self, model):
        """ Get dictionary of given instance. """
        pass
    
    def get_instance(self, env, model):
        """Return an instance.

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        model -- A template of the pywbem.CIMInstance to be returned.  The 
            key properties are set on this instance to correspond to the 
            instanceName that was requested.  The properties of the model
            are already filtered according to the PropertyList from the 
            request.  Only properties present in the model need to be
            given values.  If you prefer, you can set all of the 
            values, and the instance will be filtered for you. 

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, unrecognized 
            or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the CIM Class does exist, but the requested CIM 
            Instance does not exist in the specified namespace)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """
        
        logger = env.get_logger()
        logger.log_debug('Entering %s.get_instance()' \
                % self.__class__.__name__)
        
        params = self._get_instance(env, model)
        if params is None:
                raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "InstanceID not found.")

        #model['AvailableDiskType'] = [self.Values.AvailableDiskType.<VAL>,] # TODO 
        #model['AvailableFormFactorType'] = [self.Values.AvailableFormFactorType.<VAL>,] # TODO 
        #model['AvailablePortType'] = [self.Values.AvailablePortType.<VAL>,] # TODO 
        #model['Caption'] = '' # TODO 
        model['DataRedundancyDefault'] = params['DataRedundancyDefault'] 
        model['DataRedundancyMax'] = params['DataRedundancyMax']
        model['DataRedundancyMin'] =  params['DataRedundancyMin']
        #model['DeltaReservationDefault'] = pywbem.Uint16() # TODO 
        #model['DeltaReservationMax'] = pywbem.Uint16() # TODO 
        #model['DeltaReservationMin'] = pywbem.Uint16() # TODO 
        #model['Description'] = '' # TODO 
        model['ElementName'] = model['InstanceID']
        model['ElementType'] = self.Values.ElementType.StoragePool
        #model['Encryption'] = self.Values.Encryption.<VAL> # TODO 
        model['ExtentStripeLengthDefault'] =  params['ExtentStripeLengthDefault']
        #model['Generation'] = pywbem.Uint64() # TODO 
        model['NoSinglePointOfFailure'] = params['NoSinglePointOfFailure']
        model['NoSinglePointOfFailureDefault'] = params['NoSinglePointOfFailureDefault']
        model['PackageRedundancyDefault'] = params['PackageRedundancyDefault']
        model['PackageRedundancyMax'] = params['PackageRedundancyMax']
        model['PackageRedundancyMin'] = params['PackageRedundancyMin']
        #model['ParityLayoutDefault'] = self.Values.ParityLayoutDefault.<VAL> # TODO 
        #model['SupportedDataOrganizations'] = [self.Values.SupportedDataOrganizations.<VAL>,] # TODO 
        #model['UserDataStripeDepthDefault'] = pywbem.Uint64() # TODO 
        return model

    def _enum_instances(self, env):
        """ Enumerate instances - generator of InstanceNames """
        pass
    
    def enum_instances(self, env, model, keys_only):
        """Enumerate instances.

        The WBEM operations EnumerateInstances and EnumerateInstanceNames
        are both mapped to this method. 
        This method is a python generator

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        model -- A template of the pywbem.CIMInstances to be generated.  
            The properties of the model are already filtered according to 
            the PropertyList from the request.  Only properties present in 
            the model need to be given values.  If you prefer, you can 
            always set all of the values, and the instance will be filtered 
            for you. 
        keys_only -- A boolean.  True if only the key properties should be
            set on the generated instances.

        Possible Errors:
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.enum_instances()' \
                % self.__class__.__name__)
                
        # Prime model.path with knowledge of the keys, so key values on
        # the CIMInstanceName (model.path) will automatically be set when
        # we set property values on the model. 
        model.path.update({'InstanceID': None})
        
        for name in self._enum_instances(env):
            model.update(name)
            if keys_only:
                yield model
            else:
                try:
                    yield self.get_instance(env, model)
                except pywbem.CIMError, (num, msg):
                    if num not in (pywbem.CIM_ERR_NOT_FOUND, 
                                   pywbem.CIM_ERR_ACCESS_DENIED):
                        raise

    def set_instance(self, env, instance, modify_existing):
        """Return a newly created or modified instance.

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        instance -- The new pywbem.CIMInstance.  If modifying an existing 
            instance, the properties on this instance have been filtered by 
            the PropertyList from the request.
        modify_existing -- True if ModifyInstance, False if CreateInstance

        Return the new instance.  The keys must be set on the new instance. 

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_NOT_SUPPORTED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, unrecognized 
            or otherwise incorrect parameters)
        CIM_ERR_ALREADY_EXISTS (the CIM Instance already exists -- only 
            valid if modify_existing is False, indicating that the operation
            was CreateInstance)
        CIM_ERR_NOT_FOUND (the CIM Instance does not exist -- only valid 
            if modify_existing is True, indicating that the operation
            was ModifyInstance)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.set_instance()' \
                % self.__class__.__name__)
        # TODO create or modify the instance
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED) # Remove to implement
        return instance

    def delete_instance(self, env, instance_name):
        """Delete an instance.

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        instance_name -- A pywbem.CIMInstanceName specifying the instance 
            to delete.

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_NOT_SUPPORTED
        CIM_ERR_INVALID_NAMESPACE
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, unrecognized 
            or otherwise incorrect parameters)
        CIM_ERR_INVALID_CLASS (the CIM Class does not exist in the specified 
            namespace)
        CIM_ERR_NOT_FOUND (the CIM Class does exist, but the requested CIM 
            Instance does not exist in the specified namespace)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """ 

        logger = env.get_logger()
        logger.log_debug('Entering %s.delete_instance()' \
                % self.__class__.__name__)

        # TODO delete the resource
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED) # Remove to implement
        
    def cim_method_getsupportedstripelengths(self, env, object_name):
        """Implements LMI_StorageCapabilities.GetSupportedStripeLengths()

        For systems that support discrete ExtentStripeLengths for volume or
        pool creation, this method can be used to retrieve a list of
        supported values. Note that different implementations may support
        either the GetSupportedStripeLengths or the
        GetSupportedStripeLengthRange method. Also note that the
        advertised sizes may change after the call due to requests from
        other clients. If the system only supports a range of sizes, then
        the return value will be set to 3.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method GetSupportedStripeLengths() 
            should be invoked.

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.GetSupportedStripeLengths)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        StripeLengths -- (type [pywbem.Uint16,]) 
            List of supported ExtentStripeLengths for a Volume/Pool
            creation or modification.
            

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, 
            unrecognized or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the target CIM Class or instance does not 
            exist in the specified namespace)
        CIM_ERR_METHOD_NOT_AVAILABLE (the CIM Server is unable to honor 
            the invocation request)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_getsupportedstripelengths()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('stripelengths', type='uint16', 
        #                   value=[pywbem.Uint16(),])] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.GetSupportedStripeLengths)
        #return (rval, out_params)
        
    def cim_method_getsupportedparitylayouts(self, env, object_name):
        """Implements LMI_StorageCapabilities.GetSupportedParityLayouts()

        For systems that support Parity-based storage organizations for
        volume or pool creation, this method can be used to the supported
        parity layouts.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method GetSupportedParityLayouts() 
            should be invoked.

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.GetSupportedParityLayouts)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        ParityLayout -- (type [pywbem.Uint16,] self.Values.GetSupportedParityLayouts.ParityLayout) 
            List of supported Parity for a Volume/Pool creation or
            modification.
            

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, 
            unrecognized or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the target CIM Class or instance does not 
            exist in the specified namespace)
        CIM_ERR_METHOD_NOT_AVAILABLE (the CIM Server is unable to honor 
            the invocation request)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_getsupportedparitylayouts()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('paritylayout', type='uint16', 
        #                   value=[self.Values.GetSupportedParityLayouts.ParityLayout.<VAL>,])] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.GetSupportedParityLayouts)
        #return (rval, out_params)
        
    def cim_method_getsupportedstripedepthrange(self, env, object_name):
        """Implements LMI_StorageCapabilities.GetSupportedStripeDepthRange()

        For systems that support a range of UserDataStripeDepths for volume
        or pool creation, this method can be used to retrieve the
        supported range. Note that different implementations may support
        either the GetSupportedStripeDepths or the
        GetSupportedStripeDepthRange method. If the system only supports
        discrete values, then the return value will be set to 2.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method GetSupportedStripeDepthRange() 
            should be invoked.

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.GetSupportedStripeDepthRange)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        MaximumStripeDepth -- (type pywbem.Uint64) 
            The maximum UserDataStripeDepth for a volume/pool in bytes.
            
        MinimumStripeDepth -- (type pywbem.Uint64) 
            The minimum UserDataStripeDepth for a volume/pool in bytes.
            
        StripeDepthDivisor -- (type pywbem.Uint64) 
            A volume/pool UserDataStripeDepth must be a multiple of this
            value which is specified in bytes.
            

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, 
            unrecognized or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the target CIM Class or instance does not 
            exist in the specified namespace)
        CIM_ERR_METHOD_NOT_AVAILABLE (the CIM Server is unable to honor 
            the invocation request)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_getsupportedstripedepthrange()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('maximumstripedepth', type='uint64', 
        #                   value=pywbem.Uint64())] # TODO
        #out_params+= [pywbem.CIMParameter('minimumstripedepth', type='uint64', 
        #                   value=pywbem.Uint64())] # TODO
        #out_params+= [pywbem.CIMParameter('stripedepthdivisor', type='uint64', 
        #                   value=pywbem.Uint64())] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.GetSupportedStripeDepthRange)
        #return (rval, out_params)
        
    def cim_method_creategoalsettings(self, env, object_name,
                                      param_supportedgoalsettings=None,
                                      param_templategoalsettings=None):
        """Implements LMI_StorageCapabilities.CreateGoalSettings()

        Method to create a set of supported SettingData elements, from two
        sets of SettingData elements, provided by the caller. \nCreateGoal
        should be used when the SettingData instances that represents the
        goal will not persist beyond the execution of the client and where
        those instances are not intended to be shared with other,
        non-cooperating clients. \nBoth TemplateGoalSettings and
        SupportedGoalSettings are represented as strings containing
        EmbeddedInstances of a CIM_SettingData subclass. These embedded
        instances do not exist in the infrastructure supporting this
        method but are maintained by the caller/client. \nThis method
        should return CIM_Error(s) representing that a single named
        property of a setting (or other) parameter (either reference or
        embedded object) has an invalid value or that an invalid
        combination of named properties of a setting (or other) parameter
        (either reference or embedded object) has been requested. \nIf the
        input TemplateGoalSettings is NULL or the empty string, this
        method returns a default SettingData element that is supported by
        this Capabilities element. \nIf the TemplateGoalSettings specifies
        values that cannot be supported, this method shall return an
        appropriate CIM_Error and should return a best match for a
        SupportedGoalSettings. \nThe client proposes a goal using the
        TemplateGoalSettings parameter and gets back Success if the
        TemplateGoalSettings is exactly supportable. It gets back
        "Alternative Proposed" if the output SupportedGoalSettings
        represents a supported alternative. This alternative should be a
        best match, as defined by the implementation. \nIf the
        implementation is conformant to a RegisteredProfile, then that
        profile may specify the algorithms used to determine best match. A
        client may compare the returned value of each property against the
        requested value to determine if it is left unchanged, degraded or
        upgraded. \n\nOtherwise, if the TemplateGoalSettings is not
        applicable an "Invalid Parameter" error is returned. \n\nWhen a
        mutually acceptable SupportedGoalSettings has been achieved, the
        client may use the contained SettingData instances as input to
        methods for creating a new object ormodifying an existing object.
        Also the embedded SettingData instances returned in the
        SupportedGoalSettings may be instantiated via CreateInstance,
        either by a client or as a side-effect of the execution of an
        extrinsic method for which the returned SupportedGoalSettings is
        passed as an embedded instance.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method CreateGoalSettings() 
            should be invoked.
        param_supportedgoalsettings --  The input parameter SupportedGoalSettings (type pywbem.CIMInstance(classname='CIM_SettingData', ...)) 
            SupportedGoalSettings are elements of class CIM_SettingData, or
            a derived class. \nAt most, one instance of each SettingData
            subclass may be supplied. \nAll SettingData instances provided
            by this property are interpreted as a set, relative to this
            Capabilities instance. \n\nTo enable a client to provide
            additional information towards achieving the
            TemplateGoalSettings, an input set of SettingData instances
            may be provided. If not provided, this property shall be set
            to NULL on input.. Note that when provided, what property
            values are changed, and how, is implementation dependent and
            may be the subject of other standards. \nIf provided, the
            input SettingData instances must be ones that the
            implementation is able to support relative to the
            ManagedElement associated via ElementCapabilities. Typically,
            the input SettingData instances are created by a previous
            instantiation of CreateGoalSettings. \nIf the input
            SupportedGoalSettings is not supported by the implementation,
            then an "Invalid Parameter" (5) error is returned by this
            call. In this case, a corresponding CIM_ERROR should also be
            returned. \nOn output, this property is used to return the
            best supported match to the TemplateGoalSettings. \nIf the
            output SupportedGoalSettings matches the input
            SupportedGoalSettings, then the implementation is unable to
            improve further towards meeting the TemplateGoalSettings.
            
        param_templategoalsettings --  The input parameter TemplateGoalSettings (type pywbem.CIMInstance(classname='CIM_SettingData', ...)) 
            If provided, TemplateGoalSettings are elements of class
            CIM_SettingData, or a derived class, that is used as the
            template to be matched. . \nAt most, one instance of each
            SettingData subclass may be supplied. \nAll SettingData
            instances provided by this property are interpreted as a set,
            relative to this Capabilities instance. \nSettingData
            instances that are not relevant to this instance are ignored.
            \nIf not provided, it shall be set to NULL. In that case, a
            SettingData instance representing the default settings of the
            associated ManagedElement is used.
            

        Returns a two-tuple containing the return value (type pywbem.Uint16 self.Values.CreateGoalSettings)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        SupportedGoalSettings -- (type pywbem.CIMInstance(classname='CIM_SettingData', ...)) 
            SupportedGoalSettings are elements of class CIM_SettingData, or
            a derived class. \nAt most, one instance of each SettingData
            subclass may be supplied. \nAll SettingData instances provided
            by this property are interpreted as a set, relative to this
            Capabilities instance. \n\nTo enable a client to provide
            additional information towards achieving the
            TemplateGoalSettings, an input set of SettingData instances
            may be provided. If not provided, this property shall be set
            to NULL on input.. Note that when provided, what property
            values are changed, and how, is implementation dependent and
            may be the subject of other standards. \nIf provided, the
            input SettingData instances must be ones that the
            implementation is able to support relative to the
            ManagedElement associated via ElementCapabilities. Typically,
            the input SettingData instances are created by a previous
            instantiation of CreateGoalSettings. \nIf the input
            SupportedGoalSettings is not supported by the implementation,
            then an "Invalid Parameter" (5) error is returned by this
            call. In this case, a corresponding CIM_ERROR should also be
            returned. \nOn output, this property is used to return the
            best supported match to the TemplateGoalSettings. \nIf the
            output SupportedGoalSettings matches the input
            SupportedGoalSettings, then the implementation is unable to
            improve further towards meeting the TemplateGoalSettings.
            

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, 
            unrecognized or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the target CIM Class or instance does not 
            exist in the specified namespace)
        CIM_ERR_METHOD_NOT_AVAILABLE (the CIM Server is unable to honor 
            the invocation request)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_creategoalsettings()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('supportedgoalsettings', type='string', 
        #                   value=[pywbem.CIMInstance(classname='CIM_SettingData', ...),])] # TODO
        #rval = # TODO (type pywbem.Uint16 self.Values.CreateGoalSettings)
        #return (rval, out_params)
        
    def cim_method_getsupportedstripelengthrange(self, env, object_name):
        """Implements LMI_StorageCapabilities.GetSupportedStripeLengthRange()

        For systems that support a range of ExtentStripeLengths for volume
        or pool creation, this method can be used to retrieve the
        supported range. Note that different implementations may support
        either the GetSupportedExtentLengths or the
        GetSupportedExtentLengthRange method. Also note that the
        advertised sizes may change after the call due to requests from
        other clients. If the system only supports discrete values, then
        the return value will be set to 3.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method GetSupportedStripeLengthRange() 
            should be invoked.

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.GetSupportedStripeLengthRange)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        StripeLengthDivisor -- (type pywbem.Uint32) 
            A volume/pool ExtentStripeLength must be a multiple of this
            value which is specified in bytes.
            
        MinimumStripeLength -- (type pywbem.Uint16) 
            The minimum ExtentStripeDepth for a volume/pool in bytes.
            
        MaximumStripeLength -- (type pywbem.Uint16) 
            The maximum ExtentStripeLength for a volume/pool in bytes.
            

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, 
            unrecognized or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the target CIM Class or instance does not 
            exist in the specified namespace)
        CIM_ERR_METHOD_NOT_AVAILABLE (the CIM Server is unable to honor 
            the invocation request)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_getsupportedstripelengthrange()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('stripelengthdivisor', type='uint32', 
        #                   value=pywbem.Uint32())] # TODO
        #out_params+= [pywbem.CIMParameter('minimumstripelength', type='uint16', 
        #                   value=pywbem.Uint16())] # TODO
        #out_params+= [pywbem.CIMParameter('maximumstripelength', type='uint16', 
        #                   value=pywbem.Uint16())] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.GetSupportedStripeLengthRange)
        #return (rval, out_params)
        
    def cim_method_getsupportedstripedepths(self, env, object_name):
        """Implements LMI_StorageCapabilities.GetSupportedStripeDepths()

        For systems that support discrete UserDataStripeDepths for volume
        or pool creation, this method can be used to retrieve a list of
        supported values. Note that different implementations may support
        either the GetSupportedStripeDepths or the
        GetSupportedStripeDepthRange method. If the system only supports a
        range of sizes, then the return value will be set to 2.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method GetSupportedStripeDepths() 
            should be invoked.

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.GetSupportedStripeDepths)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        StripeDepths -- (type [pywbem.Uint64,]) 
            List of supported UserDataStripeDepths for a Volume/Pool
            creation or modification.
            

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, 
            unrecognized or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the target CIM Class or instance does not 
            exist in the specified namespace)
        CIM_ERR_METHOD_NOT_AVAILABLE (the CIM Server is unable to honor 
            the invocation request)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_getsupportedstripedepths()' \
                % self.__class__.__name__)

        # TODO do something
        raise pywbem.CIMError(pywbem.CIM_ERR_METHOD_NOT_AVAILABLE) # Remove to implemented
        out_params = []
        #out_params+= [pywbem.CIMParameter('stripedepths', type='uint64', 
        #                   value=[pywbem.Uint64(),])] # TODO
        #rval = # TODO (type pywbem.Uint32 self.Values.GetSupportedStripeDepths)
        #return (rval, out_params)
        
    def cim_method_createsetting(self, env, object_name,
                                 param_settingtype=None):
        """Implements LMI_StorageCapabilities.CreateSetting()

        Method to create and populate a StorageSetting instance from a
        StorageCapability instance. This removes the need to populate
        default settings and other settings in the context of each
        StorageCapabilities (which could be numerous). If the underlying
        instrumentation supports the StorageSettingWithHints subclass,
        then an instance of that class will be created instead.
        
        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName 
            specifying the object on which the method CreateSetting() 
            should be invoked.
        param_settingtype --  The input parameter SettingType (type pywbem.Uint16 self.Values.CreateSetting.SettingType) 
            If \'Default\' is passed for the CreateDefault parameter, the
            Max, Goal, and Min setting attributes are set to the Default
            values of the parent StorageCapabilities when the instance is
            created. \nIf set to \'Goal\' the new StorageSetting
            attributes are set to the related attributes of the parent
            StorageCapabilities, e.g. Min to Min, Goal to Default, and Max
            to Max. \n\nThis method maybe deprecated in lieu of intrinsics
            once limitations in the CIM Operations are addressed.
            

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.CreateSetting)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        NewSetting -- (type REF (pywbem.CIMInstanceName(classname='CIM_StorageSetting', ...)) 
            Reference to the created StorageSetting instance.
            

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, 
            unrecognized or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the target CIM Class or instance does not 
            exist in the specified namespace)
        CIM_ERR_METHOD_NOT_AVAILABLE (the CIM Server is unable to honor 
            the invocation request)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.cim_method_createsetting()' \
                % self.__class__.__name__)

        # find the capabilities
        params = self._get_instance(env, object_name)
        if not params:
            pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND)

        # find unused setting InstanceID
        i = settingManager.generateId()
        
        setting = {
                'InstanceID': str(i),
                'ChangeableType': LMI_StorageSetting.Values.ChangeableType.Changeable___Transient,
                'ElementName': str(i),
                'LMIAllocationType' : params['LMIAllocationType'] ,
        }
        if not param_settingtype:
            param_settingtype = self.Values.CreateSetting.SettingType.Default
        
        if param_settingtype == self.Values.CreateSetting.SettingType.Default:
            setting.update({
                    'DataRedundancyMin' : params['DataRedundancyDefault'],
                    'DataRedundancyMax' : params['DataRedundancyDefault'],
                    'DataRedundancyGoal': params['DataRedundancyDefault'],
                    'PackageRedundancyMin': params['PackageRedundancyDefault'],
                    'PackageRedundancyMax': params['PackageRedundancyDefault'],
                    'PackageRedundancyGoal': params['PackageRedundancyDefault'],
                    'ExtentStripeLength' : params['ExtentStripeLengthDefault'],
                    'ExtentStripeLengthMin' : params['ExtentStripeLengthDefault'],
                    'ExtentStripeLengthMax' : params['ExtentStripeLengthDefault']
            })
        elif param_settingtype == self.Values.CreateSetting.SettingType.Goal:
            setting.update({
                    'DataRedundancyMin' : params['DataRedundancyMin'],
                    'DataRedundancyMax' : params['DataRedundancyMax'],
                    'DataRedundancyGoal': params['DataRedundancyDefault'],
                    'PackageRedundancyMin': params[' PackageRedundancyMin'],
                    'PackageRedundancyMax': params[' PackageRedundancyMax'],
                    'PackageRedundancyGoal': params[' PackageRedundancyDefault'],
                    'ExtentStripeLength' : params['ExtentStripeLengthDefault'],
                    'ExtentStripeLengthMin' : params['ExtentStripeLengthDefault'],
                    'ExtentStripeLengthMax' : params['ExtentStripeLengthDefault']
            })
        else:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER, 'Unsupported settingtype')
 
        #TODO: this is not thread-safe, other user might allocate the instanceID       
        openlmi.storage.setSetting(setting)
        
        newsetting = pywbem.CIMParameter('newsetting', type='reference', 
                           value = openlmi.storage.getSettingName(setting))
        rval = self.Values.CreateSetting.Success
        return (rval, [newsetting, ])
        
    class Values(object):
        class SupportedDataOrganizations(object):
            Other = pywbem.Uint16(0)
            Unknown = pywbem.Uint16(1)
            Fixed_Block = pywbem.Uint16(2)
            Variable_Block = pywbem.Uint16(3)
            Count_Key_Data = pywbem.Uint16(4)

        class ParityLayoutDefault(object):
            Non_Rotated_Parity = pywbem.Uint16(2)
            Rotated_Parity = pywbem.Uint16(3)

        class AvailablePortType(object):
            Unknown = pywbem.Uint16(0)
            other = pywbem.Uint16(1)
            SAS = pywbem.Uint16(2)
            SATA = pywbem.Uint16(3)
            SAS_SATA = pywbem.Uint16(4)
            FC = pywbem.Uint16(5)

        class AvailableDiskType(object):
            Unknown = pywbem.Uint16(0)
            Other = pywbem.Uint16(1)
            Hard_Disk_Drive = pywbem.Uint16(2)
            Solid_State_Drive = pywbem.Uint16(3)

        class Encryption(object):
            Unknown = pywbem.Uint16(0)
            Not_Supported = pywbem.Uint16(1)
            Supported = pywbem.Uint16(2)

        class GetSupportedParityLayouts(object):
            Method_completed_OK = pywbem.Uint32(0)
            Method_not_supported = pywbem.Uint32(1)
            Choice_not_aavailable_for_this_capability = pywbem.Uint32(2)
            class ParityLayout(object):
                Non_Rotated_Parity = pywbem.Uint16(2)
                Rotated_Parity = pywbem.Uint16(3)

        class GetSupportedStripeDepthRange(object):
            Method_completed_OK = pywbem.Uint32(0)
            Method_not_supported = pywbem.Uint32(1)
            Use_GetSupportedStripeDepths_instead = pywbem.Uint32(2)

        class AvailableFormFactorType(object):
            Unknown = pywbem.Uint16(0)
            Other = pywbem.Uint16(1)
            Not_Reported = pywbem.Uint16(2)
            _5_25_inch = pywbem.Uint16(3)
            _3_5_inch = pywbem.Uint16(4)
            _2_5_inch = pywbem.Uint16(5)
            _1_8_inch = pywbem.Uint16(6)

        class GetSupportedStripeDepths(object):
            Method_completed_OK = pywbem.Uint32(0)
            Method_not_supported = pywbem.Uint32(1)
            Use_GetSupportedStripeDepthRange_instead = pywbem.Uint32(2)

        class CreateGoalSettings(object):
            Success = pywbem.Uint16(0)
            Not_Supported = pywbem.Uint16(1)
            Unknown = pywbem.Uint16(2)
            Timeout = pywbem.Uint16(3)
            Failed = pywbem.Uint16(4)
            Invalid_Parameter = pywbem.Uint16(5)
            Alternative_Proposed = pywbem.Uint16(6)
            # DMTF_Reserved = ..
            # Vendor_Specific = 32768..65535

        class GetSupportedStripeLengthRange(object):
            Method_completed_OK = pywbem.Uint32(0)
            Method_not_supported = pywbem.Uint32(1)
            Choices_not_available_for_this_Capability = pywbem.Uint32(2)
            Use_GetSupportedStripeLengths_instead = pywbem.Uint32(3)

        class GetSupportedStripeLengths(object):
            Method_completed_OK = pywbem.Uint32(0)
            Method_not_supported = pywbem.Uint32(1)
            Choices_not_available_for_this_Capability = pywbem.Uint32(2)
            Use_GetSupportedStripeLengthRange_instead = pywbem.Uint32(3)

        class ElementType(object):
            Unknown = pywbem.Uint16(0)
            Reserved = pywbem.Uint16(1)
            Any_Type = pywbem.Uint16(2)
            StorageVolume = pywbem.Uint16(3)
            StorageExtent = pywbem.Uint16(4)
            StoragePool = pywbem.Uint16(5)
            StorageConfigurationService = pywbem.Uint16(6)
            LogicalDisk = pywbem.Uint16(7)
            StorageTier = pywbem.Uint16(8)

        class CreateSetting(object):
            Success = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unspecified_Error = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            # DMTF_Reserved = ..
            # Vendor_Specific = 32768..65535
            class SettingType(object):
                Default = pywbem.Uint16(2)
                Goal = pywbem.Uint16(3)

## end of class LMI_StorageCapabilitiesProvider
