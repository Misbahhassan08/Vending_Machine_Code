import time
import ast
import os
#from datetime import datetime
import spidev
import RPi.GPIO as GPIO
import Helpers.logger as logger
from Helpers.Graphics.Constants import *
from Helpers.Graphics.Macros import *
import Helpers.configuration as config

class GraphicsHAL():
    def __init__(self, _ScreenResetPin=5, _bus=0, _device=0):
        self.Debug = config.get_value("debug", "GraphicsDriverHAL") == "True"
        self.DebugSPI = config.get_value("debug", "GraphicsDriverHalSPI") == "True"
        self._LogResponse("Setting up Screen GPIO")
        self._Bus = _bus
        self._Device = _device
        self._CurrentCachePosition = RAM_G + 4096 # Save 4096 to use the first 4096 as a deposit buffer for Flash
        self._CachedGraphics = {}
        self.ArtData = {}
        self.FontData = {}
        self._FlashBlockToWrite = 1
        self._ScreenResetPin = ScreenResetPin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._ScreenResetPin, GPIO.OUT)
        GPIO.output(self._ScreenResetPin, GPIO.LOW)
        #GP3 P3
        self._ScreenPowerPin = 22
        GPIO.setup(self._ScreenPowerPin, GPIO.OUT)
        GPIO.output(self._ScreenPowerPin, GPIO.LOW)
        self._EVEInit()
    def __del__(self):
        self._spi.close()
    def _EVEInit(self):
        self.ScreenPowerOff()
        self.ScreenResetLow()
        self.ScreenResetHigh()
        self.ScreenPowerOn()
        self._LogResponse("Setting up Screen SPI")
        self._spi = spidev.SpiDev() #The actual SPI Device
        self._spi.open(self._Bus, self._Device)
        self._spi.max_speed_hz = 3000000
        self._spi.mode = 0x00

        self._LogResponse("Initializing Screen")
        self._LogResponse("CLKEXT" + str(self._SendHostCommand(CLKEXT)))
        self._LogResponse("CLKSEL" + str(self._SendHostCommand(CLKSEL)))
        self._LogResponse("ACTIVE" + str(self._SendHostCommand(ACTIVE)))
        time.sleep(0.3) # Give the processor time to start up
        self._LogResponse("Waiting for Co-Processor to become active")
        #print("REG_ID")
        while(self._Read8(REG_ID) != 0x7C):
            time.sleep(0.01)
        #print("REG_CPURESET")
        while(self._Read16(REG_CPURESET) != 0x00):
            time.sleep(0.01)
        # Module type: 0x10 for FT810, 0x11 for FT811, 0x12 for FT812, 0x13 for FT813, 0x15 for BT815, 0x16 for BT815
        self._LogResponse("Screen Model ID is: " + hex(self._Read8(0xC0001)))
        #self._Write32(REG_FREQUENCY, 0x3938700) # Configure the system clock to 60MHz
        self._Write32(REG_FREQUENCY, 0x44AA200) # 72MHz is the recomended clock frequency‭
        self._SetupWQVGA()
        self._LogResponse("Co-Processor Active")
        self._SetFlashSpeedToFast()
        self._ScreenInit()
    def _ScreenInit(self):
        self._LogResponse("Prepareing First Display List")
        self.StartDisplayList(0, 0, 0)
        self.DrawText(Text="Loading", x=240, y=136, font=29, options=OPT_CENTERY|OPT_CENTERX)
        self.EndDisplayList()
        self._Write8(REG_PWM_DUTY, 0x80)  #Set backlight duty cycle
        self._Write16(REG_PWM_HZ, 0x00FA) #Set backlight frequency
        self._LogResponse("Starting PCLK")
        self._Write8(REG_PCLK, 5) #Configure the PCLK divisor. This leads to the output of the first display list
        self.WaitForCoProcessor()
        self.TurnBacklightOn()
        self.WaitForCoProcessor()
        self._LogResponse("Preparing DL Cash")
        self._PrepareCache()
        self.WaitForCoProcessor()
        self._LogResponse("Getting Flash Font Data")
        self._GetFontData()
        self._LogResponse("Getting Flash Art Data")
        self._GetArtData()
        self.WaitForCoProcessor()
        self._LogResponse("Display HAL Loaded")
    def _SetupWQVGA(self):
        self._LogResponse("Setting up for WQVGA 480x272")
        #Configure display registers for WQVGA 480x272 resolution
        self._Write16(REG_HCYCLE, 548)
        self._Write16(REG_HOFFSET, 43)
        self._Write16(REG_HSYNC0, 0)
        self._Write16(REG_HSYNC1, 41)
        self._Write16(REG_VCYCLE, 292)
        self._Write16(REG_VOFFSET, 12)
        self._Write16(REG_VSYNC0, 0)
        self._Write16(REG_VSYNC1, 10)
        self._Write8(REG_SWIZZLE, 0)
        self._Write8(REG_PCLK_POL, 1)
        self._Write8(REG_CSPREAD, 1)
        self._Write8(REG_DITHER, 1)
        self._Write16(REG_HSIZE, 480)
        self._Write16(REG_VSIZE, 272)
