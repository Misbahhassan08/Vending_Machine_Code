#!/usr/bin/env python3
import os
#import ast
#import threading
#import time
#from datetime import datetime, timedelta
#import Helpers.logger as logger
import Helpers.Graphics.HAL as GraphicsDriver
#import Helpers.encoder as encoder
#import Helpers.GlobalFunctions as s
from Helpers.Graphics.Constants import *
from Helpers.Graphics.Macros import *

ScreenResetPin = 5
ScreenBus = 0
ScreenDeviceID = 0

GD = GraphicsDriver.GraphicsHAL(ScreenResetPin, ScreenBus, ScreenDeviceID)

def LoadFontsIntoFlash():
    FontList = []
    FontArray = []
    for file in os.listdir("/Share/Art"):
        if file.endswith(".glyph"):
            FontList.append([str(file), str(file).split(".")[0]])
    FontList.sort()

    GD._FlashBlockToWrite = 4
    print("Writing Fonts to flash")
    for FileDetail in FontList:
        GD.StartDisplayList(0, 0, 0)
        GD.DrawText(Text=FileDetail[0], x=0, y=136, font=20)
        GD.EndDisplayList()
        GD.WaitForCoProcessor()
        FileName = FileDetail[0]
        FontName = FileDetail[1]
        FontSize = FileDetail[1].split("_")[1]
        print(FontName, FontSize)
        FontAddress = GD.FlashWriteFileToFlashBlock("/Share/Art/" + FileName, -1)
        XFontAddress = 0 # load a dummy xfont address.  This is populated at run time so the xfont data can be placed anywhere in RAM_G
        FontArray.append([FontName, [FontAddress, XFontAddress, FontSize]])
        GD.FontData = FontArray
    with open('/Share/Art/FontList', 'w') as f:
        f.write(str(FontArray))
    print("Fonts in Flash")
def LoadImagesIntoFlash():
    ArtList = []
    ArtArray = []
    for file in os.listdir("/Share/Art"):
        if file.endswith(".raw"):
            ArtList.append([str(file), str(file).split("_")])
    ArtList.sort()

    for FileDetail in ArtList:
        FileName = FileDetail[0]
        ImageName = FileDetail[1][0]
        ImageWidth = FileDetail[1][1].split("x")[0]
        ImageHeight = FileDetail[1][1].split("x")[1]
        CompressionType = FileDetail[1][5]
        print(GD._GetFlashSpeed(), FileName, ImageWidth, ImageHeight, CompressionType)
        ArtArray.append([ImageName, [GD._FlashBlockToWrite, ImageWidth, ImageHeight, CompressionType]])
        with open('/Share/Art/ArtList', 'w') as f:
            f.write(str(ArtArray))
        GD._GetArtData()
        _ = GD.FlashWriteFileToFlashBlock("/Share/Art/" + FileName, -1)
        # GD.StartDisplayList(0, 0, 0)
        # GD.DrawImageFromFlash(ImageName)
        # GD.DrawText(Text=FileDetail[1][0], x=0, y=136, font=20)
        # GD.EndDisplayList()
        # GD.WaitForCoProcessor()
    with open('/Share/Art/ArtList', 'w') as f:
        f.write(str(ArtArray))
    print("Images in Flash")
def EraseFlash():
    print("Erasing Flash")
    GD._FlashErase()
    print("Flash Erased")
def WriteArtVersion():
    print("Writing Art Version to Flash Block 1")
    GD.FlashWriteFileToFlashBlock("/Share/Art/_ArtVersion.txt", 1)
    print("Art Version Write Done")
def WriteDriver():
    print("Writing Blob to first flash block")
    GD.FlashWriteFileToFlashBlock("/Share/Art/BT815.blob", 0)
    print("Blob Write Done")
def _SetFlashSpeedToFast():
    print("Setting flash to fast. Result:", GD._SetFlashSpeedToFast())
def ClearFlashCache():
    print("Clearing Flash Cache")
    GD.ClearFlashCache()
    print("Flash Cache Cleared")
def GetStatus():
    print("Flash Speed:", GD._GetFlashSpeed())
    print("Error Report:", GD._GetCoProcessorErrorReport())
    return GD._GetFlashSpeed()
def GetArtVersion():
    print("Art Version:", GD.ReadStringFromFlashBlock(FlashBlockToRead=1))
def WriteAllFlash():
    EraseFlash()
    GetStatus()
    WriteDriver()
    if GetStatus() not in "Fast":
        RecoverFlash()
    _SetFlashSpeedToFast()
    GetStatus()
    if GetStatus() in "Fast":
        LoadFontsIntoFlash()
    if GetStatus() in "Fast":
        LoadImagesIntoFlash()
    if GetStatus() in "Fast":
        WriteArtVersion()
    if GetStatus() in "Fast":
        GD.ClearFlashCache()
    GetStatus()
def RecoverFlash():
    print("Error Report:", GD._GetCoProcessorErrorReport())
    GD.RecoverCoProcessor()
    print("Error Report:", GD._GetCoProcessorErrorReport())
    _SetFlashSpeedToFast()
    print("Error Report:", GD._GetCoProcessorErrorReport())
    print(GD._GetFlashSpeed())
    print("Error Report:", GD._GetCoProcessorErrorReport())

GetArtVersion()
WriteAllFlash()
#if GetStatus() in "Fast":
#    LoadFontsIntoFlash()
# GD.ScreenPowerOff()
# while True:
#     pass
# GD.RecoverScreen()
# GD.ScreenInit()
# WriteDriver()
# _SetFlashSpeedToFast()
#
#
ClearFlashCache()

# #GD.FlashWriteFileToFlashBlock("/Share/Art/Water-Drop-GIF_0.anim", 2)
# GD.WaitForCoProcessor()
# GD.StartDisplayList(0, 255, 0)
# GD.DrawAnimationFromFlash("Test")
# # # GD._HAL.DrawImageFromFlash("WaterDrop1", 0, 0, 0)
# GD.EndDisplayList()
# GD.WaitForCoProcessor()
# print("Flash Updated")
# print("Error Report:", GD._GetCoProcessorErrorReport())


# while True:
#     for Art in GD.ArtData:
#         GD.StartDisplayList()
#         GD.DrawImageFromFlash(Art, 0, 0, 0)
#         GD.EndDisplayList()
#         GD.WaitForCoProcessor()
#         print(Art, GD.ArtData.get(Art))
#         time.sleep(2)