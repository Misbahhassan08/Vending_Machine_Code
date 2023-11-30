from datetime import datetime
import time
import threading
import queue
#import json
#import requests
import Helpers.GlobalFunctions as s
import Helpers.beep as beep
#import Helpers.flowmeter as flowmeter
import Helpers.configuration as config
import Helpers.logger as logger

class Brew(threading.Thread):
    # Initialize a new instance of the class Brew
    def __init__(self, FlowObject, _MainQueue, _APIQueue):
        threading.Thread.__init__(self)
        self.Debug = config.get_value('debug', 'Brew') == "True"
        self._Buzzer = beep.Beep()
        self._FlowMeter = FlowObject
        self._Brewing = False
        self._BrewQueue = queue.Queue()
        self._TargetYield = 0 # in liters or gallons
        self._TargetToDispense = 0 # Same as yeild, but in ml or oz
        self._TargetFlowRate = 0
        self._LastBrewIntervalIndex = -1
        self._FirstBrewIntervalIndex = -1
        self._IntervalRemainingSeconds = 0
        self._ProfileToBrew = None
        self._BrewProfileSecondsPaused = 0
        self._BrewProfileRemainingSeconds = 0
        self._ProfileBrewStartTime = None
        self._IntervalType = None
        self._IntervalDuration = None
        self._IntervalStartTime = None
        self._IntervalDurationInSeconds = 0
        self._IntervalSecondsPaused = 0
        self._IntervalElapsedSeconds = 0
        self._BrewingComplete = False
        self._BrewingPaused = False
        self._BrewHistoryID = 0
        self._IsMetric = config.get_value("app", "units") == "Metric"
        self.MainQueue = _MainQueue #Keep a pointer to the Main Queue
        self.APIQueue = _APIQueue #Keep a pointer to the Main Queue
        # Start the brew thread
        self.start()
    def __del__(self):
        try:
            pass
            #self.CloseAllThreads()
        except Exception as e:
            logger.error("Brew __del__: " + str(e))
    def run(self):
        s.SetThreadName("BrewBrew")
        self._LogResponse("BrewThread Running")
        while(True):
            Message = self._BrewQueue.get()
            if("StartBrewing" in Message):
                self._LogResponse("Brew command received")
                self._BrewProfile()

# Public Functions
    def BrewProfile(self, ProfileToBrew):
        self._ProfileToBrew = ProfileToBrew
        self._BrewQueue.put("StartBrewing")
    def CancelBrew(self):
        self._Brewing = False
        self._FlowMeter.StopWaterFlow()
        self._LogResponse("Brew Canceled")
    def PauseBrew(self):
        self._LogResponse("Brew Paused")
        try:
            self._BrewingPaused = True
            self._FlowMeter.StopWaterFlow()
        except Exception as e:
            logger.error("Brew Pause Exception: " + str(e))
    def ResumeBrew(self):
        self._LogResponse("Brew Resumed")
        try:
            self._BrewingPaused = False
            if(self._IntervalType == "brew"):
                self._FlowMeter.StartWaterFlow(TargetDispenseAmount=self._TargetToDispense, SendWaterToPreInfuseVessel=False, SendWaterToBrewer=True, ResumeFlow=True)
        except Exception as e:
            logger.error("Brew Resume Exception: " + str(e))
