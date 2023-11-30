#import threading
import sys
import spidev
import RPi.GPIO as GPIO
import time
from GraphicsDriverInclude import *
spi = spidev.SpiDev() #The actual SPI Device

def DisableDebug():
    global Debug
    if(Debug):
        print("Debug Off")
    Debug = False
def EnableDebug():
    global Debug
    Debug = True
    print("Debug On")  

def PrintResponse(Response):
    global Debug
    if(Debug):
        print(Response)

#Display List Macro's
def VERTEX2F(x,y):
    value = ((0x01<<30)|(((x)&0x7FFF)<<15)|(((y)&0x7FFF)<<0))
    PrintResponse("VERTEX2F: " + hex(value) + " " + str(value))
    return value 
def VERTEX2II(x,y,handle,cell):
	value = ((0x02<<30)|(((x)&0x1FF)<<21)|(((y)&0x1FF)<<12)|(((handle)&0x1F)<<7)|(((cell)&0x7F)<<0))
	PrintResponse("VERTEX2II: " + hex(value) + " " + str(value))
	return value 
def BITMAP_SOURCE(addr):
	value = ((0x01<<24)|(((addr)&0xFFFFF)<<0))
	PrintResponse("BITMAP_SOURCE: " + hex(value) + " " + str(value))
	return value 
def CLEAR_COLOR_RGB(red,green,blue):
	value = ((0x02<<24)|(((red)&0xFF)<<16)|(((green)&0xFF)<<8)|(((blue)&0xFF)<<0)) 
	PrintResponse("CLEAR_COLOR_RGB: " + hex(value) + " " + str(value))
	return value
def TAG(s):
	value = ((0x03<<24)|(((s)&0xFF)<<0))
	PrintResponse("VERTEX2II: " + hex(value) + " " + str(value))
	return value
def COLOR_RGB(red,green,blue):
    value = ((0x04<<24)|(((red)&0xFF)<<16)|(((green)&0xFF)<<8)|(((blue)&0xFF)<<0))
    PrintResponse("COLOR_RGB: " + hex(value) + " " + str(value))
    return value
def BITMAP_HANDLE(handle):
    value = ((0x05<<24)|(((handle)&0x1F)<<0))
    PrintResponse("VERTEX2II: " + hex(value) + " " + str(value))
    return value 
def CELL(cell): 
    value = ((0x06<<24)|(((cell)&0x7F)<<0))
    PrintResponse("CELL: " + hex(value) + " " + str(value))
    return value 
def BITMAP_LAYOUT(format,linestride,height): 
    value = ((0x07<<24)|(((format)&0x1F)<<19)|(((linestride)&0x3FF)<<9)|(((height)&0x1FF)<<0))
    PrintResponse("BITMAP_LAYOUT: " + hex(value) + " " + str(value))
    return value 
def BITMAP_SIZE(filter,wrapx,wrapy,width,height): 
    value = ((0x08<<24)|(((filter)&0x01)<<20)|(((wrapx)&0x01)<<19)|(((wrapy)&0x01)<<18)|(((width)&0x1FF)<<9)|(((height)&0x1FF)<<0))
    PrintResponse("BITMAP_SIZE: " + hex(value) + " " + str(value))
    return value 
def ALPHA_FUNC(func,ref): 
    value = ((0x09<<24)|(((func)&0x07)<<8)|(((ref)&0xFF)<<0))
    PrintResponse("ALPHA_FUNC: " + hex(value) + " " + str(value))
    return value 
def STENCIL_FUNC(func,ref,mask): 
    value = ((0x0A<<24)|(((func)&0x07)<<16)|(((ref)&0xFF)<<8)|(((mask)&0xFF)<<0))
    PrintResponse("STENCIL_FUNC: " + hex(value) + " " + str(value))
    return value 
def BLEND_FUNC(src,dst): 
    value = ((0x0B<<24)|(((src)&0x07)<<3)|(((dst)&0x07)<<0))
    PrintResponse("BLEND_FUNC: " + hex(value) + " " + str(value))
    return value 
