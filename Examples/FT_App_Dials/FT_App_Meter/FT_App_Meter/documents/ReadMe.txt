; Copyright (c) Future Technology Devices International 2013



; THIS SOFTWARE IS PROVIDED BY FUTURE TECHNOLOGY DEVICES INTERNATIONAL LIMITED ``AS IS'' AND ANY EXPRESS
; OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
; FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL FUTURE TECHNOLOGY DEVICES INTERNATIONAL LIMITED
; BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
; BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
; INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
; (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
; THE POSSIBILITY OF SUCH DAMAGE.



Objective: 
==========
This ReadMe file contains the details of Meter Demo application release package. 

This package contains the FT800 Meter Demo application targeting Windows PC and Arduino platform.  

This application demonstrates interactive Meter Demo using Points,Track & Stencil commands based on FT800 platform.


Release package contents:
=========================
The folder structure is shown as below.


+---Bin
|   \---Msvc_win32
|   	\--libMPSSE.a - MPSSE file.
|   	\--ftd2xx.dll - ftd2xx library file.

+---Docs
+---Hdr
|   \---\FT_CoPro_Cmds.h  - Includes the Coprocessor commands.
|   \---\FT_DataTypes.h - Includes the FT800 datatypes.
|   \---\FT_FontT_Table.h - Includes the font width and height values.
|   \---\FT_Gpu.h - Includes the Gpu commands.
|   \---\FT_Gpu_Hal.h - Includes the Gpu Hal commands.
|   \---\FT_Hal_Utils.h - Inclues the hal utilities.
|   \---\FT_Platform.h - Inclues Platform specific commands.
|   \---\FT_App_MeterDemo.h - The Meter demo header file.
|
|   \---Msvc_win32
|   	\--ftd2xx.h - ftd2xx library file
|   	\--libMPSSE_spi - MPSSE header file
|
+---Project
|   \---Arduino
|   	\---FT_App_MeterDemo
		\---\FT_App_MeterDemo.ino - Main file of Rotary Demo
|   		\---\FT_CoPro_Cmds.h  - Includes the Coprocessor commands.
|		\---\FT_CoPro_Cmds.cpp - Coprocessor commands source code.
|  		\---\FT_DataTypes.h - Includes the FT800 datatypes.
|   		\---\FT_FontT_Table.h - Includes the font width and height values.
|   		\---\FT_Gpu.h - Includes the Gpu commands.
|   		\---\FT_Gpu_Hal.h - Includes the Gpu Hal commands.
|		\---\FT_Gpu_Hal.cpp -Gpu Hal commands source code.	
|   		\---\FT_Hal_Utils.h - Inclues the hal utilities.
|   		\---\FT_Platform.h - Inclues Platform specific commands.
|   		\---\FT_App_MeterDemo.h - The Rotary dial  header file.
|
|   \---Msvc_win32
|       \---FT_App_MeterDemo
|		\---FT_App_MeterDemo.sln– solution file of RotaryDial Demo application
|		\---FT_App_MeterDemo.vcxproj – project file of RotaryDial Demo application
|		\---FT_App_MeterDemo.vcxproj.filters
|		\---FT_App_MeterDemo.vcxproj.user
|
+---Src
|   	\---FT_CoPro_Cmds.c - Coprocessor commands source file.
|   	\---FT_Gpu_Hal.c - Gpu hal source commands file.
|   	\---FT_App_MeterDemo.c - Main file of Meter Demo.
|   	\---FT_App_MeterDemo_RawData.c- Contains the Bitmap properties ann bitmap arrays.
|
+--Test	– folder containing input test files such as .wav, .jpg, .raw etc


Configuration Instructions:
===========================
This section contains details regarding various configurations supported by this software.

Two display profiles are supported by this software: (1) WQVGA (480x272) (2) QVGA (320x240)
Two arduino platforms are supported by this software: (1) VM800P – FTDI specific module (2) Arduino pro

The above two configurations can be enabled/disabled via commenting/uncommenting macors in FT_Platform.h file. For MVSC/PC platform please look into .\FT_App_MeterDemo\Hdr\FT_Platform.h and for arduino platform please look into .\FT_App_MeterDemo\Project\Aurdino\FT_App_MeterDemo\FT_Platform.h

By default WQVGA display profile is enabled. To enable QVGA, uncomment “#define SAMAPP_DISPLAY_QVGA” macro in respective FT_Platform.h file.

For arduino platform please uncomment any one of the macros (1) “#define  FT_ATMEGA_328P” – FTDI specific module (2) “#define ARDUINO_PRO_328” – arduino pro. At any point of time only one macro should be uncommented/enabled.

The Absolute dial can be activated by enabling the following macro "#define Absolute Dial" in FT_Platform.h. This Dial is enabled by default. The Absolute dial works only in Landscape Mode.

The Relative dial can be activated by enabling the following macro  "#define Relative Dial" in FT_Platform.h. The Relative dial works only in Portrait Mode.



Installation Instruction:
=========================

Unzip the package onto a respective project folder and open the solution/sketch file in the project folder and execute it. For MSVC/PC platform please execute .\\FT_App_MeterDemo\Project\Msvc_win32\\FT_App_MeterDemo\\FT_App_MeterDemo.sln solution. For arduino platform please execute.\\FT_App_MeterDemo\Project\Aurdino\\FT_App_MeterDemo\\FT_App_MeterDemo.ino sketch.

The MSVC project file is compatible with Microsoft visual C++ 2010 Express.
The arduino project file is compatible with Arduino 1.0.5.
For arduino platform copy the files under TEST folder to SD card.


Reference Information:
======================
Please refer to AN_FT_App_MeterDemo for more information on application design, setup etc.
Please refer to FT800_Programmer_Guide for more information on programming FT800.

Known Limitations/issues:
=========================
1. This application contains only SPI interface to FT800.
2. The SPI host(Arduino, Windows PC) are assuming the data layout in memory as Little Endian format. 



Extra Information:
==================
N.A


Release Notes (Version Significance):
=====================================
Version 1.0 - Final version based on the requirements.
Version 0.1 - intial draft of the release notes



