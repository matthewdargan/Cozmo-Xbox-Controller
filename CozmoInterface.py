#Initialize Cozmo File
#Matthew Dargan, Daniel Stutz

import cozmo
import xbox 

def cozmo_program(robot: cozmo.robot.Robot):
    """
    TODO: Comment function
    """
    joy = xbox.Joystick()
    is_cozmo_in_use = True

    # continous loop that checks for xbox controller input until we are done with the program
    # xbox home button will be used to terminate
    while (is_cozmo_in_use):
        # get y-axis input from left stick before if statements
        y = joy.leftY()

        if joy.Guide():
            # close the xbox python interface program
            joy.close()

            # so we don't go through the while loop again
            is_cozmo_in_use = False
        elif y is not None:
            # call cozmo movement function
            cozmo_movement(robot, scalar=y)

def cozmo_movement(robot: cozmo.robot.Robot, scalar):
    """
    TODO: Comment function
    """

    # TODO: Change speed parameter to do some cool scalar math
    robot.drive_straight(cozmo.util.distance_mm(scalar), cozmo.util.speed_mmps(150)).wait_for_completed()

if __name__ == '__main__':
	cozmo.run_program(cozmo_program, use_viewer=False, force_viewer_on_top=False)