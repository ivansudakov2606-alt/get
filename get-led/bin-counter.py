import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
leds = [16, 12, 25, 17, 23, 22, 24]
GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, 0)
num = 0
sleep_time = 0.2
def dec2bin(value):
    return [int(element) for element in bin (value)[2:].zfill(8)]
    if GPIO.input(up):
        num = num + 1
        print(num, dec2bin(num))
        time.sleep(sleep_time)
        GPIO.output(leds, dec2bin(num))