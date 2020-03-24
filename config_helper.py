import configparser

config_parser = configparser.RawConfigParser()
config_parser.read('config.properties')


def get_section(section_name):
    return config_parser[section_name]


def get(section_name, property_name):
    return config_parser[section_name][property_name]
