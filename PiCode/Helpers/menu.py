#!/usr/bin/env python3
#import json
import os
import threading
import queue
import time
from datetime import datetime
import Helpers.logger as logger
#import Helpers.checkin as checkin
import Helpers.wificontroller as wificontroller
import Helpers.Graphics.Screen as GraphicsDriver
import Helpers.encoder as encoder
import Helpers.configuration as config
import Helpers.profile as profile
import Helpers.brew as brew
import Helpers.flowmeter as flowmeter
import Helpers.GlobalFunctions as s
#from Helpers.Graphics.Screens import *

class Menu(threading.Thread):
    def __init__(self, _MainQueue, _APIQueue):
        threading.Thread.__init__(self)
# Command, Data
# DrawImageFromFlash: ImageName, X, Y, Rotate Angle
        logger.info("Menu Thread Starting")
        self.MainQueue = _MainQueue #Keep a pointer to the Main Queue
        self.APIQueue = _APIQueue #Keep a pointer to the API Queue
        self.daemon = True
        # Keyboard tracking variables
        self.KeyboardShift = True
        self.KeyboardRow = 0
        self.KeyboardColumn = 0
        self.EncoderDebug = config.get_value('debug', 'Encoder') == "True"
        self.EncoderMode = "NavigateMenu" #NavigateMenu for menu operation, Keyboard for Keyboard
        self._LastEncoderAction = ""
        self.CurrentKeyboardKey = "~"
        self.KeyboardString = ""
        self.KeyboardInputTitle = ""
        self.KeyboardMode = "Wifi"
        # Encoder Tracking Variables
        self.EncoderAction = ""
        # GPIO Ports
        self.FlowMeterPin = 21
        self.Enc_A = 24  # Encoder input A: input GPIO 20 (active high)
        self.Enc_B = 23  # Encoder input B: input GPIO 21 (active high)
        self.Enc_C = 18
        #Bus ID (Found in /dev/spi... Default is 0
        #Device ID (Found in /dev/spi... Default is 0
        #hooked to the !RST pin on  the screen default is 5
        self.ScreenResetPin = 5
        self.ScreenBus = 0
        self.ScreenDeviceID = 0

        self.BrewStatusWorker = s.AsynchronousWorker(None)
        self._Calibrated = config.get_value("calibration", "calibrated") == "True"
        # Menus
        self.MainMenuScreen1 = ["~Main Menu~", "Settings", "Calibrate", "", ""]
        self.UpdateMainMenu()
        self.MainMenu = [self.MainMenuScreen1]
        self.BrewProfileMenu = [[""]]
        self.WifiSSIDMenu = [[""]]
        self.SettingsScreen1 = ["Settings", "Calibrate Flow Meter", "Connect to Wifi", "Display System Info", "                           <- Back"]
        self.SettingsScreen2 = ["Settings", "", "Exit Application", "Connect SSH", "                           <- Back"]
        self.SettingsMenu = [self.SettingsScreen1]
        # Menu Tracking Variabls
        self.ActiveMenu = self.MainMenu
        self.SelectedScreen = 0
        self.SelectedMenuItem = 2
        self.ActiveBrewProfile = ""
        #self.ActiveBrew = ""
        self.BrewWizardSelectedButton = ""
        self.DoseStarted = False
        self.BrewCurrentDoseAmount = 0
        self.DoseCompleted = False
        self.TargetDoseAmount = 0
        self.CancelStarted = False

        self.RotaryEncoder = encoder.Encoder(self.Enc_A, self.Enc_B, self.Enc_C, self.Navigator)
        self.GD = None
        self.WaterFlowMeter = flowmeter.FlowMeter(self.MainQueue, self.FlowMeterPin)

        self.Brewer = brew.Brew(self.WaterFlowMeter, self.MainQueue, self.APIQueue)
        self.BrewStarted = False
        self.CurrentFlowRate = 0
        self.CurrentYield = 0
        self.RemainingTime = 0
        self.BrewIntervalRemaining = 0
        self.RestIntervalRemaining = 0
        self.BrewingPaused = False
        self.BrewingComplete = False
        self.Brewing = False
        self.BrewProfileID = 0
        self.BrewStartDateTime = datetime.now()
        # Wifi Tracking Variables
        self.wifi = wificontroller.WifiController(self.MainQueue)
        self.WIFISelectedSSID = ""
        self.WifiPassword = ""
        self.start()
    def run(self):
        s.SetThreadName("BrewMenu")
        logger.info("Menu Thread Running")
        #self.RotaryEncoder = encoder.Encoder(self.Enc_A, self.Enc_B, self.Enc_C)
        self.GD = GraphicsDriver.GraphicsDriver(self.ScreenResetPin, self.ScreenBus, self.ScreenDeviceID)
        time.sleep(.25)
        #Draw the initial screen
        self.DrawMainScreen()
        config.set_value('AppStatus', 'ApplicationStatus', 'Idle')
        while(True):
            self.CheckForMessages()
        logger.info("Menu Thread Ended")
    def CheckForMessages(self):
        try:
            Message = self.MainQueue.get()
            if(Message == "Update"):
                self.GD.DrawSpinner("Updating")
                while(True):
                    time.sleep(1)  #Lock the thread and wait for the updater to kill the application
            if("Navigate" in Message):
                Values = Message.split(":")
                EncoderAction = Values[1]
                self.Navigate(EncoderAction)
            if("WifiSignalStrength" in Message):
                self.GD.WifiStrength = self.wifi.WifiSignalStrength()
                if(self.EncoderMode == "NavigateMenu" and self.ActiveMenu[0] == self.MainMenuScreen1):
                    self.DrawMainScreen()
                else:
                    if(self.EncoderMode == "NavigateMenu"):
                        self.GD.DrawMenu(self.ActiveMenu[self.SelectedScreen], self.SelectedMenuItem)
            if("WaterFlowing" in Message):
                try:
                    self.GD.WaterIsFlowing = True
                    if(config.get_value("debug", "FlowMeter") == "True"):
                        logger.info("WaterFlowing:"+Message)
                    Values = Message.split(":")
                    self.TargetDoseAmount = Values[1]
                    self.BrewCurrentDoseAmount = Values[2]
                    if(self.EncoderMode == "FlowCalibrationPrompt"):
                        if(not self.DoseCompleted):
                            self.GD.DrawFlowCalibrationPrompt(self.DoseStarted, self.WaterFlowMeter.GetCurrentTicks(), self.BrewWizardSelectedButton, self.DoseCompleted)
                    if(self.EncoderMode == "BrewWizardPage4"):
                        if(not self.DoseCompleted):
                            self.BrewWizardSelectedButton = "Cancel"
                        else:
                            self.BrewWizardSelectedButton = ''
                        self.DisplayBrewWizardPage4()
                except Exception as e:
                    logger.error("WaterFlowing Message: " + str(e))
            if("WaterFlowStopped" in Message):
                try:
                    self.GD.WaterIsFlowing = False
                    if(config.get_value("debug", "FlowMeter") == "True"):
                        logger.info("WatterFlowStopped:"+Message)
                    Values = Message.split(":")
                    ticks = Values[1]
                    if(self.EncoderMode == "FlowCalibrationPrompt"):
                        if(self.BrewWizardSelectedButton == "Stop"):
                            config.set_value("calibration", "calibrated", True)
                            is_metric = config.get_value("app", "units") == "Metric"
                            if(is_metric):
                                config.set_value("calibration", "water_level", 1000) #1000 ml
                            else:
                                config.set_value("calibration", "water_level", 32) #32 oz
                        config.set_value("calibration", "ticks", int(ticks))
                        self._Calibrated = True
                        self.DoseCompleted = True
                        self.BrewWizardSelectedButton = "Continue"
                        #self.GD.DrawFlowCalibrationPrompt(self.DoseStarted, ticks, '', self.DoseCompleted)
                        self.ReturnToMenu()
                    if(self.EncoderMode == "BrewWizardPage4"):
                        self.DoseCompleted = True
                        self.BrewWizardSelectedButton = ''
                        try:
                            self.DisplayBrewWizardPage4()
                        except Exception as e:
                            logger.error("Menu Message WaterFlowStopped Excception: " + str(e))
                except Exception as e:
                    logger.error("WaterFlowStopped Message: " + str(e))
            if("Brewing:" in Message):
                try:
                    if(config.get_value("debug", "BrewScreenUpdates") == "True"):
                        logger.info("Brewing:"+Message)
                    self.DrawBrewStatus(Message)
                    self.QueueBrewStatusAPIUpdate()
                except Exception as e:
                    logger.error("Brewing Message: " + str(e))
            if("BrewingComplete:" in Message):
                try:
                    logger.info("BrewingComplete:"+Message)
                    config.set_value("AppStatus", "ApplicationStatus", "Idle")
                    self.BrewWizardSelectedButton = "Continue"
                    self.EncoderMode = "Brewing"
                    self.CancelStarted = False
                    #self.CancelBrew()
                    self.DrawBrewStatus(Message)
                    self.QueueBrewStatusAPIUpdate()
                except Exception as e:
                    logger.error("BrewingComplete Message: " + str(e))
        except queue.Empty:
            pass
        except Exception as e:
            logger.error("Menu Message Exception: " + str(e))
        time.sleep(0.01)
    def DrawMainScreen(self):
        self.GD.DrawScreenMainMenu(self._Calibrated, self.ActiveMenu[self.SelectedScreen][self.SelectedMenuItem])
    def DisplayBrewWizardPage4(self):
        self.GD.DrawScreenBrewWizardPage4(TargetDoseAmount=self.TargetDoseAmount, CurrentDoseAmount=self.BrewCurrentDoseAmount, DoseComplete=self.DoseCompleted, SelectedKey=self.BrewWizardSelectedButton)
    def DrawBrewStatus(self, Message):
        Values = Message.split(":")
        self.CurrentFlowRate = Values[1]
        self.CurrentYield = Values[2]
        self.RemainingTime = Values[3]
        self.BrewIntervalRemaining = Values[4]
        self.RestIntervalRemaining = Values[5]
        self.BrewingPaused = Values[6] == "True"
        self.BrewingComplete = Values[7] == "True"
        self.BrewProfileID = Values[9]
        self.BrewStarted = True
        if(self.EncoderMode == "Brewing"):
            self.GD.DrawBrewing(self.ActiveBrewProfile.TargetFlowRate, self.CurrentFlowRate, self.ActiveBrewProfile.ConcentrateYield, self.CurrentYield, self.ActiveBrewProfile.TotalMinutes, self.RemainingTime, self.BrewIntervalRemaining, self.RestIntervalRemaining, self.BrewingPaused, self.BrewingComplete, self.BrewWizardSelectedButton, self.CancelStarted)
        if(self.EncoderMode == "BrewWizardPage6"):
            self.GD.DrawScreenBrewWizardPage6(self.ActiveBrewProfile.TargetFlowRate, self.CurrentFlowRate, self.BrewWizardSelectedButton)
    def QueueBrewStatusAPIUpdate(self):
        # if we are not already sending an update, send an update
        BrewStatusAPIAlreadyQueued =  False
        if(len(self.APIQueue.queue) > 0):
            for item in self.APIQueue.queue:
                if "BrewStatus" in item:
                    BrewStatusAPIAlreadyQueued = True
        if(not BrewStatusAPIAlreadyQueued):
            if(self.BrewStatusWorker.isAlive() is not True):
                self.BrewStatusWorker = s.AsynchronousWorker(self.SendBrewStatus)
    # This function should only be called from an asynchronus worker or it will block screen drawing.
    def SendBrewStatus(self):
        try:
            self.APIQueue.put(
                "BrewStatus:" +
                str(self.BrewStartDateTime).replace(':', '_') + ":" +
                str(self.BrewProfileID) + ":" +
                str(self.ActiveBrewProfile.BrewProfileName) + ":" +
                str(self.CurrentFlowRate) + ":" +
                str(self.CurrentYield) + ":" +
                str(self.ActiveBrewProfile.TotalMinutes) + ":" +
                str(self.RemainingTime) + ":" +
                str(self.BrewIntervalRemaining) + ":" +
                str(self.RestIntervalRemaining) + ":" +
                str(self.BrewingPaused) + ":" +
                str(self.BrewingComplete) + ":" +
                str(self.ActiveBrewProfile.TargetFlowRate) + ":" +
                str(self.ActiveBrewProfile.ConcentrateYield)
            )
        except Exception as e:
            logger.error("Menu SendBrewStatus Exception:" + str(e))
    def Navigate(self, EncoderAction):
        if(self.EncoderDebug):
            logger.info("Encoder Mode: " + str(self.EncoderMode))
            logger.info("BrewWizard Selected Button: " + str(self.BrewWizardSelectedButton))
            logger.info("Active Menu: " + str(self.ActiveMenu))
            logger.info("Active Brew Profile: " + str(self.ActiveBrewProfile))

        self.UpdateMainMenu()
        try:
            if(EncoderAction == "Left"):
                if(self.EncoderDebug):
                    logger.info("Navigator-Left")
                self.ScrollLeft()
            if(EncoderAction == "Right"):
                if(self.EncoderDebug):
                    logger.info("Navigator-Right")
                self.ScrollRight()
            if(EncoderAction == "Up"):
                if(self.EncoderDebug):
                    logger.info("Navigator-Up")
                if(self._LastEncoderAction == "Down"):
                    if(self.EncoderDebug):
                        logger.info("Navigator-Down/Up")
                    self.ButtonPressed()
            if(EncoderAction == "Down"):
                if(self.EncoderDebug):
                    logger.info("Navigator-Down")
                self.ButtonDown()
            if(EncoderAction == "LongPress"):
                if(self.EncoderDebug):
                    logger.info("Navigator-LongPress")
                self.ButtonLongPress()
            if(EncoderAction == "VeryLongPress"):
                if(self.EncoderDebug):
                    logger.info("Navigator-VeryLongPress")
                self.ButtonVeryLongPress()
        except Exception as e:
            logger.error("Menu Navigator Exception" + e)
        self._LastEncoderAction = EncoderAction
        if(self.EncoderDebug):
            logger.info("End Navigate")
    def Navigator(self, EncoderAction):
        # Send the navigate signal to the main queue
        # This prevents screen draws on navigate from occuring while other screen drawing is happening.
        if(self.EncoderDebug):
            logger.info("Start Navigate")
        NavigationAlreadyQueued = False
        if(len(self.MainQueue.queue) > 0):
            for item in self.MainQueue.queue:
                if "Navigate" in item:
                    NavigationAlreadyQueued = True
        if(not NavigationAlreadyQueued):
            self.MainQueue.put("Navigate:" + EncoderAction)
