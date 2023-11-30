from Helpers.Graphics.Constants import *

# Built in fonts: 16-32
# Available Custom Fonts
# Montserrat-Regular_14_ASTC
# Montserrat-Regular_16_ASTC
# Montserrat-Regular_22_ASTC
# Montserrat-Bold_14_ASTC
# Montserrat-Bold_16_ASTC
# Montserrat-Bold_22_ASTC
# Montserrat-BoldItalic_14_ASTC
# Montserrat-BoldItalic_16_ASTC
# Montserrat-BoldItalic_22_ASTC

# Position Variables
LeftButtonX = 77
RightButtonX = 250
ButtonY = 214


ButtonIconXOffset = 8
ButtonIconYOffset = 9

ButtonTextXOffset = 36+36
ButtonTextYOffset = 19
ButtonTextFontName = 'Montserrat-BoldItalic_14_ASTC'
ButtonTextOnR = 255
ButtonTextOnG = 255
ButtonTextOnB = 255
ButtonTextOffR = 118
ButtonTextOffG = 20
ButtonTextOffB = 18

PageTitleTextX = 13
PageTitleTextY = 20
TextBoxFontName = 'Montserrat-Regular_16_ASTC'
TextBoxFontR = 0
TextBoxFontG = 0
TextBoxFontB = 0
TextBoxFontXOffset = 0
TextBoxFontYOffset = 18
TextBoxLeftWidth = 4
TextBoxRightWidth = 4
ProgressBarFillXOffset = 1
ProgressBarFillYOffset = 1
ProgressBarTextXOffset = 0
ProgressBarTextYOffset = 15
# End Position Variables
# Animations
AnimationWaterFlowing = {
        'ID': 'AnimationWaterFlowing',
        'Type': 'DrawAnimation',
        'AnimationName': 'WaterFlowing',
        'visible': False,
        'x': 414,
        'y': 12,
        'FrameCount': 5,
        'FrameSkip': 2,
        'AnimationMode': 'Loop'
    }
AnimationFlowNozzle = {
        'ID': 'AnimationFlowNozzle',
        'Type': 'DrawAnimation',
        'AnimationName': 'SprayNozzle',
        'visible': True,
        'x': 290,
        'y': 90,
        'FrameCount': 4,
        'FrameSkip': 10,
        'AnimationMode': 'PlayReverse'
    }
AnimationWirelessSearch = [
    {
        'ID': 'txt',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'Scanning for Wifi Access Points',
        'x': 240,
        'y': 70,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_CENTERX
    },
    {
        'ID': 'AnimationWirelessSearch',
        'Type': 'DrawAnimation',
        'AnimationName': 'Wireless',
        'visible': True,
        'x': 195,
        'y': 110,
        'FrameCount': 4,
        'FrameSkip': 10,
        'AnimationMode': 'Loop'
    }]
# End Animations
# Icons
IconWifiStrength = {
        'ID': 'WifiStrength',
        'Type': 'WifiStrength',
        'visible': True,
        'x': 442,
        'y': 12
    }
# End Icons
# Common
imgWaterMark = {
        'ID': 'imgWaterMark',
        'Type': 'DrawImage',
        'ImageName': 'BrewBombLogo',
        'visible': True,
        'x': 70,
        'y': 79,
        'Alpha': 255
    }
PageTitle = [
    # {
    #     'ID': 'imgPageTitle',
    #     'Type': 'DrawImage',
    #     'ImageName': 'Title',
    #     'visible': True,
    #     'x': 12,
    #     'y': 12
    # },
    {
        'ID': 'txtPageTitle',
        'Type': 'DrawText',
        'visible': True,
        'Text': '',
        'x': PageTitleTextX,
        'y': PageTitleTextY,
        'r': 255,
        'g': 255,
        'b': 255,
        'FontName': 'Montserrat-Bold_22_ASTC',
        'options': OPT_CENTERY
    }
    ]
