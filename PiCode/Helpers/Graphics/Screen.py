import threading
#import sys
import time
import queue
from datetime import timedelta

#import threading
import Helpers.logger as logger
import Helpers.Graphics.HAL as HAL
import Helpers.GlobalFunctions as s
import Helpers.configuration as config
from Helpers.Graphics.Constants import *
from Helpers.Graphics.Macros import *
from Helpers.Graphics.Screens import *
from Helpers.Graphics.ScreenCommon import *

# For drawing bitmaps from flash see: https://brtchip.com/wp-content/uploads/Support/Documentation/Programming_Guides/ICs/EVE/BRT_AN_033_BT81X_Series_Programming_Guide.pdf
# 4.12 BITMAP_SOURCE
# 5.22 CMD_LOADIMAGE
# 5.72 CMD_SETBITMAP
# 6 ASTC (Format required for flash images)

class GraphicsDriver(threading.Thread):
#Bus ID (Found in /dev/spi... Default is 0
#Device ID (Found in /dev/spi... Default is 0
#hooked to the !RST pin on the screen default is 5
    def __init__(self, _ScreenResetPin=5, _bus=0, _device=0):
        try:
            threading.Thread.__init__(self)
            self.DisplayQ = queue.Queue() #Create an event queue for the driver
            self.daemon = True
            self.Debug = False
            self.WaterIsFlowing = False
            self.WifiStrength = -255
            self._AnimationTracker = {}
            self._Active_kwargs = {}
            self._Active_Screen = None

            self._HAL = HAL.GraphicsHAL(_ScreenResetPin, _bus, _device)
            self._HAL.WaitForCoProcessor()
            self.DrawSpinner()
            self._CheckFlashArt()
            # self._HAL.WaitForCoProcessor()
            # self._HAL.TurnBacklightOn()
            self._HAL.WaitForCoProcessor()
            self._CacheObjects()

            self.start()
        except Exception as e:
            print(e)
            logger.error(e)
    def __del__(self):
        del self._HAL
    def DrawScreen(self, Screen, **kwargs):
        try:
            kwargs["AnimationWaterFlowing_visible"] = self.WaterIsFlowing
            self._HAL.WaitForCoProcessor()
            self._HAL.StartDisplayList()
            for ScreenElement in Screen:
                #print(ScreenElement)
                if ScreenElement['Type'] == 'WifiStrength':
                    x = ScreenElement['x']
                    y = ScreenElement['y']
                    visible = ScreenElement['visible']
                    try:
                        WifiStrength = ScreenElement['WifiStrength']
                    except:
                        WifiStrength = s.WifiSignalStrength()
                    for key, value in kwargs.items():
                        if ScreenElement['ID'] in key:
                            if key.split("_")[1] == 'x':
                                x = value
                            if key.split("_")[1] == 'y':
                                y = value
                            if key.split("_")[1] == 'visible':
                                visible = value
                            if key.split("_")[1] == 'WifiStrength':
                                WifiStrength = value
                    if not visible in (False, 'False'):
                        self._DrawWifi(x, y, WifiStrength)
                if ScreenElement['Type'] == 'DrawProgressBar':
                    visible = ScreenElement['visible']
                    Progress = ScreenElement['Progress']
                    x = ScreenElement['x']
                    y = ScreenElement['y']
                    h = ScreenElement['h']
                    w = ScreenElement['w']
                    for key, value in kwargs.items():
                        if ScreenElement['ID'] in key:
                            if key.split("_")[1] == 'Progress':
                                Progress = value
                            if key.split("_")[1] == 'x':
                                x = value
                            if key.split("_")[1] == 'y':
                                y = value
                            if key.split("_")[1] == 'h':
                                h = value
                            if key.split("_")[1] == 'w':
                                w = value
                            if key.split("_")[1] == 'visible':
                                visible = value
                    if not visible in (False, 'False'):
                        self._DrawProgressBar(Progress=Progress, x=x, y=y, h=h, w=w)
                if ScreenElement['Type'] == 'DrawSpinner':
                    visible = ScreenElement['visible']
                    try:
                        x = ScreenElement['x']
                    except:
                        x = 240
                    try:
                        y = ScreenElement['y']
                    except:
                        y = 136
                    try:
                        r = ScreenElement['r']
                    except:
                        r = 255
                    try:
                        g = ScreenElement['g']
                    except:
                        g = 255
                    try:
                        b = ScreenElement['b']
                    except:
                        b = 255
                    try:
                        style = ScreenElement['style']
                    except:
                        style = 0
                    for key, value in kwargs.items():
                        if ScreenElement['ID'] in key:
                            if key.split("_")[1] == 'Progress':
                                Progress = value
                            if key.split("_")[1] == 'x':
                                x = value
                            if key.split("_")[1] == 'y':
                                y = value
                            if key.split("_")[1] == 'r':
                                r = value
                            if key.split("_")[1] == 'g':
                                g = value
                            if key.split("_")[1] == 'b':
                                b = value
                    if not visible in (False, 'False'):
                        self._DrawSpinner(x=x, y=y, r=r, g=g, b=b, style=style)
                if ScreenElement['Type'] == 'DrawImage':
                    ImageName = ScreenElement['ImageName']
                    x = ScreenElement['x']
                    y = ScreenElement['y']
                    visible = ScreenElement['visible']
                    try:
                        RotateAngle = ScreenElement['RotateAngle']
                    except:
                        RotateAngle = 0
                    try:
                        Alpha = ScreenElement['Alpha']
                    except:
                        Alpha = 255
                    try:
                        StretchX = ScreenElement['StretchX']
                    except:
                        StretchX = 0
                    try:
                        StretchY = ScreenElement['StretchY']
                    except:
                        StretchY = 0
                    try:
                        r = ScreenElement['r']
                    except:
                        r = 0
                    try:
                        g = ScreenElement['g']
                    except:
                        g = 0
                    try:
                        b = ScreenElement['b']
                    except:
                        b = 0
                    for key, value in kwargs.items():
                        if ScreenElement['ID'] in key:
                            if key.split("_")[1] == 'ImageName':
                                ImageName = value
                            if key.split("_")[1] == 'x':
                                x = value
                            if key.split("_")[1] == 'y':
                                y = value
                            if key.split("_")[1] == 'RotateAngle':
                                RotateAngle = value
                            if key.split("_")[1] == 'Alpha':
                                Alpha = value
                            if key.split("_")[1] == 'r':
                                r = value
                            if key.split("_")[1] == 'g':
                                g = value
                            if key.split("_")[1] == 'b':
                                b = value
                            if key.split("_")[1] == 'visible':
                                visible = value
                            if key.split("_")[1] == 'StretchX':
                                StretchX = value
                            if key.split("_")[1] == 'StretchY':
                                StretchY = value
                    if not visible in (False, 'False'):
                        #print(ImageName, Alpha)
                        self._HAL.DrawImageFromFlash(ImageName, x, y, RotateAngle, Alpha, StretchX, StretchY, r, g, b)
                if ScreenElement['Type'] == 'DrawAnimation':
                    AnimationName = ScreenElement['AnimationName']
                    x = ScreenElement['x']
                    y = ScreenElement['y']
                    FrameCount = int(ScreenElement['FrameCount'])
                    visible = ScreenElement['visible']
                    try:
                        AnimationMode = ScreenElement['AnimationMode']
                    except:
                        AnimationMode = 'Loop'
                    try:
                        FrameSkip = ScreenElement['FrameSkip']
                    except:
                        FrameSkip = 0
                    if not AnimationName in self._AnimationTracker.keys():
                        self._AnimationTracker.update({AnimationName: [AnimationMode, 0, 0]})

                    try:
                        RotateAngle = ScreenElement['RotateAngle']
                    except:
                        RotateAngle = 0
                    try:
                        Alpha = ScreenElement['Alpha']
                    except:
                        Alpha = 255
                    try:
                        StretchX = ScreenElement['StretchX']
                    except:
                        StretchX = 0
                    try:
                        StretchY = ScreenElement['StretchY']
                    except:
                        StretchY = 0
                    for key, value in kwargs.items():
                        if ScreenElement['ID'] in key:
                            if key.split("_")[1] == 'AnimationName':
                                ImageName = value
                            if key.split("_")[1] == 'x':
                                x = value
                            if key.split("_")[1] == 'y':
                                y = value
                            if key.split("_")[1] == 'RotateAngle':
                                RotateAngle = value
                            if key.split("_")[1] == 'Alpha':
                                Alpha = value
                            if key.split("_")[1] == 'visible':
                                visible = value
                            if key.split("_")[1] == 'StretchX':
                                StretchX = value
                            if key.split("_")[1] == 'StretchY':
                                StretchY = value
                    if not visible in (False, 'False'):
                        #print(self._AnimationTracker)
                        CurrentFrame = int(self._AnimationTracker.get(AnimationName)[1])
                        NextFame = CurrentFrame
                        AnimationMode = self._AnimationTracker.get(AnimationName)[0]
                        FrameSkipCounter = self._AnimationTracker.get(AnimationName)[2]
                        if(FrameSkipCounter == 0):
                            if AnimationMode == 'Loop':
                                NextFame += 1
                                if NextFame > FrameCount - 1:
                                    NextFame = 0
                            elif AnimationMode == 'PlayReverse' or AnimationMode == 'ReversePlay':
                                if AnimationMode == 'PlayReverse':
                                    NextFame += 1
                                else:
                                    NextFame -= 1
                                if NextFame < 0:
                                    NextFame = 1
                                    AnimationMode = 'PlayReverse'
                                if NextFame > FrameCount - 1:
                                    NextFame = FrameCount - 2
                                    AnimationMode = 'ReversePlay'
                        FrameSkipCounter += 1
                        if FrameSkipCounter > FrameSkip:
                            FrameSkipCounter = 0
                        self._AnimationTracker[AnimationName] = [AnimationMode, NextFame, FrameSkipCounter]

                        self._HAL.DrawImageFromFlash(AnimationName + str(CurrentFrame), x, y, RotateAngle, Alpha, StretchX, StretchY)
                if ScreenElement['Type'] == 'ImageButton':
                    ImageName = ScreenElement['ImageName']
                    x = ScreenElement['x']
                    y = ScreenElement['y']
                    visible = ScreenElement['visible']
                    selected = ScreenElement['selected']
                    Text = ScreenElement['Text']
                    Icon = ''
                    try:
                        RotateAngle = ScreenElement['RotateAngle']
                    except:
                        RotateAngle = 0
                    try:
                        Alpha = ScreenElement['Alpha']
                    except:
                        Alpha = 255
                    try:
                        r = ScreenElement['r']
                    except:
                        r = 0
                    try:
                        g = ScreenElement['g']
                    except:
                        g = 0
                    try:
                        b = ScreenElement['b']
                    except:
                        b = 0
                    try:
                        Icon = ScreenElement['Icon']
                    except:
                        Icon = ''
                    for key, value in kwargs.items():
                        if ScreenElement['ID'] in key:
                            if key.split("_")[1] == 'selected':
                                selected = value
                            if key.split("_")[1] == 'x':
                                x = value
                            if key.split("_")[1] == 'y':
                                y = value
                            if key.split("_")[1] == 'RotateAngle':
                                RotateAngle = value
                            if key.split("_")[1] == 'r':
                                r = value
                            if key.split("_")[1] == 'g':
                                g = value
                            if key.split("_")[1] == 'b':
                                b = value
                            if key.split("_")[1] == 'Text':
                                Text = value
                            if key.split("_")[1] == 'visible':
                                visible = value
                    if selected or selected == 'True':
                        ImageName += 'On'
                        IconName = Icon + 'On'
                        TextR = ButtonTextOnR
                        TextG = ButtonTextOnG
                        TextB = ButtonTextOnB
                    else:
                        ImageName += 'Off'
                        IconName = Icon + 'Off'
                        TextR = ButtonTextOffR
                        TextG = ButtonTextOffG
                        TextB = ButtonTextOffB
                    if not visible in (False, 'False'):
                        self._HAL.DrawImageFromFlash(ImageName, x, y, RotateAngle, r=r, g=g, b=b)
                        if(Icon != ''):
                            self._HAL.DrawImageFromFlash(IconName, x + ButtonIconXOffset, y + ButtonIconYOffset)
                        if(self.IsInt(ButtonTextFontName)):
                            self._HAL.DrawText(Text=Text, x=x+ButtonTextXOffset, y=y+ButtonTextYOffset, font=ButtonTextFontName, r=TextR, g=TextG, b=TextB, options=OPT_CENTER)
                        else:
                            self._HAL.DrawCustomFontText(Text=Text, x=x+ButtonTextXOffset, y=y+ButtonTextYOffset, FontName=ButtonTextFontName, r=TextR, g=TextG, b=TextB, options=OPT_CENTER)
                if ScreenElement['Type'] == 'DrawText':
                    x = ScreenElement['x']
                    y = ScreenElement['y']
                    FontName = ScreenElement['FontName']
                    visible = ScreenElement['visible']
                    try:
                        Text = ScreenElement['Text']
                    except:
                        Text = ''
                    try:
                        options = ScreenElement['options']
                    except:
                        options = OPT_CENTERX|OPT_CENTERY
                    try:
                        r = ScreenElement['r']
                    except:
                        r = 0
                    try:
                        g = ScreenElement['g']
                    except:
                        g = 0
                    try:
                        b = ScreenElement['b']
                    except:
                        b = 0
                    for key, value in kwargs.items():
                        if ScreenElement['ID'] in key:
                            if key.split("_")[1] == 'Text':
                                Text = value
                            if key.split("_")[1] == 'x':
                                x = value
                            if key.split("_")[1] == 'y':
                                y = value
                            if key.split("_")[1] == 'FontName':
                                FontName = value
                            if key.split("_")[1] == 'r':
                                r = value
                            if key.split("_")[1] == 'g':
                                g = value
                            if key.split("_")[1] == 'b':
                                b = value
                            if key.split("_")[1] == 'options':
                                options = value
                            if key.split("_")[1] == 'visible':
                                visible = value
                    if not visible in (False, 'False'):
                        if(self.IsInt(FontName)):
                            self._HAL.DrawText(Text, x, y, FontName, r, g, b, options)
                        else:
                            self._HAL.DrawCustomFontText(Text, x, y, FontName, r, g, b, options)
                if ScreenElement['Type'] == 'DrawTextBox':
                    Text = ScreenElement['Text']
                    x = ScreenElement['x']
                    y = ScreenElement['y']
                    w = ScreenElement['w']
                    visible = ScreenElement['visible']
                    try:
                        r = ScreenElement['r']
                    except:
                        r = 0
                    try:
                        g = ScreenElement['g']
                    except:
                        g = 0
                    try:
                        b = ScreenElement['b']
                    except:
                        b = 0
                    for key, value in kwargs.items():
                        if ScreenElement['ID'] in key:
                            if key.split("_")[1] == 'Text':
                                Text = value
                            if key.split("_")[1] == 'x':
                                x = value
                            if key.split("_")[1] == 'y':
                                y = value
                            if key.split("_")[1] == 'w':
                                w = value
                            if key.split("_")[1] == 'visible':
                                visible = value
                            if key.split("_")[1] == 'r':
                                r = value
                            if key.split("_")[1] == 'g':
                                g = value
                            if key.split("_")[1] == 'b':
                                b = value
                    if not visible in (False, 'False'):
                        self._DrawTextBox(x, y, w, Text, r, g, b)
            self._HAL.EndDisplayList()
            self._HAL.WaitForCoProcessor()
        except Exception as e:
            print(str(e))
            logger.error("DrawScreen:" + str(e))
    def run(self):
        s.SetThreadName("BrewScreen")
        logger.info("Screen Thread Running")
        while True:
            time.sleep(0.025)
    def DrawScreenMainMenu(self, IsCalibrated, SelectedKey=""):
        kwargs = {
            "ButtonSettings_visible" : True,
            "ButtonSettings_selected" : SelectedKey == "Settings",
            "ButtonBrewSelect_visible" : IsCalibrated,
            "ButtonBrewSelect_selected" : SelectedKey == "Brew",
            "ButtonCalibrate_visible" : not IsCalibrated,
            "ButtonCalibrate_selected" : SelectedKey == "Calibrate",
            "imgWaterMark_Alpha": 255
        }
        self.DrawScreen(ScreenMainMenu, **kwargs)
    def DrawTitledSpinner(self, Title=""):
        kwargs = {
            "txtPageTitle_visible" : True,
            "txtPageTitle_Text" : Title,
            "imgWaterMark_Alpha" : 255
        }
        self.DrawScreen(ScreenSpinner, **kwargs)
