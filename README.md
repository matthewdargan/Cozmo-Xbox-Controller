# Cozmo Xbox Controller Interface
## Overview
This is a Python project that allows a user to connect either an Xbox 360 or Xbox One controller to a computer and control a Cozmo robot
using that controller via the Cozmo SDK mode from a compatible mobile device.

## Installation
To run this project:

1. Clone this repository from the terminal with `git clone https://github.com/matthewdargan/Cozmo-Xbox-Controller.git` or download it into a zip file by clicking:
[link](https://github.com/matthewdargan/Cozmo-Xbox-Controller/archive/master.zip)
2. Navigate to the directory where you cloned the repo or unzipped the repository.
3. Install the required dependencies with `pip install -r requirements.txt`.
4. Execute `python linux_scripts/cozmo_interface.py` for the Linux version or `python windows_scripts/xbox_controller.py` for the windows version from the terminal to establish a connect to the robot from your mobile device and begin using the controller.

**Note: You must install [Xboxdrv](https://github.com/xboxdrv/xboxdrv) in order to use an Xbox 360 controller on a Linux device; however, Windows devices do not require any 3rd party driver. The Linux driver only supports Xbox 360 controller but the Windows driver supports both Xbox 360 and Xbox One controllers (wired or wireless).**

## Dependencies
* [Xbox Controller Module for Linux](https://github.com/FRC4564/Xbox)
* [Xboxdrv - for Linux based systems](https://github.com/xboxdrv/xboxdrv)
* [Cozmo SDK](http://cozmosdk.anki.com/docs/)
