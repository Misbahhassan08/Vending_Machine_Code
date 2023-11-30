from Helpers.Graphics.Constants import *
from Helpers.Graphics.ScreenCommon import *

ScreenTest = CommonBackground + [
    {
        'ID': 'img',
        'Type': 'DrawImage',
        'ImageName': 'SprayNozzle0',
        'visible': True,
        'x': 100,
        'y': 100
    }
    ]
ScreenMenu = CommonBackground + PageTitle + SelectionBox
ScreenMainMenu = CommonBackground + [
    imgWaterMark,
    ButtonSettings,
    ButtonCalibrate,
    ButtonBrewSelect
    ]
ScreenSpinner = CommonBackground + PageTitle + AnimationWirelessSearch + [
    {
        'ID': 'spinner',
        'Type': 'DrawSpinner',
        'visible': False,
        'r': 0,
        'g': 0,
        'b': 0,
        'style': 1,
        'y': 210
    }
    ]
ScreenInfo = BrewWizardCommon + [
    {
        'ID': 'txt1',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'DeviceID:',
        'x': 150,
        'y': 60,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_RIGHTX
    },
    {
        'ID': 'txtDeviceID',
        'Type': 'DrawText',
        'visible': True,
        'Text': '{Device ID}',
        'x': 155,
        'y': 60,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_LEFTX
    },

    {
        'ID': 'txt2',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'EID:',
        'x': 150,
        'y': 80,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_RIGHTX
    },
    {
        'ID': 'txtElectronicSerialID_Text',
        'Type': 'DrawText',
        'visible': True,
        'Text': '{EID}',
        'x': 155,
        'y': 80,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_LEFTX
    },


    {
        'ID': 'txt3',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'SSID:',
        'x': 150,
        'y': 100,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_RIGHTX
    },
    {
        'ID': 'txtSSID',
        'Type': 'DrawText',
        'visible': True,
        'Text': '{SSID}',
        'x': 155,
        'y': 100,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_LEFTX
    },
    {
        'ID': 'txt4',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'IP Address:',
        'x': 150,
        'y': 120,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_RIGHTX
    },
    {
        'ID': 'txtIPAddress',
        'Type': 'DrawText',
        'visible': True,
        'Text': '{0.0.0.0}',
        'x': 155,
        'y': 120,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_LEFTX
    },
    {
        'ID': 'txt5',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'SSH Port:',
        'x': 150,
        'y': 140,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_RIGHTX
    },
    {
        'ID': 'txtSSHPort',
        'Type': 'DrawText',
        'visible': True,
        'Text': '{44xxx}',
        'x': 155,
        'y': 140,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_LEFTX
    }
    ]
ScreenCalibrate = BrewWizardCommon + [
    ButtonCalibrate,
    ButtonStop,
    {
        'ID': 'txtLine1',
        'Type': 'DrawText',
        'visible': False,
        'Text': '1. Place vessel under pre-infusion nozzle',
        'x': 78,
        'y': 73,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_LEFTX
    },
    {
        'ID': 'txtLine2',
        'Type': 'DrawText',
        'visible': False,
        'Text': '2. Press Calibrate to start',
        'x': 78,
        'y': 117,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_LEFTX
    },
    {
        'ID': 'txtDispenseMessage',
        'Type': 'DrawText',
        'visible': False,
        'Text': 'Press STOP when 32oz has been dispensed',
        'x': 240,
        'y': 84,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_CENTERX
    },
    {
        'ID': 'txtMessage',
        'Type': 'DrawText',
        'visible': False,
        'Text': 'Ticks',
        'x': 240,
        'y': 144,
        'r': 118,
        'g': 20,
        'b': 18,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_CENTERX
    },
    {
        'ID': 'txtTicks',
        'Type': 'DrawText',
        'visible': False,
        'Text': '0',
        'x': 240,
        'y': 160,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_CENTERX
    }
    ]# + WaterWarning # Added by the screen generator

ScreenBrewWizardPage1 = BrewWizardCommon + [
    {
        'ID': 'None',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'COFFEE ORIGIN',
        'x': 240,
        'y': 70,
        'r': 118,
        'g': 20,
        'b': 18,
        'FontName': 'Montserrat-Bold_14_ASTC',
        'options': OPT_CENTERX
    },
    {
        'ID': 'None',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'COFFEE WEIGHT',
        'x': 240,
        'y': 130,
        'r': 118,
        'g': 20,
        'b': 18,
        'FontName': 'Montserrat-Bold_14_ASTC',
        'options': OPT_CENTERX
    },
    {
        'ID': 'txtCoffeeType',
        'Type': 'DrawText',
        'visible': True,
        'Text': '{Coffee Type}',
        'x': 240,
        'y': 87,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_CENTERX
    },
    {
        'ID': 'txtCoffeeWeight',
        'Type': 'DrawText',
        'visible': True,
        'Text': '{Coffee Weight}',
        'x': 240,
        'y': 146,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_CENTERX
    }
    ]
