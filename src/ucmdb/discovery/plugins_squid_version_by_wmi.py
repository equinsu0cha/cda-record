#coding=utf-8
import sys
import logger
import re

from plugins import Plugin
from file_ver_lib import getWindowsWMIFileVer

class SquidWMIPlugin(Plugin):
    
    """
        Plugin sets Squid application version by WMI.
    """
    
    def __init__(self):
        Plugin.__init__(self)
        self.__client = None
        self.__path = None
        self.__allowedProcesses = ['squid.exe']
         
    def isApplicable(self, context):
        self.__client = context.client
        try:
            for allowedProc in self.__allowedProcesses:
                process = context.application.getProcess(allowedProc)
                if process:
                    self.__path = process.executablePath
                    if self.__path:
                        return 1
        except:
            logger.errorException(sys.exc_info()[1])
    
    def process(self, context):
        applicationOsh = context.application.getOsh()
        version = getWindowsWMIFileVer(self.__client, self.__path)
        if version:
            match = re.match('\s*(\d+)\,\s(\d+)', version)
            if match:
                version = match.group(1) + "." + match.group(2)
                logger.debug('File version: %s' % version)
                applicationOsh.setAttribute("application_version_number", version)
        else:
            logger.debug('Cannot get file version.')