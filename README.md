# Solving the Perplexus with Robot Arms and Computer Vision

This project aims to use a combination of CV and Robotics to advance the understanding of how robots can perform fine-motor skills. It is split into two components - Software and Hardware, and instructions for the setup of both parts can be found below. Sarah primarily works on software while Khushi focuses on Hardware. Each folder contains the code for each portion. 

## Software
### Installation Requirements
To run this project, you will need access to a laptop, an iPhone, and a Raspberry Pi Model 3. <br> 
Laptop configuration: install the programs Python3, OpenCV (for Python), gpiozero, and pigpio. All three can be easily installed with package managers like pip3 or brew install. <br>
Raspberry Pi configuration: If starting from scratch, set up the Raspberry Pi on N00bs and Raspbian. After which, install the gpiozero and pigpio packages – all other programs like Python are covered through the Raspbian installation. In order to make the Raspberry Pi work, you need to go into the configuration panel in settings and enable remote GPIO access. Connect this Raspberry Pi to a wifi network that isn't the school one. <br>
iPhone configuration: Install the app iPCamera by Dominik Seibold from the app store. It costs 0.99 cents, but allows for OpenCV to take in live video feed from your iPhone. View ball_tracking.py to see how this video feed is grabbed. Connect your iPhone to Wifi that isn't the school (or personal hotspot) works best if the Wifi is fast. 

### How to Run
Git clone the 'Software' folder of this repository (Sarah/Software). After the configuration steps above are complete, replace the ipAddress in each of the Python files with the one listed when you open iPCamera on your iPhone. Run each python file with PIGPIO_ADDR=(ip address of your raspberry Pi, which can be found by running hostname -I) python3 (filename.py). 

## Hardware

