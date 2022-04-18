import RPi.GPIO as GPIO
import time

def detect_human():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN)
    while(1):
        if GPIO.input(18) == True:
            print("hello!")
        else:
            print("nobody!")
            break
        time.sleep(1)