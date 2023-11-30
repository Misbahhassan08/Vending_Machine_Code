import os
#import time
#import sys
import threading
#import shlex
#import subprocess
#from datetime import datetime
#from subprocess import Popen
import prctl

import psutil
import Helpers.logger as logger
import Helpers.configuration as config

def IsMetric():
    return config.get_value("app", "units") == "Metric"
def SetThreadName(name):
    prctl.set_name(name[:16])
def ConnectSSH():
    print("starting")
    try:
        logger.info("Starting reverse tunnel")
        logger.info(os.popen("sudo systemctl restart reversetunnel.service").read())
        # remoteport = config.get_value("ssh", "ReversePort")
        # print("RemotePort:"+str(remoteport))
        # try:
        #     if((int(remoteport) < 45000) & (int(remoteport) > 44000)):
        #         pass
        #     else:
        #         remoteport = 44000
        # except Exception as e:
        #     print(e)
        #     logger.error("ReversePort error")
        #     logger.error(e)
        #     remoteport = 44000
        # print(remoteport)
        # print(os.popen("sudo mkdir /home/pi/.ssh").read())
        # print(os.popen("sudo chmod 700 /home/pi/.ssh").read())
        # print(os.popen("sudo chown pi:pi -R /home/pi/.ssh").read())
        # print(os.popen("sudo chmod 700 /home/pi/.ssh").read())
        # print(os.popen("cp /Share/id_rsa /home/pi/.ssh").read())
        # print(os.popen("sudo chmod 600 /home/pi/.ssh/id_rsa ").read())
        # print(os.popen("cp /Share/known_hosts /home/pi/.ssh").read())
        # print(os.popen("sudo chmod 644 /home/pi/.ssh/known_hosts").read())
        # print(os.popen("runuser -l pi -c 'ssh -NR *:"+str(remoteport)+":localhost:22 brewbomb@reversetunnel.mercuryinc.net -p 43022'").read())
    except Exception as e:
        #print(e)
        logger.error("Error Starting reverse tunnel: " + str(e))
def GetElectronicSerialNumber():
    # Extract serial from cpuinfo file
    cpuserial = '0000000000000000'
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = 'ERROR000000000'
    return str(cpuserial)
def GetActiveSSID():
    Response = os.popen("tail /etc/wpa_supplicant/wpa_supplicant.conf | grep 'ssid=\"'").read()
    SSID = ""
    if('ssid="' in Response):
        SSID = Response.split('ssid="')[1].replace('"', "").strip()
    return str(SSID)
def GetActiveIPAddress():
    Response = os.popen("ifconfig wlan0 | grep 'inet '").read()
    IPAddress = ""
    if('inet ' in Response):
        #  inet 192.168.86.251  netmask 255.255.255.0  broadcast 192.168.86.255
        IPAddress = Response.split('inet ')[1].split('netmask ')[0].strip()
    return str(IPAddress)
def WifiSignalStrength():
    Response = os.popen("iwconfig wlan0 | grep 'Signal level='").read()
    ConnectionStrength = -255
    for r in Response.split('\n'):
        if("Signal level=" in r):
            try:
                #          Link Quality=58/70  Signal level=-52 dBm
                ConnectionStrength = int(r.split("Signal level=")[1].replace(" dBm", "").strip())
            except Exception as e:
                logger.error(e)
    return ConnectionStrength
def GetCPUUsage():
    return str(psutil.cpu_percent())
def GetDiskUsage():
    return str(psutil.disk_usage('/').percent)
def GetRAMUsage():
    return str(psutil.virtual_memory().percent)
def GetUpTime():
    Response = os.popen("uptime").read()
    UpTime = ''
    try:
        #14:15:39 up  1:52,  4 users,  load average: 0.14, 0.14, 0.16
        UpTime = Response.split('up')[1].split(',')[0]
    except Exception as e:
        logger.error(e)
        UpTime = "0"
    return str(UpTime).strip(' ')
def GetCPUTemperature():
    temp = ''
    try:
        # temp=49.9'C
        temp = os.popen('vcgencmd measure_temp').read()
        temp = temp.replace("temp=", "").replace("'C", "").replace("\n", "")
    except Exception as e:
        logger.error(e)
        temp = "-99.99"
    return str(temp)

class AsynchronousWorker(threading.Thread):
    #Basic thread wrapper class for asynchronously running functions
    def __init__(self, FunctionToRunAsync):
        threading.Thread.__init__(self)
        self.daemon = True
        self.FunctionToRunAsync = FunctionToRunAsync
        self.start()
    def run(self):
        SetThreadName("BrewAsync")
        try:
            if(self.FunctionToRunAsync is not None):
                self.FunctionToRunAsync()
        except Exception as e:
            print(e)
            logger.error(e)
