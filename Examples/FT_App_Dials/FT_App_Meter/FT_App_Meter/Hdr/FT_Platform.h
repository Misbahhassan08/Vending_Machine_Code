#ifndef _FT_PLATFORM_H_
#define _FT_PLATFORM_H_

//#define ARDUINO_PLATFORM
#define MSVC_PLATFORM

#define SAMAPP_DISPLAY_WQVGA 1
//#define SAMAPP_DISPLAY_QVGA	 1

#define Absolute Dial
//#define Relative Dial

#ifdef  ARDUINO_PLATFORM
#define FT800_INT (3)
#define FT800_PD_N (4)
#define FT_ARDUINO_PRO_SPI_CS (10)
#define ARDUINO_PLATFORM_SPI
#define ARDUINO_PLATFORM_COCMD_BURST
#endif

#ifdef ARDUINO_PLATFORM
#include <stdio.h>
#include <Arduino.h>
#include <EEPROM.h>
#include <SPI.h>
#include <avr/pgmspace.h>
#endif

#ifdef MSVC_PLATFORM
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <Windows.h>

#include "ftd2xx.h"
#include "LibMPSSE_spi.h"
#endif


#include "FT_DataTypes.h"
#include "FT_Gpu_Hal.h"
#include "FT_Gpu.h"
#include "FT_CoPro_Cmds.h"



#ifdef MSVC_PLATFORM
#define BUFFER_OPTIMIZATION
#define MSVC_PLATFORM_SPI

#define SAMAPP_ENABLE_ROTARY_DEMO
#endif

#ifdef ARDUINO_PLATFORM
/* Compile time switch for enabling sample app api sets - please cross check the same in SampleApp_RawData.cpp file as well */


#define SAMAPP_ENABLE_ROTARY_DEMO

#endif
#endif /*_FT_PLATFORM_H_*/
/* Nothing beyond this*/




