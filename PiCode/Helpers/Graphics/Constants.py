Debug = False     #Used to enable verbose output


bus = 0               #Bus ID (Found in /dev/spi...
device = 0            #Device ID (Found in /dev/spi...
ScreenResetPin = 5   #hooked to the !RST pin on the screen

DisplayListIndex = 0
#Addresses
RAM_G         = 0x000000 #General purpose graphics RAM
ROM_FONT      = 0x1E0000 #Font table and bitmap
ROM_FONT_ADDR = 0x2FFFFC #Font table pointer address
RAM_DL        = 0x300000 #RAM_DL Display List RAM
RAM_REG       = 0x302000 #Registers
RAM_CMD       = 0x308000 #RAM_CMD Command buffer
RAM_ERR_REPORT = 0x309800 # Address of 128b Error reports
FLASH_START   = 0x800000 #Memory mapped address for attached flash

#Address Sizes
SIZE_RAM_G    = 0x000FFFFF # 1024KB|1MB
SIZE_RAM_DL   = 0x00001FFF # 8KB

#NOR Flash
REG_FLASH_STATUS     = 3155440
FLASH_STATUS_INIT    = 0x00
FLASH_STATUS_DETACHED = 0x01
FLASH_STATUS_BASIC   = 0x02
FLASH_STATUS_FULL    = 0x03
REG_FLASH_SIZE       = 3182628
CMD_FLASHATTACH      = 4294967113
CMD_FLASHDETACH      = 4294967112
CMD_FLASHERASE       = 4294967108
CMD_FLASHFAST        = 4294967114
CMD_FLASHREAD        = 4294967110
CMD_FLASHSOURCE      = 4294967118
CMD_FLASHSPIDESEL    = 4294967115
CMD_FLASHSPIRX       = 4294967117
CMD_FLASHSPITX       = 4294967116
CMD_FLASHUPDATE      = 4294967111
CMD_FLASHWRITE       = 4294967109
CMD_APPENDF          = 4294967129
CMD_CLEARCACHE       = 4294967119
CMD_SETBITMAP        = 4294967107

#Image Compression Types
ARGB1555 = 0
RGB332 = 4

COMPRESSED_RGBA_ASTC_10x10_KHR = 37819
COMPRESSED_RGBA_ASTC_10x5_KHR = 37816
COMPRESSED_RGBA_ASTC_10x6_KHR = 37817
COMPRESSED_RGBA_ASTC_10x8_KHR = 37818
COMPRESSED_RGBA_ASTC_12x10_KHR = 37820
COMPRESSED_RGBA_ASTC_12x12_KHR = 37821
COMPRESSED_RGBA_ASTC_4x4_KHR = 37808
COMPRESSED_RGBA_ASTC_5x4_KHR = 37809
COMPRESSED_RGBA_ASTC_5x5_KHR = 37810
COMPRESSED_RGBA_ASTC_6x5_KHR = 37811
COMPRESSED_RGBA_ASTC_6x6_KHR = 37812
COMPRESSED_RGBA_ASTC_8x5_KHR = 37813
COMPRESSED_RGBA_ASTC_8x6_KHR = 37814
COMPRESSED_RGBA_ASTC_8x8_KHR = 37815

#Commands
CLKEXT        = 0x44
CLKSEL        = 0x62
ACTIVE        = 0x00
RST_PULSE     = 0x68
PWRDOWN       = 0x43
PWRDOWN2      = 0x50
CMD_DLSTART   = 0xFFFFFF00
DLSWAP_FRAME  = 2