ScreenBrewWizardPage2 = BrewWizardCommon + [
    {
        'ID': 'None',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'GRINDER NAME',
        'x': 240,
        'y': 70,
        'r': 118,
        'g': 20,
        'b': 18,
        'FontName': 'Montserrat-Bold_14_ASTC',
        'options': OPT_CENTERX
    },
    {
        'ID': 'None',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'GRINDER SETTING',
        'x': 240,
        'y': 130,
        'r': 118,
        'g': 20,
        'b': 18,
        'FontName': 'Montserrat-Bold_14_ASTC',
        'options': OPT_CENTERX
    },
    {
        'ID': 'txtGrinderType',
        'Type': 'DrawText',
        'visible': True,
        'Text': '{Grinder Type}',
        'x': 240,
        'y': 87,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_CENTERX
    },
    {
        'ID': 'txtGrinderSetting',
        'Type': 'DrawText',
        'visible': True,
        'Text': '{Grinder Setting}',
        'x': 240,
        'y': 146,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_CENTERX
    }
    ]
ScreenBrewWizardPage3 = BrewWizardCommon + [
    {
        'ID': 'None',
        'Type': 'DrawText',
        'visible': True,
        'Text': '1. Place ground coffee in pre-infuse vessel',
        'x': 78,
        'y': 73,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_LEFTX
    },
    {
        'ID': 'None',
        'Type': 'DrawText',
        'visible': True,
        'Text': '2. Position vessel under dosing nozzle',
        'x': 78,
        'y': 117,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_LEFTX
    }
    ] + WaterWarning
ScreenBrewWizardPage4 = BrewWizardCommon + [
    {
        'ID': 'txtLine1',
        'Type': 'DrawText',
        'visible': True,
        'Text': '1.  Mix coffee and water thoroughly',
        'x': 78,
        'y': 103,
        'FontName': 'Montserrat-Regular_14_ASTC',
        'options': OPT_LEFTX
    },
    {
        'ID': 'txtLine2',
        'Type': 'DrawText',
        'visible': True,
        'Text': '2. Place ground coffee in brewing cylinder',
        'x': 78,
        'y': 121,
        'FontName': 'Montserrat-Regular_14_ASTC',
        'options': OPT_LEFTX
    },
    {
        'ID': 'txtLine3',
        'Type': 'DrawText',
        'visible': True,
        'Text': '3. Shape top of ground bed into a bowl',
        'x': 78,
        'y': 139,
        'FontName': 'Montserrat-Regular_14_ASTC',
        'options': OPT_LEFTX
    },
    {
        'ID': 'txtDispensetxt',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'Dispensing',
        'x': 78,
        'y': 70,
        'r': 118,
        'g': 20,
        'b': 18,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_LEFTX
    },
    {
        'ID': 'txtTargettxt',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'Target',
        'x': 263,
        'y': 56,
        'r': 118,
        'g': 20,
        'b': 18,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_CENTER
    },
    {
        'ID': 'txtDispenseTarget',
        'Type': 'DrawText',
        'visible': True,
        'Text': '0.0oz',
        'x': 263,
        'y': 78,
        'r': 118,
        'g': 20,
        'b': 18,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_CENTER
    },
    {
        'ID': 'txtCurrenttxt',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'Current',
        'x': 364,
        'y': 56,
        'r': 118,
        'g': 20,
        'b': 18,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_CENTER
    },
    {
        'ID': 'txtDispenseActual',
        'Type': 'DrawText',
        'visible': True,
        'Text': '0.0oz',
        'x': 364,
        'y': 78,
        'r': 118,
        'g': 20,
        'b': 18,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_CENTER
    },
    {
        'ID': 'pbPercentComplete',
        'Type': 'DrawProgressBar',
        'visible': True,
        'Progress': 50,
        'x': 104,
        'y': 168,
        'h': 26,
        'w': 272
    }
    ]
ScreenBrewWizardPage5 = BrewWizardCommon + [
    {
        'ID': 'None',
        'Type': 'DrawText',
        'visible': True,
        'Text': '1. Place lid on brewing cylinder',
        'x': 78,
        'y': 80,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_LEFTX
    },
    {
        'ID': 'None',
        'Type': 'DrawText',
        'visible': True,
        'Text': '2. Place brewing cylinder into position',
        'x': 78,
        'y': 106,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_LEFTX
    },
    {
        'ID': 'None',
        'Type': 'DrawText',
        'visible': True,
        'Text': '3. Lower nozzle into brewing cylinder',
        'x': 78,
        'y': 132,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_LEFTX
    }
    ] + WaterWarning