def STENCIL_OP(sfail,spass): 
    value = ((0x0C<<24)|(((sfail)&0x07)<<3)|(((spass)&0x07)<<0))
    PrintResponse("STENCIL_OP: " + hex(value) + " " + str(value))
    return value 
def POINT_SIZE(size):
    value = ((0x0D<<24)|(((size)&0x1FFF)<<0))
    PrintResponse("POINT_SIZE: " + hex(value) + " " + str(value))
    return value 
def LINE_WIDTH(width): 
    value = ((0x0E<<24)|(((width)&0xFFFF)<<0))
    PrintResponse("LINE_WIDTH: " + hex(value) + " " + str(value))
    return value 
def CLEAR_COLOR_A(alpha): 
    value = ((0x0F<<24)|(((alpha)&0xFF)<<0))
    PrintResponse("CLEAR_COLOR_A: " + hex(value) + " " + str(value))
    return value 
def COLOR_A(alpha): 
    value = ((0x10<<24)|(((alpha)&0xFF)<<0))
    PrintResponse("COLOR_A: " + hex(value) + " " + str(value))
    return value 
def CLEAR_STENCIL(s): 
    value = ((0x11<<24)|(((s)&0xFF)<<0))
    PrintResponse("CLEAR_STENCIL: " + hex(value) + " " + str(value))
    return value 
def CLEAR_TAG(s): 
    value = ((0x12<<24)|(((s)&0xFF)<<0))
    PrintResponse("CLEAR_TAG: " + hex(value) + " " + str(value))
    return value 
def STENCIL_MASK(mask): 
    value = ((0x13<<24)|(((mask)&0xFF)<<0))
    PrintResponse("STENCIL_MASK: " + hex(value) + " " + str(value))
    return value 
def TAG_MASK(mask): 
    value = ((0x14<<24)|(((mask)&0x01)<<0))
    PrintResponse("TAG_MASK: " + hex(value) + " " + str(value))
    return value 
def BITMAP_TRANSFORM_A(a): 
    value = ((0x15<<24)|(((a)&0x1FFFF)<<0))
    PrintResponse("BITMAP_TRANSFORM_A: " + hex(value) + " " + str(value))
    return value 
def BITMAP_TRANSFORM_B(b): 
    value = ((0x16<<24)|(((b)&0x1FFFF)<<0))
    PrintResponse("BITMAP_TRANSFORM_B: " + hex(value) + " " + str(value))
    return value 
def BITMAP_TRANSFORM_C(c): 
    value = ((0x17<<24)|(((c)&0xFFFFFF)<<0))
    PrintResponse("BITMAP_TRANSFORM_C: " + hex(value) + " " + str(value))
    return value 
def BITMAP_TRANSFORM_D(d): 
    value = ((0x18<<24)|(((d)&0x1FFFF)<<0))
    PrintResponse("BITMAP_TRANSFORM_D: " + hex(value) + " " + str(value))
    return value 
def BITMAP_TRANSFORM_E(e): 
    value = ((0x19<<24)|(((e)&0x1FFFF)<<0))
    PrintResponse("BITMAP_TRANSFORM_E: " + hex(value) + " " + str(value))
    return value 
def BITMAP_TRANSFORM_F(f):
    value = ((0x1A<<24)|(((f)&0xFFFFFF)<<0))
    PrintResponse("BITMAP_TRANSFORM_F: " + hex(value) + " " + str(value))
    return value 
def SCISSOR_XY(x,y):
    value = ((0x1B<<24)|(((x)&0x1FF)<<9)|(((y)&0x1FF)<<0))
    PrintResponse("SCISSOR_XY: " + hex(value) + " " + str(value))
    return value 
def SCISSOR_SIZE(width,height):
    value = ((0x1C<<24)|(((width)&0x3FF)<<10)|(((height)&0x3FF)<<0))
    PrintResponse("SCISSOR_SIZE: " + hex(value) + " " + str(value))
    return value