CMD_SIZE      = 0x00000004
CMD_TEXT             = 0xFFFFFF0C #4294967052
CMDBUF_SIZE          = 4096
CMD_APPEND           = 4294967070
CMD_BGCOLOR          = 4294967049
CMD_BITMAP_TRANSFORM = 4294967073
CMD_BUTTON           = 0xFFFFFF0D #4294967053
CMD_CALIBRATE        = 4294967061
CMD_CSKETCH          = 4294967093
CMD_CLOCK            = 4294967060
CMD_COLDSTART        = 4294967090
CMD_CRC              = 4294967043
CMD_DIAL             = 4294967085
CMD_DLSTART          = 4294967040
CMD_EXECUTE          = 4294967047
CMD_FGCOLOR          = 4294967050
CMD_GAUGE            = 4294967059
CMD_GETMATRIX        = 4294967091
CMD_GETPOINT         = 4294967048
CMD_GETPROPS         = 4294967077
CMD_GETPTR           = 4294967075
CMD_GRADCOLOR        = 4294967092
CMD_GRADIENT         = 4294967051
CMD_HAMMERAUX        = 4294967044
CMD_IDCT             = 4294967046
CMD_INFLATE          = 4294967074
CMD_INTERRUPT        = 4294967042
CMD_KEYS             = 0xFFFFFF0E #4294967054
CMD_LOADIDENTITY     = 4294967078
CMD_LOADIMAGE        = 4294967076
CMD_LOGO             = 4294967089
CMD_MARCH            = 4294967045
CMD_MEMCPY           = 4294967069
CMD_MEMCRC           = 4294967064
CMD_MEMSET           = 4294967067
CMD_MEMWRITE         = 4294967066
CMD_MEMZERO          = 4294967068
CMD_NUMBER           = 4294967086
CMD_PROGRESS         = 0xFFFFFF0F #4294967055
CMD_REGREAD          = 4294967065
CMD_RESETFONTS       = 0xFFFFFF52
CMD_ROMFONT          = 4294967103
CMD_ROTATE           = 4294967081
CMD_ROTATEAROUND     = 0xFFFFFF51
CMD_SCALE            = 4294967080
CMD_SCREENSAVER      = 4294967087
CMD_SCROLLBAR        = 4294967057
CMD_SETFONT          = 4294967083
CMD_SETFONT2         = 4294967099
CMD_SETMATRIX        = 4294967082
CMD_SKETCH           = 4294967088
CMD_SLIDER           = 4294967056
CMD_SNAPSHOT         = 4294967071
CMD_SPINNER          = 0xFFFFFF16 #4294967062
CMD_STOP             = 4294967063
CMD_SWAP             = 4294967041
CMD_TEXT             = 4294967052
CMD_TOGGLE           = 4294967058
CMD_TOUCH_TRANSFORM  = 4294967072
CMD_TRACK            = 4294967084
CMD_TRANSLATE        = 4294967079

KEEP                 = 1
L1                   = 1
L4                   = 2
L8                   = 3
LEQUAL               = 2
LESS                 = 1
LINEAR_SAMPLES       = 0
LINES                = 3
LINE_STRIP           = 4
NEAREST              = 0
BILINEAR             = 1
BORDER               = 0
REPEAT              = 1
NEVER                = 0
NOTEQUAL             = 6
ONE                  = 1
ONE_MINUS_DST_ALPHA  = 5
ONE_MINUS_SRC_ALPHA  = 4
OPT_CENTER           = 1536
OPT_CENTERX          = 512
OPT_RIGHTX           = 2048
OPT_LEFTX            = 0
OPT_CENTERY          = 1024
OPT_FILL             = 8192
OPT_3D               = 0
OPT_FLAT             = 256
OPT_MONO             = 1
OPT_NOBACK           = 4096
OPT_NODL             = 2
OPT_NOHANDS          = 49152
OPT_NOHM             = 16384
OPT_NOPOINTER        = 16384
OPT_NOSECS           = 32768
OPT_NOTICKS          = 8192
OPT_RIGHTX           = 2048
OPT_SIGNED           = 256
PALETTED             = 8
FTPOINTS             = 2
RECTS                = 9

#Text Options
OPT_FORMAT    = 4096 
OPT_FLASH     = 64
OPT_FILL      = 8192

#Begin Values
BITMAPS       = 1
POINTS        = 2
LINES         = 3   

