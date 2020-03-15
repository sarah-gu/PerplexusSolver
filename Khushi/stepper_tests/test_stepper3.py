from time import sleep
import RPi.GPIO as GPIO

DIR = 20
STEP = 21
CW = 1
CCW = 0
SPR = 100

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

step_count = SPR
delay = .001*2

for x in range(step_count):
  GPIO.output(STEP, GPIO.HIGH)
  sleep(delay)
  GPIO.output(STEP, GPIO.LOW)
  sleep(delay)

sleep(.5)
GPIO.output(DIR, CCW)

for x in range(step_count):
  GPIO.output(STEP, GPIO.HIGH)
  sleep(delay)
  GPIO.output(STEP, GPIO.LOW)
  sleep(delay)