#Brew Wizard Screens
    def DrawScreenBrewWizardPage1(self, CoffeeType, CoffeeWeight, SelectedKey=""):
        if s.IsMetric():
            uomString = " kg"
        else:
            uomString = " lbs"
        kwargs = {
            "txtPageTitle_Text" : 'Origin and Weight',
            "txtCoffeeType_Text" : CoffeeType,
            "txtCoffeeWeight_Text" : CoffeeWeight + uomString,
            "ButtonContinue_visible" : True,
            "ButtonContinue_selected" : SelectedKey == "Continue",
            "ButtonCancel_visible" : True,
            "ButtonCancel_selected" : SelectedKey == "Cancel",
        }
        self.DrawScreen(ScreenBrewWizardPage1, **kwargs)
    def DrawScreenBrewWizardPage2(self, GrinderType, GrinderSetting, SelectedKey=""):
        kwargs = {
            "txtPageTitle_Text" : 'Grinding',
            "txtGrinderType_Text" : GrinderType,
            "txtGrinderSetting_Text" : GrinderSetting,
            "ButtonContinue_visible" : True,
            "ButtonContinue_selected" : SelectedKey == "Continue",
            "ButtonCancel_visible" : True,
            "ButtonCancel_selected" : SelectedKey == "Cancel",
        }
        self.DrawScreen(ScreenBrewWizardPage2, **kwargs)
    def DrawScreenBrewWizardPage3(self, SelectedKey=""):
        kwargs = {
            "txtPageTitle_Text" : 'Pre-Infuse: Step 1',
            "ButtonDose_visible" : True,
            "ButtonDose_selected" : SelectedKey == "Dose",
            "ButtonCancel_visible" : True,
            "ButtonCancel_selected" : SelectedKey == "Cancel",
        }
        self.DrawScreen(ScreenBrewWizardPage3, **kwargs)
    def DrawScreenBrewWizardPage4(self, TargetDoseAmount, CurrentDoseAmount=0, DoseComplete=False, SelectedKey=""):
        #Angle = ((float(CurrentDoseAmount)/float(TargetDoseAmount)) * 270) - 46
        if DoseComplete:
            DispenseString = "Dispensed"
            if s.IsMetric():
                TargetDispenseString = str(TargetDoseAmount) + "ml"
                CurrentDispensedString = ('%.1f' % float(CurrentDoseAmount)) + "ml"
            else:
                TargetDispenseString = str(TargetDoseAmount) + "oz"
                CurrentDispensedString = ('%.1f' % float(CurrentDoseAmount)) + "oz"
        else:
            DispenseString = "Dispensing"
            if s.IsMetric():
                TargetDispenseString = str(TargetDoseAmount) + "ml"
                CurrentDispensedString = ('%.1f' % float(CurrentDoseAmount)) + "ml"
            else:
                TargetDispenseString = str(TargetDoseAmount) + "oz"
                CurrentDispensedString = ('%.1f' % float(CurrentDoseAmount)) + "oz"
        PercentDone = int((float(CurrentDoseAmount)/float(TargetDoseAmount))*100)
        kwargs = {
            "txtPageTitle_Text" : 'Pre-Infuse: Step 2',
            "ButtonContinue_visible" : DoseComplete,
            "ButtonContinue_selected" : SelectedKey == "Continue",
            "ButtonCancel_visible" : True,
            "ButtonCancel_selected" : SelectedKey == "Cancel",
            "txtLine1_visible" : DoseComplete,
            "txtLine2_visible" : DoseComplete,
            "txtLine3_visible" : DoseComplete,
            "txtDispensetxt_Text" : DispenseString,
            "txtDispenseTarget_Text" : TargetDispenseString,
            "txtDispenseActual_Text" : CurrentDispensedString,
            "pbPercentComplete_Progress" : PercentDone
        }
        self.DrawScreen(ScreenBrewWizardPage4, **kwargs)
    def DrawScreenBrewWizardPage5(self, SelectedKey=""):
        kwargs = {
            "txtPageTitle_Text" : 'Start Brew',
            "ButtonBrewStart_visible" : True,
            "ButtonBrewStart_selected" : SelectedKey == "Brew",
            "ButtonCancel_visible" : True,
            "ButtonCancel_selected" : SelectedKey == "Cancel",
        }
        self.DrawScreen(ScreenBrewWizardPage5, **kwargs)
    def DrawScreenBrewWizardPage6(self, TargetFlowRate, CurrentFlowRate, SelectedKey=""):
        kwargs = {
            "txtPageTitle_Text" : 'Flow and Nozzle',
            "txtMatchFlowRate_Text" : str('%.2f' % float(TargetFlowRate)),
            "txtFlowRate_Text" : str('%.2f' % float(CurrentFlowRate)),
            "ButtonContinue_visible" : True,
            "ButtonContinue_selected" : SelectedKey == "Continue",
            "ButtonCancel_visible" : False,
            "ButtonCancel_selected" : SelectedKey == "Cancel",
        }
        self.DrawScreen(ScreenBrewWizardPage6, **kwargs)
    def IsInt(self, IntToTest):
        try:
            int(IntToTest)
            return True
        except ValueError:
            return False
    def GetFormattedTimeString(self, Seconds):
        try:
            if(not self.IsInt(Seconds)):
                Seconds = int(0)
            if(int(Seconds) < 0):
                Seconds = 0
            if(int(Seconds) > 86399):
                Seconds = 86399
            return (("00" + str(timedelta(seconds=(int(Seconds)))))[1:])
        except:
            return "00:00:00"
    def DrawBrewing(self, TargetFlowRate, CurrentFlowRate, TargetYield, CurrentYield, TotalTime, RemainingTime, BrewIntervalRemaining, RestIntervalRemaining, BrewingPaused, BrewingComplete, SelectedKey="", CancelStarted=False):
        #print(TargetFlowRate, CurrentFlowRate, TargetYield, CurrentYield, TotalTime, RemainingTime, BrewIntervalRemaining, RestIntervalRemaining, BrewingPaused, BrewingComplete, SelectedKey)
        pbPercentComplete_Progress = int((float(CurrentYield)/float(TargetYield)) * 100)
        if pbPercentComplete_Progress > 100:
            pbPercentComplete_Progress = 100
        if pbPercentComplete_Progress < 0:
            pbPercentComplete_Progress = 0
        try:
            FlowRateString = str(('%.2f' % float(CurrentFlowRate)))
        except:
            FlowRateString = "0.00"
        BrewingPageTitle = 'Brewing'
        if(BrewingComplete):
            BrewingPageTitle = 'Brewing Complete'
        kwargs = {
            "txtPageTitle_Text" : BrewingPageTitle,
            "ButtonPause_visible" : not BrewingComplete and not BrewingPaused,
            "ButtonPause_selected" : SelectedKey == "Pause",
            "ButtonResume_visible" : not BrewingComplete and BrewingPaused,
            "ButtonResume_selected" : SelectedKey == "Resume",
            "ButtonContinue_visible" : BrewingComplete,
            "ButtonContinue_selected" : SelectedKey == "Continue",
            "ButtonCancel_visible" : not BrewingComplete,
            "ButtonCancel_selected" : SelectedKey == "Cancel",

            "txtTargettxt_visible" : not BrewingComplete,
            "txtCurrenttxt_visible" : not BrewingComplete,
            "txtLine1_visible" : not BrewingComplete,
            "txtFlowRateTarget_visible" : not BrewingComplete,
            "txtFlowRateActual_visible" : not BrewingComplete,
            "txtLine2_visible" : not BrewingComplete,
            "txtYieldTarget_visible" : not BrewingComplete,
            "txtYieldActual_visible" : not BrewingComplete,
            "txtLine3_visible" : not BrewingComplete,
            "txtTimeTarget_visible" : not BrewingComplete,
            "txtTimeRemaining_visible" : not BrewingComplete,
            "txtLine4_visible" : not BrewingComplete,
            "txtBrewIntervalTime_visible" : not BrewingComplete,
            "txtRestIntervalTime_visible" : not BrewingComplete,
            "pbPercentComplete_visible" : not BrewingComplete,

            "txtComplete_visible" : BrewingComplete,
            "txtBrewYield_visible" : BrewingComplete,
            "txtYieldComplete_visible" : BrewingComplete,
            "txtYieldComplete_Text" : str('%.2f' % float(CurrentYield)),

            "txtFlowRateTarget_Text" : str('%.2f' % float(TargetFlowRate)),
            "txtFlowRateActual_Text" : FlowRateString,
            "txtYieldTarget_Text" : str('%.2f' % float(TargetYield)),
            "txtYieldActual_Text" : str('%.2f' % float(CurrentYield)),
            "txtTimeTarget_Text" : self.GetFormattedTimeString(int(TotalTime*60)),
            "txtTimeRemaining_Text" : self.GetFormattedTimeString(int(RemainingTime)),
            "txtBrewIntervalTime_Text" : self.GetFormattedTimeString(int(BrewIntervalRemaining or 0)),
            "txtRestIntervalTime_Text" : self.GetFormattedTimeString(int(RestIntervalRemaining or 0)),

            "pbPercentComplete_Progress" : pbPercentComplete_Progress
        }
        if BrewingComplete:
            kwargs["imgWaterMark_Alpha"] = 255
        ScreenToDraw = ScreenBrewing
        if CancelStarted:
            ScreenToDraw = ScreenBrewing + ConfirmCancel
            kwargs["btnCancelCancel_selected"] = SelectedKey == "CancelCancel"
            kwargs["btnCancelConfirm_selected"] = SelectedKey == "CancelConfirm"

            # kwargs["ButtonPause_visible"] = False
            # kwargs["ButtonPause_selected"] = False
            # kwargs["ButtonResume_visible"] = False
            # kwargs["ButtonResume_selected"] = False
            # kwargs["ButtonContinue_visible"] = False
            # kwargs["ButtonContinue_selected"] = False
            # kwargs["ButtonCancel_visible"] = False
            # kwargs["ButtonCancel_selected"] = False

        #print(ScreenToDraw, kwargs)
        self.DrawScreen(ScreenToDraw, **kwargs)#, pbPercentComplete_Progress=pbPercentComplete_Progress, txtRemainingTime_Text=txtRemainingTime_Text, txtFlowRateActual_Text=txtFlowRateActual_Text, txtFlowRateTarget_Text=txtFlowRateTarget_Text, ButtonPause_visible=ButtonPause_visible, ButtonPause_selected=ButtonPause_selected, ButtonResume_visible=ButtonResume_visible, ButtonResume_selected=ButtonResume_selected, ButtonContinue_visible=ButtonContinue_visible, ButtonContinue_selected=ButtonContinue_selected, ButtonCancel_visible=ButtonCancel_visible, ButtonCancel_selected=ButtonCancel_selected, WifiStrength_WifiStrength=WifiStrength_WifiStrength, WaterDrop_visible=WaterDrop_visible, WaterDrop_y=WaterDrop_y)
