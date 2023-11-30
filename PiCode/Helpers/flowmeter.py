import threading
from datetime import datetime
import time
import queue
import automationhat
import RPi.GPIO as GPIO
import Helpers.logger as logger
import Helpers.configuration as config
import Helpers.GlobalFunctions as s

class FlowMeter(threading.Thread):
    # Initialize a new instance of the class FlowMeter
    def __init__(self, MainQueue, FlowMeterPin):
        threading.Thread.__init__(self)
        self.Debug = config.get_value("debug", "FlowMeter") == "True"
        #Private Variables
        self._FlowMeterQueue = queue.Queue()
        self._MainQueue = MainQueue #Keep a pointer to the Main Queue
        self._SensorConstant = 0
        self._ticks = 0
        self._TargetDispenseAmount = 0
        self._WaterShouldBeFlowing = False
        self._ResumeFlow = False
        self._SendWaterToPreInfuseVessel = False
        self._SendWaterToBrewer = False
        self._LastTickTime = datetime.now()
        self._LastRates = []
        # IO variables
        self._FlowMeterPin = FlowMeterPin
        GPIO.setwarnings(True)
        # Use the Raspberry Pi BCM pins
        GPIO.setmode(GPIO.BCM)
        # define the FlowMeter input
        GPIO.setup(self._FlowMeterPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Rate Variables
        self._Rates = []
        # Start up the message Queue Thread
        self.start()
    def run(self):
        s.SetThreadName("BrewFlow")
        self._LogResponse("FlowMeterThread Running")
        GPIO.add_event_detect(self._FlowMeterPin, GPIO.FALLING, callback=self._FlowMeterTick) # bouncetime in mSec
        while(True):
            Message = self._FlowMeterQueue.get()
            if("StartWaterFlow" in Message):
                try:
                    self._StartWaterFlow()
                    self._QueueWaterFlowingNotification()
                    try:
                        while(self._WaterShouldBeFlowing and not self._HaveReachedTargetDoesAmount()):
                            self._QueueWaterFlowingNotification()
                            self._MonitorWaterFlow()
                            time.sleep(0.01) #yield some processor time
                    except Exception as e:
                        logger.error("StartWaterflow Loop Exception: " + str(e))
                    self._StopWaterFlow()
                    self._QueueWaterFlowingNotification(True)
                    self._LogResponse("Water flow stopped with " + str(self._ticks) + " ticks.")
                    self._MainQueue.put("WaterFlowStopped:" + str(self._ticks))
                except Exception as e:
                    logger.error("StartWaterFlow Exception:" + str(e))
    def _MonitorWaterFlow(self):
        try:
            try:
                if len(self._Rates) > 1:
                    if self._Rates[1] == 0:
                        self._Rates.pop(0)
                while len(self._Rates) > 1 and abs(int(((self._Rates[0]/self._Rates[1])-1) * 100)) > 5:
                    self._Rates.pop(0)
            except Exception as e:
                print(e)
            if (datetime.now() - self._LastTickTime).total_seconds() > 5:
                if self._LastRates == self._Rates:
                    try:
                        self._Rates = []
                        #print("rates cleared")
                    except:
                        pass
                self._LastRates = self._Rates
                self._LastTickTime = datetime.now()
        except Exception as e:
            print(e)
    # Calculate the average flowrate
    def GetAverageFlowRate(self):
        if(self._WaterShouldBeFlowing):
            RatesTotal = 0
            RateIndex = 1
            #print(self._Rates)
            for rate in self._Rates:
                #print(rate)
                #if rate[0] == 0:
                #    RatesTotal += 0
                #else:
                RatesTotal += rate#(rate[1]/rate[0])
                RateIndex += 1
            if(len(self._Rates) == 0):
                AverageMsPerTick = 0
            else:
                AverageMsPerTick = RatesTotal/len(self._Rates)
            if AverageMsPerTick == 0:
                EstimatedTicksPerSecond = 0
            else:
                EstimatedTicksPerSecond = 1000/AverageMsPerTick
            EstimatedTicksPerMin = EstimatedTicksPerSecond  * 60
            EstimatedFlowRatePerMin = EstimatedTicksPerMin * self._SensorConstant
            #print(self._Rates)
            #print("AverageMsPerTick", AverageMsPerTick, "EstimatedTicksPerSecond", EstimatedTicksPerSecond, "EstimatedTicksPerMin", EstimatedTicksPerMin, "EstimatedFlowRatePerMin", EstimatedFlowRatePerMin)
            return EstimatedFlowRatePerMin
        else:
            return 0

# Public Functions
    # Resets the tick counter back to 0
    def ResetFlowMeter(self):
        self._ticks = 0 # Reset the tick counter to 0
    # Sends a mesage to the flow meter thread to open the coresponding selonoids and start the tick counter
    def StartWaterFlow(self, TargetDispenseAmount=0, SendWaterToPreInfuseVessel=False, SendWaterToBrewer=False, ResumeFlow=False):
        self._LogResponse("StartWaterFlow TargetDispenseAmount:" + str(TargetDispenseAmount) + " SendWaterToPreInfuseVessel:" + str(SendWaterToPreInfuseVessel) + " SendWaterToBrewer:" + str(SendWaterToBrewer) + " ResumeFlow:" + str(ResumeFlow))
        if(self._WaterShouldBeFlowing):
            logger.error("Send Water Request while water is running. Call StopFlow First")
        else:
            self._WaterShouldBeFlowing = True
            self._TargetDispenseAmount = TargetDispenseAmount
            self._SendWaterToPreInfuseVessel = SendWaterToPreInfuseVessel
            self._SendWaterToBrewer = SendWaterToBrewer
            self._ResumeFlow = ResumeFlow
            self._FlowMeterQueue.put("StartWaterFlow")
    # Causes the flow meter thread to close all selonoids
    def StopWaterFlow(self):
        self._LogResponse("StopWaterFlow")
        # This triggers the flow meter thread to stop water flow
        self._WaterShouldBeFlowing = False
    # Returns the current tick count
    def GetCurrentTicks(self):
        return self._ticks
    # Returns the current dispensed amount
    def GetCurrentDispensedAmount(self):
        return (self._ticks * self._SensorConstant)
# End Public Functions
# Private Functions
    def _LogResponse(self, Message):
        if(self.Debug):
            logger.info(Message)
    # This function updates the curret dispensed ammount and will return true if the current dispensed amount is >= the target dispense requested amount
    def _HaveReachedTargetDoesAmount(self):
        if(self._TargetDispenseAmount <= 0):
            return False # Always return false because the user has requested a process where they will stop the water flow manually
        else:
            # Calculate the current dispensed amount and return wether it is greater than the target
            return ((self._ticks * self._SensorConstant) >= self._TargetDispenseAmount)
    # This is an internal class function for stopping water flow.
    def _StopWaterFlow(self):
        try:
            self._Rates = []
            self._LogResponse("_StopWaterFlow")
            self._WaterShouldBeFlowing = False
            automationhat.relay.one.off()
            automationhat.relay.two.off()
            automationhat.relay.three.off()
        except Exception as e:
            logger.error("_StopWaterFlow: " + str(e))
    def _StartWaterFlow(self):
        try:
            self._LogResponse("_StartWaterFlow")
            self._Rates = []
            if(self._SendWaterToPreInfuseVessel or self._SendWaterToBrewer):
                self._PrepareToStartWaterFlow()
                self._LogResponse("Opening Main Water Valve")
                automationhat.relay.one.on()   # Open the main water solenoid
                if(self._SendWaterToBrewer):
                    self._LogResponse("Sending Water to Brewer")
                    automationhat.relay.two.on() # Open the brewer solenoid
                if(self._SendWaterToPreInfuseVessel):
                    self._LogResponse("Sending Water to Pre Infuse Vessel")
                    automationhat.relay.three.on() # Open the preinfuse vessel solenoid
            else:
                logger.error("No valid water destination provided to _StartWaterFlow")
        except Exception as e:
            logger.error("_StartWaterFlow: " + str(e))
    # Handles the event raised when an interrupt occurs from the flow meter
    def _FlowMeterTick(self, _):
        if(self._WaterShouldBeFlowing):
            self._ticks += 1
            self._Rates.append((datetime.now() - self._LastTickTime).total_seconds()*1000)
            if(len(self._Rates) > 104):
                self._Rates.pop(0)
            self._LastTickTime = datetime.now()
    # This function should be called before water starts flowing to any location
    def _PrepareToStartWaterFlow(self):
        # If we are resuming flow, don't clear the counter variables
        if(self._ResumeFlow):
            pass
        else:
            self._ticks = 0 # Reset the tick counter to 0
        self._Rates = []
        # Get calibrated flow sensor constant
        self._SensorConstant = round(float(config.get_value("calibration", "water_level")) / float(config.get_value("calibration", "ticks")), 8)
        # Start the flow rate tracking thread
        #self._TrackFlowRateThread = threading.Thread(target=self.TrackFlowRate)
        #self._TrackFlowRateThread.daemon = True
        #self._TrackFlowRateThread.start()
        time.sleep(0.1) #Give the threads time to start
    # This function queues a message to the host thread
    def _QueueWaterFlowingNotification(self, ForceMessage=False):
        try:
            # format is WaterFlowing:{TargetAmount}:{CurrentAmount}
            if((len(self._MainQueue.queue) < 1) or (ForceMessage)):
                self._MainQueue.put("WaterFlowing:"+str(self._TargetDispenseAmount)+":"+str((self._ticks * self._SensorConstant)))
        except Exception as e:
            logger.error("_QueueWaterFlowingNotification: " + str(e))
# End Private Functions
