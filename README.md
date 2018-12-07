# Autonomous Electric Wheelchair
Computer vision has many applications in robotics. This project aim to use computer vision as a feedback loop for an electric wheelchair . Allowing it to navigate the indoor enviroment.

## Dependencies
This project is based largely on interfacing with a physcial hardware, such as motor, relays, etc. As a result a list of hardware dependencies has also been included.

### Software Dependencies

For manual control via web browser the following dependencies are required;
* OpenCV-4.0.0-alpha (https://github.com/opencv)
* OpenKinect Library (https://github.com/OpenKinect/libfreenect)
* MJPG Streamer (https://github.com/jacksonliam/mjpg-streamer)
* Apache 

For autonomous navigation the above dependencies and the follow are requird;
* Anaconda Python Platform (https://anaconda.com) with the following packages installed
* Numpy `conda install -c anaconda numpy` 
* Opencv `conda install -c conda-forge opencv`
* Matlibplot `conda install -c conda-forge matplotlib`
* pip `conda install pip`
* imutils `pip install imutils`

### Hardware Dependencies
* Arduino MEGA
* RaspberryPi 3
* Microsoft Kinect V1 (Note that the V2 Kinect Sensor requires USB 3.0 Support)
* Pololu G2 H-Bridge [Motor Driver](https://www.pololu.com/product/2995) (24v21)  

## Installation

1. Installation of Apache (Any web-server will do, but I prefer Apache) iincluding PHP. This guide from howtoraspberrypi is helpful for beginners (https://howtoraspberrypi.com/how-to-install-web-server-raspberry-pi-lamp/).
1. Build and Install OpenCV. I used `4.0.0-alpha`. However, you can use the most up to date version. This tutorial will get you started at [pyimagesearch](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/)
1. Clon, Build and Install the OpenKinect library. [Here](https://naman5.wordpress.com/2014/06/24/experimenting-with-kinect-using-opencv-python-and-open-kinect-libfreenect/) is a great tutorial for doing just that.

## Acknowledgents
* Queen's University Belfast
* PyImageSearch

## Copyright
This source code is copyright, All rights reserved, Ryan McCartney, 2018