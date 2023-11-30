import sys
import time
import threading
import Helpers.Graphics.Screen as GraphicsDriver
import Helpers.encoder as encoder

KeyboardShift = True
# GPIO Ports
Enc_A = 24  # Encoder input A: input GPIO 20 (active high)
Enc_B = 23  # Encoder input B: input GPIO 21 (active high)
Enc_C = 18

KeyboardRow = 0
KeyboardColumn = 0

RotaryEncoder = encoder.Encoder(Enc_A, Enc_B, Enc_C)

GD = GraphicsDriver.GraphicsDriver(5,0,0)

GD.DrawSpinner()

GD.BacklightOn()

time.sleep(.5)

EncoderMode = "NavigateMenu" #NavigateMenu for menu operation, Keyboard for Keyboard
CurrentKeyboardKey = "a"

KeyboardString = " "

#Example for drawing a menu
MainMenuScreen1 = ["~Main Menu~", "Brew", "Settings", "", ""]
MainMenu = [MainMenuScreen1]

BrewProfilesScreen1 = ["~Brew Profiles~", "Profile 1", "Profile 2", "Profile 3", "Profile 4"]
BrewProfilesScreen2 = ["~Brew Profiles~", "Profile 5", "Profile 6", "Profile 7", "Profile 8"]
BrewProfilesScreen3 = ["~Brew Profiles~", "Profile 9", "", "", "Back"]
BrewProfileMenu = [BrewProfilesScreen1, BrewProfilesScreen2, BrewProfilesScreen3]

SettingsScreen1 = ["~Settings~", "Calibrate", "Wifi", "", "Back"]
SettingsMenu = [SettingsScreen1]

ActiveMenu = MainMenu
SelectedScreen = 0
SelectedMenuItem = 1

GD.DrawMenu(ActiveMenu[SelectedScreen], SelectedMenuItem, False, 0)

def SimulateBrew(Profile):
    ProgressScreen = [Profile, "            Progress", "", "Brewing", ""]
    Counter = 0
    while(Counter < 101):
        if(Counter==12):
            ProgressScreen[3] = "Brewing."
        if(Counter==24):
            ProgressScreen[3] = "Brewing.."
        if(Counter==36):
            ProgressScreen[3] = "Brewing..."
        if(Counter==48):
            ProgressScreen[3] = "Brewing"
        if(Counter==60):
            ProgressScreen[3] = "Brewing."
        if(Counter==72):
            ProgressScreen[3] = "Brewing.."
        if(Counter==84):
            ProgressScreen[3] = "Brewing..."
        if(Counter==96):
            ProgressScreen[3] = "Brewing"
        GD.DrawMenu(ProgressScreen, 0, True, Counter)
        time.sleep(.01)    
        Counter += 1
    Counter = 0
    ProgressScreen[3] = "Infusing"
    while(Counter < 11):
        if(Counter==2):
            ProgressScreen[3] = "Infusing."
        if(Counter==4):
            ProgressScreen[3] = "Infusing.."
        if(Counter==6):
            ProgressScreen[3] = "Infusing..."
        if(Counter==8):
            ProgressScreen[3] = "Infusing"
        if(Counter==10):
            ProgressScreen[3] = "Infusing."
        GD.DrawMenu(ProgressScreen, 0, True, Counter*10)
        time.sleep(.5)    
        Counter += 1
    
    time.sleep(.5)
    ProgressScreen[3] = "Brewing Completed!"
    GD.DrawMenu(ProgressScreen, 0, True, 100)
    time.sleep(5)
    
def DoKeyboard():
    global EncoderMode, CurrentKeyboardKey, KeyboardRow, KeyboardColumn, KeyboardShift, KeyboardString
    KeyboardString = " "
    EncoderMode = "Keyboard"
    KeyboardRow = 0
    KeyboardColumn = 0
    KeyboardShift = True
    CurrentKeyboardKey = "~"
    GD.DrawKeyboard(KeyboardShift,CurrentKeyboardKey, KeyboardString)

def MenuAction(Menu, CurrentItem):
    global ActiveMenu
    global SelectedMenuItem
    global SelectedScreen
    
    SkipDraw = False
    if(Menu == MainMenu):
        SelectedMenuItem = 1
        SelectedScreen = 0
        if(CurrentItem == "Settings"):
            ActiveMenu = SettingsMenu
        if(CurrentItem == "Brew"):
            ActiveMenu = BrewProfileMenu
    if(Menu == BrewProfileMenu):
        if(CurrentItem == "Back"):
            SelectedMenuItem = 1
            SelectedScreen = 0
            ActiveMenu = MainMenu
        else:
            #print(SelectedScreen)
            #print(SelectedMenuItem)
            #print(ActiveMenu[SelectedScreen][SelectedMenuItem])
            SimulateBrew(ActiveMenu[SelectedScreen][SelectedMenuItem])
    if(Menu == SettingsMenu):
        if(CurrentItem == "Back"):
            SelectedMenuItem = 2
            SelectedScreen = 0
            ActiveMenu = MainMenu
        if(CurrentItem == "Wifi"):
            DoKeyboard()
            SkipDraw = True
            return None
    if(SkipDraw == False):
        GD.DrawMenu(ActiveMenu[SelectedScreen], SelectedMenuItem, False, 0)

