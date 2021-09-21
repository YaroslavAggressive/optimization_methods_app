from enum import Enum


class ErrorMessage(Enum):

    """
    Class with all messages of errors, which current program can detect and process
    """

    ERROR_INCORRECT_DIMENSION = "Too much or not enough variables for start minimization process"
    ERROR_INCORRECT_BOUNDS = "Left border is superior to the right or they are equal"
    ERROR_TOO_MUCH_BOUNDS = "Too many values entered for the boundaries of the uncertainty interval"
    ERROR_NOT_APPLICABLE_ACCURACY = "Entered calculation precision is less than or equal to zero"
    ERROR_INVALID_VALUE = "Incorrect input of numerical values"
    ERROR_INCORRECT_TARGET_FUNCTION = "Objective function entered incorrectly"
    ERROR_WRONG_DIMENSION = "Incorrect number of minimization measurements selected"

