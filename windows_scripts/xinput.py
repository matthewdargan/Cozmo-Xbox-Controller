#!/usr/bin/env python

"""
https://github.com/r4dian/Xbox-360-Controller-for-Python/blob/master/xinput.py
A module for getting input from Microsoft XBox 360 controllers via the XInput library on Windows.

Adapted from Jason R. Coombs' code here:
http://pydoc.net/Python/jaraco.input/1.0.1/jaraco.input.win32.xinput/
under the MIT licence terms

Upgraded to Python 3
Modified to add dead zones, reduce noise, and support vibration
"""

import ctypes
import sys
import time
from operator import attrgetter

# structs according to
# http://msdn.microsoft.com/en-gb/library/windows/desktop/ee417001%28v=vs.85%29.aspx


class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ('buttons', ctypes.c_ushort),  # wButtons
        ('left_trigger', ctypes.c_ubyte),  # bLeftTrigger
        ('right_trigger', ctypes.c_ubyte),  # bLeftTrigger
        ('l_thumb_x', ctypes.c_short),  # sThumbLX
        ('l_thumb_y', ctypes.c_short),  # sThumbLY
        ('r_thumb_x', ctypes.c_short),  # sThumbRx
        ('r_thumb_y', ctypes.c_short),  # sThumbRy
    ]


class XINPUT_STATE(ctypes.Structure):
    _fields_ = [
        ('packet_number', ctypes.c_ulong),  # dwPacketNumber
        ('gamepad', XINPUT_GAMEPAD),  # Gamepad
    ]


class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                ("wRightMotorSpeed", ctypes.c_ushort)]

class XINPUT_BATTERY_INFORMATION(ctypes.Structure):
    _fields_ = [("BatteryType", ctypes.c_ubyte),
                ("BatteryLevel", ctypes.c_ubyte)]

xinput = ctypes.windll.xinput1_4
#xinput = ctypes.windll.xinput9_1_0  # this is the Win 8 version ?
# xinput1_2, xinput1_1 (32-bit Vista SP1)
# xinput1_3 (64-bit Vista SP1)


def struct_dict(struct):
    """
    take a ctypes.Structure and return its field/value pairs
    as a dict.
    """
    get_pair = lambda field_type: (
        field_type[0], getattr(struct, field_type[0]))
    return dict(list(map(get_pair, struct._fields_)))


ERROR_DEVICE_NOT_CONNECTED = 1167
ERROR_SUCCESS = 0


class XInputJoystick:
    """
    XInputJoystick
    Example:
    controller_one = XInputJoystick(0)
    """

    max_devices = 4  # maximum number of connected devices

    def __init__(self, device_number):
        self.device_number = device_number
        self._last_state = self.get_state()

    def get_state(self):
        """Get the state of the controller represented by this object"""
        state = XINPUT_STATE()
        res = xinput.XInputGetState(self.device_number, ctypes.byref(state))
        if res == ERROR_SUCCESS:
            self._last_state = struct_dict(state.gamepad)
            return self._last_state
        if res != ERROR_DEVICE_NOT_CONNECTED:
            self._last_state = None
            raise RuntimeError(
                "Unknown error %d attempting to get state of device %d" % (res, self.device_number))

    def is_connected(self):
        return self._last_state is not None

    @staticmethod
    def enumerate_devices():
        """Returns the devices that are connected"""
        devices = list(
            map(XInputJoystick, list(range(XInputJoystick.max_devices))))
        return [device for device in devices if device.is_connected()]

    def set_vibration(self, left_motor, right_motor):
        """Control the speed of both motors separately"""
        # Set up function argument types and return type
        XInputSetState = xinput.XInputSetState
        XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUT_VIBRATION)]
        XInputSetState.restype = ctypes.c_uint

        vibration = XINPUT_VIBRATION(int(left_motor * 65535), int(right_motor * 65535))
        XInputSetState(self.device_number, ctypes.byref(vibration))

    def get_battery_information(self):
        """Get battery type & charge level"""
        BATTERY_DEVTYPE_GAMEPAD = 0x00
        BATTERY_DEVTYPE_HEADSET = 0x01
        # Set up function argument types and return type
        XInputGetBatteryInformation = xinput.XInputGetBatteryInformation
        XInputGetBatteryInformation.argtypes = [ctypes.c_uint, ctypes.c_ubyte, ctypes.POINTER(XINPUT_BATTERY_INFORMATION)]
        XInputGetBatteryInformation.restype = ctypes.c_uint 

        battery = XINPUT_BATTERY_INFORMATION(0,0)
        XInputGetBatteryInformation(self.device_number, BATTERY_DEVTYPE_GAMEPAD, ctypes.byref(battery))

        #define BATTERY_TYPE_DISCONNECTED       0x00
        #define BATTERY_TYPE_WIRED              0x01
        #define BATTERY_TYPE_ALKALINE           0x02
        #define BATTERY_TYPE_NIMH               0x03
        #define BATTERY_TYPE_UNKNOWN            0xFF
        #define BATTERY_LEVEL_EMPTY             0x00
        #define BATTERY_LEVEL_LOW               0x01
        #define BATTERY_LEVEL_MEDIUM            0x02
        #define BATTERY_LEVEL_FULL              0x03
        battery_type = "Unknown" if battery.BatteryType == 0xFF \
            else ["Disconnected", "Wired", "Alkaline", "Nimh"][battery.BatteryType]
        level = ["Empty", "Low", "Medium", "Full"][battery.BatteryLevel]
        return battery_type, level


