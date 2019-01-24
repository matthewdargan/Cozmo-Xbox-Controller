# Cozmo Xbox Controller Interface
## Overview
This is a Python project that allows a user to connect an Xbox 360 controller to a computer and control a Cozmo robot
using that controller via the Cozmo SDK mode from a compatible mobile device.

## Installation
To run this project:

1. Clone this repository from the terminal with `git clone https://github.com/matthewdargan/Cozmo-Xbox-Controller.git` or download it into a zip file by clicking:
[link](https://github.com/matthewdargan/Cozmo-Xbox-Controller/archive/master.zip)
2. Navigate to the directory where you cloned the repo or unzipped the repository.
3. Install the required dependencies with `pip install -r requirements.txt`.
4. Execute `python CozmoInterface.py` from the terminal to establish a connect to the robot from your mobile device and begin using the controller.

**Note: You must install [Xboxdrv](https://github.com/xboxdrv/xboxdrv) in order to use an Xbox 360 controller on a Linux device; however, Windows devices do not require any 3rd party driver.**

## Dependencies
* [Xbox Controller Module](https://github.com/martinohanlon/XboxController)
* [Pygame](https://www.pygame.org/wiki/GettingStarted)
* [Xboxdrv - for Linux based systems](https://github.com/xboxdrv/xboxdrv)