#End Brew Wizard Screens
#Menu should be an array of strings. Index 0 is menu name, 1 is line 1, 2 is line 2, 3 is line 3, and 4 is line 4
#No more than 4 lines in each menu
#if an item should not be selected, its text needs to be blank
#Blank text will prevent the outline box from being drawn.
    def DrawMenu(self, Menu, SelectedLine, DisplayTitle=True):
        kwargs = {
            "ctrlMenu_MenuItems" : Menu,
            "ctrlMenu_SelectedLine" : SelectedLine,
            "txtPageTitle_visible" : DisplayTitle,
            "txtPageTitle_Text" : Menu[0],
            "imgMenuLineSelected1_visible" : SelectedLine == 1,
            "imgMenuLineSelected2_visible" : SelectedLine == 2,
            "imgMenuLineSelected3_visible" : SelectedLine == 3,
            "imgMenuLineSelected4_visible" : SelectedLine == 4,
            "txtMenuLine1_Text" : Menu[1],
            "txtMenuLine2_Text" : Menu[2],
            "txtMenuLine3_Text" : Menu[3],
            "txtMenuLine4_Text" : Menu[4],
        }
        self.DrawScreen(ScreenMenu, **kwargs)

    def DrawFlowCalibrationPrompt(self, Calibrating, ticks=0, SelectedKey="", CalibrationComplete=False):
        _PageTitle = "Calibration"
        if Calibrating:
            _PageTitle = "Calibrating"
        kwargs = {
            "txtPageTitle_Text" : _PageTitle,
            "txt1_visible" : not Calibrating,
            "txtLine1_visible" : not Calibrating,
            "txt2_visible" : not Calibrating,
            "txtLine2_visible" : not Calibrating,
            "txtDispenseMessage_visible" : Calibrating,
            "txtMessage_visible" : Calibrating,
            "txtTicks_visible" : Calibrating,
            "txtTicks_Text" : str(ticks),
            "ButtonCalibrate_visible" : not Calibrating,
            "ButtonCalibrate_selected" : SelectedKey == "Calibrate",
            "ButtonCancel_visible" : True,
            "ButtonCancel_selected" : SelectedKey == "Cancel",
            "ButtonStop_visible" : Calibrating,
            "ButtonStop_selected" : SelectedKey == "Stop",
        }
        ScreenToDraw = ScreenCalibrate
        if not Calibrating:
            ScreenToDraw = ScreenCalibrate + WaterWarning
        self.DrawScreen(ScreenToDraw, **kwargs)

