# Raspberry camera controller

Here you can find a Web Server developed to run in a [Raspberry Pi 3 B+]. The server has been made to manage the [Camera module v2].

# System setup

## Operative system

For the development of the Web Server I used the following operative system, **[Raspbian Buster with desktop and recommended software]**

To burn the image in the SD I used [Raspberry Pi Imager]

The latest version of this operative system already comes with Python 2.7 and Python 3.7, here we will use Python 3.7

When first start the OS, is good to update the packages running:

`sudo apt-get update`

## Activate camera

The server has been made to manage the [Camera module v2], here you can find the [instructions to enable it].

## VNC Remote access

To make the access and control of the Raspberry easier we can use a VNC Viewer from your PC. Follow the instructions here [VNC Viewer instructions].

## Python environment

This server is developed using Python 3.7 that comes with the Raspbian OS.

### pip package manager

To update the pip package manager we run

`pip3 install -U pip`

To properly use pip3 in Raspbian is better to run it using

`python3 -m pip`

You can check the installed version running

`python3 -m pip -V`

### pipenv environment manager

To easily install the packages [pipenv] has been used.

To install it run

`python3 -m pip install pipenv`

To properly use [pipenv] in Raspbian we need to execute it as follow

`python3 -m pipenv`


[Raspberry Pi 3 B+]: https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/
[Camera module v2]: https://www.raspberrypi.org/products/camera-module-v2/
[instructions to enable it]: https://www.raspberrypi.org/documentation/usage/camera/
[Raspbian Buster with desktop and recommended software]: https://www.raspberrypi.org/downloads/raspbian/
[Raspberry Pi Imager]: https://www.raspberrypi.org/downloads/
[VNC Viewer instructions]: https://www.raspberrypi.org/documentation/remote-access/vnc/
[pipenv]: https://pipenv-es.readthedocs.io/
