""" Xbox 360 controller interface for cozmo
Authors: Matthew Dargan, Daniel Stutz
"""

import cozmo
from cozmo.util import degrees

import xbox
from colors import Colors


def cozmo_program(robot: cozmo.robot.Robot):
    """
    Main function controlling the state of cozmo based on the Xbox controller inputs.

    :param robot: cozmo robot object
    """

    joy = xbox.Joystick()

    # continous loop that checks for Xbox controller input until we are done with the program
    # Note: Xbox home button will be used to terminate
    while joy.connected():
        # refresh the Xbox inputs from the driver
        joy.refresh()

        y = joy.leftY()  # get y-axis input from left stick before if statements
        x = joy.rightX()  # get x-axis input from left stick before if statements
        left_trigger = joy.leftTrigger()  # get scalar for the left trigger
        right_trigger = -joy.rightTrigger()  # get scalar for the right trigger and negate it

        if joy.Guide():
            # close the Xbox python interface program
            joy.close()
            robot.say_text("I am done with this program.").wait_for_completed()
            exit()

        elif y:
            # double the speed if the left bumper is pressed
            if joy.leftBumper():
                cozmo_movement(robot, scalar=y, speed=300)
            else:
                cozmo_movement(robot, scalar=y)

        elif x:
            # double the rotational speed if the right bumper is pressed
            # TODO: we have to figure out how to speed the treads to turn
            if joy.rightBumper():
                cozmo_rotate(robot, scalar=x, speed=350)
            else:
                cozmo_rotate(robot, scalar=x)

        elif left_trigger:
            # move the lift height up by some scalar asynchronously
            robot.set_lift_height(left_trigger)

        elif right_trigger:
            # move the lift height down by some scalar asynchronously
            robot.set_lift_height(right_trigger)

        elif joy.A():
            # woof
            robot.play_anim(name="anim_petdetection_dog_01").wait_for_completed()

        elif joy.B():
            # bark
            robot.play_anim(name="anim_petdetection_dog_02").wait_for_completed()

        elif joy.X():
            # dog 3
            robot.play_anim(name="anim_petdetection_dog_03").wait_for_completed()

        elif joy.Y():
            # good boy
            robot.play_anim(name="anim_petdetection_dog_04").wait_for_completed()

        elif joy.dpadUp():
            robot.set_backpack_lights_off()

        elif joy.dpadDown():
            robot.set_all_backpack_lights(Colors.BLUE)

        elif joy.dpadLeft():
            robot.set_all_backpack_lights(Colors.RED)

        elif joy.dpadRight():
            robot.set_all_backpack_lights(Colors.GREEN)

        elif joy.Back():
            robot.say_text("Beep beep beep!")

        elif joy.Start():
            robot.say_text("You're a legend!")


def cozmo_movement(robot: cozmo.robot.Robot, scalar, speed=150):
    """
    Asynchronous wrapper function that moves cozmo linearly.

    :param robot: cozmo robot object
    :param scalar: scalar of distance to move cozmo
    :param speed: speed that cozmo should move at
    """

    # TODO: Change speed parameter to do some cool scalar math
    robot.drive_straight(cozmo.util.distance_mm(scalar), cozmo.util.speed_mmps(speed))


def cozmo_rotate(robot: cozmo.robot.Robot, scalar, speed=175):
    """
    Asynchronous wrapper function that rotates cozmo.

    :param robot: cozmo robot object
    :param scalar: angle that cozmo should rotate
    :param speed: speed that cozmo should rotate at
    """

    # TODO: Change speed parameter to do some cool scalar math
    robot.turn_in_place(angle=scalar, num_retries=2, speed=degrees(speed))


if __name__ == '__main__':
    cozmo.run_program(cozmo_program, use_viewer=False, force_viewer_on_top=False)
