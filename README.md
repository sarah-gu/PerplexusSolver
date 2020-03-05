# Solving the Perplexus with Robot Arms and Computer Vision

This project aims to use a combination of CV and Robotics to advance the understanding of how robots can perform fine-motor skills. It is split into two components - Software and Hardware, and instructions for the setup of both parts can be found below. Sarah primarily works on software while Khushi focuses on Hardware. Each folder contains the code for each portion. 

## Software
### Installation Requirements
To run this project, you will need access to a laptop, an iPhone, and a Raspberry Pi Model 3. <br> 
Laptop configuration: install the programs Python3, OpenCV (for Python), gpiozero, and pigpio. All three can be easily installed with package managers like pip3 or brew install. <br>
Raspberry Pi configuration: If starting from scratch, set up the Raspberry Pi on N00bs and Raspbian. After which, install the gpiozero and pigpio packages – all other programs like Python are covered through the Raspbian installation. In order to make the Raspberry Pi work, you need to go into the configuration panel in settings and enable remote GPIO access. Connect this Raspberry Pi to a wifi network that isn't the school one. <br>
iPhone configuration: Install the app iPCamera by Dominik Seibold from the app store. It costs 0.99 cents, but allows for OpenCV to take in live video feed from your iPhone. View ball_tracking.py to see how this video feed is grabbed. If you want to test the code with just the computer video camera, comment out the line linking to the ipCam video stream and replace. Connect your iPhone to Wifi that isn't the school or a personal hotspot. Works best if the connection is fast. <br>

### Info on Darknet

Darknet: For ball detection, darknet contains everything needed for custom training except for the training data. train.txt and test.txt within the custom folder contain links to a folder on the local machine. To replicate, download the training data from this link (). Inside generate.py in the Software folder, change the path file to wherever you would like the weights to be saved. Then run python3 generate.py and move the newly created train.txt and test.txt files to the custom folder inside darknet. To train, run ./train.sh. <br>

However, you do not need to custom train again to replicate this project. Inside the backup folder within darknet, the yolov3-tiny.backup file contains the most up-to-date training weights. In testing the code, view the runYOLO folder and run the run.sh file. This will tell YOLO to classify all the balls within the given video stream. Classification will be put into output.avi. Currently working to integrate this code into the interface.py file. <br>

### How to Run
Git clone the 'Software' folder of this repository (Sarah/Software). After the configuration steps above are complete, replace the ipAddress in each of the Python files with the one listed when you open iPCamera on your iPhone. Run this python file with PIGPIO_ADDR=(ip address of your raspberry Pi, which can be found by running hostname -I) python3 interface.py.  
Currently the interface.py uses a naive LSV masking backend for ball detection, YOLO implementation coming soon. 

## Hardware