def CALL(dest):
    value = ((0x1D<<24)|(((dest)&0xFFFF)<<0))
    PrintResponse("CALL: " + hex(value) + " " + str(value))
    return value 
def JUMP(dest):
    value = ((0x1E<<24)|(((dest)&0xFFFF)<<0))
    PrintResponse("JUMP: " + hex(value) + " " + str(value))
    return value 
def BEGIN(prim):
	value = ((0x1F<<24)|(((prim)&0x0F)<<0))
	PrintResponse("BEGIN: " + hex(value) + " " + str(value))
	return value
def COLOR_MASK(r,g,b,a):
    value = ((0x20<<24)|(((r)&0x01)<<3)|(((g)&0x01)<<2)|(((b)&0x01)<<1)|(((a)&0x01)<<0))
    PrintResponse("COLOR_MASK: " + hex(value) + " " + str(value))
    return value
def CLEAR(c,s,t):
	value = (((0x26<<24)|(((c)&0x01)<<2)|(((s)&0x01)<<1)|(((t)&0x01)<<0)))
	PrintResponse("CLEAR: " + hex(value) + " " + str(value))
	return value
def END():
    value = (0x21<<24)
    PrintResponse("END: " + hex(value) + " " + str(value))
    return value
def SAVE_CONTEXT():
    value = ((0x22<<24))
    PrintResponse("SAVE_CONTEXT: " + hex(value) + " " + str(value))
    return value 
def RESTORE_CONTEXT():
    value = ((0x23<<24))
    PrintResponse("RESTORE_CONTEXT: " + hex(value) + " " + str(value))
    return value 
def RETURN():
    value = ((0x24<<24))
    PrintResponse("RETURN: " + hex(value) + " " + str(value))
    return value 
def MACRO(m):
    value = ((0x25<<24)|(((m)&0x01)<<0))
    PrintResponse("MACRO: " + hex(value) + " " + str(value))
    return value 
def DISPLAY():
	value = 00 << 24
	PrintResponse("DISPLAY: " + hex(value) + " " + str(value))
	return value

def Write32(Register, Value):
	Buffer = [
		(0x80 | ((Register >> 16) & 0xFF)),
		((Register >> 8) & 0xFF),
		(Register & 0xFF),
		(Value & 0xFF),
		((Value >> 8) & 0xFF),
		((Value >> 16) & 0xFF),
		((Value >> 24) & 0xFF)
		]
	PrintResponse("Write32:" + str(Buffer))
	Response = spi.xfer(Buffer)
def Write16(Register, Value):
	Buffer = [
		(0x80 | ((Register >> 16) & 0xFF)),
		((Register >> 8) & 0xFF),
		(Register & 0xFF),
		(Value & 0xFF),
		((Value >> 8) & 0xFF)
		]
	PrintResponse("Write16:" + str(Buffer))
	Response = spi.xfer(Buffer)
def Write8(Register, Value):
	Buffer = [
		(0x80 | ((Register >> 16) & 0xFF)),
		((Register >> 8) & 0xFF),
		(Register & 0xFF),
		(Value & 0xFF)
		]
	PrintResponse("Write8:" + str(Buffer))
	Response = spi.xfer(Buffer)
def Read16(Register):
	Buffer = [
		(((Register >> 16) & 0xFF)),
		((Register >> 8) & 0xFF),
		(Register & 0xFF),
		0x00,
		0x00,
		0x00
		]
	PrintResponse("Read16:" + str(Buffer))
	Response = spi.xfer(Buffer)
	PrintResponse("Response: " + str(Response))
	return ((Buffer[4] << 8) + Buffer[5])
def Read8(Register):
	Buffer = [
		(((Register >> 16) & 0xFF)),
		((Register >> 8) & 0xFF),
		(Register & 0xFF),
		0x00,
		0x00
		]
	PrintResponse("Read8:" + str(Buffer))
	Response = spi.xfer(Buffer)
	PrintResponse("Response: " + str(Response))
	return Buffer[4]
