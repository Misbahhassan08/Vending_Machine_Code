import time
import sys
import RPi.GPIO as GPIO

FlowEmulatorPin = 14
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(FlowEmulatorPin, GPIO.OUT)
try:
    FlowRate = int(sys.argv[1])/1000
except:
    FlowRate = 0.0 #Default to fast flow

print("Ticking every", FlowRate, "seconds!")
while(True):
    GPIO.output(FlowEmulatorPin, 1)
    time.sleep(FlowRate)
    GPIO.output(FlowEmulatorPin, 0)
    time.sleep(0.0001)