# Start Public Functions
    # Used to turn on the reset pin
    def ScreenPowerOn(self):
        self._LogResponse("Powering Screen On")
        GPIO.output(self._ScreenPowerPin, GPIO.HIGH)
        time.sleep(.25)
    # Used to turn off the reset pin
    def ScreenPowerOff(self):
        try:
            if(self._Read8(REG_PCLK) == 5):
                self.TurnBacklightOff()
        except:
            pass
        self._LogResponse("Powering Screen Off")
        GPIO.output(self._ScreenPowerPin, GPIO.LOW)
        time.sleep(.25)
    # Used to turn on the reset pin
    def ScreenResetHigh(self):
        self._LogResponse("Setting Reset Pin High")
        GPIO.output(self._ScreenResetPin, GPIO.HIGH)
        time.sleep(.25)
    # Used to turn off the reset pin
    def ScreenResetLow(self):
        self._LogResponse("Setting Reset Pin Low")
        GPIO.output(self._ScreenResetPin, GPIO.LOW)
        time.sleep(.25)
    def CacheDisplayList(self, ObjectName):
        self.WaitForCoProcessor()
        DisplayListLength = self._Read16(REG_CMD_DL) # Reading the REG_CMD_DL tells us where the end of the new DL is in RAM_DL and therefore the size of our new 'static' display list
        # Copy the cashable display list from RAM_DL to RAM_G
        self._Write32(REG_CMDB_WRITE, CMD_MEMCPY) # Command to copy a block of memory within the FT800
        self._Write32(REG_CMDB_WRITE, self._CurrentCachePosition) # First parameter is destination
        self._Write32(REG_CMDB_WRITE, RAM_DL) # Second parameter is the source, here we copy from start of RAM_DL
        self._Write32(REG_CMDB_WRITE, DisplayListLength) # Third parameter is length of data to copy, as determined above
        # Wait for the coprocessor to move the cashable display list
        self.WaitForCoProcessor()
        self._CachedGraphics[ObjectName] = [self._CurrentCachePosition, DisplayListLength]
        #print(self.CachedGraphics)
        self._CurrentCachePosition += DisplayListLength + 1
    def AddCachedCommandToDisplayList(self, ObjectName):
        try:
            CacheObjectAddresses = self._CachedGraphics[ObjectName]
            self._Write32(REG_CMDB_WRITE, CMD_APPEND) #Start clearing memory
            self._Write32(REG_CMDB_WRITE, CacheObjectAddresses[0]) # Start Address
            self._Write32(REG_CMDB_WRITE, CacheObjectAddresses[1]) # Length
        except Exception as e:
            logger.error(e)
    def TurnBacklightOff(self):
        self._LogResponse("Turning Backlight Off")
        self._Write16(REG_GPIOX_DIR, 0x0000)
        self._Write16(REG_GPIOX, 0x0000)
    def TurnBacklightOn(self):
        self._LogResponse("Turning Backlight On")
        self._Write16(REG_GPIOX_DIR, 0xFFFF)
        self._Write16(REG_GPIOX, 0xFFFF)
    def WaitForCoProcessor(self):
        #StartTime = datetime.now() # Get time to cancel if
        #HasLoggedInThisLoop = False
        while(self._Read16(REG_CMD_READ) != self._Read16(REG_CMD_WRITE)): # Wait for the coprocessor to finish, or .5 seconds (in case the processor dies)
            time.sleep(0.001)
            if("ERROR:" in self._GetCoProcessorErrorReport()):
                logger.error("CoProcessor Error: " + self._GetCoProcessorErrorReport())
                self._ClearErrorReport()
                self.RecoverCoProcessor()
            #if(((datetime.now()-StartTime).total_seconds() < .5)):
            #    self._LogResponse("Wait Timout!")
                #break
            # if(((datetime.now()-StartTime).total_seconds() < .1) and not HasLoggedInThisLoop):
            #     #print("Waiting On Graphics Co Processor")
            #     logger.error("Waiting On Graphics Co Processor")
            #     HasLoggedInThisLoop = True
    # This funciton can be used to recover the co-processor if bad input data is sent to the screen
    def RecoverCoProcessor(self):
        self._LogResponse("Recover CoProcessor Requested")
        #self._SendHostCommand(RST_PULSE)
        self._SetupWQVGA()
        #PatchPointer = self._Read16(REG_COPRO_PATCH_PTR)
        self._Write32(REG_CPURESET, 1)
        self._Write32(REG_CMD_READ, 0)
        self._Write32(REG_CMD_WRITE, 0)
        self._Write32(REG_CMD_DL, 0)
        self._Write32(REG_CPURESET, 0)
        #time.sleep(0.35)
        # while(self._Read16(REG_CPURESET) != 0x00)):
        #     print("REG_CPURESET != 0x00")
        #self._Write16(REG_COPRO_PATCH_PTR, PatchPointer)
        #if("display list must be empty" in self._GetCoProcessorErrorReport()):
        # Happens after CMD_CLEARCACHE is called with a non-empty display list. This case send the PCLK to 0 and needs to be reset to enable screen refreshes
        self._Write8(REG_PCLK, 5) #//Configure the PCLK divisor to 2, i.e. PCLK = System CLK/2 This leads to the output of the first display list
        self._SetFlashSpeedToFast()
    def StartEmptyDisplayList(self):
        self._Write32(REG_CMDB_WRITE, CMD_DLSTART)
    def StartDisplayList(self, r=255, g=255, b=255):
        self._Write32(REG_CMDB_WRITE, CMD_DLSTART)
        self._Write32(REG_CMDB_WRITE, CLEAR_COLOR_RGB(r, g, b))
        self._Write32(REG_CMDB_WRITE, CLEAR(1, 1, 1)) #//Clear to initinitial colour
    def EndDisplayList(self):
        self._Write32(REG_CMDB_WRITE, DISPLAY()) #//End the display list
        self._Write32(REG_CMDB_WRITE, CMD_SWAP) #Swap to the new display list
    def AddCommandToDisplayList(self, Command):
        self._Write32(REG_CMDB_WRITE, Command) #//Clear to initial colour
    def AddStringToDisplayList(self, Text):
        LetterCount = 0
        intLetters = 0x00000000
        for letter in self._SplitText(Text):  # Convert string to array of letters
            intLetters += (ord(letter) << LetterCount*8)  # Convert letter to int, then shift it to its place in the 32bit int
            LetterCount += 1
            if (LetterCount > 3): #if we have 4 letters write them to the display list
                self._Write32(REG_CMDB_WRITE, intLetters)
                LetterCount = 0
                intLetters = 0x00000000
        if(LetterCount < 4): #if we had a string that is not increments of 4 bytes, transmit it now. It will contain a terminating 0 because intLetters was initiallized to 0x00000000
            self._Write32(REG_CMDB_WRITE, intLetters)
        else: #if we had a string that was increments of 4 bytes, send a blank string terminator
            self._Write32(REG_CMDB_WRITE, 0x00010101)
