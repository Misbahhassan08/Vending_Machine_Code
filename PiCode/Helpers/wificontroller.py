import os
import time
import threading
import queue
import Helpers.logger as logger
import Helpers.GlobalFunctions as s

class WifiController(threading.Thread):
    # Initialize a new WifiController class
    def __init__(self, _MainQueue):
        threading.Thread.__init__(self)
        self.MainQueue = _MainQueue #Keep a pointer to the Main Queue
        self.daemon = True
        try:
            self.ConnectedSSID = ""
            self.ConnectionStrength = -255
            self.PreviousConnectionStrength = -255
        except Exception as e:
            logger.error(e)
        self.start()
    def run(self):
        s.SetThreadName("BrewWiFi")
        logger.info("Wifi Started")
        while(True):
            self.ConnectionStrength = self.WifiSignalStrength()
            if(self.PreviousConnectionStrength != self.ConnectionStrength):
                self.MainQueue.put("WifiSignalStrength")
            time.sleep(1)
    def GetAvailableSSIDs(self):
        DeDupSSIDs = []
        try:
            AvailableSSIDs = os.popen("sudo iw dev wlan0 scan | grep SSID:").read()
            SSIDs = []
            for n in AvailableSSIDs.split('\n'):
                if(n.replace("SSID:", "").strip() != ""):
                    SSIDs.append(n.replace("SSID:", "").strip().replace("\\x20", " "))
            DeDupSSIDs = list(dict.fromkeys(SSIDs))
            DeDupSSIDs.sort()
            DeDupSSIDs.append("Hidden Network")
        except Exception as e:
            logger.error(e)
        return DeDupSSIDs
    def GetActiveSSID(self):
        return s.GetActiveSSID()
    def GetActiveIPAddress(self):
        return s.GetActiveIPAddress()
    def IsConnected(self):
        Response = os.popen("iwconfig wlan0 | grep 'ESSID:\"'").read()
        for r in Response.split('\n'):
            if("wlan0" in r):
                try:
                    # wlan0     IEEE 802.11  ESSID:"MIHome"
                    # wlan0     IEEE 802.11  ESSID:off/any
                    self.ConnectedSSID = r.split("ESSID:\"")[1].replace("\"", "").strip()
                except Exception as e:
                    logger.error(e)
        return (self.ConnectedSSID != "")
    def WifiSignalStrength(self):
        self.ConnectionStrength = s.WifiSignalStrength()
        return self.ConnectionStrength
    def Connect(self, SSID, PassPhrase):
        logger.info("Connecting to: " + SSID)
        PassKey = ""
        if(PassPhrase == ""):
            PassKey = "key_mgmt=NONE"
        else:
            Response = os.popen("wpa_passphrase '" + SSID + "' '" + PassPhrase + "'").read()
            CommandResponse = Response.split("\n")
            if(len(CommandResponse) == 6):
                PassKey = CommandResponse[3].strip()
        #Write the suplican file
        # https://w1.fi/cgit/hostap/plain/wpa_supplicant/wpa_supplicant.conf
        #
        #ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
        #update_config=1
        #country=US
        #
        #if the network has a blank password:
        #network={
        #ssid="MYSSID"
        #key_mgmt=NONE
        #}
        #network={
        #        ssid="MIHome"
        #        psk=9c0779262989a483f26966b82b6c2af8d83c90e787517336eb0f38790d80f6ec
        #}
        f = open("/etc/wpa_supplicant/wpa_supplicant.conf", "w")
        f.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
        f.write("update_config=1\n")
        f.write("country=US\n")
        f.write("network={\n")
        f.write("ssid=\"" + SSID + "\"\n")
        f.write(PassKey)
        f.write("\n}\n")
        f.write("\n")
        f.close()
        logger.info("Taking down wlan0")
        os.popen("sudo ifconfig wlan0 down")
        time.sleep(.25)
        logger.info("Reconfiguring wpa_cli")
        os.popen("wpa_cli -i wlan0 reconfigure")
        time.sleep(.25)
        logger.info("Bringing up wlan0")
        os.popen("sudo ifconfig wlan0 up")
        return self.IsConnected()
