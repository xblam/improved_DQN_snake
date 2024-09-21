#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt_library as btl
from bt.composites import *

from bt.robot_behavior import robot_behavior
from bt.globals import BATTERY_LEVEL, GENERAL_CLEANING, SPOT_CLEANING, DUSTY_SPOT_SENSOR, HOME_PATH, CHARGING

# Main body of the assignment
current_blackboard = btl.Blackboard()

current_blackboard.set_in_environment(BATTERY_LEVEL, 29)
current_blackboard.set_in_environment(SPOT_CLEANING, False)
current_blackboard.set_in_environment(GENERAL_CLEANING, True)
current_blackboard.set_in_environment(DUSTY_SPOT_SENSOR, False)
current_blackboard.set_in_environment(HOME_PATH, "")
current_blackboard.set_in_environment(CHARGING, False)

done = False
while not done:
    # Each cycle in this while-loop is equivalent to 1 second time

    # Step 1: Change the environment
    #   - Change the battery level (charging or depleting)
    #   - Simulate the response of the dusty spot sensor
    #   - Simulate user input commands

    battery = current_blackboard.get_in_environment(BATTERY_LEVEL, 0) # get battery level
    if current_blackboard.get_in_environment(CHARGING, False): # check if the battery is charging
        current_blackboard.set_in_environment(BATTERY_LEVEL, battery+1)
    else: current_blackboard.set_in_environment(BATTERY_LEVEL, battery-1)

    # is_dirty = current_blackboard.get_in_environment(DUSTY_SPOT_SENSOR)
    user_input = input("change value of dustry sensor, 1 for dirty 0 for clean: ")
    current_blackboard.set_in_environment(DUSTY_SPOT_SENSOR, user_input)

    random_number = random.choice([0, 1])
    current_blackboard.set_in_environment(DUSTY_SPOT_SENSOR, random_number)

    # Step 2: Evaluating the behavior tree


    # Print the state of the tree nodes before the evaluation
    print('BEFORE -------------------------------------------------------------------------')
    btl.print_states(current_blackboard)
    print('================================================================================')

    result = robot_behavior.evaluate(current_blackboard)

    # Print the state of the tree nodes before the evaluation
    print('AFTER --------------------------------------------------------------------------')
    btl.print_states(current_blackboard)
    print('================================================================================')

    # Step 3: Determine if your solution must terminate
    done = True
