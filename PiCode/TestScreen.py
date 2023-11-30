#!/usr/bin/env python3
#import os
#import threading
import sys
import time
import importlib
import Helpers.Graphics.Screen as GraphicsDriver
from Helpers.Graphics.Constants import *
from Helpers.Graphics.Macros import *
import Helpers.Graphics.Screens
from Helpers.Graphics.Screens import *


ScreenResetPin = 5
ScreenBus = 0
ScreenDeviceID = 0
GD = GraphicsDriver.GraphicsDriver(ScreenResetPin, ScreenBus, ScreenDeviceID)

while True:
    try:
        importlib.reload(Helpers.Graphics.Screens)
        importlib.reload(Helpers.Graphics.ScreenCommon)
        importlib.reload(Helpers.Graphics.Screen)
        from Helpers.Graphics.ScreenCommon import *
        from Helpers.Graphics.Screens import *
        try:
            ScreenName = eval(sys.argv[1])
        except:
            ScreenName = BlankExample
        GD.DrawScreen(ScreenName)
        time.sleep(0.025)
    except:
        time.sleep(0.1)
