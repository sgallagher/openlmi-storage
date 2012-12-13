#!/usr/bin/python
# -*- Coding:utf-8 -*-
#
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


import logging
import inspect

TRACE_WARNING = logging.INFO - 1
TRACE_INFO = logging.INFO - 2
TRACE_VERBOSE = logging.DEBUG

class CMPILogHandler(logging.Handler):
    """
        A handler class, which sends log messages to CMPI log.
    """

    def __init__(self, cmpi_logger, *args, **kwargs):
        self.cmpi_logger = cmpi_logger
        super(CMPILogHandler, self).__init__(*args, **kwargs)

    def emit(self, record):
        msg = self.format(record)
        if record.levelno >= logging.ERROR:
            self.cmpi_logger.log_error(msg)
        elif record.levelno >= logging.WARNING:
            self.cmpi_logger.log_warn(msg)
        elif record.levelno >= logging.INFO:
            self.cmpi_logger.log_info(msg)
        elif record.levelno >= TRACE_WARNING:
            self.cmpi_logger.trace_warn(record.filename, msg)
        elif record.levelno >= TRACE_INFO:
            self.cmpi_logger.trace_info(record.filename, msg)
        elif record.levelno >= logging.DEBUG:
            self.cmpi_logger.trace_verbose(record.filename, msg)

class CMPILogger(logging.getLoggerClass()):
    """
        A logger class, which adds trace_method level log methods.
    """
    def trace_warn(self, msg, *args, **kwargs):
        """ Log message with TRACE_WARNING severity. """
        self.log(TRACE_WARNING, msg, *args, **kwargs)

    def trace_info(self, msg, *args, **kwargs):
        """ Log message with TRACE_INFO severity. """
        self.log(TRACE_INFO, msg, *args, **kwargs)

    def trace_verbose(self, msg, *args, **kwargs):
        """ Log message with TRACE_VERBOSE severity. """
        self.log(TRACE_VERBOSE, msg, *args, **kwargs)

logging.setLoggerClass(CMPILogger)

def trace_method(func):
    """ Decorator, trace entry and exit for a class method. """
    classname = inspect.getouterframes(inspect.currentframe())[1][3]
    def helper_func(*args, **kwargs):
        """ Helper function, wrapping real function by trace_method decorator."""
        logger.log(TRACE_VERBOSE,
                "Entering %s.%s" % (classname, func.__name__,))
        try:
            ret = func(*args, **kwargs)
        except Exception, e:
            logger.log(TRACE_WARNING,
                    "%s.%s threw exception %s" % (
                            classname,
                            func.__name__,
                            str(e)))
            raise
        logger.log(
                TRACE_VERBOSE,
                "Exiting %s.%s" % (classname, func.__name__))
        return ret
    helper_func.__name__ = func.__name__
    helper_func.__doc__ = func.__doc__
    helper_func.__module__ = func.__module__
    return helper_func

def trace_function(func):
    """ Decorator, trace entry and exit for a function outside any class. """
    def helper_func(*args, **kwargs):
        """ Helper function, wrapping real function by trace_method decorator."""
        logger.log(TRACE_VERBOSE,
                "Entering %s" % (func.__name__,))
        try:
            ret = func(*args, **kwargs)
        except Exception, e:
            logger.log(TRACE_WARNING,
                    "%s threw exception %s" % (func.__name__, str(e)))
            raise
        logger.log(
                TRACE_VERBOSE,
                "Exiting %s" % (func.__name__))
        return ret
    helper_func.__name__ = func.__name__
    helper_func.__doc__ = func.__doc__
    helper_func.__module__ = func.__module__
    return helper_func

class LogManager(object):
    """
        Class, which takes care of CMPI logging.
        There should be only one instance of this class and it should be
        instantiated as soon as possible, even before reading a config.
        The config file can be provided later by set_config call.
    """
    FORMAT_STDERR = '%(levelname)s: %(message)s'
    FORMAT_CMPI = '%(levelname)s: %(message)s'

    LOGGER_NAME = "openlmi.storage"

    def __init__(self, env):
        """
            Initialize logging.
        """
        formatter = logging.Formatter(self.FORMAT_CMPI)

        self.cmpi_handler = CMPILogHandler(env.get_logger())
        self.cmpi_handler.setLevel(logging.DEBUG)
        self.cmpi_handler.setFormatter(formatter)

        self.logger = logging.getLogger(self.LOGGER_NAME)
        self.logger.addHandler(self.cmpi_handler)
        self.logger.setLevel(logging.INFO)

        self.stderr_handler = None
        self.config = None

        global logger  # IGNORE:W0603
        logger = self.logger
        logger.info("CMPI log started")

    @trace_method
    def set_config(self, config):
        """
            Set a configuration of logging. It applies its setting immediately
            and also subscribes for configuration changes.
        """
        self.config = config
        config.add_listener(self._config_changed)
        # apply the config
        self._config_changed(config)

    @trace_method
    def _config_changed(self, config):
        """
            Apply changed configuration, i.e. start/stop sending to stderr
            and set appropriate log level.
        """
        if config.tracing:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        if config.stderr:
            # start sending to stderr
            if not self.stderr_handler:
                # create stderr handler
                formatter = logging.Formatter(self.FORMAT_STDERR)
                self.stderr_handler = logging.StreamHandler()
                self.stderr_handler.setLevel(logging.DEBUG)
                self.stderr_handler.setFormatter(formatter)
                self.logger.addHandler(self.stderr_handler)
                self.logger.info("Started logging to stderr.")
        else:
            # stop sending to stderr
            if self.stderr_handler:
                self.logger.info("Stopped logging to stderr.")
                self.logger.removeHandler(self.stderr_handler)
            self.stderr_handler = None

    def destroy(self):
        if self.stderr_handler:
            self.logger.removeHandler(self.stderr_handler)
            self.stderr_handler = None
        self.logger.removeHandler(self.cmpi_handler)
        self.cmpi_handler = None
        self.config.remove_listener(self._config_changed)



logger = None
