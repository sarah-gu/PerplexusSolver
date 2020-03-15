# import the necessary packages
from gpiozero import LED
from gpiozero import OutputDevice as stepper
from time import sleep
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())


#greenLower = (34,41,136) #silver ball hsv
#greenUpper= (116,255,255)
greenLower = (13,9,0) #silver ball hsv
greenUpper= (179,37,122)
#greenLower = (0,106,226)
#greenUpper= (179,255,255)#orange ball hsv
pts = deque(maxlen=args["buffer"])


if not args.get("video", False):
    #vs = cv2.VideoCapture("http://192.168.12.186/live?type=out.mp4")
#vs = cv2.VideoCapture("http://192.0.0.1/live?type=out.mp4")
    vs = VideoStream(src=0).start()

#vid is saved
else:
#vs = cv2.VideoCapture("https://192.168.12.186/live?type=out.mp4")
    vs = VideoStream(src=0).start()

time.sleep(2.0)


master = tk.Tk()
ret = True

def controlgpio():
#    GPIO.setmode(GPIO.BOARD)
#    control_pins = [7,11,13,15]
    IN1 = stepper(17)
    IN2 = stepper(39)
    IN3 = stepper(20)
    IN4 = stepper(21)
    stepDir  = -1
    mode = 1
    stepPins = [IN1,IN2,IN3,IN4]
    seq = [
                    [1,0,0,0],
                    [1,1,0,0],
                    [0,1,0,0],
                    [0,1,1,0],
                    [0,0,1,0],
                    [0,0,1,1],
                    [0,0,0,1],
                    [1,0,0,1]
                    ]
    stepCount = len(seq)
    stepCounter = 0
    while True:                          # Start main loop
        for pin in range(0,4):
            xPin=stepPins[pin]          # Get GPIO
            if seq[stepCounter][pin]!=0:
                xPin.on()
            else:
                xPin.off()
            stepCounter += stepDir
            if (stepCounter >= stepCount):
                stepCounter = 0
            if (stepCounter < 0):
                stepCounter = stepCount+stepDir
        time.sleep(waitTime)
#    red.off()
def reset():
    print ("to be implemented")

def callback():
    print ("click!")

b = ttk.Button(master, text="OK", command=callback)
gpiobutton = ttk.Button(master, text="Move", command=controlgpio)
reset = ttk.Button(master, text="Reset to Start", command=reset)

imageFrame = ttk.Frame(master, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

b.grid(row = 0, column=1, padx=0, pady=0)
gpiobutton.grid(row=0, column = 2, padx = 0, pady = 0)
reset.grid(row=0, column = 3, padx = 0, pady = 0)
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)
def show_frame():
    ret,frame = vs.read()

    #cv2.imshow("Frame", frame)

    frame = frame[1] if args.get("video", False) else frame

    frame = imutils.resize(frame, width=600)
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:

        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    pts.appendleft(center)
    for i in range(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)
#key = cv2.waitKey(1) & 0xFF

sleep(1)
show_frame()

tk.mainloop()
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()

# otherwise, release the camera
else:
    vs.release()

# close all windows
cv2.destroyAllWindows()