def SendHostCommand(Command, Value1 = 0, Value2 = 0):
	Buffer = [Command, Value1, Value2]
	PrintResponse("Command:" + str(Buffer))
	Response = spi.xfer(Buffer)
	PrintResponse("Response: " + str(Response))
def ConfigureDisplayRegisters():
	PrintResponse("Setting up for WQVGA 480x272")
	#Configure display registers for WQVGA 480x272 resolution

	Write16(REG_HCYCLE, 548);
	Write16(REG_HOFFSET, 43);
	Write16(REG_HSYNC0, 0);
	Write16(REG_HSYNC1, 41);
	Write16(REG_VCYCLE, 292);
	Write16(REG_VOFFSET, 12);
	Write16(REG_VSYNC0, 0);
	Write16(REG_VSYNC1, 10);
	Write8(REG_SWIZZLE, 0);
	Write8(REG_PCLK_POL, 1);
	Write8(REG_CSPREAD, 1);
	#Write8(REG_DITHER, 1)
	Write16(REG_HSIZE, 480);
	Write16(REG_VSIZE, 272);

def ScreenPowerOn():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ScreenResetPin, GPIO.OUT)
    GPIO.output(ScreenResetPin, GPIO.HIGH)
    
def ScreenPowerOff():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ScreenResetPin, GPIO.OUT)
    GPIO.output(ScreenResetPin, GPIO.LOW)

def BacklightOn():
	Write16(REG_GPIOX_DIR, 0xFFFF)
	Write16(REG_GPIOX, 0xFFFF)

def BacklightOff():
	Write16(REG_GPIOX_DIR, 0x0000)
	Write16(REG_GPIOX, 0x0000)

def StartDisplayList(r,g,b):
    global DisplayListIndex
    DisplayListIndex = 0
    Write32(REG_CMDB_WRITE,CMD_DLSTART)
    DisplayListIndex += 4
    Write32(REG_CMDB_WRITE, CLEAR_COLOR_RGB(r,g,b))
    DisplayListIndex += 4
    Write32(REG_CMDB_WRITE, CLEAR(1,1,1)) #//Clear to initinitial colour

def AddCommandToDisplayList(Command):
    global DisplayListIndex
    DisplayListIndex += 4
    Write32(REG_CMDB_WRITE, Command) #//Clear to initial colour
    
def AddStringToDisplayList(Text):
    global DisplayListIndex
    LetterCount = 0
    intLetters = 0x00000000
    for letter in split(Text):  # Convert string to array of letters
        intLetters += (ord(letter) << LetterCount*8)  # Convert letter to int, then shift it to its place in the 32bit int
        LetterCount += 1
        if (LetterCount > 3): #if we have 4 letters write them to the display list
            Write32(REG_CMDB_WRITE, intLetters)
            LetterCount = 0
            intLetters = 0x00000000
    if(LetterCount < 4): #if we had a string that is not increments of 4 bytes, transmit it now. It will contain a terminating 0 because intLetters was initiallized to 0x00000000
        Write32(REG_CMDB_WRITE, intLetters)
    else: #if we had a string that was increments of 4 bytes, send a blank string terminator
        AddCommandToDisplayList(0x00010101)

def EndDisplayList():
    global DisplayListIndex
    DisplayListIndex += 4
    Write32(REG_CMDB_WRITE, DISPLAY()) #//End the display list
    DisplayListIndex += 4
    Write32(REG_CMDB_WRITE, CMD_SWAP) #Swap to the new display list

