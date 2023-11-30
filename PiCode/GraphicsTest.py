#!/usr/bin/env python3
#import os
#import threading
import time
from datetime import datetime#, timedelta
import Helpers.Graphics.Screen as GraphicsDriver
#import Helpers.encoder as encoder
#import Helpers.GlobalFunctions as s
from Helpers.Graphics.Constants import *
from Helpers.Graphics.Macros import *
from Helpers.Graphics.Screens import *

ScreenResetPin = 5
ScreenBus = 0
ScreenDeviceID = 0

GD = GraphicsDriver.GraphicsDriver(ScreenResetPin, ScreenBus, ScreenDeviceID)
#GD._HAL.RecoverScreen()
#print("Setting flash to fast. Result:", GD._HAL.SetFlashSpeedToFast())

# GD._HAL.WaitForCoProcessor()
# GD._HAL.StartDisplayList(0, 255, 0)
# GD._HAL.DrawAnimationFromFlash("Test")
# # # GD._HAL.DrawImageFromFlash("WaterDrop1", 0, 0, 0)
# GD._HAL.EndDisplayList()
# GD._HAL.WaitForCoProcessor()
# time.sleep(1)
# while True:
#     pass
# Command, Data
# DrawImageFromFlash: ImageName, X, Y, Rotate Angle


WaterFlowing = True
WaterDropAnimationY = 0
WaterFlowingCounter = 0
Percentage = 0
IconWaterFlowing_ImageName = "Brewing" + str(WaterDropAnimationY)
while True:
    starttime = datetime.now()
    IconWaterFlowing_visible = WaterFlowing
    WaterDrop_y = WaterDropAnimationY
    imgProgress_StretchX = Percentage
    IconWaterFlowing_ImageName = "Brewing" + str(WaterDropAnimationY)
    GD.DrawScreen(ScreenMainMenu, IconWaterFlowing_visible=IconWaterFlowing_visible, IconWaterFlowing_ImageName=IconWaterFlowing_ImageName, imgProgress_StretchX=imgProgress_StretchX)
    print(datetime.now()-starttime)
    time.sleep(.025)

    WaterDropAnimationY += 1
    if WaterDropAnimationY > 4:
        WaterDropAnimationY = 0
    # WaterFlowingCounter += 1
    # if WaterFlowingCounter > 25:
    #     WaterFlowingCounter = 0
    #     WaterFlowing = not WaterFlowing
    Percentage += 1
    if Percentage > 100:
        Percentage = 0


# while True:
#     for Font in GD._HAL.FontData:
#         print(Font, GD._HAL.FontData.get(Font))
#         GD._HAL.StartDisplayList()
#         GD._HAL.DrawCustomFontText(Text=Font, x=240, y=136, FontName=Font, options=OPT_CENTERY|OPT_CENTERX)
#         GD._HAL.EndDisplayList()
#         GD._HAL.WaitForCoProcessor()
#         time.sleep(2)
#     for Art in GD._HAL.ArtData:
#         GD._HAL.StartDisplayList()
#         GD._HAL.DrawImageFromFlash(Art, 0, 0, 0)
#         GD._HAL.EndDisplayList()
#         GD._HAL.WaitForCoProcessor()
#         print(Art, GD._HAL.ArtData.get(Art))
#         time.sleep(.5)

# AngleTracker = True
# ButtonSwitch = False
# Angle = -45
# LastTime = datetime.now()
# TimeDiff = 0
# Percentage = 0

# while True:
#     if Percentage > 100:
#         AngleTracker = False
#         time.sleep(0.25)
#     if Percentage < 0:
#         AngleTracker = True
#         time.sleep(0.25)
#         ButtonSwitch = not ButtonSwitch
#     if AngleTracker:
#         Percentage += 1
#     else:
#         Percentage -= 1

#     Angle = ((Percentage/100) * 270) - 46
#     PreInfuseText = (str(('%.3f' % float(TimeDiff))))
#     if AngleTracker:
#         Cancel = 'Cancel-Off'
#     else:
#         Cancel = 'Cancel-On'
#     GD._HAL.DrawScreen(ScreenPreInfuse2, ButtonContinue_visible=(not AngleTracker), ButtonCancel_selected=AngleTracker, txtPreInfuseTarget_Text=PreInfuseText, PreInfuseNeedle_RotateAngle=Angle)

#     TimeDiff = (datetime.now()-LastTime).total_seconds()
#     LastTime = datetime.now()
#     #time.sleep(0.1)
