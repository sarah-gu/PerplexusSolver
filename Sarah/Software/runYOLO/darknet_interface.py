# import the necessary packages
from gpiozero import LED
from gpiozero import OutputDevice as stepper
from time import sleep
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import subprocess
import os
import imutils
import time
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from yolo_utils import infer_image, show_image
FLAGS = []
# construct the argument parse and parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--video",
                help="path to the (optional) video file")


parser.add_argument('-m', '--model-path',
                        type=str,
                        default='./yolov3-coco/',
                        help='The directory where the model weights and \
                        configuration files are.')

parser.add_argument('-w', '--weights',
                    type=str,
                    default='./yolov3-coco/yolov3.weights',
                    help='Path to the file which contains the weights \
                    for YOLOv3.')

parser.add_argument('-cfg', '--config',
                    type=str,
                    default='./yolov3-coco/yolov3.cfg',
                    help='Path to the configuration file for the YOLOv3 model.')

parser.add_argument('-i', '--image-path',
                    type=str,
                    help='The path to the image file')


parser.add_argument('-vo', '--video-output-path',
                    type=str,
                    default='./output.avi',
                    help='The path of the output video file')

parser.add_argument('-l', '--labels',
                    type=str,
                    default='./yolov3-coco/coco-labels',
                    help='Path to the file having the \
                    labels in a new-line seperated way.')

parser.add_argument('-c', '--confidence',
                    type=float,
                    default=0.5,
                    help='The model will reject boundaries which has a \
                    probabiity less than the confidence value. \
                    default: 0.5')

parser.add_argument('-th', '--threshold',
                    type=float,
                    default=0.3,
                    help='The threshold to use when applying the \
                    Non-Max Suppresion')

parser.add_argument('--download-model',
                    type=bool,
                    default=False,
                    help='Set to True, if the model weights and configurations \
                    are not present on your local machine.')

parser.add_argument('-t', '--show-time',
                    type=bool,
                    default=False,
                    help='Show the time taken to infer each image.')

FLAGS, args = parser.parse_known_args()
labels = open(FLAGS.labels).read().strip().split('\n')
colors = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')

net = cv2.dnn.readNetFromDarknet(FLAGS.config, FLAGS.weights)
    
    # Get the output layer names of the model
layer_names = net.getLayerNames()
layer_names = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]




if FLAGS.image_path is None and FLAGS.video is None:
    print ('Neither path to an image or path to video provided')
    print ('Starting Inference on Webcam')
# vs = cv2.VideoCapture("http://192.168.1.159/live?type=out.mp4") #IPCamera address
#vs = cv2.VideoCapture("http://192.0.0.1/live?type=out.mp4")
    vs = VideoStream(src=0).start()

#vid is saved
else:
#vs = cv2.VideoCapture("https://192.168.12.186/live?type=out.mp4")
    vs = VideoStream(src=0).start() #normal video camera

time.sleep(2.0)

count = 0
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

def show_frame():
    global count, boxes, confidences, classids, idxs
    print(count)
    frame = vs.read() #inference on computer video cam
    #ret, frame = vs.read() #inference on ipCamera
    
    #cv2.imshow("Frame", frame)
    
    #frame = frame[1] if FLAGS.video is None else frame
    
    frame = imutils.resize(frame, width=600)
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    height, width = frame.shape[:2]
    
    if count == 0:
        count += 1
        frame, boxes, confidences, classids, idxs = infer_image(net, layer_names, \
                                                                height, width, frame, colors, labels, FLAGS)

    
    else:
        frame, boxes, confidences, classids, idxs = infer_image(net, layer_names, \
                                                                height, width, frame, colors, labels, FLAGS, boxes, confidences, classids, idxs, infer=False)
        count = (count + 1) % 6
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)


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

sleep(1)
show_frame()

tk.mainloop()
# if we are not using a video file, stop the camera video stream
if FLAGS.video is None:
    vs.stop()

# otherwise, release the camera
else:
    vs.release()

# close all windows
cv2.destroyAllWindows()