def InitDisplay():
    spi.open(bus,device)
    spi.max_speed_hz = 30000
    spi.mode = 0x00
    SendHostCommand(CLKEXT)
    SendHostCommand(CLKSEL)
    SendHostCommand(ACTIVE)
    time.sleep(.400)
    while(Read8(REG_ID) != 0x7C):
        print (Read8(REG_ID))
        print("REG_ID != 0x7C")
        sys.exit()
    while(Read16(REG_CPURESET) != 0x00):
        print("REG_CPURESET != 0x00")
        #sys.exit()
    Write32(REG_FREQUENCY, 0x3938700) # Configure the system clock to 60MHz
    ConfigureDisplayRegisters()

    StartDisplayList(0,0,0)
    EndDisplayList()
    Write8(REG_PWM_DUTY, 0x80)  #Set backlight duty cycle
    Write16(REG_PWM_HZ, 0x00FA) #Set backlight frequency
    Write8(REG_PCLK,5) #//Configure the PCLK divisor to 2, i.e. PCLK = System CLK/2 This leads to the output of the first display list

def ShortInit():
    #spi.open(bus,device)
    #spi.max_speed_hz = 30000
    #spi.mode = 0x00
    #SendHostCommand(CLKEXT)
    #SendHostCommand(CLKSEL)
    #SendHostCommand(ACTIVE)
    #time.sleep(.400)
    #while(Read8(REG_ID) != 0x7C):
    #    print (Read8(REG_ID))
    #    print("REG_ID != 0x7C")
    #    sys.exit()
    #while(Read16(REG_CPURESET) != 0x00):
    #    print("REG_CPURESET != 0x00")
        #sys.exit()
    #Write32(REG_FREQUENCY, 0x3938700) # Configure the system clock to 60MHz
    ConfigureDisplayRegisters()

    #StartDisplayList(0,0,0)
    #EndDisplayList()
    #Write8(REG_PWM_DUTY, 0x80)  #Set backlight duty cycle
    #Write16(REG_PWM_HZ, 0x00FA) #Set backlight frequency
    #Write8(REG_PCLK,5) #//Configure the PCLK divisor to 2, i.e. PCLK = System CLK/2 This leads to the output of the first display list
    Write32(REG_CPURESET, 1)
    Write32(REG_CMD_READ, 0)
    Write32(REG_CMD_WRITE, 0)
    Write32(REG_CPURESET, 0)
    while(Read16(REG_CMD_WRITE) != Read16(REG_CMD_READ)):
        print("REG_CPURESET != 0x00")
    

def DrawMenuOutline():
    AddCommandToDisplayList( LINE_WIDTH(20) );
    AddCommandToDisplayList( BEGIN(LINES) );
    #Top Line
    AddCommandToDisplayList( VERTEX2II(20, 20, 0, 0) );
    AddCommandToDisplayList( VERTEX2II(460, 20, 0, 0) );
    #Bottom Line
    AddCommandToDisplayList( VERTEX2II(20, 252, 0, 0) );
    AddCommandToDisplayList( VERTEX2II(460, 252, 0, 0) );
    #Right Line
    AddCommandToDisplayList( VERTEX2II(460, 20, 0, 0) );
    AddCommandToDisplayList( VERTEX2II(460, 252, 0, 0) );
    #Left Line
    AddCommandToDisplayList( VERTEX2II(20, 20, 0, 0) );
    AddCommandToDisplayList( VERTEX2II(20, 252, 0, 0) );

    AddCommandToDisplayList(END())

def split(word):
    return [char for char in word]