# Pulbic Draw Functions
    def DrawText(self, Text, x, y, font=31, r=0, g=0, b=0, options=OPT_CENTERX|OPT_CENTERY):
        self.AddCommandToDisplayList(COLOR_RGB(r, g, b))
        self.AddCommandToDisplayList(CMD_TEXT)
        self.AddCommandToDisplayList(((y & 0xFFFF)<<16) + (x & 0xFFFF))
        self.AddCommandToDisplayList(((options & 0xFFFF)<<16) + (font & 0xFFFF))
        self.AddStringToDisplayList(Text)
    def DrawCustomFontText(self, Text, x, y, FontName, r=0, g=0, b=0, options=OPT_CENTERX|OPT_CENTERY):
        Font = self.FontData.get(FontName)
        FontHandle = int(Font[2])
        xFontAddress = int(Font[1])
        # update the flash font address dynamically
        # see https://brtchip.com/wp-content/uploads/Support/Documentation/Programming_Guides/ICs/EVE/BRT_AN_033_BT81X_Series_Programming_Guide.pdf
        # page 100 for structure definition of xFont structure
        # Flash block address * 4096 is flash address /32 is block address then or 0x800000 for flash base address
        FontFlashBlockAddress = FLASH_START|int((int(Font[0])*4096)/32)
        self._Write32(RAM_G+xFontAddress + 32, FontFlashBlockAddress)
        self._Write32(REG_CMDB_WRITE, SAVE_CONTEXT())
        self._Write32(REG_CMDB_WRITE, CMD_SETFONT2) #Start clearing memory
        self._Write32(REG_CMDB_WRITE, int(FontHandle)) #Font Handel
        self._Write32(REG_CMDB_WRITE, int(xFontAddress)) #xfont in RAMG
        self._Write32(REG_CMDB_WRITE, 0) # when using xfonts this should be 0
        self.AddCommandToDisplayList(COLOR_RGB(r, g, b))
        self.AddCommandToDisplayList(CMD_TEXT)
        self.AddCommandToDisplayList(((y & 0xFFFF)<<16) + (x & 0xFFFF))
        self.AddCommandToDisplayList(((options & 0xFFFF)<<16) + (FontHandle & 0xFFFF))
        self.AddStringToDisplayList(Text)
        self._Write32(REG_CMDB_WRITE, RESTORE_CONTEXT())
    def DrawImageFromFlash(self, ImageName, x=0, y=0, RotateAngle=0, Alpha=255, StretchX=0, StretchY=0, r=0, g=0, b=0):
        try:
            Art = self.ArtData.get(ImageName)
            if Art is None:
                return
            FlashBlockForStartOfImage = int(Art[0]) # Flash Start Address Block
            ImageWidth = int(Art[1])
            ImageHeight = int(Art[2])
            ImageFormat = self._GetImageFormat(Art[3])
            #print(FlashBlockForStartOfImage, ImageWidth, ImageHeight, ImageFormat, (FLASH_START|int(int(4096*FlashBlockForStartOfImage)/32)))
            # Setup the image format
            #print(ImageName, FlashBlockForStartOfImage, ImageWidth, ImageHeight, ImageFormat, Art)

            self._Write32(REG_CMDB_WRITE, CMD_SETBITMAP)
            self._Write32(REG_CMDB_WRITE, FLASH_START|int(int(4096*FlashBlockForStartOfImage)/32))
            self._Write32(REG_CMDB_WRITE, (int(ImageWidth)<<16)|(ImageFormat & 0xffff))
            self._Write32(REG_CMDB_WRITE, ImageHeight)
            # Display the image at the XY location
            self._Write32(REG_CMDB_WRITE, SAVE_CONTEXT())
            self._Write32(REG_CMDB_WRITE, BEGIN(BITMAPS))
            if StretchX != 0 or StretchY != 0:
                if StretchX != 0 and StretchY != 0:
                    self._Write32(REG_CMDB_WRITE, BITMAP_SIZE(filter=NEAREST, wrapx=REPEAT, wrapy=REPEAT, width=StretchX, height=StretchY))
                else:
                    if StretchX != 0:
                        self._Write32(REG_CMDB_WRITE, BITMAP_SIZE(filter=NEAREST, wrapx=REPEAT, wrapy=BORDER, width=StretchX, height=ImageHeight))
                    if StretchY != 0:
                        self._Write32(REG_CMDB_WRITE, BITMAP_SIZE(filter=NEAREST, wrapx=BORDER, wrapy=REPEAT, width=ImageWidth, height=StretchY))
            if RotateAngle != 0:
                #print("RotateAngle", RotateAngle)
                self._Write32(REG_CMDB_WRITE, CMD_LOADIDENTITY)
                self._Write32(REG_CMDB_WRITE, CMD_ROTATEAROUND)
                self._Write32(REG_CMDB_WRITE, int(ImageWidth/2)) # Pixel X to rotate/scale around
                self._Write32(REG_CMDB_WRITE, int(ImageHeight/2)) # Pixel Y to rotate/scale around
                self._Write32(REG_CMDB_WRITE, int((RotateAngle*65536)/360)) # Rotation Angle
                self._Write32(REG_CMDB_WRITE, 1*65536) # Image Scale
                self._Write32(REG_CMDB_WRITE, CMD_SETMATRIX)
            if Alpha != 255:
                #print("Alpha", Alpha)
                self._Write32(REG_CMDB_WRITE, COLOR_A(Alpha))
            if r+g+b > 0:
                self.AddCommandToDisplayList(COLOR_RGB(r, g, b))
            self._Write32(REG_CMDB_WRITE, VERTEX2II(x, y, 0, 0))
            self._Write32(REG_CMDB_WRITE, END())
            self._Write32(REG_CMDB_WRITE, RESTORE_CONTEXT())
        except Exception as e:
            print(e)
            logger.error("DrawImageFromFlash: " + str(e))