def OnLastScreen(Menu):
    return (SelectedScreen == (len(Menu) - 1))

def OnFirstScreen(Menu):
    return (SelectedScreen == 0)

def OnFirstScreenMenuItem(Screen):
    return (SelectedMenuItem == 1)

def OnLastScreenMenuItem(Screen):
    MenuItem = 1 # skip the menu name
    LastMenuItem = 1
    while(MenuItem < 5):
        if(Screen[MenuItem] != ""):
            LastMenuItem = MenuItem
        MenuItem += 1
    return (LastMenuItem == SelectedMenuItem)

def GetFirstScreenMenuItem(Screen):
    MenuItem = 1 # skip the menu name
    FirstMenuItem = 1
    while(MenuItem < 5):
        if(Screen[MenuItem] != ""):
            FirstMenuItem = MenuItem
            break
        MenuItem += 1
    return FirstMenuItem
    
def GetLastScreenMenuItem(Screen):
    MenuItem = 1 # skip the menu name
    LastMenuItem = 1
    while(MenuItem < 5):
        if(Screen[MenuItem] != ""):
            LastMenuItem = MenuItem
        MenuItem += 1
    return LastMenuItem

def GetNextRightScreenMenuItem(Screen,CurrentSelectedItem):
    _CurrentSelectedItem = CurrentSelectedItem + 1
    
    while(Screen[_CurrentSelectedItem] == ""):
        _CurrentSelectedItem += 1
    return _CurrentSelectedItem
    
def GetNextLeftScreenMenuItem(Screen,CurrentSelectedItem):
    _CurrentSelectedItem = CurrentSelectedItem - 1
    
    while(Screen[_CurrentSelectedItem] == ""):
        _CurrentSelectedItem -= 1
    return _CurrentSelectedItem

def ButtonPressed():
    global EncoderMode, KeyboardString, KeyboardShift
    if(EncoderMode == "Keyboard"):
        if(CurrentKeyboardKey == "Space"):
            KeyboardString += " "
        elif(CurrentKeyboardKey == "Shift"):
            KeyboardShift = (KeyboardShift != True)
        elif(CurrentKeyboardKey == "Done"):
            EncoderMode = "NavigateMenu"
            GD.DrawMenu(ActiveMenu[SelectedScreen], SelectedMenuItem, False, 0)
            return
        else:
            KeyboardString += CurrentKeyboardKey
        GD.DrawKeyboard(KeyboardShift,CurrentKeyboardKey, KeyboardString)

    if(EncoderMode == "NavigateMenu"):
        MenuAction(ActiveMenu, ActiveMenu[SelectedScreen][SelectedMenuItem])

def ScrollKeyboard(Direction):
    global CurrentKeyboardKey, KeyboardRow, KeyboardColumn, KeyboardShift, KeyboardString
    if(KeyboardShift):
        KeyboardRow1 = ["~","!","@","#","$","%","^","&","*","(",")","_","+"]
        KeyboardRow2 = ["Q","W","E","R","T","Y","U","I","O","P","{","}","|"]
        KeyboardRow3 = ["A","S","D","F","G","H","J","K","L",":","\""]
        KeyboardRow4 = ["Z","X","C","V","B","N","M","<",">","?"]
    else:
        KeyboardRow1 = ["`","1","2","3","4","5","6","7","8","9","0","-","="]
        KeyboardRow2 = ["q","w","e","r","t","y","u","i","o","p","[","]","\\"]
        KeyboardRow3 = ["a","s","d","f","g","h","j","k","l",";","'"]
        KeyboardRow4 = ["z","x","c","v","b","n","m",",",".","/"]
    KeyboardRow5 = ["Space", "Shift", "Done"]
    
    Keyboard=[KeyboardRow1, KeyboardRow2, KeyboardRow3, KeyboardRow4, KeyboardRow5]

    if(Direction == "Right"):
        KeyboardColumn += 1
    elif(Direction == "Left"):
        KeyboardColumn -= 1

    if(KeyboardRow > 4):
        KeyboardRow = 4
    if(KeyboardRow < 0):
        KeyboardRow = 0
        
    if(KeyboardColumn > len(Keyboard[KeyboardRow])-1):
        KeyboardColumn = 0
        KeyboardRow += 1
    if(KeyboardColumn < 0):
        KeyboardRow -= 1
        KeyboardColumn = len(Keyboard[KeyboardRow])-1        

    if(KeyboardRow > 4):
        KeyboardRow = 4
        KeyboardColumn = len(Keyboard[KeyboardRow])-1
    if(KeyboardRow < 0):
        KeyboardRow = 0
        KeyboardColumn = 0
        
    CurrentKeyboardKey = Keyboard[KeyboardRow][KeyboardColumn]
    
    GD.DrawKeyboard(KeyboardShift,CurrentKeyboardKey, KeyboardString)