# Draws an info screen
    def DrawInfoScreen(self, SerialNumber, ElectronicSerialNumber, SSID, IPAddress, SSHPort):
        kwargs = {
            "txtPageTitle_Text" : 'Device Info',
            "txtDeviceID_Text" : str(SerialNumber),
            "txtElectronicSerialID_Text" : str(ElectronicSerialNumber),
            "txtSSID_Text" : str(SSID),
            "txtIPAddress_Text" : str(IPAddress),
            "txtSSHPort_Text" : str(SSHPort),
            "ButtonContinue_visible" : True,
            "ButtonContinue_selected" : True,
            "ButtonCancel_visible" : False
        }
        self.DrawScreen(ScreenInfo, **kwargs)
# Draws an animated spinner
    def DrawSpinner(self, Text="Loading", x=240, y=136):
        style = 0
        scale = 0
        self._HAL.WaitForCoProcessor()
        self._HAL.StartDisplayList(0, 0, 0)
        self._DrawMenuTitle(Text)
        self._HAL.AddCommandToDisplayList(CMD_SPINNER)
        self._HAL.AddCommandToDisplayList(((y & 0xFFFF)<<16) + (x & 0xFFFF))
        self._HAL.AddCommandToDisplayList(((scale & 0xFFFF)<<16) + (style & 0xFFFF))
        self._HAL.EndDisplayList()
        self._HAL.WaitForCoProcessor()
