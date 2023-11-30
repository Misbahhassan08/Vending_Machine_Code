from RPi import GPIO
import time

clk = 24
dt = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)

clkLastState = GPIO.input(clk)

def _EncoderRotated(pin):
    # int MSB = digitalRead(encoderPinA); //MSB = most significant bit
    # int LSB = digitalRead(encoderPinB); //LSB = least significant bit

    # int encoded = (MSB << 1) |LSB; //converting the 2 pin value to single number
    # int sum  = (lastEncoded << 2) | encoded; //adding it to the previous encoded value

    # if(sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) encoderValue   ;
    # if(sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) encoderValue --;

    # lastEncoded = encoded; //store this value for next time
    #print(pin)
    global PreviousClockState, PreviousDataState
    CurrentClockState = GPIO.input(clk)
    CurrentDataState = GPIO.input(dt)
    prevEncoded = (PreviousClockState << 1) | PreviousDataState
    Encoded = (CurrentClockState << 1) | CurrentDataState
    EncoderSum = (prevEncoded << 2) | Encoded

    motion = "none"
    if(EncoderSum == 0b1101 or EncoderSum == 0b0100 or EncoderSum == 0b0010 or EncoderSum == 0b1011):
        motion = "right"
    if(EncoderSum == 0b1110 or EncoderSum == 0b0111 or EncoderSum == 0b0001 or EncoderSum == 0b1000):
        motion = "left"

    if motion in ["left", "right"]:
        print(motion)
    PreviousClockState = CurrentClockState
    PreviousDataState = CurrentDataState


PreviousClockState = GPIO.input(clk)
PreviousDataState = GPIO.input(dt)
counter = 0
clkLastState = GPIO.input(clk)
GPIO.add_event_detect(clk, GPIO.BOTH, callback=_EncoderRotated)
GPIO.add_event_detect(dt, GPIO.BOTH, callback=_EncoderRotated)
while True:
    #print(GPIO.input(clk), GPIO.input(dt))
    pass
    #time.sleep(1)
GPIO.cleanup()