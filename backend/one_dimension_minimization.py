from math import sqrt
from numpy import finfo
from itertools import count
from backend.fibonacci_processing import FibonacciMethods as fbn
from logging import Logger
from backend.error_message import ErrorMessage

CONSTANT_TAO = (sqrt(5) - 1) / 2  # golden ratio constant
CONSTANT_ZERO = 0.0  # to return a "neat" zero instead of a machine epsilon
CONSTANTS_DELTA = 0.01  # delta for dichotomy method
BOUNDS_NUMBER = 2  # number of boundaries of uncertainty interval for finding optimum
# of function that the list should contain in corresponding variable
EMPTY_STR = ""


class OneDimMinimization:

    """
    Class uniting a set of static methods for minimizing one-dimensional
    functions on a given interval and selected accuracy

    Parameters:
    ----------
    error_msg: str
        String to store the error message, if any
    logger: Logger
        Logger for monitoring program operation
    """

    error_msg = EMPTY_STR
    logger = Logger(EMPTY_STR)

    @staticmethod
    def dichotomy_method(func, interval: list = [], eps: float = 0.) -> list:

        """
        Method for minimizing a one-dimensional function using a dichotomy

        Parameters:
        ----------
        func: Any
            Target function of finding the minimum
        interval: list
            Segment where the minimum is being searched for
        eps: float
            Required accuracy of the minimum search

        Returns:
        -------
            List of parameters, which includes the coordinate of the optimum of the function and its value,
             as well as the sequence of the boundaries of the uncertainty interval in the process of minimization
        """

        # processing exceptions, which can ruin work of one dimension minimization
        if len(interval) != BOUNDS_NUMBER:
            OneDimMinimization.logger.error(ErrorMessage.ERROR_TOO_MUCH_BOUNDS.value)
            OneDimMinimization.error_msg = ErrorMessage.ERROR_TOO_MUCH_BOUNDS.value
            return []

        if len(func.free_symbols) > 1:
            OneDimMinimization.logger.error(ErrorMessage.ERROR_WRONG_DIMENSION.value)
            OneDimMinimization.error_msg = ErrorMessage.ERROR_WRONG_DIMENSION.value
            return []

        elif len(func.free_symbols) == 0:
            return [(interval[0] + interval[1]) / 2, float(func), {0: (interval[0], interval[1])}]

        variable = next(iter(func.free_symbols))

        left_bound, right_bound = interval[0], interval[1]

        iter_counter = count()  # iterations counter
        borders_list = {next(iter_counter): (left_bound, right_bound)}

        delta = eps * CONSTANTS_DELTA

        while right_bound - left_bound > eps:
            x_center = (right_bound + left_bound) / 2
            u, v = x_center - delta, x_center + delta
            f_u, f_v = func.subs(variable, u), func.subs(variable, v)

            if f_u > f_v:
                left_bound = u
            else:
                right_bound = v

            borders_list.update({next(iter_counter): (left_bound, right_bound)})

        res = CONSTANT_ZERO if (right_bound + left_bound) / 2 < finfo(float).eps else (right_bound + left_bound) / 2
        return [res, func.subs(variable, res), borders_list]

    @staticmethod
    def golden_ratio_method(func, interval: list = [], eps: float = 0.) -> list:

        """
        Method for minimizing a one-dimensional function using a golden ratio method

        Parameters:
        ----------
        func: Any
            Target function of finding the minimum
        interval: list
            Segment where the minimum is being searched for
        eps: float
            Required accuracy of the minimum search

        Returns:
        -------
            List of parameters, which includes the coordinate of the optimum of the function and its value,
             as well as the sequence of the boundaries of the uncertainty interval in the process of minimization
        """

        # processing exceptions, which can ruin work of one dimension minimization
        if len(interval) != BOUNDS_NUMBER:
            OneDimMinimization.logger.error(ErrorMessage.ERROR_TOO_MUCH_BOUNDS.value)
            OneDimMinimization.error_msg = ErrorMessage.ERROR_TOO_MUCH_BOUNDS.value
            return []  # in case of an error, return an empty list

        if len(func.free_symbols) > 1:
            OneDimMinimization.logger.error(ErrorMessage.ERROR_WRONG_DIMENSION.value)
            OneDimMinimization.error_msg = ErrorMessage.ERROR_WRONG_DIMENSION.value
            return []  # in case of an error, return an empty list

        elif len(func.free_symbols) == 0:
            return [(interval[0] + interval[1]) / 2, float(func), {0: (interval[0], interval[1])}]

        variable = next(iter(func.free_symbols))

        left_bound, right_bound = interval[0], interval[1]

        iter_counter = count()  # iterations counter
        borders_list = {next(iter_counter): (left_bound, right_bound)}

        while right_bound - left_bound > eps:
            lambda_k = left_bound + (1 - CONSTANT_TAO) * (right_bound - left_bound)
            mu_k = left_bound + CONSTANT_TAO * (right_bound - left_bound)
            lambda_value = func.subs(variable, lambda_k)
            mu_value = func.subs(variable, mu_k)
            if lambda_value > mu_value:
                left_bound = lambda_k
            else:
                right_bound = mu_k
            borders_list.update({next(iter_counter): (left_bound, right_bound)})

        res = CONSTANT_ZERO if (right_bound + left_bound) / 2 < finfo(float).eps else (right_bound + left_bound) / 2
        return [res, func.subs(variable, res), borders_list]

    @staticmethod
    def bisection_method(func, interval: list = [], eps: float = 0.) -> list:

        """
        Method for minimizing a one-dimensional function using a bisection method

        Parameters:
        ----------
        func: Any
            Target function of finding the minimum
        interval: list
            Segment where the minimum is being searched for
        eps: float
            Required accuracy of the minimum search

        Returns:
        -------
            List of parameters, which includes the coordinate of the optimum of the function and its value,
             as well as the sequence of the boundaries of the uncertainty interval in the process of minimization
        """

        # processing exceptions, which can ruin work of one dimension minimization
        if len(interval) != BOUNDS_NUMBER:
            OneDimMinimization.logger.error(ErrorMessage.ERROR_TOO_MUCH_BOUNDS.value)
            OneDimMinimization.error_msg = ErrorMessage.ERROR_TOO_MUCH_BOUNDS.value
            return []  # in case of an error, return an empty list

        if len(func.free_symbols) > 1:
            OneDimMinimization.logger.error(ErrorMessage.ERROR_WRONG_DIMENSION.value)
            OneDimMinimization.error_msg = ErrorMessage.ERROR_WRONG_DIMENSION.value
            return []  # in case of an error, return an empty list

        if len(func.free_symbols) == 0:
            return [(interval[0] + interval[1]) / 2, float(func), {0: (interval[0], interval[1])}]

        variable = next(iter(func.free_symbols))

        left_bound, right_bound = interval[0], interval[1]
        x_center = (right_bound + left_bound) / 2

        iter_counter = count()  # iterations counter
        borders_list = {next(iter_counter): (left_bound, right_bound)}

        while right_bound - left_bound > eps:
            f_x_middle = func.subs(variable, x_center)
            x_1, x_2 = right_bound / 4 + 3 * left_bound / 4, 3 * right_bound / 4 + left_bound / 4

            if func.subs(variable, x_1) < f_x_middle:
                right_bound = x_center
                x_center = x_1
            else:
                if func.subs(variable, x_2) < f_x_middle:
                    left_bound = x_center
                    x_center = x_2
                else:
                    left_bound = x_1
                    right_bound = x_2

            borders_list.update({next(iter_counter): (left_bound, right_bound)})

        res = CONSTANT_ZERO if (right_bound + left_bound) / 2 < finfo(float).eps else (right_bound + left_bound) / 2
        return [res, func.subs(variable, res), borders_list]

    @staticmethod
    def fibonacci_method(func, interval: list = [], eps: float = 0.) -> list:

        """
        Method for minimizing a one-dimensional function using fibonacci method

        Parameters:
        ----------
        func: Any
            Target function of finding the minimum
        interval: list
            Segment where the minimum is being searched for
        eps: float
            Required accuracy of the minimum search
        draw: bool
            Boolean parameter responsible for disclosing / hiding rendering of the minimization process

        Returns:
        -------
            List of parameters, which includes the coordinate of the optimum of the function and its value,
             as well as the sequence of the boundaries of the uncertainty interval in the process of minimization
        """

        # processing exceptions, which can ruin work of one dimension minimization
        if len(interval) != BOUNDS_NUMBER:
            OneDimMinimization.logger.error(ErrorMessage.ERROR_TOO_MUCH_BOUNDS.value)
            OneDimMinimization.error_msg = ErrorMessage.ERROR_TOO_MUCH_BOUNDS.value
            return []  # in case of an error, return an empty list

        if len(func.free_symbols) > 1:
            OneDimMinimization.logger.error(ErrorMessage.ERROR_WRONG_DIMENSION.value)
            OneDimMinimization.error_msg = ErrorMessage.ERROR_WRONG_DIMENSION.value
            return []  # in case of an error, return an empty list

        if len(func.free_symbols) == 0:
            return [(interval[0] + interval[1]) / 2, float(func), {0: (interval[0], interval[1])}]

        variable = next(iter(func.free_symbols))

        left_bound, right_bound = interval[0], interval[1]

        # find the closest fibonacci number to the given
        f_n = fbn.nearest_fibonacci_number(int((right_bound - left_bound) / eps))
        n = fbn.index_of_fibonacci(f_n)  # find the number of a given fibonacci number in a row
        if fbn.error_msg:
            OneDimMinimization.error_msg = fbn.error_msg
            return []  # in case of an error, return an empty list

        iter_num = 0
        borders_list = {iter_num: (left_bound, right_bound)}

        lambda_k = left_bound + fbn.get_fibonacci_number(n - iter_num - 1) / fbn.\
            get_fibonacci_number(n - iter_num + 1) * (right_bound - left_bound)
        if fbn.error_msg:
            OneDimMinimization.error_msg = fbn.error_msg
            return []  # in case of an error, return an empty list
        mu_k = left_bound + fbn.get_fibonacci_number(n - iter_num) / fbn.\
            get_fibonacci_number(n - iter_num + 1) * (right_bound - left_bound)
        if fbn.error_msg:
            OneDimMinimization.error_msg = fbn.error_msg
            return []  # in case of an error, return an empty list

        for k in range(iter_num, n - 2):

            f_lambda = func.subs(variable, lambda_k)
            f_mu = func.subs(variable, mu_k)

            if f_lambda > f_mu:
                left_bound = lambda_k
                lambda_k = mu_k
                mu_k = left_bound + fbn.get_fibonacci_number(n - k) / fbn.\
                    get_fibonacci_number(n - k + 1) * (right_bound - left_bound)
                if fbn.error_msg:
                    OneDimMinimization.error_msg = fbn.error_msg
                    return []  # in case of an error, return an empty list
            else:
                right_bound = mu_k
                mu_k = lambda_k
                lambda_k = left_bound + fbn.get_fibonacci_number(n - k - 1) / fbn.\
                    get_fibonacci_number(n - k + 1) * (right_bound - left_bound)
                if fbn.error_msg:
                    OneDimMinimization.error_msg = fbn.error_msg
                    return []  # in case of an error, return an empty list

            borders_list.update({k: (left_bound, right_bound)})

        res = CONSTANT_ZERO if (right_bound + left_bound) / 2 < finfo(float).eps else (right_bound + left_bound) / 2
        return [res, func.subs(variable, res), borders_list]