"""
* Bitmasks for the joysticks buttons, determines what has
* been pressed on the joystick, these need to be mapped
* to whatever device you're using instead of an xbox 360
* joystick
"""

GAMEPAD_DPAD_UP          = 0x0001
GAMEPAD_DPAD_DOWN        = 0x0002
GAMEPAD_DPAD_LEFT        = 0x0004
GAMEPAD_DPAD_RIGHT       = 0x0008
GAMEPAD_START            = 0x0010
GAMEPAD_BACK             = 0x0020
GAMEPAD_LEFT_THUMB       = 0x0040
GAMEPAD_RIGHT_THUMB      = 0x0080
GAMEPAD_LEFT_SHOULDER    = 0x0100
GAMEPAD_RIGHT_SHOULDER   = 0x0200
GAMEPAD_LEFT_BUMBER      = GAMEPAD_LEFT_SHOULDER
GAMEPAD_RIGHT_BUMBER     = GAMEPAD_RIGHT_SHOULDER
GAMEPAD_A                = 0x1000
GAMEPAD_B                = 0x2000
GAMEPAD_X                = 0x4000
GAMEPAD_Y                = 0x8000

"""
 * Defines the flags used to determine if the user is pushing
 * down on a button, not holding a button, etc
"""

KEYSTROKE_KEYDOWN        = 0x0001
KEYSTROKE_KEYUP          = 0x0002
KEYSTROKE_REPEAT         = 0x0004

"""
 * Defines the codes which are returned by XInputGetKeystroke
"""

VK_PAD_A                        = 0x5800
VK_PAD_B                        = 0x5801
VK_PAD_X                        = 0x5802
VK_PAD_Y                        = 0x5803
VK_PAD_RSHOULDER                = 0x5804
VK_PAD_LSHOULDER                = 0x5805
VK_PAD_LTRIGGER                 = 0x5806
VK_PAD_RTRIGGER                 = 0x5807
VK_PAD_DPAD_UP                  = 0x5810
VK_PAD_DPAD_DOWN                = 0x5811
VK_PAD_DPAD_LEFT                = 0x5812
VK_PAD_DPAD_RIGHT               = 0x5813
VK_PAD_START                    = 0x5814
VK_PAD_BACK                     = 0x5815
VK_PAD_LTHUMB_PRESS             = 0x5816
VK_PAD_RTHUMB_PRESS             = 0x5817
VK_PAD_LTHUMB_UP                = 0x5820
VK_PAD_LTHUMB_DOWN              = 0x5821
VK_PAD_LTHUMB_RIGHT             = 0x5822
VK_PAD_LTHUMB_LEFT              = 0x5823
VK_PAD_LTHUMB_UPLEFT            = 0x5824
VK_PAD_LTHUMB_UPRIGHT           = 0x5825
VK_PAD_LTHUMB_DOWNRIGHT         = 0x5826
VK_PAD_LTHUMB_DOWNLEFT          = 0x5827
VK_PAD_RTHUMB_UP                = 0x5830
VK_PAD_RTHUMB_DOWN              = 0x5831
VK_PAD_RTHUMB_RIGHT             = 0x5832
VK_PAD_RTHUMB_LEFT              = 0x5833
VK_PAD_RTHUMB_UPLEFT            = 0x5834
VK_PAD_RTHUMB_UPRIGHT           = 0x5835
VK_PAD_RTHUMB_DOWNRIGHT         = 0x5836
VK_PAD_RTHUMB_DOWNLEFT          = 0x5837

