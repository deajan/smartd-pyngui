#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# This file is part of ofunctions module

"""
servce_control allows to interact with windows / unix services

Versioning semantics:
    Major version: backward compatibility breaking changes
    Minor version: New functionality
    Patch version: Backwards compatible bug fixes

"""

__intname__ = 'smartd_pyngui.smartd_config'
__author__ = 'Orsiris de Jong'
__copyright__ = 'Copyright (C) 2012-2020 Orsiris de Jong'
__licence__ = 'BSD 3 Clause'
__version__ = '1.0.0'
__build__ = '2020041302'


import os
import sys
from datetime import datetime
from logging import getLogger

SMARTD_CONF_FILENAME = 'smartd.conf'
DEFAULT_UNIX_PATH = '/etc/smartd'

logger = getLogger()


class SmartDConfiguration:
    """
    This class can read / write smartd.conf files

    Standard smartd.conf files are read into 'default' section
    If the file has been written by this class, it will have

    - A header: '# smartd_pyngui 1.0 conf file'
    - a Disk type list: '# __spinning /dev/sda /dev/sdb\n# __nvme /dev/sdc\n __ssd /dev/sdd
    - Various sections of configuration settings per disk type (eg /dev/sdX [config])
    - If no disk type list exists, than the __spinning type will be used

    """
    smart_conf_file = ""

    def __init__(self, file_path=None, app_root=None, app_executable=None):
        # TODO investigate file_path usage here (which refers to both smartd and alert conf files)

        self.app_root = app_root
        self.app_executable = app_executable


        ##*# Multi drive type config enabled ##*#
        self.multi_drive_config_explanation = '# Since smartd cannot set different settings per drive type, ' \
                                              'we analyzed the drives on your computer and assigned settings ' \
                                              'corresponding to the drive types. When drives change, a re-run ' \
                                              'of the tool is required.'
        self.smart_conf_file = None


        # Use __spinning drive settings for all drive types
        self.global_drive_settings = False

        # Drive types
        # Default gets populated when no other configs exist
        self.drive_types = ['__spinning', '__ssd', '__nvme', '__removable']

        # Contains smartd drive configurations
        self.config_list = {}
        # Contains lists of drives per drive_types
        self.drive_list = {}
        for drive_type in self.drive_types:
            self.config_list[drive_type] = []
            self.drive_list[drive_type] = []

        # Contains smartd global alert configuration
        self.config_list_alerts = []



        self.set_smartd_defaults()


        if file_path is not None:
            self.smart_conf_file = file_path
            if not os.path.isfile(self.smart_conf_file):
                logger.info("Using new file [" + self.smart_conf_file + "].")
        else:
            if os.name == 'nt':
                # Get program files environment
                try:
                    program_files_x86 = os.environ["ProgramFiles(x86)"]
                except KeyError:
                    program_files_x86 = os.environ["ProgramFiles"]

                try:
                    program_files_x64 = os.environ["ProgramW6432"]
                except KeyError:
                    program_files_x64 = os.environ["ProgramFiles"]

                smart_conf_file_possible_paths = [
                    os.path.join(self.app_root, SMARTD_CONF_FILENAME),
                    os.path.join(program_files_x64, 'smartmontools for Windows', 'bin', SMARTD_CONF_FILENAME),
                    os.path.join(program_files_x86, 'smartmontools for Windows', 'bin', SMARTD_CONF_FILENAME),
                    os.path.join(program_files_x64, 'smartmontools', 'bin', SMARTD_CONF_FILENAME),
                    os.path.join(program_files_x86, 'smartmontools', 'bin', SMARTD_CONF_FILENAME)
                ]
            else:
                smart_conf_file_possible_paths = [
                    os.path.join(self.app_root, SMARTD_CONF_FILENAME),
                    os.path.join('/etc/smartmontools', SMARTD_CONF_FILENAME),
                    os.path.join('/etc/smartd', SMARTD_CONF_FILENAME),
                    os.path.join('/etc', SMARTD_CONF_FILENAME),
                    os.path.join('etc/smartmontools', SMARTD_CONF_FILENAME),
                    os.path.join('etc/smartd', SMARTD_CONF_FILENAME),
                    os.path.join('/etc', SMARTD_CONF_FILENAME)
                ]


            for possible_smartd_path in smart_conf_file_possible_paths:
                if os.path.isfile(possible_smartd_path):
                    self.smart_conf_file = possible_smartd_path
                    break

        if self.smart_conf_file is None:
            self.smart_conf_file = os.path.join(self.app_root, SMARTD_CONF_FILENAME)
        else:
            logger.debug('Found configuration file in [%s].' % self.smart_conf_file)

    def set_smartd_defaults(self):
        self.drive_list['__spinning'] = ['DEVICESCAN']
        self.drive_list['__ssd'] = []
        self.drive_list['__nvme'] = []
        self.drive_list['__removable'] = []

        self.config_list['__spinning'] = ['-H', '-C 197+', '-l error', '-U 198+', '-l selftest', '-t', '-f', '-I 194',
                                          '-W 20,55,60', '-n sleep,7,q',
                                          '-s (L/../../4/13|S/../../0,1,2,3,4,5,6/10)']
        self.config_list['__ssd'] = ['-H', '-C 197+', '-l error', '-U 198+', '-l selftest', '-t', '-f', '-I 194',
                                     '-W 40,65,75', '-n sleep,7,q',
                                     '-s (L/../../4/13|S/../../0,1,2,3,4,5,6/10)']
        self.config_list['__nvme'] = ['-H', '-C 197+', '-l error', '-U 198+', '-l selftest', '-t', '-f', '-I 194',
                                      '-W 40,80,85', '-n sleep,7,q',
                                      '-s (L/../../4/13|S/../../0,1,2,3,4,5,6/10)']
        self.config_list['__removable'] = ['-H', '-C 197+', '-l error', '-U 198+', '-l selftest', '-t', '-f', '-I 194',
                                           '-W 20,55,60', '-n sleep,7,q',
                                           '-s (L/../../4/13|S/../../0,1,2,3,4,5,6/10)']

        # Default behavior is to for smartmontools to launch this app with --alert
        self.config_list_alerts = ['-m <nomailer>', '-M exec "%s --alert"' % self.app_executable]

    # TODO use 4 different config lists
    def read_smartd_conf_file(self, conf_file=None):
        current_drive_type = '__spinning'
        # Contains smartd drive configurations
        config_list = {}
        # Contains lists of drives per drive_types
        drive_list = {}
        for drive_type in self.drive_types:
            config_list[drive_type] = []
            drive_list[drive_type] = []
        if conf_file is None:
            conf_file = self.smart_conf_file
        try:
            with open(conf_file, 'r') as conf:
                for line in conf:
                    if line[0] != "\n" and line[0] != "\r" and line[0] != " ":
                        if line.startswith('##*# Multi drive type config enabled ##*#'):
                            self.global_drive_settings = True
                        elif line.startswith('##*# __spinning drives type ##*#'):
                            current_drive_type = '__spinning'
                        elif line.startswith('##*# __nvme drives type ##*#'):
                            current_drive_type = '__nvme'
                        elif line.startswith('##*# __ssd drives type ##*#'):
                            current_drive_type = '__ssd'
                        elif line.startswith('##*# __removable drives type ##*#'):
                            current_drive_type = '__removable'
                        elif not line[0] == "#":
                            try:
                                cfg = line.split(' -')
                                cfg = [cfg[0]] + ['-' + item for item in cfg[1:]]
                                #  Remove unnecessary blanks and newlines
                                for i, _ in enumerate(cfg):
                                    cfg[i] = cfg[i].strip()
                                drive_list[current_drive_type].append(cfg[0])
                                del cfg[0]
                                config_list[current_drive_type] = cfg
                            except Exception:
                                msg = "Cannot read in config file [%s]." % conf_file
                                logger.error(msg)
                                logger.debug('Trace:', exc_info=True)
                                raise ValueError(msg)
                self.smart_conf_file = conf_file
            self.drive_list = drive_list
            self.config_list = config_list
            # TODO sg.Popup('Read configuration succeed')
        except IOError:
            msg = 'Cannot read from config file [%s].' % conf_file
            logger.error(msg)
            logger.debug('Trace:', exc_info=True)
            # TODO sg.Popup('Read configuration failed: {0}.'.format(msg))

    def write_smartd_conf_file(self):
        try:
            with open(self.smart_conf_file, 'w') as conf:
                try:
                    conf.write(f'# This file was generated on {datetime.now():%d-%B-%Y %H:%m:%S} by '
                             f'{APP_NAME} {APP_VERSION} - {APP_URL}\n')
                    if self.global_drive_settings:
                        drive_types = self.drive_types
                        conf.write(f'##*# Multi drive type config enabled ##*#\n')
                        conf.write(self.multi_drive_config_explanation + '\n\n')
                    else:
                        drive_types = ['__spinning']
                    conf.write('\n\n')
                    for drive_type in drive_types:
                        conf.write(f'\n##*# {drive_type} drives type ##*#\n')
                        for drive in self.drive_list[drive_type]:
                            line = drive
                            for arg in self.config_list[drive_type]:
                                line += " " + arg
                            conf.write(line + "\n")
                except ValueError as exc:
                    msg = 'Cannot write data in config file [{0}]: {1}'.format(self.smart_conf_file, exc)
                    logger.error(msg)
                    logger.debug('Trace', exc_info=True)
                    raise ValueError(msg)
        except Exception as exc:
            msg = 'Cannot write to config file [{0}]: {1}'.format(self.smart_conf_file, exc)
            logger.error(msg)
            logger.debug('Trace', exc_info=True)
            raise ValueError(msg)