# Draws a keyboard and string input
    def DrawKeyboard(self, Shift, SelectedKey, Text="", Title="Enter Text"):
        self._HAL.StartDisplayList(0, 0, 0)
        self._HAL.AddCommandToDisplayList(CLEAR(1, 1, 1))# // clear screen
        self._DrawMenuTitle(Title)
        self._DrawKeyboardText(Text, 1, 1, 28)
        self._DrawMenuTextOutline(1) #Force the text to be outlined
        if(Shift):
            Line1Keys = "~!@#$%^&*()_+"
            Line2Keys = "QWERTYUIOP{}|"
            Line3Keys = "ASDFGHJKL:\""
            Line4Keys = "ZXCVBNM<>?"
        else:
            Line1Keys = "`1234567890-="
            Line2Keys = "qwertyuiop[]\\"
            Line3Keys = "asdfghjkl;'"
            Line4Keys = "zxcvbnm,./"
        self._DrawKeys(Line1Keys, 30, 103, 420, 20, SelectedKey)
        self._DrawKeys(Line2Keys, 30, 131, 420, 20, SelectedKey)
        self._DrawKeys(Line3Keys, 30, 159, 420, 20, SelectedKey)
        self._DrawKeys(Line4Keys, 30, 187, 420, 20, SelectedKey)
        if(SelectedKey == "Space"):
            self._DrawButton("Space", 30, 215, 80, 20, False)
        else:
            self._DrawButton("Space", 30, 215, 80, 20, True)
        if(SelectedKey == "Shift"):
            self._DrawButton("Shift", 115, 215, 80, 20, False)
        else:
            self._DrawButton("Shift", 115, 215, 80, 20, True)
        if(SelectedKey == "BackSpace"):
            self._DrawButton("BackSpace", 200, 215, 80, 20, False)
        else:
            self._DrawButton("BackSpace", 200, 215, 80, 20, True)
        if(SelectedKey == "Done"):
            self._DrawButton("Done", 285, 215, 80, 20, False)
        else:
            self._DrawButton("Done", 285, 215, 80, 20, True)
        if(SelectedKey == "Cancel"):
            self._DrawButton("Cancel", 370, 215, 80, 20, False)
        else:
            self._DrawButton("Cancel", 370, 215, 80, 20, True)
        self._HAL.EndDisplayList()