"""
 * Deadzones are for analogue joystick controls on the joypad
 * which determine when input should be assumed to be in the
 * middle of the pad. This is a threshold to stop a joypad
 * controlling the game when the player isn't touching the
 * controls.
"""

GAMEPAD_LEFT_THUMB_DEADZONE  = 7849
GAMEPAD_RIGHT_THUMB_DEADZONE = 8689
GAMEPAD_THUMB_MAX            = 32767
GAMEPAD_TRIGGER_THRESHOLD    = 30


"""
 * Defines what type of abilities the type of joystick has
 * DEVTYPE_GAMEPAD is available for all joysticks, however
 * there may be more specific identifiers for other joysticks
 * which are being used.
"""

DEVTYPE_GAMEPAD          = 0x01
DEVSUBTYPE_GAMEPAD       = 0x01
DEVSUBTYPE_WHEEL         = 0x02
DEVSUBTYPE_ARCADE_STICK  = 0x03
DEVSUBTYPE_FLIGHT_SICK   = 0x04
DEVSUBTYPE_DANCE_PAD     = 0x05
DEVSUBTYPE_GUITAR        = 0x06
DEVSUBTYPE_DRUM_KIT      = 0x08

"""
 * These are used with the XInputGetCapabilities function to
 * determine the abilities to the joystick which has been
 * plugged in.
"""

CAPS_VOICE_SUPPORTED     = 0x0004
FLAG_GAMEPAD             = 0x00000001

"""
 * Defines the status of the battery if one is used in the
 * attached joystick. The first two define if the joystick
 * supports a battery. Disconnected means that the joystick
 * isn't connected. Wired shows that the joystick is a wired
 * joystick.
"""

BATTERY_DEVTYPE_GAMEPAD         = 0x00
BATTERY_DEVTYPE_HEADSET         = 0x01
BATTERY_TYPE_DISCONNECTED       = 0x00
BATTERY_TYPE_WIRED              = 0x01
BATTERY_TYPE_ALKALINE           = 0x02
BATTERY_TYPE_NIMH               = 0x03
BATTERY_TYPE_UNKNOWN            = 0xFF
BATTERY_LEVEL_EMPTY             = 0x00
BATTERY_LEVEL_LOW               = 0x01
BATTERY_LEVEL_MEDIUM            = 0x02
BATTERY_LEVEL_FULL              = 0x03

"""
 * How many joysticks can be used with this library. Games that
 * use the xinput library will not go over this number.
"""

XUSER_MAX_COUNT                 = 4
XUSER_INDEX_ANY                 = 0x000000FF

CAPS_FFB_SUPPORTED              = 0x0001


def example():
    """
    Grab 1st available gamepad, logging changes to the screen.
    L & R analogue triggers set the vibration motor speed.
    """
    joysticks = XInputJoystick.enumerate_devices()
    device_numbers = list(map(attrgetter('device_number'), joysticks))

    print('found %d devices: %s' % (len(joysticks), device_numbers))

    if not joysticks:
        sys.exit(0)

    j = joysticks[0]
    print('using %d' % j.device_number)

    battery = j.get_battery_information()
    print(battery)

    while True:
        state = j.get_state()
        print(state)
        time.sleep(.01)


if __name__ == "__main__":
    example()