def DrawTextOutline(LineNumber):
    RecX = 20 #Start x position of the rectangle
    RecY = 25 #Start y posotion of the rectangle
    RecH = 45 #Rectangle Height
    RecW = 430 #Rectangle Width
    RecY = (RecH * LineNumber)
    
    AddCommandToDisplayList( LINE_WIDTH(15) );
    AddCommandToDisplayList( BEGIN(LINES) );
    #Top Line
    AddCommandToDisplayList( VERTEX2II(RecX, RecY, 0, 0) );
    AddCommandToDisplayList( VERTEX2II(RecX+RecW, RecY, 0, 0) );
    #Bottom Line
    AddCommandToDisplayList( VERTEX2II(RecX, RecY+RecH, 0, 0) );
    AddCommandToDisplayList( VERTEX2II(RecX+RecW, RecY+RecH, 0, 0) );
    #Right Line
    AddCommandToDisplayList( VERTEX2II(RecX+RecW, RecY, 0, 0) );
    AddCommandToDisplayList( VERTEX2II(RecX+RecW, RecY+RecH, 0, 0) );
    #Left Line
    AddCommandToDisplayList( VERTEX2II(RecX, RecY, 0, 0) );
    AddCommandToDisplayList( VERTEX2II(RecX, RecY+RecH, 0, 0) );
    
    AddCommandToDisplayList(END())

def DrawText(Text, LineNumber, SelectedLine):
    #Line one starts at x 25 y 25
    x = 25
    y = 23
    CharacterSpacing = 10
    CharacterHeight = 35
    y = y + (CharacterHeight * LineNumber) + (CharacterSpacing * LineNumber)
    options = OPT_CENTERY
    font = 31
    
    AddCommandToDisplayList(CMD_TEXT)
    AddCommandToDisplayList(((y & 0xFFFF)<<16) + (x & 0xFFFF))
    AddCommandToDisplayList(((options & 0xFFFF)<<16) + (font & 0xFFFF))
    AddStringToDisplayList(Text)
    
    if((LineNumber == SelectedLine) & (Text != "")):
        DrawTextOutline(LineNumber)

def DrawMenuTitle(Text):
    #Line one starts at x 25 y 25
    x = 240
    y = 25
    options = OPT_CENTER
    font = 31
    
    AddCommandToDisplayList(CMD_TEXT)
    AddCommandToDisplayList(((y & 0xFFFF)<<16) + (x & 0xFFFF))
    AddCommandToDisplayList(((options & 0xFFFF)<<16) + (font & 0xFFFF))
    AddStringToDisplayList(Text)


def DrawKeys(Keys, x, y, w, h, PressedKey):
    options = OPT_CENTERY|ord(PressedKey)
    font = 31
    
    AddCommandToDisplayList(CMD_KEYS)
    AddCommandToDisplayList(((y & 0xFFFF)<<16) + (x & 0xFFFF))
    AddCommandToDisplayList(((h & 0xFFFF)<<16) + (w & 0xFFFF))
    AddCommandToDisplayList(((options & 0xFFFF)<<16) + (font & 0xFFFF))
    AddStringToDisplayList(Keys)
    
def DrawButton(Text, x, y, w, h, Pressed):
    options = OPT_3D
    if(Pressed):
        options = OPT_FLAT

    font = 18
    AddCommandToDisplayList(CMD_BUTTON)
    AddCommandToDisplayList(((y & 0xFFFF)<<16) + (x & 0xFFFF))
    AddCommandToDisplayList(((h & 0xFFFF)<<16) + (w & 0xFFFF))
    AddCommandToDisplayList(((options & 0xFFFF)<<16) + (font & 0xFFFF))
    AddStringToDisplayList(Text)
    
def DrawSpinner(Text):
    x = 240
    y = 136
    style = 0
    sclae = 0
    StartDisplayList(0,0,0)
    AddCommandToDisplayList(CLEAR(1, 1, 1))#; // clear screen
    DrawText(Text, 1, 0)
    AddCommandToDisplayList(CMD_SPINNER)
    AddCommandToDisplayList(((y & 0xFFFF)<<16) + (x & 0xFFFF))
    AddCommandToDisplayList(((sclae & 0xFFFF)<<16) + (style & 0xFFFF))
    EndDisplayList()
        
