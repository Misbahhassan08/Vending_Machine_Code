#!/usr/bin/env python3

import configparser as ConfigParser
import os
import io
import Helpers.logger as logger

filepath = "/Share/Helpers/settings.ini"

# Gets a configuration value from the settings file
def get_value(section, name):
    try:
        config = ConfigParser.ConfigParser()
        config.optionxform = str
        config.read(filepath)
        return config[section][name]
    except Exception as e:
        logger.error("Config get_value Exception: " + str(e))
# Sets a configuration value in the settings file
def set_value(section, name, value):
    try:
        config = ConfigParser.ConfigParser()
        config.optionxform = str
        config.read(filepath)
        if (not config.has_section(str(section))):
            config[str(section)] = {}
        config[str(section)][str(name)] = str(value)
        with open(filepath, 'w') as configfile:
            config.write(configfile)
    except Exception as e:
        logger.error("Config set_value Exception: " + str(e))
def get_sections(name):
    config = ConfigParser.ConfigParser()
    config.optionxform = str
    config.read(filepath)
    ret = []
    try:
        for (key, _) in config.items(name):
            ret.append(key)
    except Exception as e:
        logger.error("Config get_sections Exception: " + str(e))
    ret.sort()
    return ret
def clear_section(name):
    try:
        config = ConfigParser.ConfigParser()
        config.optionxform = str
        config.read(filepath)
        for val in config.options(name):
            config.remove_option(name, val)
        with open(filepath, 'w') as configfile:
            config.write(configfile)
    except Exception as e:
        logger.error("Config clear_section Exception: " + str(e))
    logger.info(dict(config[str(name)]))