ScreenBrewWizardPage6 = BrewWizardCommon + [
    {
        'ID': 'NONE',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'Target',
        'x': 263,
        'y': 56,
        'r': 118,
        'g': 20,
        'b': 18,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_CENTER
    },
    {
        'ID': 'txtMatchFlowRate',
        'Type': 'DrawText',
        'visible': True,
        'Text': '0.00',
        'x': 263,
        'y': 78,
        'r': 118,
        'g': 20,
        'b': 18,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_CENTER
    },
    {
        'ID': 'NONE',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'Current',
        'x': 364,
        'y': 56,
        'r': 118,
        'g': 20,
        'b': 18,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_CENTER
    },
    {
        'ID': 'txtFlowRate',
        'Type': 'DrawText',
        'visible': True,
        'Text': '0.00',
        'x': 364,
        'y': 78,
        'r': 118,
        'g': 20,
        'b': 18,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_CENTER
    },
    {
        'ID': 'NONE',
        'Type': 'DrawText',
        'visible': True,
        'Text': '1. Match Flow Rate',
        'x': 78,
        'y': 73,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_LEFTX
    },
    {
        'ID': 'None',
        'Type': 'DrawText',
        'visible': True,
        'Text': '2. Adjust nozzle height',
        'x': 78,
        'y': 117,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_LEFTX
    },
    AnimationFlowNozzle
    ]
ScreenBrewing = BrewWizardCommon + [
    {
        'ID': 'txtTargettxt',
        'Type': 'DrawText',
        'visible': False,
        'Text': 'Target',
        'x': 263,
        'y': 56,
        'r': 118,
        'g': 20,
        'b': 18,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_CENTER
    },
    {
        'ID': 'txtCurrenttxt',
        'Type': 'DrawText',
        'visible': False,
        'Text': 'Current',
        'x': 364,
        'y': 56,
        'r': 118,
        'g': 20,
        'b': 18,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_CENTER
    },
    {
        'ID': 'txtLine1',
        'Type': 'DrawText',
        'visible': False,
        'Text': 'Flow Rate:',
        'x': 198,
        'y': 78,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_RIGHTX|OPT_CENTERY
    },
    {
        'ID': 'txtFlowRateTarget',
        'Type': 'DrawText',
        'visible': False,
        'Text': '0.00',
        'x': 263,
        'y': 78,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_CENTER
    },
    {
        'ID': 'txtFlowRateActual',
        'Type': 'DrawText',
        'visible': False,
        'Text': '0.00',
        'x': 364,
        'y': 78,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_CENTER
    },
    {
        'ID': 'txtLine2',
        'Type': 'DrawText',
        'visible': False,
        'Text': 'Yield:',
        'x': 198,
        'y': 101,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_RIGHTX|OPT_CENTERY
    },
    {
        'ID': 'txtYieldTarget',
        'Type': 'DrawText',
        'visible': False,
        'Text': '0.0oz',
        'x': 263,
        'y': 101,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_CENTER
    },
    {
        'ID': 'txtYieldActual',
        'Type': 'DrawText',
        'visible': False,
        'Text': '0.0oz',
        'x': 364,
        'y': 101,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_CENTER
    },
    {
        'ID': 'txtLine3',
        'Type': 'DrawText',
        'visible': False,
        'Text': 'Total Time:',
        'x': 198,
        'y': 124,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_RIGHTX|OPT_CENTERY
    },
    {
        'ID': 'txtTimeTarget',
        'Type': 'DrawText',
        'visible': False,
        'Text': '00:00:00',
        'x': 263,
        'y': 124,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_CENTER
    },
    {
        'ID': 'txtTimeRemaining',
        'Type': 'DrawText',
        'visible': False,
        'Text': '00:00:00',
        'x': 364,
        'y': 124,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_CENTER
    },
    {
        'ID': 'txtLine4',
        'Type': 'DrawText',
        'visible': False,
        'Text': 'Interval Time:',
        'x': 198,
        'y': 147,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_RIGHTX|OPT_CENTERY
    },
    {
        'ID': 'txtBrewIntervalTime',
        'Type': 'DrawText',
        'visible': False,
        'Text': '00:00:00',
        'x': 263,
        'y': 147,
        'r': 48,
        'g': 97,
        'b': 119,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_CENTER
    },
    {
        'ID': 'txtRestIntervalTime',
        'Type': 'DrawText',
        'visible': False,
        'Text': '00:00:00',
        'x': 364,
        'y': 147,
        'r': 118,
        'g': 18,
        'b': 20,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_CENTER
    },
    {
        'ID': 'pbPercentComplete',
        'Type': 'DrawProgressBar',
        'visible': False,
        'Progress': 50,
        'x': 104,
        'y': 168,
        'h': 26,
        'w': 272
    },
    {
        'ID': 'txtComplete',
        'Type': 'DrawText',
        'visible': False,
        'Text': 'Confirm Brew Details',
        'x': 240,
        'y': 55,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_CENTERX
    },
    {
        'ID': 'txtBrewYield',
        'Type': 'DrawText',
        'visible': False,
        'Text': 'Yield',
        'x': 240,
        'y': 94,
        'r': 118,
        'g': 18,
        'b': 20,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_CENTERX
    },
    {
        'ID': 'txtYieldComplete',
        'Type': 'DrawText',
        'visible': False,
        'Text': '0.0oz',
        'x': 240,
        'y': 110,
        'FontName': 'Montserrat-Regular_14_ASTC',
        'options': OPT_CENTERX
    }
    ]