### Driver Functions
### !!!Do not call directly!!!
    def _DrawMenuTitle(self, Text):
        #Line one starts at x 25 y 25
        font = 31
        options = OPT_CENTER
        x = 240
        y = 25
        #self._HAL.AddCommandToDisplayList(CMD_RESETFONTS)
        #self._HAL.AddCommandToDisplayList(COLOR_RGB(0x00, 0x00, 0x00))
        self._HAL.AddCommandToDisplayList(COLOR_RGB(0xFF, 0xFF, 0xFF))
        self._HAL.AddCommandToDisplayList(CMD_TEXT)
        self._HAL.AddCommandToDisplayList(((y & 0xFFFF)<<16) + (x & 0xFFFF))
        self._HAL.AddCommandToDisplayList(((options & 0xFFFF)<<16) + (font & 0xFFFF))
        self._HAL.AddStringToDisplayList(Text)

    def _DrawText(self, Text, x, y, font=31, options=OPT_CENTERY):
        self._HAL.AddCommandToDisplayList(COLOR_RGB(0xFF, 0xFF, 0xFF))
        self._HAL.AddCommandToDisplayList(CMD_TEXT)
        self._HAL.AddCommandToDisplayList(((y & 0xFFFF)<<16) + (x & 0xFFFF))
        self._HAL.AddCommandToDisplayList(((options & 0xFFFF)<<16) + (font & 0xFFFF))
        self._HAL.AddStringToDisplayList(Text)
    def _DrawKeyboardText(self, Text, LineNumber, SelectedLine, font=31, options=OPT_CENTERY):
        #Line one starts at x 25 y 25
        x = 25
        y = 25
        CharacterSpacing = 10
        CharacterHeight = 35
        self._HAL.AddCommandToDisplayList(COLOR_RGB(0xFF, 0xFF, 0xFF))
        y = y + (CharacterHeight * LineNumber) + (CharacterSpacing * LineNumber)
        self._HAL.AddCommandToDisplayList(CMD_TEXT)
        self._HAL.AddCommandToDisplayList(((y & 0xFFFF)<<16) + (x & 0xFFFF))
        self._HAL.AddCommandToDisplayList(((options & 0xFFFF)<<16) + (font & 0xFFFF))
        self._HAL.AddStringToDisplayList(Text)
        if((LineNumber == SelectedLine) & (Text != "")):
            self._DrawMenuTextOutline(LineNumber)

    def _DrawMenuTextOld(self, Text, LineNumber, SelectedLine, font=31, options=OPT_CENTERY):
        #Line one starts at x 25 y 25
        x = 25
        y = 23
        CharacterSpacing = 10
        CharacterHeight = 35
        y = y + (CharacterHeight * LineNumber) + (CharacterSpacing * LineNumber)

        self._HAL.AddCommandToDisplayList(CMD_TEXT)
        self._HAL.AddCommandToDisplayList(((y & 0xFFFF)<<16) + (x & 0xFFFF))
        self._HAL.AddCommandToDisplayList(((options & 0xFFFF)<<16) + (font & 0xFFFF))
        self._HAL.AddStringToDisplayList(Text)

        if((LineNumber == SelectedLine) & (Text != "")):
            self._DrawMenuTextOutline(LineNumber)

    def _DrawMenuText(self, Text, LineNumber, SelectedLine, font=31, options=OPT_CENTERY):
        #Line one starts at x 25 y 25
        x = 140
        y = 100
        CharacterSpacing = 10
        CharacterHeight = 10
        y = y + (CharacterHeight * LineNumber) + (CharacterSpacing * LineNumber)
        if(LineNumber == 1):
            self._DrawRectangle(RecX=x-15, RecY=y-15, RecH=88, RecW=230, r=0, g=0, b=0)
        self._HAL.DrawCustomFontText(Text=Text, x=x, y=y, FontName='Montserrat-Regular_16_ASTC', r=0, g=0, b=0, options=OPT_CENTERY)
        # self._HAL.AddCommandToDisplayList(CMD_TEXT)
        # self._HAL.AddCommandToDisplayList(((y & 0xFFFF)<<16) + (x & 0xFFFF))
        # self._HAL.AddCommandToDisplayList(((options & 0xFFFF)<<16) + (font & 0xFFFF))
        # self._HAL.AddStringToDisplayList(Text)
        if((LineNumber == SelectedLine) & (Text != "")):
            self._DrawRectangle(RecX=x-5, RecY=y-10, RecH=17, RecW=200, r=0, g=0, b=0)
            #self._DrawMenuTextOutline(LineNumber)
    def _DrawSpinner(self, x=240, y=136, r=255, g=255, b=255, style=0):
        scale = 0
        self._HAL.AddCommandToDisplayList(SAVE_CONTEXT())
        self._HAL.AddCommandToDisplayList(COLOR_RGB(r, g, b))
        self._HAL.AddCommandToDisplayList(CMD_SPINNER)
        self._HAL.AddCommandToDisplayList(((y & 0xFFFF)<<16) + (x & 0xFFFF))
        self._HAL.AddCommandToDisplayList(((scale & 0xFFFF)<<16) + (style & 0xFFFF))
        self._HAL.AddCommandToDisplayList(RESTORE_CONTEXT())
    def _DrawTextBox(self, x, y, w, Text, r=0, g=0, b=0):
        self._HAL.DrawImageFromFlash(ImageName='TextBoxLeft', x=x, y=y, RotateAngle=0, Alpha=255, StretchX=0, StretchY=0, r=r, g=g, b=b)
        self._HAL.DrawImageFromFlash(ImageName='TextBoxCenter', x=x+TextBoxLeftWidth-1, y=y, RotateAngle=0, Alpha=255, StretchX=w-TextBoxLeftWidth-TextBoxRightWidth, StretchY=0, r=r, g=g, b=b)
        self._HAL.DrawImageFromFlash(ImageName='TextBoxRight', x=x+w-TextBoxRightWidth-1, y=y, RotateAngle=0, Alpha=255, StretchX=0, StretchY=0, r=r, g=g, b=b)
        if(self.IsInt(TextBoxFontName)):
            self._HAL.DrawText(Text=Text, x=x+TextBoxLeftWidth+TextBoxFontXOffset, y=y+TextBoxFontYOffset, font=TextBoxFontName, r=TextBoxFontR, g=TextBoxFontG, b=TextBoxFontB, options=OPT_CENTERY)
        else:
            self._HAL.DrawCustomFontText(Text=Text, x=x+TextBoxLeftWidth+TextBoxFontXOffset, y=y+TextBoxFontYOffset, FontName=TextBoxFontName, r=TextBoxFontR, g=TextBoxFontG, b=TextBoxFontB, options=OPT_CENTERY)
    def _DrawWifi(self, x, y, WifiStrength):
        # -30 dBm is pretty much max
        # -67 dBm Verry Good (Streaming video/voip/...)
        # -70 dBm Ok (email/web/...)
        # -80 dBm Not so good
        # -90 dBm probably unusable
        if WifiStrength > -45:
            self._HAL.DrawImageFromFlash("Connectivity3", x, y)
        elif WifiStrength > -65:
            self._HAL.DrawImageFromFlash("Connectivity2", x, y)
        elif WifiStrength > -80:
            self._HAL.DrawImageFromFlash("Connectivity1", x, y)
        elif WifiStrength >= -150:
            self._HAL.DrawImageFromFlash("Connectivity0", x, y)
        elif WifiStrength < -150:
            self._HAL.DrawImageFromFlash("ConnectivityNone", x, y)
    def _DrawRectangle(self, RecX=20, RecY=25, RecH=45, RecW=430, r=0, g=0, b=0):
        #Start x position of the rectangle
        #Start y posotion of the rectangle
        #Rectangle Height
        #Rectangle Width
        self._HAL.AddCommandToDisplayList(SAVE_CONTEXT())
        self._HAL.AddCommandToDisplayList(COLOR_RGB(r, g, b))
        self._HAL.AddCommandToDisplayList(LINE_WIDTH(15))
        self._HAL.AddCommandToDisplayList(BEGIN(LINES))
        #Top Line
        self._HAL.AddCommandToDisplayList(VERTEX2II(RecX, RecY, 0, 0))
        self._HAL.AddCommandToDisplayList(VERTEX2II(RecX+RecW, RecY, 0, 0))
        #Bottom Line
        self._HAL.AddCommandToDisplayList(VERTEX2II(RecX, RecY+RecH, 0, 0))
        self._HAL.AddCommandToDisplayList(VERTEX2II(RecX+RecW, RecY+RecH, 0, 0))
        #Right Line
        self._HAL.AddCommandToDisplayList(VERTEX2II(RecX+RecW, RecY, 0, 0))
        self._HAL.AddCommandToDisplayList(VERTEX2II(RecX+RecW, RecY+RecH, 0, 0))
        #Left Line
        self._HAL.AddCommandToDisplayList(VERTEX2II(RecX, RecY, 0, 0))
        self._HAL.AddCommandToDisplayList(VERTEX2II(RecX, RecY+RecH, 0, 0))
        self._HAL.AddCommandToDisplayList(END())
        self._HAL.AddCommandToDisplayList(RESTORE_CONTEXT())
    def _DrawMenuTextOutline(self, LineNumber):
        RecX = 20 #Start x position of the rectangle
        RecY = 25 #Start y posotion of the rectangle
        RecH = 45 #Rectangle Height
        RecW = 430 #Rectangle Width
        RecY = (RecH * LineNumber)
        self._HAL.AddCommandToDisplayList(LINE_WIDTH(15))
        self._HAL.AddCommandToDisplayList(BEGIN(LINES))
        #Top Line
        self._HAL.AddCommandToDisplayList(VERTEX2II(RecX, RecY, 0, 0))
        self._HAL.AddCommandToDisplayList(VERTEX2II(RecX+RecW, RecY, 0, 0))
        #Bottom Line
        self._HAL.AddCommandToDisplayList(VERTEX2II(RecX, RecY+RecH, 0, 0))
        self._HAL.AddCommandToDisplayList(VERTEX2II(RecX+RecW, RecY+RecH, 0, 0))
        #Right Line
        self._HAL.AddCommandToDisplayList(VERTEX2II(RecX+RecW, RecY, 0, 0))
        self._HAL.AddCommandToDisplayList(VERTEX2II(RecX+RecW, RecY+RecH, 0, 0))
        #Left Line
        self._HAL.AddCommandToDisplayList(VERTEX2II(RecX, RecY, 0, 0))
        self._HAL.AddCommandToDisplayList(VERTEX2II(RecX, RecY+RecH, 0, 0))
        self._HAL.AddCommandToDisplayList(END())
    def _DrawProgressBar(self, Progress, x, y, h, w):
        # MaxValue = 100
        # options = OPT_3D #OPT_FLAT
        # self._HAL.AddCommandToDisplayList(SAVE_CONTEXT())
        # self._HAL.AddCommandToDisplayList(COLOR_RGB(foreground_r, foreground_g, foreground_b))
        # self._HAL.AddCommandToDisplayList(CMD_BGCOLOR)
        # self._HAL.AddCommandToDisplayList(COLOR_RGB(background_r, background_g, background_b))
        # self._HAL.AddCommandToDisplayList(CMD_PROGRESS)
        # self._HAL.AddCommandToDisplayList(((y & 0xFFFF)<<16) + (x & 0xFFFF))
        # self._HAL.AddCommandToDisplayList(((h & 0xFFFF)<<16) + (w & 0xFFFF))
        # self._HAL.AddCommandToDisplayList(((Progress & 0xFFFF)<<16) + (options & 0xFFFF))
        # self._HAL.AddCommandToDisplayList(((0x00 & 0xFFFF)<<16) + (MaxValue & 0xFFFF))
        # self._HAL.AddCommandToDisplayList(RESTORE_CONTEXT())

        if Progress < 0:
            Progress = 0
        if Progress > 100:
            Progress = 100
        ProgressPercent = int((Progress/100) * (w-(ProgressBarFillXOffset*3)))
        Text = str(Progress) + "%"
        if ProgressPercent <= 0:
            ProgressPercent = 1 # StretchX will draw the image at its original length if o is passed in
        self._HAL.DrawImageFromFlash(ImageName='ProgressFill', x=x+ProgressBarFillXOffset, y=y+ProgressBarFillYOffset, RotateAngle=0, Alpha=255, StretchX=ProgressPercent, StretchY=0)

        self._HAL.DrawImageFromFlash(ImageName='ProgressBoxLeft', x=x, y=y, RotateAngle=0, Alpha=255, StretchX=0, StretchY=0)
        self._HAL.DrawImageFromFlash(ImageName='ProgressBoxCenter', x=x+TextBoxLeftWidth-1, y=y, RotateAngle=0, Alpha=255, StretchX=w-TextBoxLeftWidth-TextBoxRightWidth, StretchY=0)
        self._HAL.DrawImageFromFlash(ImageName='ProgressBoxRight', x=x+w-TextBoxRightWidth-1, y=y, RotateAngle=0, Alpha=255, StretchX=0, StretchY=0)

        if(self.IsInt(TextBoxFontName)):
            self._HAL.DrawText(Text=Text, x=x+w+ProgressBarTextXOffset, y=y+ProgressBarTextYOffset, font=TextBoxFontName, r=TextBoxFontR, g=TextBoxFontG, b=TextBoxFontB, options=OPT_LEFTX|OPT_CENTERY)
        else:
            self._HAL.DrawCustomFontText(Text=Text, x=x+w+ProgressBarTextXOffset, y=y+ProgressBarTextYOffset, FontName=TextBoxFontName, r=TextBoxFontR, g=TextBoxFontG, b=TextBoxFontB, options=OPT_LEFTX|OPT_CENTERY)
    def _DrawKeys(self, Keys, x, y, w, h, PressedKey):
        if(len(PressedKey) > 1):
            options = OPT_CENTERY
        else:
            options = OPT_CENTERY|ord(PressedKey)
        font = 22
        self._HAL.AddCommandToDisplayList(CMD_KEYS)
        self._HAL.AddCommandToDisplayList(((y & 0xFFFF)<<16) + (x & 0xFFFF))
        self._HAL.AddCommandToDisplayList(((h & 0xFFFF)<<16) + (w & 0xFFFF))
        self._HAL.AddCommandToDisplayList(((options & 0xFFFF)<<16) + (font & 0xFFFF))
        self._HAL.AddStringToDisplayList(Keys)
    def _DrawButton(self, Text, x, y, w, h, Pressed, font=18):
        options = OPT_3D
        if(not Pressed):
            options = OPT_FLAT
        self._HAL.AddCommandToDisplayList(SAVE_CONTEXT())
        self._HAL.AddCommandToDisplayList(CMD_FGCOLOR)
        self._HAL.AddCommandToDisplayList(0x00101010)
        self._HAL.AddCommandToDisplayList(CMD_BGCOLOR)
        self._HAL.AddCommandToDisplayList(0x00505050)
        #self._HAL.AddCommandToDisplayList(CMD_GRADCOLOR)
        #self._HAL.AddCommandToDisplayList(0x00202020)
        self._HAL.AddCommandToDisplayList(CMD_BUTTON)
        self._HAL.AddCommandToDisplayList(((y & 0xFFFF)<<16) + (x & 0xFFFF))
        self._HAL.AddCommandToDisplayList(((h & 0xFFFF)<<16) + (w & 0xFFFF))
        self._HAL.AddCommandToDisplayList(((options & 0xFFFF)<<16) + (font & 0xFFFF))
        self._HAL.AddStringToDisplayList(Text)
        self._HAL.AddCommandToDisplayList(RESTORE_CONTEXT())
