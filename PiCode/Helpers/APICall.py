import threading
import time
import os
import queue
from datetime import datetime

import json

import requests

import Helpers.logger as logger
import Helpers.configuration as config
import Helpers.GlobalFunctions as s

BrewerStatusAPICallInProgress = False

class APICall(threading.Thread):
    # Initialize a new instance of the class Checkin
    def __init__(self, _MainQueue, _APIQueue):
        threading.Thread.__init__(self)
        logger.info("API Thread Starting")
        self.Debug = config.get_value('debug', 'APICalls') == "True"
        self.MainQueue = _MainQueue #Keep a pointer to the Main Queue
        self.APIQueue = _APIQueue #Keep a pointer to the API Queue
        self._LastCheckinTime = datetime.now()
        self.daemon = True
        self.start()
    def run(self):
        s.SetThreadName("BrewAPI")
        logger.info("API Thread Running")
        config.set_value('AppStatus', 'ApplicationStatus', 'Starting')
        self.APIQueue.put("Checkin")
        while(True):
            self.CheckForMessages()
            try:
                if((datetime.now()-self._LastCheckinTime).seconds > 10):
                    self.APIQueue.put("Checkin")
                    self._LastCheckinTime = datetime.now()
            except Exception as e:
                logger.error("API Loop Exception: " + str(e))
        logger.info("API Thread Ended")

    def CheckForMessages(self):
        try:
            Message = self.APIQueue.get_nowait()
            global BrewerStatusAPICallInProgress
            Headers = {}
            APICommand = ''
            if(Message == "Checkin"):
                Headers = {
                    'User-Agent': 'BrewBomb',
                    'BrewerSerialNumber': config.get_value('AppInfo', 'BrewerSerialNumber'),
                    'ElectronicSerialNumber': s.GetElectronicSerialNumber(),
                    'ApplicationStatus': config.get_value('AppStatus', 'ApplicationStatus'),
                    'SoftwareVersion': config.get_value('AppInfo', 'SoftwareVersion'),
                    'CPUUsage': s.GetCPUUsage(),
                    'DiskUsage': s.GetDiskUsage(),
                    'RamUsage': s.GetRAMUsage(),
                    'UpTime': s.GetUpTime(),
                    'CPUTemperature': s.GetCPUTemperature(),
                    'WifiSSID': s.GetActiveSSID(),
                    'WifiSignalStrength': str(s.WifiSignalStrength()),
                    'IPAddress': s.GetActiveIPAddress()
                    }
                APICommand = 'BrewerAPICheckin'

            if("BrewStatus" in Message):
                try:
                    Values = Message.split(":")
                    Headers = {
                        'User-Agent': 'BrewBomb',
                        'BrewerSerialNumber': config.get_value('AppInfo', 'BrewerSerialNumber'),
                        'ElectronicSerialNumber': s.GetElectronicSerialNumber(),
                        'BrewStartDateTime': Values[1],
                        'BrewProfileID': Values[2],
                        'BrewProfileName': Values[3],
                        'CurrentFlowRate': Values[4],
                        'CurrentYield': Values[5],
                        'TotalMinutes': Values[6],
                        'RemainingTime': Values[7],
                        'BrewIntervalRemaining': Values[8],
                        'RestIntervalRemaining': Values[9],
                        'BrewingPaused': Values[10],
                        'BrewingComplete': Values[11],
                        'TargetFlowRate': Values[12],
                        'TargetYield': Values[13]
                    }
                    if(BrewerStatusAPICallInProgress == False):
                        BrewerStatusAPICallInProgress = True
                        APICommand = 'BrewerAPIBrewStatus'
                except Exception as e:
                    logger.error("BrewStatus API Message Error: " + str(e))
            if(APICommand != ''):
                self.ProcessAPICall(APICommand, Headers)
        except queue.Empty:
            time.sleep(0.1)
        except Exception as e:
            logger.error("API Loop Exception: " + str(e))

    def ProcessAPICall(self, APICommand, Headers):
        global BrewerStatusAPICallInProgress
        if(self.Debug):
            logger.info("API Call In Progress: " + str(BrewerStatusAPICallInProgress))
            logger.info("API Command: " + str(APICommand))
            logger.info("API Headers: " + str(Headers))
        data = requests.post('https://portal.Brewbomb.com/_api/brewer.aspx?Command=' + APICommand, headers=Headers, timeout=5)

        try:
            if(self.Debug):
                logger.info("API Response: " + str(data.text))
            if(APICommand == 'BrewerAPIBrewStatus'):
                BrewerStatusAPICallInProgress = False
            else:
                result = json.loads(data.text)
                self.ProcessResponse(result)
        except Exception as e:
            logger.error("API Response Exception: " + str(e))

    def ProcessResponse(self, Response):
        # elif("SendConfig" in Response):
        #     self.SendConfig()
        if("Response" in Response): # Check if there is a response key in the resposne
            if(Response['Response'] == "Success"):
                if("HasCommands" in Response): # Check if there are commands to do
                    if(self.Debug):
                        logger.info("Response HasCommands: " + str(Response["HasCommands"]))
                if("UpdateApplicatoin" in Response):
                    self.MainQueue.put("Update")
                    time.sleep(0.5)
                    logger.info('Updating Application')
                    logger.info(os.popen("runuser -l pi -c 'sudo python3 /Update/main.py'").read())
                if("OpenSSHTunnel" in Response):
                    logger.info('Starting SSH')
                    s.ConnectSSH()
                if("DisableFirewall" in Response):
                    logger.info('Stopping Firewall')
                    logger.info(os.popen("sudo systemctl stop ufw").read())
                if("UpdateProfiles" in Response):
                    self.UpdateProfiles(Response)
                if("SendConfig" in Response):
                    self.SendConfig()
            else:
                if(self.Debug):
                    logger.info("Response: " + str(Response))
        else:
            if(self.Debug):
                logger.info("Unknown Response: " + str(Response))
    def UpdateProfiles(self, Response):
        try:
            UnParsedProfiles = Response["UpdateProfiles"]
            profiles = json.loads(json.dumps(UnParsedProfiles))
            config.clear_section("profiles")
            for item in profiles:
                config.set_value("profiles", item['BrewProfileName'], item)
            logger.info("Profile Update Requested: " + str(Response))
        except Exception as e:
            logger.error("Update Profiles Exception: " + str(e))
    def SendConfig(self):
        Headers = {
            'User-Agent': 'BrewBomb',
            'BrewerSerialNumber': config.get_value('AppInfo', 'BrewerSerialNumber'),
            'ElectronicSerialNumber': s.GetElectronicSerialNumber(),
            "Configuration": open("/Share/Helpers/settings.ini", 'r').read()
        }
        self.ProcessAPICall('BrewerAPIMergeConfig', Headers)
