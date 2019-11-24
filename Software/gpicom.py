from gpiozero import LED
from time import sleep
red = LED(17)
while True:
    red.on()
    print("This works!!" )
    sleep(1)
    red.off()
    sleep(1)