#Registers
REG_COPRO_PATCH_PTR     = 0x7162
REG_ID                  = 0x302000  #8 r/o 7Ch Identification register, always reads as 7Ch
REG_FRAMES              = 0x302004  #32 r/o 0 Frame counter, since reset
REG_CLOCK               = 0x302008  #32 r/o 0 Clock cycles, since reset
REG_FREQUENCY           = 0x30200C  #28 r/w 60000000 Main clock frequency (Hz)
REG_RENDERMODE          = 0x302010  #1 r/w 0 Rendering mode: 0 = normal, 1 = single-line
REG_SNAPY               = 0x302014  #11 r/w 0 Scanline select for RENDERMODE 1
REG_SNAPSHOT            = 0x302018  #1 r/w - Trigger for RENDERMODE 1
REG_SNAPFORMAT          = 0x30201C  #6 r/w 20h Pixel format for scanline readout
REG_CPURESET            = 0x302020  #3 r/w 2 Graphics, audio and touch engines reset control. Bit2: audio, bit1: touch, bit0: graphics
REG_TAP_CRC             = 0x302024  #32 r/o - Live video tap crc. Frame CRC is computed every DL SWAP.
REG_TAP_MASK            = 0x302028  #32 r/w FFFFFFFFh Live video tap mask
REG_HCYCLE              = 0x30202C  #12 r/w 224h Horizontal total cycle count
REG_HOFFSET             = 0x302030  #12 r/w 02Bh Horizontal display start offset
REG_HSIZE               = 0x302034  #12 r/w 1E0h Horizontal display pixel count
REG_HSYNC0              = 0x302038  #12 r/w 000h Horizontal sync fall offset
REG_HSYNC1              = 0x30203C  #12 r/w 029h Horizontal sync rise offset
REG_VCYCLE              = 0x302040  #12 r/w 124h Vertical total cycle count
REG_VOFFSET             = 0x302044  #12 r/w 00Ch Vertical display start offset
REG_VSIZE               = 0x302048  #12 r/w 110h Vertical display line count
REG_VSYNC0              = 0x30204C  #10 r/w 000h Vertical sync fall offset
REG_VSYNC1              = 0x302050  #10 r/w 00Ah Vertical sync rise offset
REG_DLSWAP              = 0x302054  #2 r/w 0 Display list swap control
REG_ROTATE              = 0x302058  #3 r/w 0 Screen rotation control. Allow normal/mirrored/inverted for landscape or portrait orientation.
REG_OUTBITS             = 0x30205C  #9 r/w 1B6h/000h Output bit resolution, 3 bits each for R/G/B. Default is 6/6/6 bits for FT810/FT811, and 8/8/8 bits for FT812/FT813 (0b 000 means 8 bits)
REG_DITHER              = 0x302060  #1 r/w 1 Output dither enable
REG_SWIZZLE             = 0x302064  #4 r/w 0 Output RGB signal swizzle
REG_CSPREAD             = 0x302068  #1 r/w 1 Output clock spreading enable
REG_PCLK_POL            = 0x30206C  #1 r/w 0 PCLK polarity: 0 = output on PCLK rising edge, 1 = output on PCLK falling edge
REG_PCLK                = 0x302070  #8 r/w 0 PCLK frequency divider, 0 = disable
REG_TAG_X               = 0x302074  #11 r/w 0 Tag query X coordinate
REG_TAG_Y               = 0x302078  #11 r/w 0 Tag query Y coordinate
REG_TAG                 = 0x30207C  #8 r/o 0 Tag query result
REG_VOL_PB              = 0x302080  #8 r/w FFh Volume for playback
REG_VOL_SOUND           = 0x302084  #8 r/w FFh Volume for synthesizer sound
REG_SOUND               = 0x302088  #16 r/w 0 Sound effect select
REG_PLAY                = 0x30208C  #1 r/w 0h Start effect playback
REG_GPIO_DIR            = 0x302090  #8 r/w 80h Legacy GPIO pin direction, 0 = input , 1 = output
REG_GPIO                = 0x302094  #8 r/w 00h Legacy GPIO read/write
REG_GPIOX_DIR           = 0x302098  #16 r/w 8000h Extended GPIO pin direction, 0 = input , 1 = output
REG_GPIOX               = 0x30209C  #16 r/w 0080h Extended GPIO read/write
REG_INT_FLAGS           = 0x3020A8  #8 r/o 00h Interrupt flags, clear by read
REG_INT_EN              = 0x3020Ac  #1 r/w 0 Global interrupt enable, 1=enable
REG_INT_MASK            = 0x3020B0  #8 r/w FFh Individual interrupt enable, 1=enable
REG_PLAYBACK_START      = 0x3020B4  #20 r/w 0 Audio playback RAM start address
REG_PLAYBACK_LENGTH     = 0x3020B8  #20 r/w 0 Audio playback sample length (bytes)
REG_PLAYBACK_READPTR    = 0x3020BC  #20 r/o - Audio playback current read pointer
REG_PLAYBACK_FREQ       = 0x3020C0  #16 r/w 8000 Audio playback sampling frequency (Hz)
REG_PLAYBACK_FORMAT     = 0x3020C4  #2 r/w 0 Audio playback format
REG_PLAYBACK_LOOP       = 0x3020C8  #1 r/w 0 Audio playback loop enable
REG_PLAYBACK_PLAY       = 0x3020CC  #1 r/w 0 Start audio playback
REG_PWM_HZ              = 0x3020D0  #14 r/w 250 BACKLIGHT PWM output frequency (Hz)
REG_PWM_DUTY            = 0x3020D4  #8 r/w 128 BACKLIGHT PWM output duty cycle 0=0%, 128=100%
REG_MACRO_0             = 0x3020D8  #32 r/w 0 Display list macro command 0
REG_MACRO_1             = 0x3020DC  #32 r/w 0 Display list macro command 1
REG_CMD_READ            = 0x3020F8  #12 r/w 0 Command buffer read pointer
REG_CMD_WRITE           = 0x3020FC  #12 r/o 0 Command buffer write pointer
REG_CMD_DL              = 0x302100  #13 r/w 0 Command display list offset
REG_TOUCH_MODE          = 0x302104  #2 r/w 3 Touch-screen sampling mode
REG_TOUCH_ADC_MODE      = 0x302108  #1 r/w 1 Set Touch ADC mode Set capacitive touch operation mode: 0: extended mode (multi-touch) 1: FT800 compatibility mode (single touch).
REG_CTOUCH_EXTENDED     = REG_TOUCH_ADC_MODE
REG_TOUCH_CHARGE        = 0x30210C  #16 r/w 9000 Touch charge time, units of 6 clocks
REG_TOUCH_SETTLE        = 0x302110  #4 r/w 3 Touch settle time, units of 6 clocks
REG_TOUCH_OVERSAMPLE    = 0x302114  #4 r/w 7 Touch oversample factor
REG_TOUCH_RZTHRESH      = 0x302118  #16 r/w FFFFh Touch resistance threshold
REG_TOUCH_RAW_XY        = 0x30211C  #32 r/o - Compatibility mode: touch-screen raw (x-MSB16; y-LSB16) Extended mode: touch-screen screen data for touch 1 (x-MSB16; y-LSB16)
REG_CTOUCH_TOUCH1_XY    = REG_TOUCH_RAW_XY
REG_TOUCH_RZ            = 0x302120  #16 r/o - Compatibility mode: touch-screen resistance Extended mode: touch-screen screen Y data for touch 4
REG_CTOUCH_TOUCH4_Y     = REG_TOUCH_RZ
REG_TOUCH_SCREEN_XY     = 0x302124  #32 r/o - Compatibility mode: touch-screen screen (x-MSB16; y-LSB16) Extended mode: touch-screen screen data for touch 0 (x-MSB16; y-LSB16)
REG_CTOUCH_TOUCH0_XY    = REG_TOUCH_SCREEN_XY
REG_TOUCH_TAG_XY        = 0x302128  #32 r/o - Touch-screen screen (x-MSB16; yLSB16) used for tag 0 lookup
REG_TOUCH_TAG           = 0x30212C  #8 r/o - Touch-screen tag result 0
REG_TOUCH_TAG1_XY       = 0x302130  #32 r/o - Touch-screen screen (x-MSB16; yLSB16) used for tag 1 lookup
REG_TOUCH_TAG1          = 0x302134  #8 r/o - Touch-screen tag result 1
REG_TOUCH_TAG2_XY       = 0x302138  #32 r/o - Touch-screen screen (x-MSB16; yLSB16) used for tag 2 lookup
REG_TOUCH_TAG2          = 0x30213C  #8 r/o - Touch-screen tag result 2
REG_TOUCH_TAG3_XY       = 0x302140  #32 r/o - Touch-screen screen (x-MSB16; yLSB16) used for tag 3 lookup
REG_TOUCH_TAG3          = 0x302144  #8 r/o - Touch-screen tag result 3
REG_TOUCH_TAG4_XY       = 0x302148  #32 r/o - Touch-screen screen (x-MSB16; yLSB16) used for tag 4 lookup
REG_TOUCH_TAG4          = 0x30214C  #8 r/o - Touch-screen tag result 4
REG_TOUCH_TRANSFORM_A   = 0x302150  #32 r/w 00010000h Touch-screen transform coefficient (s15.16)
REG_TOUCH_TRANSFORM_B   = 0x302154  #32 r/w 00000000h Touch-screen transform coefficient (s15.16)
REG_TOUCH_TRANSFORM_C   = 0x302158  #32 r/w 00000000h Touch-screen transform coefficient (s15.16)
REG_TOUCH_TRANSFORM_D   = 0x30215C  #32 r/w 00000000h Touch-screen transform coefficient (s15.16)
REG_TOUCH_TRANSFORM_E   = 0x302160  #32 r/w 00010000h Touch-screen transform coefficient (s15.16)
REG_TOUCH_TRANSFORM_F   = 0x302164  #32 r/w 00000000h Touch-screen transform coefficient (s15.16)
REG_TOUCH_CONFIG        = 0x302168  #16 r/w 8381h(FT810/FT812) 0381h(FT811/FT813) Touch configuration. RTP/CTP select RTP: short-circuit, sample clocks CTP: I2C address, CTPM type, lowpower mode
REG_CTOUCH_TOUCH4_X     = 0x30216C  #16 r/o - Extended mode: touch-screen screen X data for touch 4
REG_BIST_EN             = 0x302174  #1 r/w 0 BIST memory mapping enable
REG_TRIM                = 0x302180  #8 r/w 0 Internal relaxation clock trimming
REG_ANA_COMP            = 0x302184  #8 r/w 0 Analogue control register
REG_SPI_WIDTH           = 0x302188  #3 r/w 0 QSPI bus width setting Bit [2]: extra dummy cycle on read Bit [1:0]: bus width (0=1-bit, 1=2-bit, 2=4-bit)
REG_TOUCH_DIRECT_XY     = 0x30218C  #32 r/o - Compatibility mode: Touch screen direct (x-MSB16; y-LSB16) conversions Extended mode: touch-screen screen data for touch 2 (x-MSB16; y-LSB16)
REG_CTOUCH_TOUCH2_XY    = REG_TOUCH_DIRECT_XY
REG_TOUCH_DIRECT_Z1Z2   = 0x302190  #32 r/o - Compatibility mode: Touch screen direct (z1-MSB16; z2-LSB16) conversions Extended mode: touch-screen screen data for touch 3 (x-MSB16; y-LSB16)
REG_CTOUCH_TOUCH3_XY    = REG_TOUCH_DIRECT_Z1Z2
REG_DATESTAMP           = 0x302564  #128 r/o - Stamp date code
REG_CMDB_SPACE          = 0x302574  #12 r/w FFCh Command DL (bulk) space available
REG_CMDB_WRITE          = 0x302578  #32 w/o 0 Command DL (bulk) write

#Animation
REG_ANIM_ACTIVE     = 3182636
ANIM_ONCE           = 0
ANIM_LOOP           = 1
ANIM_HOLD           = 2
CMD_ANIMDRAW        = 4294967126
CMD_ANIMFRAME       = 4294967130
CMD_ANIMSTART       = 4294967123
CMD_ANIMSTOP        = 4294967124
CMD_ANIMXY          = 4294967125