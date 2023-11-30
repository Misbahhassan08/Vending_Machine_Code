import threading
from datetime import datetime, timedelta
import time
import queue
import Helpers.logger as logger
import automationhat

class Beep(threading.Thread):
    # Initialize a new instance of the class Beep
    def __init__(self):
        threading.Thread.__init__(self)
        self.isDaemon = True
        #Private Variables
        self._BeepQueue = queue.Queue()
        self._BeepPatterns = [[.1],[.1,.05,.1,.05,.1,.05,.1,.5,.1,.05,.1,.05,.1,.05,.1,.5,.1,.05,.1,.05,.1,.05,.1,.5,.1,.05,.1,.05,.1,.05,.1],[.25,.025,.25,.025,.25,.025,.25,.5,.25,.025,.25,.025,.25,.025,.25,.5,.25,.025,.25,.025,.25,.025,.25,.5,.25,.025,.25,.025,.25,.025,.25]]
        # Start up the message Queue Thread
        self.start()
    def run(self):
        logger.info("BeepThread Running")
        while(True):
            Message = self._BeepQueue.get()
            if("BeepPattern:" in Message):
                Values = Message.split(":")
                BeepPattern = Values[1]
                self._Beep(int(BeepPattern))
# Public Functions
    def Beep(self, Pattern=1):
        self._BeepQueue.put("BeepPattern:" + str(Pattern))
# End Public Functions
# Private Functions
    def _Beep(self, Pattern=1):
        BeepTrack = "BeepOff"
        BeepPattern = self._BeepPatterns[Pattern]
        for BeepInterval in BeepPattern:
            if(BeepTrack == "BeepOn"):
                automationhat.output.three.off()
                BeepTrack = "BeepOff"
            else:
                automationhat.output.three.on()
                BeepTrack = "BeepOn"
            time.sleep(BeepInterval)
        automationhat.output.three.off()
# End Private Functions