SelectionBox = [
    {
        'ID': 'imgSelectionBox',
        'Type': 'DrawImage',
        'ImageName': 'SelectionBox',
        'visible': True,
        'x': 78,
        'y': 59
    },
    {
        'ID': 'imgMenuLineSelected1',
        'Type': 'DrawImage',
        'ImageName': 'Highlight',
        'visible': True,
        'x': 79,
        'y': 69,
        'StretchX': 322
    },
    {
        'ID': 'imgMenuLineSelected2',
        'Type': 'DrawImage',
        'ImageName': 'Highlight',
        'visible': True,
        'x': 79,
        'y': 105,
        'StretchX': 322
    },
    {
        'ID': 'imgMenuLineSelected3',
        'Type': 'DrawImage',
        'ImageName': 'Highlight',
        'visible': True,
        'x': 79,
        'y': 141,
        'StretchX': 322
    },
    {
        'ID': 'imgMenuLineSelected4',
        'Type': 'DrawImage',
        'ImageName': 'Highlight',
        'visible': True,
        'x': 79,
        'y': 177,
        'StretchX': 322
    },
    {
        'ID': 'txtMenuLine1',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'Menu Line 1',
        'x': 104,
        'y': 73,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_LEFTX
    },
    {
        'ID': 'txtMenuLine2',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'Menu Line 2',
        'x': 104,
        'y': 109,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_LEFTX
    },
    {
        'ID': 'txtMenuLine3',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'Menu Line 3',
        'x': 104,
        'y': 145,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_LEFTX
    },
    {
        'ID': 'txtMenuLine4',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'Menu Line 4',
        'x': 104,
        'y': 181,
        'FontName': 'Montserrat-Regular_16_ASTC',
        'options': OPT_LEFTX
    }
    ]
WaterWarning = [
    {
        'ID': 'None',
        'Type': 'DrawImage',
        'ImageName': 'WarningBox',
        'visible': True,
        'x': 77,
        'y': 155
    },
    {
        'ID': 'None',
        'Type': 'DrawImage',
        'ImageName': 'Warning',
        'visible': True,
        'x': 85,
        'y': 163
    },
    {
        'ID': 'None',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'Continuing will dispense water',
        'x': 240,
        'y': 167,
        'r': 118,
        'g': 20,
        'b': 18,
        'FontName': 'Montserrat-Regular_14_ASTC',
        'options': OPT_CENTERX
    }
    ]
# End Common
# Buttons
ButtonBrewSelect = {
        'ID': 'ButtonBrewSelect',
        'Type': 'ImageButton',
        'ImageName': 'Button',
        'visible': True,
        'Icon': 'IconDrop',
        'selected': False,
        'Text': "BREW",
        'x': RightButtonX,
        'y': ButtonY
    }
ButtonBrewStart = {
        'ID': 'ButtonBrewStart',
        'Type': 'ImageButton',
        'ImageName': 'Button',
        'visible': False,
        'selected': False,
        'Text': "BREW",
        'x': RightButtonX,
        'y': ButtonY
    }
ButtonCalibrate = {
        'ID': 'ButtonCalibrate',
        'Type': 'ImageButton',
        'ImageName': 'Button',
        'visible': False,
        'selected': False,
        'Text': "CALIBRATE",
        'x': RightButtonX,
        'y': ButtonY
    }
ButtonCancel = {
        'ID': 'ButtonCancel',
        'Type': 'ImageButton',
        'ImageName': 'Button',
        'visible': True,
        'selected': False,
        'Text': "CANCEL",
        'x': LeftButtonX,
        'y': ButtonY
    }
ButtonContinue = {
        'ID': 'ButtonContinue',
        'Type': 'ImageButton',
        'ImageName': 'Button',
        'visible': False,
        'selected': False,
        'Text': 'CONTINUE',
        'x': RightButtonX,
        'y': ButtonY
    }
ButtonDose = {
        'ID': 'ButtonDose',
        'Type': 'ImageButton',
        'ImageName': 'Button',
        'visible': False,
        'selected': False,
        'Text': 'DOSE',
        'x': RightButtonX,
        'y': ButtonY
    }
ButtonStop = {
        'ID': 'ButtonStop',
        'Type': 'ImageButton',
        'ImageName': 'Button',
        'visible': False,
        'selected': False,
        'Text': 'STOP',
        'x': RightButtonX,
        'y': ButtonY
    }
