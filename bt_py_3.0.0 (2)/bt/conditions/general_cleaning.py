#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# Version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt_library as btl
from ..globals import BATTERY_LEVEL


class BatteryLessThan30(btl.Condition):
    """
    Implementation of the condition "general_cleaning".
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message('check general cleaning')

        return self.report_succeeded(blackboard) \
            if blackboard.get_in_environment(GENERAL CLEANING, 0)\
            else self.report_failed(blackboard)