#Event Handlers
    def ButtonDown(self):
        return
    def ButtonPressed(self):
        if(self.EncoderDebug):
                logger.info("ButtonPressed EncoderMode: " + str(self.EncoderMode) + " SelectedButton: " + str(self.BrewWizardSelectedButton) + " KeyboardKey: " + str(self.CurrentKeyboardKey))
        if(self.EncoderMode == "Info"):
            self.EncoderMode = "NavigateMenu"
            self.ReturnToMenu()
            return
        if(self.EncoderMode == "BrewWizardPage1"):
            if(self.BrewWizardSelectedButton == "Continue"):
                self.EncoderMode = "BrewWizardPage2"
                self.GD.DrawScreenBrewWizardPage2(str(self.ActiveBrewProfile.CoffeeGrinderName), str(self.ActiveBrewProfile.CoffeeGrinderSetting))
                return
            if(self.BrewWizardSelectedButton == "Cancel"):
                self.ReturnToMenu()
                return
        if(self.EncoderMode == "BrewWizardPage2"):
            if(self.BrewWizardSelectedButton == "Continue"):
                if(self.ActiveBrewProfile.PreInfuse == 0):
                    self.EncoderMode = "BrewWizardPage5"
                    self.GD.DrawScreenBrewWizardPage5()
                    self.DoseStarted = False
                    self.DoseCompleted = True
                    self.TargetDoseAmount = 0
                else:
                    self.EncoderMode = "BrewWizardPage3"
                    self.GD.DrawScreenBrewWizardPage3()
                return
            if(self.BrewWizardSelectedButton == "Cancel"):
                self.ReturnToMenu()
                return
        if(self.EncoderMode == "BrewWizardPage3"):
            if(self.BrewWizardSelectedButton == "Dose"):
                self.EncoderMode = "BrewWizardPage4"
                self.BrewWizardSelectedButton = "Cancel"
                self.BrewCurrentDoseAmount = 0
                self.DoseStarted = True
                self.DoseCompleted = False
                self.TargetDoseAmount = (self.ActiveBrewProfile.CoffeeWeight * self.ActiveBrewProfile.PreInfuse)
                self.DisplayBrewWizardPage4()
                self.WaterFlowMeter.StartWaterFlow(TargetDispenseAmount=self.TargetDoseAmount, SendWaterToPreInfuseVessel=True, SendWaterToBrewer=False, ResumeFlow=False)
                return
            if(self.BrewWizardSelectedButton == "Cancel"):
                self.ReturnToMenu()
                return
        if(self.EncoderMode == "BrewWizardPage4"):
            if(self.BrewWizardSelectedButton == "Continue"):
                self.EncoderMode = "BrewWizardPage5"
                self.GD.DrawScreenBrewWizardPage5()
                return
            if(self.BrewWizardSelectedButton == "Cancel"):
                if(self.DoseStarted):
                    self.BrewWizardSelectedButton = ""
                    self.WaterFlowMeter.StopWaterFlow()
                self.ReturnToMenu()
                return
        if(self.EncoderMode == "BrewWizardPage5"):
            if(self.BrewWizardSelectedButton == "Brew"):
                self.EncoderMode = "BrewWizardPage6"
                self.StartBrew()
                self.BrewWizardSelectedButton = ""
                self.GD.DrawScreenBrewWizardPage6(self.ActiveBrewProfile.TargetFlowRate, self.CurrentFlowRate, self.BrewWizardSelectedButton)
                return
            if(self.BrewWizardSelectedButton == "Cancel"):
                self.ReturnToMenu()
                return
        if(self.EncoderMode == "BrewWizardPage6"):
            if(self.BrewWizardSelectedButton == "Continue"):
                self.EncoderMode = "Brewing"
                return
            # if(self.BrewWizardSelectedButton == "Cancel"):
            #     self.ReturnToMenu()
            #     return
        if(self.EncoderMode == "Brewing"):
            if(self.BrewWizardSelectedButton == "Continue"):
                self.ReturnToMenu()
                return
            if(self.BrewWizardSelectedButton == "Resume"):
                self.ResumeBrew()
                return
            if(self.BrewWizardSelectedButton == "Pause"):
                self.PauseBrew()
                return
            if(self.BrewWizardSelectedButton == "Cancel"):
                self.CancelStarted = True
            if(self.BrewWizardSelectedButton == "CancelCancel"):
                self.CancelStarted = False
            if(self.BrewWizardSelectedButton == "CancelConfirm"):
                self.CancelBrew()
                #self.ReturnToMenu()
                #return
        if(self.EncoderMode == "FlowCalibrationPrompt"):
            if(self.BrewWizardSelectedButton == "Calibrate"):
                self.BrewWizardSelectedButton = ""
                self.DoseStarted = True
                self.DoseCompleted = False
                self.GD.DrawFlowCalibrationPrompt(self.DoseStarted, 0, self.BrewWizardSelectedButton, self.DoseCompleted)
                self.WaterFlowMeter.StartWaterFlow(0, True, False, False)
            if(self.BrewWizardSelectedButton == "Continue"):
                self.ReturnToMenu()
                return
            if(self.BrewWizardSelectedButton == "Stop"):
                self.WaterFlowMeter.StopWaterFlow()
            if(self.BrewWizardSelectedButton == "Cancel"):
                if(self.DoseStarted & (not self.DoseCompleted)):
                    self.BrewWizardSelectedButton = ""
                    self.WaterFlowMeter.StopWaterFlow()
                else:
                    self.ReturnToMenu()
                return
        if(self.EncoderMode == "Keyboard"):
            if(self.CurrentKeyboardKey == "Space"):
                self.KeyboardString += " "
            elif(self.CurrentKeyboardKey == "BackSpace"):
                self.KeyboardString = self.KeyboardString[:-1]
            elif(self.CurrentKeyboardKey == "Shift"):
                self.KeyboardShift = (not self.KeyboardShift)
            elif(self.CurrentKeyboardKey == "Cancel"):
                self.WIFISelectedSSID = ""
                self.WifiPassword = ""
                self.KeyboardMode = ""
                self.ActiveMenu = self.SettingsMenu
                self.KeyboardString = ""
                self.SelectedMenuItem = 2
                self.SelectedScreen = 0
                self.EncoderMode = "NavigateMenu"
                self.ReturnToMenu()
                return
            elif(self.CurrentKeyboardKey == "Done"):
                self.EncoderMode = "NavigateMenu"
                if(self.KeyboardMode == "Wifi"):
                    self.WifiPassword = self.KeyboardString
                    self.KeyboardString = ""
                    self.ActiveMenu = self.SettingsMenu
                    self.SelectedMenuItem = 2
                    self.SelectedScreen = 0
                    self.ConfigureWifi()
                self.KeyboardMode = ""
                self.ReturnToMenu()
                return
            else:
                self.KeyboardString += self.CurrentKeyboardKey
            self.GD.DrawKeyboard(self.KeyboardShift, self.CurrentKeyboardKey, self.KeyboardString, self.KeyboardInputTitle)
        if(self.EncoderMode == "NavigateMenu"):
            self.MenuAction(self.ActiveMenu, self.ActiveMenu[self.SelectedScreen][self.SelectedMenuItem])
    def ButtonLongPress(self):
        self.KeyboardShift = (not self.KeyboardShift)
        self.NavigateKeyboard("None")
    def ButtonVeryLongPress(self):
        print("Very Long Press")
        logger.info("Very Long Press")
        logger.info("Enabling Hidden Screens")
        self.SettingsMenu = [self.SettingsScreen1, self.SettingsScreen2]
    def ScrollLeft(self):
        if(self.EncoderMode == "FlowCalibrationPrompt"):
            self.BrewWizardSelectedButton = "Cancel"
            self.GD.DrawFlowCalibrationPrompt(self.DoseStarted, self.WaterFlowMeter.GetCurrentTicks(), self.BrewWizardSelectedButton, self.DoseCompleted)
        if(self.EncoderMode == "BrewWizardPage1"):
            self.BrewWizardSelectedButton = "Cancel"
            self.GD.DrawScreenBrewWizardPage1(str(self.ActiveBrewProfile.CoffeeOriginName), str(self.ActiveBrewProfile.CoffeeWeight), self.BrewWizardSelectedButton)
        if(self.EncoderMode == "BrewWizardPage2"):
            self.BrewWizardSelectedButton = "Cancel"
            self.GD.DrawScreenBrewWizardPage2(str(self.ActiveBrewProfile.CoffeeGrinderName), str(self.ActiveBrewProfile.CoffeeGrinderSetting), self.BrewWizardSelectedButton)
        if(self.EncoderMode == "BrewWizardPage3"):
            self.BrewWizardSelectedButton = "Cancel"
            self.GD.DrawScreenBrewWizardPage3(self.BrewWizardSelectedButton)
        if(self.EncoderMode == "BrewWizardPage4"):
            self.BrewWizardSelectedButton = "Cancel"
            self.DisplayBrewWizardPage4()
        if(self.EncoderMode == "BrewWizardPage5"):
            self.BrewWizardSelectedButton = "Cancel"
            self.GD.DrawScreenBrewWizardPage5(self.BrewWizardSelectedButton)
        if(self.EncoderMode == "BrewWizardPage6"):
            self.BrewWizardSelectedButton = ""
            self.GD.DrawScreenBrewWizardPage6(self.ActiveBrewProfile.TargetFlowRate, self.CurrentFlowRate, self.BrewWizardSelectedButton)
        if(self.EncoderMode == "Brewing"):
            if(self.BrewingComplete):
                self.BrewWizardSelectedButton = "Continue"
            else:
                if self.CancelStarted:
                    self.BrewWizardSelectedButton = "CancelCancel"
                else:
                    self.BrewWizardSelectedButton = "Cancel"
        if(self.EncoderMode == "NavigateMenu"):
            # navigating left decrement to the next menu item up:
            #   if we are on the first screen
            #        move to the next non-blank menu item
            #        if we are on the last non-blank menu item, don't increment
            #   if we are not on the first screen
            #        if we are on the last non-blank item
            #             move to the last non-blank item on the next screen
            try:
                if(self.OnFirstScreen(self.ActiveMenu)):
                    if(not self.OnFirstScreenMenuItem(self.ActiveMenu[self.SelectedScreen])):
                        self.SelectedMenuItem = self.GetNextLeftScreenMenuItem(self.ActiveMenu[self.SelectedScreen], self.SelectedMenuItem)
                        if(self.SelectedMenuItem < 1):
                            self.SelectedMenuItem = self.GetFirstScreenMenuItem(self.ActiveMenu[self.SelectedScreen])
                else:
                    if(self.OnFirstScreenMenuItem(self.ActiveMenu[self.SelectedScreen])):
                        self.SelectedScreen -= 1
                        self.SelectedMenuItem = self.GetNextLeftScreenMenuItem(self.ActiveMenu[self.SelectedScreen], 5)
                    else:
                        self.SelectedMenuItem = self.GetNextLeftScreenMenuItem(self.ActiveMenu[self.SelectedScreen], self.SelectedMenuItem)
            except Exception as e:
                logger.error("Menu ScrollLeft Exception:" + str(e))
        if(self.EncoderMode == "Keyboard"):
            self.NavigateKeyboard("Left")
        if(self.EncoderMode == "NavigateMenu"):
            if(self.ActiveMenu[0] == self.MainMenuScreen1):
                self.DrawMainScreen()
            else:
                self.GD.DrawMenu(self.ActiveMenu[self.SelectedScreen], self.SelectedMenuItem)
    def ScrollRight(self):
        if(self.EncoderMode == "FlowCalibrationPrompt"):
            if(not self.DoseStarted):
                self.BrewWizardSelectedButton = "Calibrate"
                self.GD.DrawFlowCalibrationPrompt(self.DoseStarted, 0, self.BrewWizardSelectedButton, self.DoseCompleted)
            else:
                self.BrewWizardSelectedButton = "Stop"
                self.GD.DrawFlowCalibrationPrompt(self.DoseStarted, self.WaterFlowMeter.GetCurrentTicks(), self.BrewWizardSelectedButton, self.DoseCompleted)
        if(self.EncoderMode == "BrewWizardPage1"):
            self.BrewWizardSelectedButton = "Continue"
            self.GD.DrawScreenBrewWizardPage1(str(self.ActiveBrewProfile.CoffeeOriginName), str(self.ActiveBrewProfile.CoffeeWeight), self.BrewWizardSelectedButton)
        if(self.EncoderMode == "BrewWizardPage2"):
            self.BrewWizardSelectedButton = "Continue"
            self.GD.DrawScreenBrewWizardPage2(str(self.ActiveBrewProfile.CoffeeGrinderName), str(self.ActiveBrewProfile.CoffeeGrinderSetting), self.BrewWizardSelectedButton)
        if(self.EncoderMode == "BrewWizardPage3"):
            self.BrewWizardSelectedButton = "Dose"
            self.GD.DrawScreenBrewWizardPage3(self.BrewWizardSelectedButton)
        if(self.EncoderMode == "BrewWizardPage4"):
            if(self.DoseStarted):
                if(self.DoseCompleted):
                    self.BrewWizardSelectedButton = "Continue"
            else:
                self.BrewWizardSelectedButton = "Dose"
            self.DisplayBrewWizardPage4()
        if(self.EncoderMode == "BrewWizardPage5"):
            self.BrewWizardSelectedButton = "Brew"
            self.GD.DrawScreenBrewWizardPage5(self.BrewWizardSelectedButton)
        if(self.EncoderMode == "BrewWizardPage6"):
            self.BrewWizardSelectedButton = "Continue"
            self.GD.DrawScreenBrewWizardPage6(self.ActiveBrewProfile.TargetFlowRate, self.CurrentFlowRate, self.BrewWizardSelectedButton)
        if(self.EncoderMode == "Brewing"):
            if(self.BrewStarted and not self.BrewingComplete):
                if self.CancelStarted:
                    self.BrewWizardSelectedButton = "CancelConfirm"
                else:
                    if(str(self.BrewingPaused) == "True"):
                        self.BrewWizardSelectedButton = "Resume"
                        return
                    else:
                        self.BrewWizardSelectedButton = "Pause"
                        return
            if(self.BrewingComplete):
                self.BrewWizardSelectedButton = "Continue"
        if(self.EncoderMode == "NavigateMenu"):
            # navigating right increment to the next menu item down:
            #   if we are on the last screen
            #        move to the next non-blank menu item
            #        if we are on the last non-blank menu item, don't increment
            #   if we are not on the last screen
            #        if we are on the last non-blank item
            #             move to the first non-blank item on the next screen
            try:
                if(self.OnLastScreen(self.ActiveMenu)):
                    if(not self.OnLastScreenMenuItem(self.ActiveMenu[self.SelectedScreen])):
                        self.SelectedMenuItem = self.GetNextRightScreenMenuItem(self.ActiveMenu[self.SelectedScreen], self.SelectedMenuItem)
                        if(self.SelectedMenuItem > 4):
                            self.SelectedMenuItem = self.GetLastScreenMenuItem(self.ActiveMenu[self.SelectedScreen])
                else:
                    if(self.OnLastScreenMenuItem(self.ActiveMenu[self.SelectedScreen])):
                        self.SelectedScreen += 1
                        self.SelectedMenuItem = self.GetNextRightScreenMenuItem(self.ActiveMenu[self.SelectedScreen], 0)
                    else:
                        self.SelectedMenuItem = self.GetNextRightScreenMenuItem(self.ActiveMenu[self.SelectedScreen], self.SelectedMenuItem)
            except Exception as e:
                logger.error("Menu ScrollRight Exception:" + str(e))
        if(self.EncoderMode == "Keyboard"):
            self.NavigateKeyboard("Right")
        if(self.EncoderMode == "NavigateMenu"):
            if(self.ActiveMenu[0] == self.MainMenuScreen1):
                self.DrawMainScreen()
            else:
                self.GD.DrawMenu(self.ActiveMenu[self.SelectedScreen], self.SelectedMenuItem)