# End Public Draw Functions
# Flash Related Pulbic Functions
    def FlashVersionIsLatest(self):
        try:
            ExpectedArtVersion = open('/Share/Art/_ArtVersion.txt', 'r').read()
        except:
            ExpectedArtVersion = "NoArtVersionInArtFolder"
        try:
            CurrentArtVersion = self.ReadStringFromFlashBlock(FlashBlockToRead=1)
        except:
            CurrentArtVersion = "NoArtVersionInFlash"
        return ExpectedArtVersion == CurrentArtVersion

    def _DrawFlashUpdateProgress(self, TitleText="Loading", Progress=0, FileProgress=0, FileName="", ShowData=True):
        SpinnerX = 240
        SpinnerY = 136
        style = 0
        scale = 0
        TitleFont = 31
        TitleOptions = OPT_CENTER
        TitleX = 240
        TitleY = 25
        FileX = 30
        FileY = 185
        FileFont = 20
        FileOptions = OPT_CENTERY|OPT_CENTERY
        ProgressMaxValue = 100
        ProgressOptions = OPT_3D #OPT_FLAT
        ProgressX = 30
        ProgressY = 240
        ProgressH = 25
        ProgressW = 410

        FileProgressMaxValue = 100
        FileProgressOptions = OPT_3D #OPT_FLAT
        FileProgressX = 30
        FileProgressY = 200
        FileProgressH = 25
        FileProgressW = 410

        self.WaitForCoProcessor()
        self.StartDisplayList(0, 0, 0)

        self.AddCommandToDisplayList(COLOR_RGB(0xFF, 0xFF, 0xFF))

        self.AddCommandToDisplayList(CMD_TEXT)
        self.AddCommandToDisplayList(((TitleY & 0xFFFF)<<16) + (TitleX & 0xFFFF))
        self.AddCommandToDisplayList(((TitleOptions & 0xFFFF)<<16) + (TitleFont & 0xFFFF))
        self.AddStringToDisplayList(TitleText)

        if ShowData:
            self.AddCommandToDisplayList(CMD_TEXT)
            self.AddCommandToDisplayList(((FileY & 0xFFFF)<<16) + (FileX & 0xFFFF))
            self.AddCommandToDisplayList(((FileOptions & 0xFFFF)<<16) + (FileFont & 0xFFFF))
            self.AddStringToDisplayList(FileName)

            self.AddCommandToDisplayList(CMD_PROGRESS)
            self.AddCommandToDisplayList(((ProgressY & 0xFFFF)<<16) + (ProgressX & 0xFFFF))
            self.AddCommandToDisplayList(((ProgressH & 0xFFFF)<<16) + (ProgressW & 0xFFFF))
            self.AddCommandToDisplayList(((Progress & 0xFFFF)<<16) + (ProgressOptions & 0xFFFF))
            self.AddCommandToDisplayList(((0x00 & 0xFFFF)<<16) + (ProgressMaxValue & 0xFFFF))

            self.AddCommandToDisplayList(CMD_PROGRESS)
            self.AddCommandToDisplayList(((FileProgressY & 0xFFFF)<<16) + (FileProgressX & 0xFFFF))
            self.AddCommandToDisplayList(((FileProgressH & 0xFFFF)<<16) + (FileProgressW & 0xFFFF))
            self.AddCommandToDisplayList(((FileProgress & 0xFFFF)<<16) + (FileProgressOptions & 0xFFFF))
            self.AddCommandToDisplayList(((0x00 & 0xFFFF)<<16) + (FileProgressMaxValue & 0xFFFF))

            self.AddCommandToDisplayList(CMD_SPINNER)
            self.AddCommandToDisplayList(((SpinnerY & 0xFFFF)<<16) + (SpinnerX & 0xFFFF))
            self.AddCommandToDisplayList(((scale & 0xFFFF)<<16) + (style & 0xFFFF))

        self.EndDisplayList()
        self.WaitForCoProcessor()
    def UpdateFlashArt(self):
        self._DrawFlashUpdateProgress(TitleText="Updating Firmware", Progress=0, FileProgress=0, FileName="", ShowData=False)
        self._LogResponse("Erasing Flash")
        self._FlashErase()
        self._LogResponse("Flash Erased")
        self._DrawFlashUpdateProgress(TitleText="Updating Firmware", Progress=10, FileProgress=0, FileName="")
        self._LogResponse("Flash Speed:" + str(self._GetFlashSpeed()))
        self._LogResponse("Error Report:" + str(self._GetCoProcessorErrorReport()))
        self._LogResponse("Writing Blob to first flash block")
        self.FlashWriteFileToFlashBlock("/Share/Art/BT815.blob", 0)
        self._LogResponse("Blob Write Done")
        self._DrawFlashUpdateProgress(TitleText="Updating Firmware", Progress=20, FileProgress=0, FileName="")
        if self._GetFlashSpeed() not in "Fast":
            self._LogResponse("Error Report:" + str(self._GetCoProcessorErrorReport()))
            self.RecoverCoProcessor()
            self._LogResponse("Error Report:" + str(self._GetCoProcessorErrorReport()))
            self._SetFlashSpeedToFast()
            self._LogResponse("Error Report:" + str(self._GetCoProcessorErrorReport()))
            self._LogResponse(self._GetFlashSpeed())
            self._LogResponse("Error Report:" + str(self._GetCoProcessorErrorReport()))
        self._SetFlashSpeedToFast()
        self._DrawFlashUpdateProgress(TitleText="Updating Firmware", Progress=30, FileProgress=0, FileName="")
        if self._GetFlashSpeed() in "Fast":
            self._LoadFontsIntoFlash()
        self._DrawFlashUpdateProgress(TitleText="Updating Firmware", Progress=40, FileProgress=0, FileName="")
        if self._GetFlashSpeed() in "Fast":
            self._LoadImagesIntoFlash()
        self._DrawFlashUpdateProgress(TitleText="Updating Firmware", Progress=50, FileProgress=0, FileName="")
        if self._GetFlashSpeed() in "Fast":
            self.FlashWriteFileToFlashBlock("/Share/Art/_ArtVersion.txt", 1)
        self._DrawFlashUpdateProgress(TitleText="Updating Firmware", Progress=60, FileProgress=0, FileName="")
        if self._GetFlashSpeed() in "Fast":
            self.ClearFlashCache()
        self._DrawFlashUpdateProgress(TitleText="Updating Firmware", Progress=70, FileProgress=0, FileName="")
        self._LogResponse("Getting Flash Font Data")
        self._GetFontData()
        self._DrawFlashUpdateProgress(TitleText="Updating Firmware", Progress=80, FileProgress=0, FileName="")
        self._LogResponse("Getting Flash Art Data")
        self._GetArtData()
        self._DrawFlashUpdateProgress(TitleText="Updating Firmware", Progress=90, FileProgress=0, FileName="")
        self.WaitForCoProcessor()
        self._DrawFlashUpdateProgress(TitleText="Updating Firmware", Progress=100, FileProgress=0, FileName="")
    def _LoadFontsIntoFlash(self):
        FontList = []
        FontArray = []
        for file in os.listdir("/Share/Art"):
            if file.endswith(".glyph"):
                FontList.append([str(file), str(file).split(".")[0]])
        FontList.sort()

        FileCounter = 0
        self._FlashBlockToWrite = 4
        print("Writing Fonts to flash")
        for FileDetail in FontList:
            print(FileCounter, len(FontList), (FileCounter/len(FontList)))
            self._DrawFlashUpdateProgress(TitleText="Loading Fonts", Progress=70, FileProgress=int((FileCounter/len(FontList))*100), FileName=FileDetail[0])
            FileName = FileDetail[0]
            FontName = FileDetail[1]
            FontSize = FileDetail[1].split("_")[1]
            print(FontName, FontSize)
            FontAddress = self.FlashWriteFileToFlashBlock("/Share/Art/" + FileName, -1)
            XFontAddress = 0 # load a dummy xfont address.  This is populated at run time so the xfont data can be placed anywhere in RAM_G
            FontArray.append([FontName, [FontAddress, XFontAddress, FontSize]])
            self.FontData = FontArray
            FileCounter += 1
        with open('/Share/Art/FontList', 'w') as f:
            f.write(str(FontArray))
        print("Fonts in Flash")
    def _LoadImagesIntoFlash(self):
        ArtList = []
        ArtArray = []
        for file in os.listdir("/Share/Art"):
            if file.endswith(".raw"):
                ArtList.append([str(file), str(file).split("_")])
        ArtList.sort()
        FileCounter = 0
        for FileDetail in ArtList:
            self._DrawFlashUpdateProgress(TitleText="Loading Art", Progress=80, FileProgress=int((FileCounter/len(ArtList))*100), FileName=FileDetail[0])
            FileName = FileDetail[0]
            ImageName = FileDetail[1][0]
            ImageWidth = FileDetail[1][1].split("x")[0]
            ImageHeight = FileDetail[1][1].split("x")[1]
            CompressionType = FileDetail[1][5]
            print(self._GetFlashSpeed(), FileName, ImageWidth, ImageHeight, CompressionType)
            ArtArray.append([ImageName, [self._FlashBlockToWrite, ImageWidth, ImageHeight, CompressionType]])
            with open('/Share/Art/ArtList', 'w') as f:
                f.write(str(ArtArray))
            self._GetArtData()
            _ = self.FlashWriteFileToFlashBlock("/Share/Art/" + FileName, -1)
            # GD.StartDisplayList(0, 0, 0)
            # GD.DrawImageFromFlash(ImageName)
            # GD.DrawText(Text=FileDetail[1][0], x=0, y=136, font=20)
            # GD.EndDisplayList()
            # GD.WaitForCoProcessor()
            FileCounter += 1
        with open('/Share/Art/ArtList', 'w') as f:
            f.write(str(ArtArray))
        print("Images in Flash")
        # For Co Processor Errors see: Page 106 Coprocessor Faults https://brtchip.com/wp-content/uploads/Support/Documentation/Programming_Guides/ICs/EVE/BRT_AN_033_BT81X_Series_Programming_Guide.pdf
    def _GetCoProcessorErrorReport(self):
        ByteCounter = 0
        String = ""
        for ByteCounter in range(0, 127):
            byte = self._Read8(RAM_ERR_REPORT + ByteCounter)
            if int(byte) > 31 and int(byte) < 127:
                String += chr(byte)
        if "ERROR:" in String:
            return String
        else:
            return ""
    def _ClearErrorReport(self):
        for ByteCounter in range(0, 127):
            self._Write8(RAM_ERR_REPORT + ByteCounter, 0x00)
    def _DetatchFlash(self):
        self._LogResponse("Attempting to Detatch Flash")
        self.WaitForCoProcessor()
        self._Write32(REG_CMDB_WRITE, CMD_FLASHDETACH)
        self.WaitForCoProcessor()
    def _AttatchFlash(self):
        self._LogResponse("Attempting to Attach Flash")
        self.WaitForCoProcessor()
        self._Write32(REG_CMDB_WRITE, CMD_FLASHATTACH)
        self.WaitForCoProcessor()
    def _SetFlashSpeedToFast(self):
        self.WaitForCoProcessor()
        # Check for flash attached state
        self._LogResponse("_SetFlashSpeedToFast")
        self._LogResponse("Current Flash Speed: " + str(self._GetFlashSpeed()))
        if not self._GetFlashSpeed() == "Fast":
        # If detached, attached
            if self._GetFlashSpeed() == "Detached":
                self._AttatchFlash()
                #print(self._GetFlashSpeed())
            elif self._GetFlashSpeed() == "Init":
                self._AttatchFlash()
                #print(self._GetFlashSpeed())
        # Set Flash state to fast
            self._LogResponse("Flash not fast. Executing Fast Command")
            self.WaitForCoProcessor()
            IntialCommandLocation = RAM_CMD + self._Read16(REG_CMD_READ)
            self._Write32(REG_CMDB_WRITE, CMD_FLASHFAST)
            self._Write32(REG_CMDB_WRITE, 0xFFFFFFFF)  # Set the Response to something other than the list of error values to ensure we don't falsly identify 0x0000 or some error
            self.WaitForCoProcessor()
            self._LogResponse("Flash not fast. Checking for CMD_FLASHFAST result")
            FastFlashResult = self._Read32(IntialCommandLocation + 4)
            FastFlashResultString = ""

            if FastFlashResult == 0x0000:
                self._LogResponse("Flash is Fast")
                return self._GetFlashSpeed()
            elif FastFlashResult == 0xE001:
                FastFlashResultString = "0xE001 flash is not supported"
            elif FastFlashResult == 0xE002:
                FastFlashResultString = "0xE002 no header detected in sector 0 - is flash blank?"
            elif FastFlashResult == 0xE003:
                FastFlashResultString = "0xE003 sector 0 data failed integrity check"
            elif FastFlashResult == 0xE004:
                FastFlashResultString = "0xE004 device/blob mismatch - was correct blob loaded?"
            elif FastFlashResult == 0xE005:
                FastFlashResultString = "0xE005 failed full-speed test - check board wiring"
            elif FastFlashResult == 0xFFFFFFFF:
                FastFlashResultString = "0xFFFF CMD_FLASHFAST Timeout"
            else:
                FastFlashResultString = "Unknown Error: " + str(FastFlashResult)
            self._LogResponse("Flash fast error: " + str(FastFlashResultString))
            return FastFlashResultString
        else:
            self._LogResponse("Flash Already Fast")
            return "Fast"
    def _GetFlashSpeed(self):
        FlashStatus = self._Read8(REG_FLASH_STATUS)
        if(FlashStatus == FLASH_STATUS_BASIC):
            return "Basic"
        elif(FlashStatus == FLASH_STATUS_FULL):
            return "Fast"
        elif(FlashStatus == FLASH_STATUS_DETACHED):
            return "Detached"
        elif(FlashStatus == FLASH_STATUS_INIT):
            return "Init"
        else:
            return "Unknown Flash Speed:" + str(FlashStatus)
    def _GetFlashSize(self):
        return(str(self._Read8(REG_FLASH_SIZE)))
    def ClearFlashCache(self):
        self._LogResponse("Clearning Flash Cache")
        self._Write32(REG_CMDB_WRITE, CMD_DLSTART)
        self._Write32(REG_CMDB_WRITE, CMD_CLEARCACHE)
        self.WaitForCoProcessor()
    def _FlashErase(self):
        self._LogResponse("Erasing Flash")
        self._Write32(REG_CMDB_WRITE, CMD_FLASHERASE)
        self.WaitForCoProcessor()
    def _FlashUpdate(self, FlashBlockToWrite, GRamSourceAddress, NumberOfBytes=4096):
        self._LogResponse("_FlashUpdate:FlashBlockToWrite=" + str(FlashBlockToWrite) + " GRamSourceAddress:" + str(GRamSourceAddress) + " NumberOfBytes:" + str(NumberOfBytes))
        self.WaitForCoProcessor()
        FlashDestinationAddress = (FlashBlockToWrite * 4096)
        self._Write32(REG_CMDB_WRITE, CMD_FLASHUPDATE)
        self._Write32(REG_CMDB_WRITE, int(FlashDestinationAddress))
        self._Write32(REG_CMDB_WRITE, int(GRamSourceAddress))
        self._Write32(REG_CMDB_WRITE, int(NumberOfBytes))
        self.WaitForCoProcessor()
    def ReadStringFromFlashBlock(self, FlashBlockToRead=1):
        self._ClearRAM_GBuffer()
        self._Write32(REG_CMDB_WRITE, CMD_FLASHREAD)
        self._Write32(REG_CMDB_WRITE, RAM_G)
        self._Write32(REG_CMDB_WRITE, int(FlashBlockToRead*4096))
        self._Write32(REG_CMDB_WRITE, 4096)
        self.WaitForCoProcessor()
        ByteTracker = 0
        String = ""
        while (ByteTracker < 4096):
            byte = self._Read8(RAM_G + ByteTracker)
            if int(byte) > 31 and int(byte) < 127:
                String += chr(byte)
            ByteTracker += 1
        return String
    def FlashWriteFileToFlashBlock(self, SourceFile, FlashBlockToWrite=1):
        self._LogResponse("FlashWriteFileToFlashBlock:SourceFile=" + str(SourceFile) + " FlashBlockToWrite:" + str(FlashBlockToWrite))
        self.WaitForCoProcessor()
        ByteTracker = 0
        if FlashBlockToWrite >= 0: # negative flash values allow continued writing to flash
            self._FlashBlockToWrite = FlashBlockToWrite
        File = open(SourceFile, "rb")
        FirstFlashBlock = self._FlashBlockToWrite
        self._ClearRAM_GBuffer()
        for byte in bytearray(File.read()):
            self._Write8(RAM_G + ByteTracker, byte)
            #print(self._Read8(RAM_G + ByteTracker))
            #print("Address:", RAM_G + ByteTracker, "Value:", byte)
            ByteTracker += 1
            if ByteTracker > 4095:
                print(self._FlashBlockToWrite, ByteTracker)
                self._FlashUpdate(self._FlashBlockToWrite, RAM_G, 4096)
                ByteTracker = 0
                self._FlashBlockToWrite += 1
                self._ClearRAM_GBuffer()
        if(ByteTracker > 0):
            print(self._FlashBlockToWrite, ByteTracker)
            self._FlashUpdate(self._FlashBlockToWrite, RAM_G, 4096)
            self._FlashBlockToWrite += 1
        return FirstFlashBlock
    def FlashWriteStringToFlashBlock(self, StringToWrite, FlashBlockToWrite=1):
        ByteTracker = 0
        if FlashBlockToWrite >= 0: # negative flash values allow continued writing to flash
            self._FlashBlockToWrite = FlashBlockToWrite
        self._ClearRAM_GBuffer()
        for char in StringToWrite:
            self._Write8(RAM_G + ByteTracker, ord(char))
            #print("Address:", RAM_G + ByteTracker, "Value:", int.from_bytes(byte, byteorder='big'))
            ByteTracker += 1
            if ByteTracker > 4095:
                print(self._FlashBlockToWrite, ByteTracker)
                self._FlashUpdate(self._FlashBlockToWrite, RAM_G, 4096)
                ByteTracker = 0
                self._FlashBlockToWrite += 1
        if(ByteTracker > 0):
            self._ClearRAM_GBuffer()
            for _ in range(ByteTracker, 4095):
                self._Write8(RAM_G + ByteTracker, 0)
            print(self._FlashBlockToWrite, ByteTracker)
            self._FlashUpdate(self._FlashBlockToWrite, RAM_G, 4096)
            self._FlashBlockToWrite += 1