# End Public Functions
# Private Functions
    def _LogResponse(self, Message):
        if(self.Debug):
            logger.info(Message)
    def _GetLastBrewIntervalIndex(self):
        LastBrewIntervalIndex = -1
        for IntervalIndex, Interval in enumerate(self._ProfileToBrew.GetIntervals()):
            if(Interval[0] == "brew"):
                LastBrewIntervalIndex = IntervalIndex
        if(LastBrewIntervalIndex < 0):
            logger.error("No Brew intervals found!")
        return LastBrewIntervalIndex
    def _GetFirstBrewIntervalIndex(self):
        FirstBrewIntervalIndex = -1
        for IntervalIndex, Interval in enumerate(self._ProfileToBrew.GetIntervals()):
            if(Interval[0] == "brew"):
                FirstBrewIntervalIndex = IntervalIndex
                return FirstBrewIntervalIndex
        logger.error("No Brew intervals found!")
        return -1 # No brew intervals found
    def _GetCurrentYield(self):
        CurrentDispensed = self._FlowMeter.GetCurrentDispensedAmount()
        # Coffee Weight * Absorption Rate = Total Weight in lbs
        TotalWeightInLbs = float(self._ProfileToBrew.CoffeeWeight) * float(self._ProfileToBrew.AbsorptionFactor)
        # PreInfuse Oz/lb * Coffee Weight = Total To PreInfused Oz
        TotalPreInfusedInOz = float(self._ProfileToBrew.PreInfuse) * float(self._ProfileToBrew.CoffeeWeight)
        if self._IsMetric:
            return round(CurrentDispensed - TotalWeightInLbs - TotalPreInfusedInOz, 2)
        else:
            return round(CurrentDispensed - (((TotalWeightInLbs / 8.35) * 128) - TotalPreInfusedInOz), 2) / 128
    def _GetTargetToDispense(self):
        if(self._IsMetric):
            return (self._TargetYield * 1000) + ((float(self._ProfileToBrew.CoffeeWeight) * float(self._ProfileToBrew.AbsorptionFactor)) - (float(self._ProfileToBrew.PreInfuse) * float(self._ProfileToBrew.CoffeeWeight)))
        else:
            # Target Yeild * 128 = Target Yield in Oz
            TargetYieldInOz = float(self._ProfileToBrew.ConcentrateYield) * 128
            # Coffee Weight * Absorption Rate = Total Weight in lbs
            TotalWeightInLbs = float(self._ProfileToBrew.CoffeeWeight) * float(self._ProfileToBrew.AbsorptionFactor)
            # 8.35 = Weight per Gallon
            WeightPerGallon = 8.35
            # Total Weight in lbs / Weight per Gallon = Weight In Gallons
            WeightInGallons = TotalWeightInLbs/WeightPerGallon
            # Weight In Gallons / 128 = Weight in Oz
            WeightInOz = WeightInGallons * 128
            # PreInfuse Oz/lb * Coffee Weight = Total To PreInfused Oz
            TotalPreInfusedInOz = float(self._ProfileToBrew.PreInfuse) * float(self._ProfileToBrew.CoffeeWeight)
            # Weight in Oz - Total to PreInfuse in Oz = Amount to add to Total Yield
            AmountToAddToTotalYield = WeightInOz - TotalPreInfusedInOz
            # Target Yeild in Oz + Amount to add to Total Yeild = Total water to dispense
            TotalWaterToDispenseInOz = TargetYieldInOz + AmountToAddToTotalYield
            #print(TargetYieldInOz, WeightInGallons, WeightInOz, TotalPreInfusedInOz, AmountToAddToTotalYield, TotalWaterToDispenseInOz)
            return TotalWaterToDispenseInOz
    def _GetTargetFlowRate(self):
        if(self._IsMetric):
            return (self._TargetYield * 1000) / int(self._ProfileToBrew.BrewMinutes)
        else:
            return (self._TargetYield * 128) / int(self._ProfileToBrew.BrewMinutes)
    def _WaitForIntervalToComplete(self):
        #wait for the interval to finish
        self._IntervalDurationInSeconds = int(self._IntervalDuration) * 60 # convert brew duration to seconds
        self._IntervalStartTime = datetime.strptime((str(datetime.now())[:19]), '%Y-%m-%d %H:%M:%S') # strip off miliseconds. Helps with time formatting
        self._IntervalSecondsPaused = 0 # used to track interval pause time
        self._IntervalElapsedSeconds = 0
        self._IntervalRemainingSeconds = self._IntervalDurationInSeconds
        # While brewing, and the interval has time remaining
        while(self._Brewing and (self._IntervalRemainingSeconds >= 0)):
            CurrentLoopTime = (datetime.now()-self._IntervalStartTime).seconds #loop tracking variable so we don't have to get get datetime.now a bunch of times
            # if we are paused, track the number of paused seconds
            # this needs to be tested before self._IntervalElapsedSeconds is incremented
            if(self._BrewingPaused and (self._IntervalElapsedSeconds < CurrentLoopTime)):
                self._IntervalSecondsPaused += 1
                self._BrewProfileSecondsPaused += 1
            # Set elapsed seconds
            self._IntervalElapsedSeconds = CurrentLoopTime
            # Calculate remaining seconds, inlcuding paused time
            self._IntervalRemainingSeconds = self._IntervalDurationInSeconds - self._IntervalElapsedSeconds + self._IntervalSecondsPaused
            self._QueueWaterBrewStatusNotification()
            if(not self._TargetToDispenseNotReached() and self._IntervalType == "brew"):
                break
    # returns true if water still needs to be dispensed
    def _TargetToDispenseNotReached(self):
        return self._FlowMeter.GetCurrentDispensedAmount() < self._TargetToDispense
    def _GetBrewProfileRemainingSeconds(self):
        return (self._ProfileToBrew.TotalMinutes * 60) - ((datetime.now()-self._ProfileBrewStartTime).seconds) + self._BrewProfileSecondsPaused
    # This function queues a message to the host thread
    def _QueueWaterBrewStatusNotification(self, MessageHeader="Brewing:", ForceMessage=False):
        BrewIntervalRemaining = ""
        RestIntervalRemaining = ""
        if(self._IntervalType == "rest"):
            RestIntervalRemaining = self._IntervalRemainingSeconds
        else:
            BrewIntervalRemaining = self._IntervalRemainingSeconds
        try:
            MessageAlreadyQueued = False
            for item in self.MainQueue.queue:
                if "Brewing" in item:
                    MessageAlreadyQueued = True
        except:
            MessageAlreadyQueued = False
        #logger.info("MessageAlreadyQueued:" + str(MessageAlreadyQueued) + " ForceMessage:" + str(ForceMessage))
        if((not MessageAlreadyQueued) or (ForceMessage)):
             # need to get the remaining time
            self.MainQueue.put(MessageHeader + str(self._FlowMeter.GetAverageFlowRate()) + ":" + str(self._GetCurrentYield()) + ":" + str(self._GetBrewProfileRemainingSeconds()) + ":" + str(BrewIntervalRemaining) + ":" + str(RestIntervalRemaining) + ":" + str(self._BrewingPaused) + ":" + str(self._BrewingComplete) + ":" + str(self._BrewHistoryID) + ":" + str(self._ProfileToBrew.BrewProfileID))
        time.sleep(.05)
    def _BrewProfile(self):
        try:
            self._ProfileBrewStartTime = datetime.strptime((str(datetime.now())[:19]), '%Y-%m-%d %H:%M:%S') # strip off miliseconds. Helps with time formatting
            self._BrewProfileRemainingSeconds = int(self._ProfileToBrew.TotalMinutes) * 60
            self._Brewing = True
            self._BrewProfileSecondsPaused = 0
            self._TargetYield = float(self._ProfileToBrew.ConcentrateYield)
            self._TargetToDispense = self._GetTargetToDispense()
            self._TargetFlowRate = self._GetTargetFlowRate()
            self._LastBrewIntervalIndex = self._GetLastBrewIntervalIndex()
            self._FirstBrewIntervalIndex = self._GetFirstBrewIntervalIndex()
            self._FlowMeter.ResetFlowMeter()
            self._BrewingComplete = False
            self._BrewingPaused = False
            self._BrewHistoryID = 0
            self._QueueWaterBrewStatusNotification(ForceMessage=True)

            for IntervalIndex, Interval in enumerate(self._ProfileToBrew.GetIntervals()):
                self._IntervalType = Interval[0]
                self._IntervalDuration = Interval[1]
                self._LogResponse("Brew interval change. On interval " + str(IntervalIndex) + " " + self._IntervalType)
                if(not self._Brewing):
                    self._LogResponse("Exit for self._Brewing not True")
                    break
                if(self._FlowMeter.GetCurrentDispensedAmount() >= self._TargetToDispense):
                    if(self._IntervalType == "brew"):
                        self._LogResponse("Exit for self._FlowMeter.GetCurrentDispensedAmount() >= self._TargetToDispense")
                        self._LogResponse("Current: " + str(self._FlowMeter.GetCurrentDispensedAmount()) + " Target:" + str(self._TargetToDispense))
                        break
                    else:
                        self._LogResponse("Brew Yield Reached. Waiting final rest interval.")
                if(self._IntervalType == "rest"):
                    self._FlowMeter.StopWaterFlow()
                    self._WaitForIntervalToComplete()
                if(self._IntervalType == "brew"):
                    if(IntervalIndex == self._FirstBrewIntervalIndex):
                        self._FlowMeter.StartWaterFlow(TargetDispenseAmount=self._TargetToDispense, SendWaterToPreInfuseVessel=False, SendWaterToBrewer=True, ResumeFlow=False)
                        self._WaitForIntervalToComplete()
                    else:
                        self._FlowMeter.StartWaterFlow(TargetDispenseAmount=self._TargetToDispense, SendWaterToPreInfuseVessel=False, SendWaterToBrewer=True, ResumeFlow=True)
                        self._WaitForIntervalToComplete()
                        if(IntervalIndex == self._LastBrewIntervalIndex):
                            # Continue brewing until yield is reached
                            while(self._TargetToDispenseNotReached()):
                                self._LogResponse("Brew Target not reached on last brew interval. Restarting interval " + str(IntervalIndex) + " " + self._IntervalType)
                                self._IntervalRemainingSeconds = self._IntervalDuration # Reset the current intervals remaining time
                                self._FlowMeter.StartWaterFlow(TargetDispenseAmount=self._TargetToDispense, SendWaterToPreInfuseVessel=False, SendWaterToBrewer=True, ResumeFlow=True)
                                self._WaitForIntervalToComplete()
                                if(not self._Brewing):
                                    break
                self._LogResponse("Brew interval " + str(IntervalIndex) + " " + self._IntervalType + " Complete.")
            self._LogResponse("Brew Completed: Dispensed: " + str(self._FlowMeter.GetCurrentDispensedAmount()) + " Target Dispense: " + str(self._TargetToDispense))
            self._BrewingComplete = True
            self._Brewing = False
            self._QueueWaterBrewStatusNotification(MessageHeader="BrewingComplete:", ForceMessage=True)
            self._Buzzer.Beep(1)
        except Exception as e:
            logger.error("Error Brewing: " + str(e))
# End Private Functions