#End Event Handlers
#Menu Helpers
    def UpdateMainMenu(self):
        self._Calibrated = config.get_value("calibration", "calibrated") == "True"
        if(self._Calibrated):
            self.MainMenuScreen1[2] = "Brew"
        else:
            self.MainMenuScreen1[2] = "Calibrate"
    def GetMenuScreen(self, ScreenName, Profile1, Profile2, Profile3, Profile4):
        return [ScreenName, Profile1, Profile2, Profile3, Profile4]
    def BuildBrewProfileMenu(self):
        profiles = config.get_sections("profiles")
        BrewProfilesScreen = ["Select Brew Profile", "No Profiles Available", "", "", "                           <- Back"]
        if(len(profiles) == 0):
            BrewProfilesScreen = ["Select Brew Profile", "No Profiles Available", "", "", "                           <- Back"]
            self.BrewProfileMenu = [BrewProfilesScreen]
            return
        ProfileCounter = 1
        ProfileScreenCounter = 0
        self.BrewProfileMenu = []
        for Profile in profiles:
            BrewProfilesScreen[ProfileCounter] = Profile
            ProfileCounter += 1
            if(ProfileCounter == 5):
                #print(BrewProfilesScreen)
                self.BrewProfileMenu.append(self.GetMenuScreen(BrewProfilesScreen[0], BrewProfilesScreen[1], BrewProfilesScreen[2], BrewProfilesScreen[3], BrewProfilesScreen[4]))
                #print(self.BrewProfileMenu)
                ProfileScreenCounter += 1
                ProfileCounter = 1
                BrewProfilesScreen[1] = ""
                BrewProfilesScreen[2] = ""
                BrewProfilesScreen[3] = ""
                BrewProfilesScreen[4] = "                           <- Back"
                ProfileCounter = 1
        #print(ProfileCounter, self.BrewProfileMenu)
        #if there aren't enough items in the list to roll over the first screen, then we need to add the current screen
        if(ProfileScreenCounter == 0):
            self.BrewProfileMenu.append(self.GetMenuScreen(BrewProfilesScreen[0], BrewProfilesScreen[1], BrewProfilesScreen[2], BrewProfilesScreen[3], BrewProfilesScreen[4]))
        #if there arent' enough items in the list to roll over the next screen, then we need to add the current screen
        if(ProfileCounter < 5):
            self.BrewProfileMenu.append(self.GetMenuScreen(BrewProfilesScreen[0], BrewProfilesScreen[1], BrewProfilesScreen[2], BrewProfilesScreen[3], BrewProfilesScreen[4]))
        #if there are exactly 4 items left in this screen, we need to add a new screen with the back button
        #if(ProfileCounter == 5):
        #    self.BrewProfileMenu.append(self.GetMenuScreen(BrewProfilesScreen[0], "                           <- Back", "", "", ""))

        #print(self.BrewProfileMenu)
    def BuildWifiSSIDMenu(self):
        AvailableNetworks = self.wifi.GetAvailableSSIDs()

        WifiSSIDsScreen = ["Connect Wifi", "Hidden Netowrk", "", "", "                           <- Back"]
        if(len(AvailableNetworks) == 0):
            WifiSSIDsScreen = ["Connect Wifi", "Hidden Netowrk", "", "", "                           <- Back"]
            self.WifiSSIDMenu = [WifiSSIDsScreen]
            return
        ProfileCounter = 1
        ProfileScreenCounter = 0
        self.WifiSSIDMenu = []
        for SSID in AvailableNetworks:
            WifiSSIDsScreen[ProfileCounter] = SSID
            ProfileCounter += 1
            if(ProfileCounter == 5):
                #print(WifiSSIDsScreen)
                self.WifiSSIDMenu.append(self.GetMenuScreen(WifiSSIDsScreen[0], WifiSSIDsScreen[1], WifiSSIDsScreen[2], WifiSSIDsScreen[3], WifiSSIDsScreen[4]))
                #print(self.WifiSSIDMenu)
                ProfileScreenCounter += 1
                ProfileCounter = 1
                WifiSSIDsScreen[1] = ""
                WifiSSIDsScreen[2] = ""
                WifiSSIDsScreen[3] = ""
                WifiSSIDsScreen[4] = "                           <- Back"
                ProfileCounter = 1
        #print(ProfileCounter, self.WifiSSIDMenu)
        #if there aren't enough items in the list to roll over the first screen, then we need to add the current screen
        if(ProfileScreenCounter == 0):
            self.WifiSSIDMenu.append(self.GetMenuScreen(WifiSSIDsScreen[0], WifiSSIDsScreen[1], WifiSSIDsScreen[2], WifiSSIDsScreen[3], WifiSSIDsScreen[4]))
        #if there arent' enough items in the list to roll over the next screen, then we need to add the current screen
        if(ProfileCounter < 5):
            self.WifiSSIDMenu.append(self.GetMenuScreen(WifiSSIDsScreen[0], WifiSSIDsScreen[1], WifiSSIDsScreen[2], WifiSSIDsScreen[3], WifiSSIDsScreen[4]))
        #if there are exactly 4 items left in this screen, we need to add a new screen with the back button
        #if(ProfileCounter == 5):
        #    self.WifiSSIDMenu.append(self.GetMenuScreen(WifiSSIDsScreen[0], "                           <- Back", "", "", ""))
        #print(self.WifiSSIDMenu)
    def OnLastScreen(self, _Menu):
        return (self.SelectedScreen == (len(_Menu) - 1))
    def OnFirstScreen(self, _Menu=None):
        return (self.SelectedScreen == 0)
    def OnFirstScreenMenuItem(self, Screen):
        MenuItem = 4 # skip the menu name
        FirstMenuItem = 4
        while(MenuItem > 0):
            if(Screen[MenuItem] != ""):
                FirstMenuItem = MenuItem
            MenuItem -= 1
        return (FirstMenuItem == self.SelectedMenuItem)
    def OnLastScreenMenuItem(self, Screen):
        MenuItem = 1 # skip the menu name
        LastMenuItem = 1
        while(MenuItem < 5):
            if(Screen[MenuItem] != ""):
                LastMenuItem = MenuItem
            MenuItem += 1
        return (LastMenuItem == self.SelectedMenuItem)
    def GetFirstScreenMenuItem(self, Screen):
        MenuItem = 1 # skip the menu name
        FirstMenuItem = 1
        while(MenuItem < 5):
            if(Screen[MenuItem] != ""):
                FirstMenuItem = MenuItem
                break
            MenuItem += 1
        return FirstMenuItem
    def GetLastScreenMenuItem(self, Screen):
        MenuItem = 1 # skip the menu name
        LastMenuItem = 1
        while(MenuItem < 5):
            if(Screen[MenuItem] != ""):
                LastMenuItem = MenuItem
            MenuItem += 1
        return LastMenuItem
    def GetNextRightScreenMenuItem(self, Screen, CurrentSelectedItem):
        _CurrentSelectedItem = CurrentSelectedItem + 1
        while(Screen[_CurrentSelectedItem] == ""):
            _CurrentSelectedItem += 1
        return _CurrentSelectedItem
    def GetNextLeftScreenMenuItem(self, Screen, CurrentSelectedItem):
        _CurrentSelectedItem = CurrentSelectedItem - 1
        while(Screen[_CurrentSelectedItem] == ""):
            _CurrentSelectedItem -= 1
        return _CurrentSelectedItem