def DrawProgress(Progress):
    x = 30
    y = 240
    w = 410
    h = 25
    MaxValue = 100
    options = OPT_3D #OPT_FLAT
    
    AddCommandToDisplayList(CMD_PROGRESS)
    AddCommandToDisplayList(((y & 0xFFFF)<<16) + (x & 0xFFFF))
    AddCommandToDisplayList(((h & 0xFFFF)<<16) + (w & 0xFFFF))
    AddCommandToDisplayList(((Progress & 0xFFFF)<<16) + (options & 0xFFFF))
    AddCommandToDisplayList(((0x00 & 0xFFFF)<<16) + (MaxValue & 0xFFFF))

def DrawKeyboard(Shift):
    StartDisplayList(255,0,255)
    AddCommandToDisplayList(CLEAR(1, 1, 1))#; // clear screen
    if(Shift):
        DrawKeys("~!@#$%^&*()_+", 25, 3, 410, 25, "2")
        DrawKeys("QWERTYUIOP{}|", 25, 31, 410, 25, " ")
        DrawKeys("ASDFGHJKL:\"", 25, 59, 410, 25, "a")
        DrawKeys("ZXCVBNM<>?", 25, 87, 410, 25, ".")
        DrawKeys(" \n", 25, 115, 410, 25, " ")
        DrawButton("Shift", 25, 143, 80 ,25, False)
        DrawButton("Enter", 25, 171, 80 ,25, True)
    else:
        DrawKeys("`1234567890-=", 25, 3, 410, 25, "2")
        DrawKeys("qwertyuiop[]\\", 25, 31, 410, 25, " ")
        DrawKeys("asdfghjkl;'", 25, 59, 410, 25, "a")
        DrawKeys("zxcvbnm,./", 25, 87, 410, 25, ".")
        DrawKeys(" \n", 25, 115, 410, 25, " ")
        DrawButton("Shift", 25, 143, 80 ,25, True)
        DrawButton("Enter", 25, 171, 80 ,25, False)
    EndDisplayList()

def DrawLinearKeyboard(SelectedKey, KeyboardString):
    StartDisplayList(255,0,255)
    AddCommandToDisplayList(CLEAR(1, 1, 1))#; // clear screen
    DrawMenuTitle(KeyboardString)
    keys = ""
    for x in range(32, 127):
        keys += chr(x)
    #print(keys)
    displaykeys = ""
    intSelectedKey = ord(SelectedKey)
    ##print(intSelectedKey)
    for x in range(-4, 5):
        #print(x)
        if((x+ord(SelectedKey) > 31) & (x+ord(SelectedKey) < 127)):
            displaykeys += chr(x+ord(SelectedKey))
        else:
            displaykeys += " "
    #print(displaykeys)
    DrawKeys(displaykeys, 25, 106, 430, 60, SelectedKey)
    EndDisplayList()
    
#Menu should be an array of strings. Index 0 is menu name, 1 is line 1, 2 is line 2, 3 is line 3, and 4 is line 4
#No more than 4 lines in each menu
#if an item should not be selected, its text needs to be blank
#Blank text will prevent the outline box from being drawn.
def DrawMenu(Menu, SelectedLine, DisplayProgressBar, ProgressValue):
    #print(threading.get_ident())
    StartDisplayList(0,0,0)
    AddCommandToDisplayList(CLEAR(1, 1, 1))#; // clear screen
    LineNumber = 0
    print(Menu)
    print(SelectedLine)

    for MenuItem in Menu:  # Convert string to array of letters
        if(LineNumber == 0):
            DrawMenuTitle(MenuItem)
        else:
            DrawText(MenuItem, LineNumber, SelectedLine)
        LineNumber += 1

    if(DisplayProgressBar):
        DrawProgress(ProgressValue)
    
    EndDisplayList()

def CloseSPI():
	spi.close()

def GetDeviceID():
	spi.open(bus, device)
	DeviceID = [0x0C,0x00,0x00, 0x00, 0x00,0x00,0x00,0x00]
	Response = spi.xfer2(DeviceID,5000,200,8)
	spi.close()
	PrintResponse("Sent DeviceID. mode=" + str(mode) + " cshigh=" + str(cshigh) + " Response: " + str(Response))
    