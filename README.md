# Solving the Perplexus with Robot Arms and Computer Vision

This project aims to use a combination of CV and Robotics to advance the understanding of how robots can perform fine-motor skills. It is split into two components - Software and Hardware, and instructions for the setup of both parts can be found below. Sarah primarily works on software while Khushi focuses on Hardware. Each folder contains the code for each portion. 

## Software
### Installation Requirements
To run this project, you will need access to a laptop, an iPhone, and a Raspberry Pi Model 3. <br> 
Laptop configuration: install the programs Python3, OpenCV (for Python), gpiozero, and pigpio. All three can be easily installed with package managers like pip3 or brew install. <br>
Raspberry Pi configuration: If starting from scratch, set up the Raspberry Pi on N00bs and Raspbian. After which, install the gpiozero and pigpio packages – all other programs like Python are covered through the Raspbian installation. In order to make the Raspberry Pi work, you need to go into the configuration panel in settings and enable remote GPIO access. Connect this Raspberry Pi to a wifi network that isn't the school one. <br>
iPhone configuration: Install the app iPCamera by Dominik Seibold from the app store. It allows for OpenCV to take in live video feed from your iPhone by grabbing from a localhost website and converting to an mp4. View ball_tracking.py to see exactly how this works. If you want to test the code with just your computer video camera, comment out the line linking to the ipCam video stream and replace. Connect your iPhone to Wifi that isn't the school or a personal hotspot. Works best if the connection is fast. Make sure the Raspberry Pi and iPhone are connected to the SAME Wifi. <br>

### Info on Darknet

Darknet: For ball detection, darknet53 contains everything needed for custom training except for the training data. train.txt and test.txt within the 'custom' folder contain links to a folder on the local machine. To replicate, download the training data from this link (). Inside generate.py in the Software folder, change the path file to wherever you would like the weights to be saved. Then run python3 generate.py. To train, navigate to inside the darknet53 folder and run ./train.sh. <br>

##### Notes about Training
I trained on a GeForce RTX 2080 (through https://j26.tjhsst.edu/, TJ's GPU server). I let it train for roughly 200000 iterations and this took around a day. I had around 1600 datapoints in my custom set, with some coming from a home-recorded video and others coming from a Youtube video for variation. When I originally trained with only images from the Youtube Video, the accuracy was great for images coming from that video but horrible for self-taken photos. Some errors I encountered with the GPU included a 'libcudart.so.10.1: cannot open shared object file' error, which was fixed with 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64/:$LD_LIBRARY_PATH' and 'export PATH=/usr/local/cuda/bin/:$PATH' <br>

My data points were obtained by using labelImg and ffmpeg to break up a video into images and then annotate. I firstly used ffmpeg to convert the video into a series of png images. (Command: ffmpeg -i in.mp4 img%04d.png) It was then fairly simple to use labelImg to draw bounding boxes. Save the annotated .txt file in the same folder as the images - darknet will reference this one folder to train the network. labelImg's readme has more info on how to use this program. 

### How to Run
You do not need to custom train again to replicate this project. Git clone the 'Software' folder of this repository (Sarah/Software). Inside the backup folder within darknet, the yolov3-tiny.backup file contains the most up-to-date training weights. In testing the code, view the runYOLO folder and run the interfaceRun.sh file. Before you run, replace the iPCamera address and PIGPIO_ADDR to the ones on your devices. Use the one with (en0) next to it for iPCamera. PIGPIO_ADDR can be found by running hostname -I on the Pi. This classifies using the OpenCV DNN method backend and the weights we custom trained. Change the weights in the interfaceRun.sh file to your own liking.  <br>

For pre-taken videos and testing purposes, run.sh in the same runYOLO directory is helpful. This file tells YOLO to classify all the balls within the video stream you input and doesn't connect to any hardware. Classification is parsed into output.avi. <br>

## Hardware