# Flash Functions
    def _CheckFlashArt(self):
        if not self._HAL.FlashVersionIsLatest():
            print("Outdated Art Flash")
            self._HAL.UpdateFlashArt()
    def _CacheObjects(self):
        pass
        # self._HAL.StartEmptyDisplayList()
        # self._DrawButton("Cancel", 55, 235, 140, 35, False, 25)
        # self._HAL.CacheDisplayList("ButtonCancel")
        # self._HAL.StartEmptyDisplayList()
        # self._DrawButton("Cancel", 55, 235, 140, 35, True, 25)
        # self._HAL.CacheDisplayList("ButtonSelectedCancel")
        # self._HAL.StartEmptyDisplayList()
        # self._DrawButton("Continue", 305, 235, 140, 35, False, 25)
        # self._HAL.CacheDisplayList("ButtonContinue")
        # self._HAL.StartEmptyDisplayList()
        # self._DrawButton("Continue", 305, 235, 140, 35, True, 25)
        # self._HAL.CacheDisplayList("ButtonSelectedContinue")
        #print("CurrentCachePosition:" + str(self._HAL._CurrentCachePosition))

# End Flash Functions

# Test Functions
    def DrawTest(self):
        self._HAL.StartDisplayList(0, 0, 0)
        self._HAL.AddCachedCommandToDisplayList("ButtonSelectedCancel")
        self._HAL.AddCachedCommandToDisplayList("ButtonSelectedContinue")
        self._HAL.EndDisplayList()
        time.sleep(0.5)

        self._HAL.WaitForCoProcessor()
        self._HAL.StartDisplayList(0, 0, 0)
        self._HAL.AddCachedCommandToDisplayList("ButtonCancel")
        self._HAL.AddCachedCommandToDisplayList("ButtonContinue")
        self._HAL.EndDisplayList()
        time.sleep(0.5)
        self._HAL.WaitForCoProcessor()

#End Test Functions
