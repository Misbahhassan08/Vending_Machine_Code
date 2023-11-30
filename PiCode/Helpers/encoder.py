# import threading
# import time
# from datetime import datetime
# import RPi.GPIO as GPIO
# import Helpers.logger as logger
# import Helpers.GlobalFunctions as s
# # Mechanical Encoder
# #Theory of operation https://www.best-microcontroller-projects.com/rotary-encoder.html
# class Encoder(threading.Thread):
#     def __init__(self, Enc_A, Enc_B, Enc_C, NavigatorCallback):
#         try:
#             threading.Thread.__init__(self)
#             self.daemon = True
#             self._NavigatorCallback = NavigatorCallback
#             self._CLK = Enc_A
#             self._DATA = Enc_B
#             self._PushButtonPin = Enc_C
#             self._LastEncoderState = None
#             self._DownStarted = False
#             self._prevNextCode = 0x00 #8bit
#             self._store = 0x0000 #16bit
#             GPIO.setwarnings(True)
#             # Use the Raspberry Pi BCM pins
#             GPIO.setmode(GPIO.BCM)
#             # define the Encoder switch inputs
#             GPIO.setup(self._CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#             GPIO.setup(self._DATA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#             GPIO.setup(self._PushButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#             self.start()
#         except Exception as e:
#             #print(e)
#             logger.error(e)
#     def run(self):
#         self._LastEncoderState = GPIO.input(self._CLK)
#         s.SetThreadName("BrewEncoderDown")
#         GPIO.add_event_detect(self._PushButtonPin, GPIO.FALLING, callback=self._ButtonPress) # bouncetime in mSec
#         s.SetThreadName("BrewEncoder")
#         while(True):
#             time.sleep(0.001)
#             self._DetectIO()
#     def _ButtonPress(self, pin):
#         if(self._DownStarted):
#             return
#         DownTime = datetime.now()
#         time.sleep(0.01)
#         if(GPIO.input(pin) == 0):
#             self._NavigatorCallback("Down")
#         while(GPIO.input(pin) == 0):
#             time.sleep(0)
#         TotalDownTime = (datetime.now() - DownTime).total_seconds()
#         if(TotalDownTime < 2):
#             self._NavigatorCallback("Up")
#         elif(TotalDownTime <= 5):
#             self._NavigatorCallback("LongPress")
#         elif(TotalDownTime > 5):
#             self._NavigatorCallback("VeryLongPress")
#         self._DownStarted = False
#     def _DetectIO(self):
#         if(self._read_rotary() != 0):
#             if(self._prevNextCode == 0x0b):
#                 self._NavigatorCallback("Left")
#             if(self._prevNextCode == 0x07):
#                 self._NavigatorCallback("Right")
#     # A vald CW or  CCW move returns 1, invalid returns 0.
#     def _read_rotary(self):
#         rot_enc_table = [0x00, 0x01, 0x01, 0x00, 0x01, 0x00, 0x00, 0x01, 0x01, 0x00, 0x00, 0x01, 0x00, 0x01, 0x01, 0x00]
#         self._prevNextCode = self._prevNextCode << 2
#         if(GPIO.input(self._DATA)):
#             self._prevNextCode |= 0x02
#         if(GPIO.input(self._CLK)):
#             self._prevNextCode |= 0x01
#         self._prevNextCode &= 0x0F
#         # If valid then store as 16 bit data.
#         if(rot_enc_table[self._prevNextCode]):
#             self._store = (self._store << 4) & 0xFF
#             self._store |= self._prevNextCode
#         if ((self._store&0xff) == 0x2b):
#             return -1
#         if ((self._store&0xff) == 0x17):
#             return 1
#         return 0x00



# Optical Encoder Code
import threading
import time
from datetime import datetime
import RPi.GPIO as GPIO
import Helpers.logger as logger
import Helpers.GlobalFunctions as s

#Theory of operation https://www.best-microcontroller-projects.com/rotary-encoder.html
class Encoder(threading.Thread):
    def __init__(self, Enc_A, Enc_B, Enc_C, NavigatorCallback):
        try:
            threading.Thread.__init__(self)
            self.daemon = True
            self._NavigatorCallback = NavigatorCallback
            self._CLK = Enc_A
            self._DATA = Enc_B
            self._PushButtonPin = Enc_C
            self._LastEncoderState = None
            self._DownStarted = False
            self._PreviousClockState = 0
            self._PreviousDataState = 0
            self._prevNextCode = 0x00 #8bit
            self._store = 0x0000 #16bit
            GPIO.setwarnings(True)
            # Use the Raspberry Pi BCM pins
            GPIO.setmode(GPIO.BCM)
            # define the Encoder switch inputs
            GPIO.setup(self._CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self._DATA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self._PushButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.start()
        except Exception as e:
            #print(e)
            logger.error(e)
    def run(self):
        self._LastEncoderState = GPIO.input(self._CLK)
        s.SetThreadName("BrewEncoderDown")
        GPIO.add_event_detect(self._PushButtonPin, GPIO.FALLING, callback=self._ButtonPress) # bouncetime in mSec
        s.SetThreadName("BrewEncoder")
        self._PreviousClockState = GPIO.input(self._CLK)
        self._PreviousDataState = GPIO.input(self._DATA)
        s.SetThreadName("BrewEncoderRotate")
        GPIO.add_event_detect(self._CLK, GPIO.BOTH, callback=self._EncoderRotated)
        GPIO.add_event_detect(self._DATA, GPIO.BOTH, callback=self._EncoderRotated)
        s.SetThreadName("BrewEncoder")
        while(True):
            time.sleep(1)
    def _EncoderRotated(self, _):
        CurrentClockState = GPIO.input(self._CLK)
        CurrentDataState = GPIO.input(self._DATA)

        prevEncoded = (self._PreviousClockState << 1) | self._PreviousDataState
        Encoded = (CurrentClockState << 1) | CurrentDataState
        EncoderSum = (prevEncoded << 2) | Encoded
        if(EncoderSum == 0b1101 or EncoderSum == 0b0100 or EncoderSum == 0b0010 or EncoderSum == 0b1011):
            self._NavigatorCallback("Right")
        if(EncoderSum == 0b1110 or EncoderSum == 0b0111 or EncoderSum == 0b0001 or EncoderSum == 0b1000):
            self._NavigatorCallback("Left")
        self._PreviousClockState = GPIO.input(self._CLK)
        self._PreviousDataState = GPIO.input(self._DATA)
    def _ButtonPress(self, pin):
        if(self._DownStarted):
            return
        DownTime = datetime.now()
        time.sleep(0.01)
        if(GPIO.input(pin) == 0):
            self._NavigatorCallback("Down")
        while(GPIO.input(pin) == 0):
            time.sleep(0)
        TotalDownTime = (datetime.now() - DownTime).total_seconds()
        if(TotalDownTime < 2):
            self._NavigatorCallback("Up")
        elif(TotalDownTime <= 5):
            self._NavigatorCallback("LongPress")
        elif(TotalDownTime > 5):
            self._NavigatorCallback("VeryLongPress")
        self._DownStarted = False
