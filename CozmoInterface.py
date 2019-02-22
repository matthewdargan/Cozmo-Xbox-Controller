""" Xbox 360 controller interface for cozmo
Authors: Matthew Dargan, Daniel Stutz
"""

import cozmo
from cozmo.util import degrees
import xbox


def cozmo_program(robot: cozmo.robot.Robot):
    """
    TODO: Comment function
    """

    joy = xbox.Joystick()

    # continous loop that checks for xbox controller input until we are done with the program
    # xbox home button will be used to terminate
    while joy.connected():
        # refresh the xbox inputs from the driver
        joy.refresh()

        y = joy.leftY()  # get y-axis input from left stick before if statements
        x = joy.rightX()  # get x-axis input from left stick before if statements
        left_trigger = joy.leftTrigger()  # get scalar for the left trigger
        right_trigger = joy.rightTrigger()  # get scalar for the right trigger

        if joy.Guide():
            # close the xbox python interface program
            joy.close()
            robot.say_text("I am done with this program.")
            exit()

        elif y:
            # Double the speed if the stick is pressed in
            if joy.leftBumper():
                cozmo_movement(robot, scalar=y, speed=300)
            else:
                cozmo_movement(robot, scalar=y)

        elif x:
            # Double the rotational speed if the stick is pressed in
            # TODO: we have to figure out how to speed the treads to turn
            if joy.rightBumper():
                cozmo_rotate(robot, scalar=x, speed=400)
            else:
                cozmo_rotate(robot, scalar=x)

        elif left_trigger:
            robot.set_lift_height(left_trigger).wait_for_completed()

        elif right_trigger:
            robot.set_lift_height(right_trigger).wait_for_completed()

        elif joy.A():
            robot.play_anim(name="anim_petdetection_dog_03").wait_for_completed()

        elif joy.B():
            robot.play_anim(name="anim_petdetection_dog_03").wait_for_completed()

        elif joy.X():
            robot.play_anim(name="anim_petdetection_dog_03").wait_for_completed()

        elif joy.Y():
            robot.play_anim(name="anim_petdetection_dog_03").wait_for_completed()

        elif joy.dpadUp():
            pass
        elif joy.dpadDown():
            pass
        elif joy.dpadLeft():
            pass
        elif joy.dpadRight():
            pass
            
        elif joy.Back():
            pass
        elif joy.Start():
            pass


def cozmo_movement(robot: cozmo.robot.Robot, scalar, speed=150):
    """
    TODO
    :param robot:
    :param scalar:
    :param speed:
    :return:
    """

    # TODO: Change speed parameter to do some cool scalar math
    robot.drive_straight(cozmo.util.distance_mm(scalar), cozmo.util.speed_mmps(speed)).wait_for_completed()


def cozmo_rotate(robot: cozmo.robot.Robot, scalar, speed=175):
    """
    TODO
    :param robot:
    :param scalar:
    :param speed:
    :return:
    """

    # TODO: Change speed parameter to do some cool scalar math
    robot.turn_in_place(angle=scalar, num_retries=2, speed=degrees(speed)).wait_for_completed()


if __name__ == '__main__':
    cozmo.run_program(cozmo_program, use_viewer=False, force_viewer_on_top=False)