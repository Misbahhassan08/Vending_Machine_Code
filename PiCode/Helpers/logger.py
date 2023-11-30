import logging
import threading
import requests
import prctl
#import configuration as config
#import GlobalFunctions as s

LogIsOpened = False
logger = None
hdlr = None
fomatter = None

def SetThreadName(name):
    prctl.set_name(name[:16])

class AsynchronousWorker(threading.Thread):
    #Basic thread wrapper class for asynchronously running functions
    def __init__(self, FunctionToRunAsync, message):
        threading.Thread.__init__(self)
        self.daemon = True
        self.FunctionToRunAsync = FunctionToRunAsync
        self._message = message
        self.start()
    def run(self):
        SetThreadName("UploadLogAsync")
        try:
            if(self.FunctionToRunAsync is not None):
                self.FunctionToRunAsync(self._message)
        except Exception as e:
            print(e)
            #logger.error(e)

def getSerial():
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
SerialNumber = getSerial()
UploadLogsInRealTime = False


for Line in open("/Share/Helpers/settings.ini", 'r').readlines():
    if "UploadLogsInRealTime" in Line:
        if "True" in Line:
            UploadLogsInRealTime = True

def OpenLog():
    global LogIsOpened, logger, hdlr, fomatter
    try:
        logger = logging.getLogger('root')
        hdlr = logging.FileHandler('/Share/py.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.INFO)
        LogIsOpened = True
    except:
        pass

def UploadLog(message):
    global UploadLogsInRealTime, SerialNumber
    try:
        if SerialNumber != "" and UploadLogsInRealTime:
            Headers = {
                'User-Agent': 'BrewBomb',
                'ElectronicSerialNumber': SerialNumber,
                "logMessage": str(message)
            }
            requests.post('https://portal.Brewbomb.com/_api/brewer.aspx?Command=BrewerAPIRealTimeLog', headers=Headers, timeout=1)
            #print(response, message)
    except Exception as e:
        print(e)

# Log a message to the specified log file
def log(message, level):
    global logger
    if(not LogIsOpened):
        OpenLog()
    try:
        if level == "info":
            logger.info(message)
        elif level == "error":
            logger.error(message)
        try:
            LogUploadWorker = AsynchronousWorker(UploadLog, message)
            #UploadLog(message)
        except:
            pass
    except:
        OpenLog()
    # hdlr.close()
    # logger.removeHandler(hdlr)
    # hdlr.close()

# Log an informational message to the log file
def info(message):
    log(message, "info")

# Log an error message to the log file
def error(message):
    try:
        log(logger.findCaller() + " " + message, "error")
    except:
        log(message, "error")
