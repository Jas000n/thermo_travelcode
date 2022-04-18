import RPi.GPIO as GPIO
import time

factor = 3
IN1 = 19
IN2 = 26


def move(bias):
    if (bias > 0.5):
        # 此时人脸在摄像头偏右边的位置，需要向左移
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(IN1, GPIO.OUT)
        GPIO.setup(IN2, GPIO.OUT)
        GPIO.output(IN1, True)
        GPIO.output(IN2, False)
        time.sleep(factor * (bias - 0.5))
        GPIO.cleanup()
    else:
        # 此时人脸在摄像头偏左边的位置，需要向右移
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(IN1, GPIO.OUT)
        GPIO.setup(IN2, GPIO.OUT)
        GPIO.output(IN1, False)
        GPIO.output(IN2, True)
        time.sleep(factor * (0.5 - bias))
        GPIO.cleanup()