ButtonPause = {
        'ID': 'ButtonPause',
        'Type': 'ImageButton',
        'ImageName': 'Button',
        'visible': False,
        'selected': False,
        'Text': 'PAUSE',
        'x': RightButtonX,
        'y': ButtonY
    }
ButtonResume = {
        'ID': 'ButtonResume',
        'Type': 'ImageButton',
        'ImageName': 'Button',
        'visible': False,
        'selected': False,
        'Text': 'RESUME',
        'x': RightButtonX,
        'y': ButtonY
    }
ButtonSettings = {
        'ID': 'ButtonSettings',
        'Type': 'ImageButton',
        'ImageName': 'Button',
        'Icon': 'IconGear',
        'visible': True,
        'selected': False,
        'Text': 'SETTINGS',
        'x': LeftButtonX,
        'y': ButtonY
    }

# End Buttons
# Note! Groups must be after any elements they include
# Common Groups
ConfirmCancel = [
    {
        'ID': 'Background',
        'Type': 'DrawImage',
        'ImageName': 'PopUp',
        'visible': True,
        'x': 0,
        'y': 0,
        'Alpha': 255
    },
    {
        'ID': 'None',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'Are you sure you want to Cancel?',
        'x': 240,
        'y': 80,
        'FontName': 'Montserrat-Bold_16_ASTC',
        'options': OPT_CENTERY|OPT_CENTERX
    },
    {
        'ID': 'btnCancelCancel',
        'Type': 'ImageButton',
        'ImageName': 'Button',
        'visible': True,
        'selected': False,
        'Text': 'Do Not Cancel',
        'x': 170,
        'y': 100
    },
    {
        'ID': 'btnCancelConfirm',
        'Type': 'ImageButton',
        'ImageName': 'Button',
        'visible': True,
        'selected': False,
        'Text': 'Yes Cancel',
        'x': 170,
        'y': 136
    }
    ]
CommonBackground = [
    {
        'ID': 'Background',
        'Type': 'DrawImage',
        'ImageName': 'Background',
        'visible': True,
        'x': 0,
        'y': 0,
        'Alpha': 255
    },
    {
        'ID': 'Title',
        'Type': 'DrawImage',
        'ImageName': 'Title',
        'visible': True,
        'x': 0,
        'y': 0,
        'Alpha': 255
    },
    AnimationWaterFlowing,
    IconWifiStrength
    ]
BrewWizardCommon = CommonBackground + PageTitle + [
    ButtonCancel,
    ButtonContinue,
    ButtonBrewStart,
    ButtonDose,
    ButtonPause,
    ButtonResume,
    ButtonBrewStart
    ]
# End Common Groups

###############################
###############################
###############################

# Samples

FontDisplayCaps = {
        'ID': 'txtExampleBold22',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'x': 20,
        'y': 100,
        'FontName': 'Montserrat-Bold_22_ASTC',
        'r': 0,
        'g': 0,
        'b': 0,
        'options': OPT_CENTERY
    }
FontDisplayLower = {
        'ID': 'txtExampleBold22',
        'Type': 'DrawText',
        'visible': True,
        'Text': 'abcdefghijklmnopqrstuvwxyz',
        'x': 20,
        'y': 125,
        'FontName': 'Montserrat-Bold_22_ASTC',
        'r': 0,
        'g': 0,
        'b': 0,
        'options': OPT_CENTERY
    }
FontDisplayNumbers = {
        'ID': 'txtExampleBold22',
        'Type': 'DrawText',
        'visible': True,
        'Text': '~!@#$%^&*()_+`1234567890-=',
        'x': 20,
        'y': 150,
        'FontName': 'Montserrat-Bold_22_ASTC',
        'r': 0,
        'g': 0,
        'b': 0,
        'options': OPT_CENTERY
    }

BlankExample = [
    {
        'ID': 'ButtonExample',
        'Type': 'ImageButton',
        'ImageName': 'ButtonCancel',
        'selected': False,
        'visible': True,
        'x': 16,
        'y': 235
    },
    FontDisplayCaps,
    FontDisplayLower,
    FontDisplayNumbers
    ]