#End Menu Helpers
    def ReturnToMenu(self):
        self.EncoderMode = "NavigateMenu"
        self.BrewWizardSelectedButton = ""
        #self.ActiveMenu[0] = self.MainMenuScreen1
        self.SelectedMenuItem = 1
        self.SelectedScreen = 0
        self.UpdateMainMenu()
        self.ActiveMenu = self.MainMenu

        self.DrawMainScreen()
        #self.GD.DrawMenu(self.ActiveMenu[self.SelectedScreen], self.SelectedMenuItem)
    def NavigateKeyboard(self, Direction):
        if(self.KeyboardShift):
            KeyboardRow1 = ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+"]
            KeyboardRow2 = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}", "|"]
            KeyboardRow3 = ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":", "\""]
            KeyboardRow4 = ["Z", "X", "C", "V", "B", "N", "M", "<", ">", "?"]
        else:
            KeyboardRow1 = ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="]
            KeyboardRow2 = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"]
            KeyboardRow3 = ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'"]
            KeyboardRow4 = ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"]
        KeyboardRow5 = ["Space", "Shift", "BackSpace", "Done", "Cancel"]
        Keyboard = [KeyboardRow1, KeyboardRow2, KeyboardRow3, KeyboardRow4, KeyboardRow5]
        if(Direction == "Right"):
            self.KeyboardColumn += 1
        elif(Direction == "Left"):
            self.KeyboardColumn -= 1
        if(self.KeyboardRow > 4):
            self.KeyboardRow = 4
        if(self.KeyboardRow < 0):
            self.KeyboardRow = 0
        if(self.KeyboardColumn > len(Keyboard[self.KeyboardRow])-1):
            self.KeyboardColumn = 0
            self.KeyboardRow += 1
        if(self.KeyboardColumn < 0):
            self.KeyboardRow -= 1
            self.KeyboardColumn = len(Keyboard[self.KeyboardRow])-1
        if(self.KeyboardRow > 4):
            self.KeyboardRow = 4
            self.KeyboardColumn = len(Keyboard[self.KeyboardRow])-1
        if(self.KeyboardRow < 0):
            self.KeyboardRow = 0
            self.KeyboardColumn = 0
        self.CurrentKeyboardKey = Keyboard[self.KeyboardRow][self.KeyboardColumn]
        self.GD.DrawKeyboard(self.KeyboardShift, self.CurrentKeyboardKey, self.KeyboardString, self.KeyboardInputTitle)
    def MenuAction(self, _Menu, CurrentItem):
        if(_Menu == self.MainMenu):
            self.SelectedMenuItem = 1
            self.SelectedScreen = 0
            if(CurrentItem == "Settings"):
                self.ActiveMenu = self.SettingsMenu
            if(CurrentItem == "Brew"):
                self.SelectedMenuItem = 1
                self.SelectedScreen = 0
                self.BuildBrewProfileMenu()
                self.ActiveMenu = self.BrewProfileMenu
            if(CurrentItem == "Calibrate"):
                self.StartCalibration()
                return
        if(_Menu == self.BrewProfileMenu):
            if(CurrentItem == "                           <- Back"):
                self.SelectedMenuItem = 1
                self.SelectedScreen = 0
                self.UpdateMainMenu()
                self.ActiveMenu = self.MainMenu
            else:
                if(CurrentItem != "No Profiles Available"):
                    self.StartBrewWizard(self.ActiveMenu[self.SelectedScreen][self.SelectedMenuItem])
                return
        if(_Menu == self.SettingsMenu):
            if(CurrentItem == "Exit Application"):
                self.GD.DrawSpinner("Updating")
                time.sleep(1)
                os.popen("sudo systemctl stop brewbomb.service")
            if(CurrentItem == "Connect SSH"):
                try:
                    self.GD.DrawInfoScreen(config.get_value('AppInfo', 'BrewerSerialNumber'), s.GetElectronicSerialNumber(), self.wifi.GetActiveSSID(), self.wifi.GetActiveIPAddress(), config.get_value("ssh", "ReversePort"))
                    s.ConnectSSH()
                except Exception as e:
                    logger.error("Menu MenuAction Request Exception:" + str(e))
            if(CurrentItem == "                           <- Back"):
                self.SelectedMenuItem = 2
                self.SelectedScreen = 0
                self.UpdateMainMenu()
                self.ActiveMenu = self.MainMenu
            if(CurrentItem == "Calibrate Flow Meter"):
                self.StartCalibration()
                return
            if(CurrentItem == "Connect to Wifi"):
                self.GD.DrawTitledSpinner("Scanning for Wifi")
                self.BuildWifiSSIDMenu()
                self.SelectedMenuItem = 1
                self.SelectedScreen = 0
                self.ActiveMenu = self.WifiSSIDMenu
            if(CurrentItem == "Display System Info"):
                self.EncoderMode = "Info"
                self.GD.DrawInfoScreen(config.get_value('AppInfo', 'BrewerSerialNumber'), s.GetElectronicSerialNumber(), self.wifi.GetActiveSSID(), self.wifi.GetActiveIPAddress(), config.get_value("ssh", "ReversePort"))
                return
        if(_Menu == self.WifiSSIDMenu):
            if(CurrentItem == "                           <- Back"):
                self.SelectedMenuItem = 2
                self.SelectedScreen = 0
                self.ActiveMenu = self.SettingsMenu
            else:
                self.WIFISelectedSSID = self.ActiveMenu[self.SelectedScreen][self.SelectedMenuItem]
                self.KeyboardMode = "Wifi"
                self.StartKeyboardInput("Wifi Password")
                return None
        if(self.ActiveMenu[0] == self.MainMenuScreen1):
            self.DrawMainScreen()
        else:
            self.GD.DrawMenu(self.ActiveMenu[self.SelectedScreen], self.SelectedMenuItem)
    def StartBrewWizard(self, _Profile):
        self.BrewStarted = False
        self.ActiveBrewProfile = profile.Profile()
        self.ActiveBrewProfile.get(_Profile)
        self.EncoderMode = "BrewWizardPage1"
        self.GD.DrawScreenBrewWizardPage1(str(self.ActiveBrewProfile.CoffeeOriginName), str(self.ActiveBrewProfile.CoffeeWeight))
    def StartBrew(self):
        config.set_value("AppStatus", "ApplicationStatus", "Brewing")
        self.BrewWizardSelectedButton = ""
        self.BrewStartDateTime = datetime.now()
        self.Brewing = True
        self.BrewingPaused = False
        self.CancelStarted = False
        self.Brewer.BrewProfile(self.ActiveBrewProfile)
    def StartKeyboardInput(self, InputTitle):
        self.KeyboardInputTitle = InputTitle
        self.KeyboardString = ""
        self.EncoderMode = "Keyboard"
        self.KeyboardRow = 2
        self.KeyboardColumn = 4
        self.KeyboardShift = True
        self.CurrentKeyboardKey = "G"
        self.GD.DrawKeyboard(self.KeyboardShift, self.CurrentKeyboardKey, self.KeyboardString, self.KeyboardInputTitle)
    def ConfigureWifi(self):
        self.GD.DrawSpinner("Connecting...")
        self.wifi.Connect(self.WIFISelectedSSID, self.WifiPassword)
        self.WIFISelectedSSID = ""
        self.WifiPassword = ""
    def StartCalibration(self):
        self.EncoderMode = "FlowCalibrationPrompt"
        self.DoseStarted = False
        self.DoseCompleted = False
        self.BrewWizardSelectedButton = ""
        self.GD.DrawFlowCalibrationPrompt(self.DoseStarted, self.WaterFlowMeter.GetCurrentTicks(), self.BrewWizardSelectedButton, self.DoseCompleted)
    def CancelBrew(self):
        try:
            self.Brewer.CancelBrew()
        except Exception as e:
            logger.error("Menu.CancelBrew: "+e)
        self.Brewing = False
    def PauseBrew(self):
        self.Brewer.PauseBrew()
        self.BrewWizardSelectedButton = "Resume"
        self.BrewingPaused = True
    def ResumeBrew(self):
        self.Brewer.ResumeBrew()
        self.BrewingPaused = False
        self.BrewWizardSelectedButton = "Pause"
