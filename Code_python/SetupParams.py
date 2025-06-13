"""
Setup parameters for PETER (Pneumatic Elastomeric and TPU-based Extensible Robot) system.

    This module defines the parameters and setup for the PETER system, including serial communication,
    valve control, and sensor data reading. It is designed to work with a specific hardware configuration.

Jorge F. García-Samartín
www.gsamartin.es
2024-06-13
"""

class SetupParams:
    def __init__(self):
        self.serial_port = "COM7"
        self.baudrate = 115200
        self.debug_mode = False
        self.verbose = True

    # Method for printing the argument pass to the function only if verbose is True
    def print(self, message):
        if self.verbose:
            print(message)

    # Method for printing the argument pass to the function only if debug_mode is True (verbose can be True or False)
    def print_debug(self, message, verbose=False):
        if verbose or self.debug_mode:
            print(message)
        elif self.verbose:
            # If verbose is True, but debug_mode is False, print a warning
            print(f"Warning: Debug mode is off. Message not printed: {message}")