def ScrollLeft():
        global SelectedMenuItem
        global SelectedScreen
        global EncoderMode
        global CurrentKeyboardKey
        global KeyboardString
        global GraphicsDriver
        if(EncoderMode == "NavigateMenu"):
# navigating left decrement to the next menu item up:
#   if we are on the first screen
#        move to the next non-blank menu item
#        if we are on the last non-blank menu item, don't increment
#   if we are not on the first screen
#        if we are on the last non-blank item
#             move to the last non-blank item on the next screen
            try:
                if(OnFirstScreen(ActiveMenu)):
                    if(OnFirstScreenMenuItem(ActiveMenu[SelectedScreen]) != True):
                        SelectedMenuItem = GetNextLeftScreenMenuItem(ActiveMenu[SelectedScreen], SelectedMenuItem)
                        if(SelectedMenuItem < 1):
                            SelectedMenuItem = GetFirstScreenMenuItem(ActiveMenu[SelectedScreen])
                else:
                    if(OnFirstScreenMenuItem(ActiveMenu[SelectedScreen])):
                        SelectedScreen -= 1
                        SelectedMenuItem = GetNextLeftScreenMenuItem(ActiveMenu[SelectedScreen],5)
                    else:
                        SelectedMenuItem = GetNextLeftScreenMenuItem(ActiveMenu[SelectedScreen], SelectedMenuItem)
            except Exception as e:
                print(e)
        if(EncoderMode == "Keyboard"):
            ScrollKeyboard("Left")
        if(EncoderMode == "NavigateMenu"):
            GD.DrawMenu(ActiveMenu[SelectedScreen], SelectedMenuItem, False, 0)

def ScrollRight():
        global SelectedMenuItem
        global SelectedScreen
        global EncoderMode
        global CurrentKeyboardKey
        global KeyboardString
        if(EncoderMode == "NavigateMenu"):
# navigating right increment to the next menu item down:
#   if we are on the last screen
#        move to the next non-blank menu item
#        if we are on the last non-blank menu item, don't increment
#   if we are not on the last screen
#        if we are on the last non-blank item
#             move to the first non-blank item on the next screen
            try:
                if(OnLastScreen(ActiveMenu)):
                    if(OnLastScreenMenuItem(ActiveMenu[SelectedScreen]) != True):
                        SelectedMenuItem = GetNextRightScreenMenuItem(ActiveMenu[SelectedScreen], SelectedMenuItem)
                        if(SelectedMenuItem > 4):
                            SelectedMenuItem = GetLastScreenMenuItem(ActiveMenu[SelectedScreen])
                else:
                    if(OnLastScreenMenuItem(ActiveMenu[SelectedScreen])):
                        SelectedScreen += 1
                        SelectedMenuItem = GetNextRightScreenMenuItem(ActiveMenu[SelectedScreen],0)
                    else:
                        SelectedMenuItem = GetNextRightScreenMenuItem(ActiveMenu[SelectedScreen], SelectedMenuItem)
            except Exception as e:
                print(e)
        if(EncoderMode == "Keyboard"):
            ScrollKeyboard("Right")
        if(EncoderMode == "NavigateMenu"):
            GD.DrawMenu(ActiveMenu[SelectedScreen], SelectedMenuItem, False, 0)

def ButtonLongPress():
    global KeyboardShift
    print("Long Press")
    KeyboardShift = (KeyboardShift != True)
    ScrollKeyboard("None")

def ButtonVeryLongPress():
    print("Very Long Press")


EncoderAction = ""
lock = threading.Lock()
lock.acquire()
lock.release()

while(True):
    global Scrolling
    LastEncoderAction = EncoderAction
    EncoderAction = RotaryEncoder.EncoderQ.get()
    try:
        if(EncoderAction == "Left"):
            ScrollLeft()
        if(EncoderAction == "Right"):
            ScrollRight()
        if(EncoderAction == "Up"):
            if(LastEncoderAction == "Down"):
                ButtonPressed()
        # if(EncoderAction == "Down"):
            # ButtonDown()
        if(EncoderAction == "LongPress"):
            ButtonLongPress()
            
        if(EncoderAction == "VeryLongPress"):
            ButtonVeryLongPress()
    except Exception as e:
        print(e)
    finally:
        RotaryEncoder.EncoderQ.task_done()