# End Flash Related Public Functions
# End Public Functions
# Start Private Functions
    def _LogResponse(self, Message):
        if(self.Debug):
            logger.info(Message)
    def _LogSPIResponse(self, Message):
        if(self.DebugSPI):
            logger.info(Message)
    def _GetArtData(self):
        try:
            with open('/Share/Art/ArtList', 'r') as f:
                self.ArtData = dict(ast.literal_eval(f.read()))
        except Exception as e:
            logger.error("_GetArtData: " + str(e))
    def _GetFontData(self):
        try:
            FontHandleCounter = 1
            with open('/Share/Art/FontList', 'r') as f:
                self.FontData = dict(ast.literal_eval(f.read()))
            for FontDetail in self.FontData:
                FontAddress = self.FontData[FontDetail][0]
                xFontAddress = self._CurrentCachePosition
                FontSize = self.FontData[FontDetail][2]

                File = open("/Share/Art/" + FontDetail + ".xfont", "rb")
                #print(File)
                for byte in bytearray(File.read()):
                    self._Write8(RAM_G + self._CurrentCachePosition, byte)
                    #print("Address:", RAM_G + ByteTracker, "Value:", int.from_bytes(byte, byteorder='big'))
                    self._CurrentCachePosition += 1
                FontHandle = FontHandleCounter
                self.WaitForCoProcessor()
                self._Write32(REG_CMDB_WRITE, CMD_SETFONT2) #Start clearing memory
                self._Write32(REG_CMDB_WRITE, int(FontHandle)) #Font Handel
                self._Write32(REG_CMDB_WRITE, int(xFontAddress)) #xfont in RAMG
                self._Write32(REG_CMDB_WRITE, 0) # when using xfonts this should be 0
                self.WaitForCoProcessor()

                FontDetailUpdate = {FontDetail: [FontAddress, xFontAddress, FontHandle, FontSize]}
                self.FontData.update(FontDetailUpdate)
                FontHandleCounter += 1
        except Exception as e:
            logger.error("_GetFontData: " + str(e))
    def _GetImageFormat(self, FormatString):
        if(FormatString == '4x4'):
            return COMPRESSED_RGBA_ASTC_4x4_KHR
        elif(FormatString == '10x10'):
            return COMPRESSED_RGBA_ASTC_10x10_KHR
        elif(FormatString == '10x5'):
            return COMPRESSED_RGBA_ASTC_10x5_KHR
        elif(FormatString == '10x6'):
            return COMPRESSED_RGBA_ASTC_10x6_KHR
        elif(FormatString == '10x8'):
            return COMPRESSED_RGBA_ASTC_10x8_KHR
        elif(FormatString == '12x10'):
            return COMPRESSED_RGBA_ASTC_12x10_KHR
        elif(FormatString == '12x12'):
            return COMPRESSED_RGBA_ASTC_12x12_KHR
        elif(FormatString == '5x4'):
            return COMPRESSED_RGBA_ASTC_5x4_KHR
        elif(FormatString == '5x5'):
            return COMPRESSED_RGBA_ASTC_5x5_KHR
        elif(FormatString == '6x5'):
            return COMPRESSED_RGBA_ASTC_6x5_KHR
        elif(FormatString == '6x6'):
            return COMPRESSED_RGBA_ASTC_6x6_KHR
        elif(FormatString == '8x5'):
            return COMPRESSED_RGBA_ASTC_8x5_KHR
        elif(FormatString == '8x6'):
            return COMPRESSED_RGBA_ASTC_8x6_KHR
        elif(FormatString == '8x8'):
            return COMPRESSED_RGBA_ASTC_8x8_KHR
        else:
            return COMPRESSED_RGBA_ASTC_4x4_KHR
    def _SplitText(self, word):
        return [char for char in word]
    def _ClearRAM_GBuffer(self):
        self.WaitForCoProcessor()
        # Clear space in RAM_G for cached display lists
        self._Write32(REG_CMDB_WRITE, CMD_MEMSET) #Start clearing memory
        self._Write32(REG_CMDB_WRITE, RAM_G) #From RAM_G
        self._Write32(REG_CMDB_WRITE, 0xFF) #Set to 0
        self._Write32(REG_CMDB_WRITE, 0x1000) #clear 4k bytes for display cache
        # Wait for the coprocessor to clear the space for the display lists
        self.WaitForCoProcessor()
    def _PrepareCache(self):
        self.WaitForCoProcessor()
        # Clear space in RAM_G for cached display lists
        self._Write32(REG_CMDB_WRITE, CMD_MEMSET) #Start clearing memory
        self._Write32(REG_CMDB_WRITE, RAM_G) #From RAM_G
        self._Write32(REG_CMDB_WRITE, 0x00) #Set to 0
        self._Write32(REG_CMDB_WRITE, 0x80000) #clear 512k bytes for display cache
        # Wait for the coprocessor to clear the space for the display lists
        self.WaitForCoProcessor()
    def _Write32(self, Register, Value):
        Buffer = [
            (0x80 | ((Register >> 16) & 0xFF)),
            ((Register >> 8) & 0xFF),
            (Register & 0xFF),
            (Value & 0xFF),
            ((Value >> 8) & 0xFF),
            ((Value >> 16) & 0xFF),
            ((Value >> 24) & 0xFF)
            ]
        self._LogSPIResponse("Write32:" + str(Buffer))
        Response = self._spi.xfer(Buffer)
        self._LogSPIResponse("Write32 Response:" + str(Response))
        return Response
    def _Write16(self, Register, Value):
        Buffer = [
            (0x80 | ((Register >> 16) & 0xFF)),
            ((Register >> 8) & 0xFF),
            (Register & 0xFF),
            (Value & 0xFF),
            ((Value >> 8) & 0xFF)
            ]
        self._LogSPIResponse("Write16:" + str(Buffer))
        Response = self._spi.xfer(Buffer)
        self._LogSPIResponse("Write32 Response:" + str(Response))
        return Response
    def _Write8(self, Register, Value):
        Buffer = [
            (0x80 | ((Register >> 16) & 0xFF)),
            ((Register >> 8) & 0xFF),
            (Register & 0xFF),
            (Value & 0xFF)
            ]
        self._LogSPIResponse("Write8:" + str(Buffer))
        Response = self._spi.xfer(Buffer)
        self._LogSPIResponse("Write32 Response:" + str(Response))
        return Response
    def _Read32(self, Register):
        Buffer = [
            (((Register >> 16) & 0xFF)),
            ((Register >> 8) & 0xFF),
            (Register & 0xFF),
            0x00,
            0x00,
            0x00,
            0x00,
            0x00
            ]
        self._LogSPIResponse("Read16:" + str(Buffer))
        Response = self._spi.xfer(Buffer)
        self._LogSPIResponse("Response: " + str(Response))
        return (((Buffer[7] << 24) + (Buffer[6] << 16) + (Buffer[5] << 8) + Buffer[4]) & 0xFFFFFFFF)
    def _Read16(self, Register):
        Buffer = [
            (((Register >> 16) & 0xFF)),
            ((Register >> 8) & 0xFF),
            (Register & 0xFF),
            0x00,
            0x00,
            0x00
            ]
        self._LogSPIResponse("Read16:" + str(Buffer))
        Response = self._spi.xfer(Buffer)
        self._LogSPIResponse("Response: " + str(Response))
        return (((Buffer[5] << 8) + Buffer[4]) & 0xFFFF)
    def _Read8(self, Register):
        Buffer = [
            (((Register >> 16) & 0xFF)),
            ((Register >> 8) & 0xFF),
            (Register & 0xFF),
            0x00,
            0x00
            ]
        self._LogSPIResponse("Read8:" + str(Buffer))
        Response = self._spi.xfer(Buffer)
        self._LogSPIResponse("Response: " + str(Response))
        return (Buffer[4] & 0xFF)
    def _SendHostCommand(self, Command, Value1=0, Value2=0):
        Buffer = [Command, Value1, Value2]
        self._LogSPIResponse("Command:" + str(Buffer))
        Response = self._spi.xfer(Buffer)
        self._LogSPIResponse("Response: " + str(Response))
        return Response
# End Private Functions
