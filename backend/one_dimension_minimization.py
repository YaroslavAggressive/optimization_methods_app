from math import sqrt
from numpy import finfo
from backend.plane_minimization_drawer import PlaneMinimizationDrawer, IMAGES_FOLDER
from itertools import count
from backend.gif_maker import GifMaker
import os
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
    drawer: PlaneMinimizationDrawer
        Renderer of the process of minimizing the objective function on the chart
    result_gif: str
        Name of gif-result of last minimization process of current target function
    error_msg: str
        String to store the error message, if any
    logger: Logger
        Logger for monitoring program operation
    """

    drawer = None
    result_gif = EMPTY_STR
    error_msg = EMPTY_STR
    logger = Logger(EMPTY_STR)

    @staticmethod
    def dichotomy_method(func, interval: list = [], eps: float = 0., draw: bool = False) -> float:

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
        draw: bool
            Boolean parameter responsible for disclosing / hiding rendering of the minimization process

        Returns:
        -------
            Minimum value of the function on the specified segment with the required accuracy
        """

        # processing exceptions, which can ruin work of one dimension minimization
        if len(interval) != BOUNDS_NUMBER:
            OneDimMinimization.logger.error(ErrorMessage.ERROR_TOO_MUCH_BOUNDS.value)
            OneDimMinimization.error_msg = ErrorMessage.ERROR_TOO_MUCH_BOUNDS.value
            return 0.

        if len(func.free_symbols) > 1:
            OneDimMinimization.logger.error(ErrorMessage.ERROR_WRONG_DIMENSION.value)
            OneDimMinimization.error_msg = ErrorMessage.ERROR_WRONG_DIMENSION.value
            return 0.

        elif len(func.free_symbols) == 0:
            if draw:
                OneDimMinimization.drawer = PlaneMinimizationDrawer(func, interval)
                OneDimMinimization.check_images_folder(IMAGES_FOLDER)
                OneDimMinimization.const_minimization(interval)
            return float(func)

        variable = next(iter(func.free_symbols))

        left_bound, right_bound = interval[0], interval[1]

        iter_counter = count()  # iterations counter
        iter_next = next(iter_counter)

        images_for_gif = []

        if draw:
            OneDimMinimization.drawer = PlaneMinimizationDrawer(func, interval)
            OneDimMinimization.check_images_folder(IMAGES_FOLDER)
            OneDimMinimization.draw_current_iteration(iter_next, interval, images_for_gif)

        delta = eps * CONSTANTS_DELTA

        while right_bound - left_bound > eps:
            x_center = (right_bound + left_bound) / 2
            u, v = x_center - delta, x_center + delta
            f_u, f_v = func.subs(variable, u), func.subs(variable, v)

            if f_u > f_v:
                left_bound = u
            else:
                right_bound = v

            iter_next = next(iter_counter)
            if draw:
                OneDimMinimization.drawer.update_bounds([left_bound, right_bound])
                OneDimMinimization.draw_current_iteration(iter_next, interval, images_for_gif)

        if draw:
            OneDimMinimization.draw_result_image(iter_next, left_bound, right_bound, images_for_gif)

        res = (right_bound + left_bound) / 2
        return CONSTANT_ZERO if res < finfo(float).eps else res

    @staticmethod
    def golden_ratio_method(func, interval: list = [], eps: float = 0., draw: bool = False) -> float:

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
        draw: bool
            Boolean parameter responsible for disclosing / hiding rendering of the minimization process

        Returns:
        -------
            Minimum value of the function on the specified segment with the required accuracy
        """

        # processing exceptions, which can ruin work of one dimension minimization
        if len(interval) != BOUNDS_NUMBER:
            OneDimMinimization.logger.error(ErrorMessage.ERROR_TOO_MUCH_BOUNDS.value)
            OneDimMinimization.error_msg = ErrorMessage.ERROR_TOO_MUCH_BOUNDS.value
            return 0.

        if len(func.free_symbols) > 1:
            OneDimMinimization.logger.error(ErrorMessage.ERROR_WRONG_DIMENSION.value)
            OneDimMinimization.error_msg = ErrorMessage.ERROR_WRONG_DIMENSION.value
            return 0.

        elif len(func.free_symbols) == 0:
            if draw:
                OneDimMinimization.drawer = PlaneMinimizationDrawer(func, interval)
                OneDimMinimization.check_images_folder(IMAGES_FOLDER)
                OneDimMinimization.const_minimization(interval)
            return float(func)

        variable = next(iter(func.free_symbols))

        left_bound, right_bound = interval[0], interval[1]

        iter_counter = count()  # iterations counter
        iter_next = next(iter_counter)

        images_for_gif = []

        if draw:
            OneDimMinimization.drawer = PlaneMinimizationDrawer(func, interval)
            OneDimMinimization.check_images_folder(IMAGES_FOLDER)
            OneDimMinimization.draw_current_iteration(iter_next, interval, images_for_gif)

        while right_bound - left_bound > eps:
            lambda_k = left_bound + (1 - CONSTANT_TAO) * (right_bound - left_bound)
            mu_k = left_bound + CONSTANT_TAO * (right_bound - left_bound)
            lambda_value = func.subs(variable, lambda_k)
            mu_value = func.subs(variable, mu_k)
            if lambda_value > mu_value:
                left_bound = lambda_k
            else:
                right_bound = mu_k

            iter_next = next(iter_counter)
            if draw:
                OneDimMinimization.drawer.update_bounds([left_bound, right_bound])
                OneDimMinimization.draw_current_iteration(iter_next, interval, images_for_gif)

        if draw:
            OneDimMinimization.draw_result_image(iter_next, left_bound, right_bound, images_for_gif)

        res = (right_bound + left_bound) / 2
        return CONSTANT_ZERO if res < finfo(float).eps else res

    @staticmethod
    def bisection_method(func, interval: list = [], eps: float = 0., draw: bool = False) -> float:

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
        draw: bool
            Boolean parameter responsible for disclosing / hiding rendering of the minimization process

        Returns:
        -------
            Minimum value of the function on the specified segment with the required accuracy
        """

        # processing exceptions, which can ruin work of one dimension minimization
        if len(interval) != BOUNDS_NUMBER:
            OneDimMinimization.logger.error(ErrorMessage.ERROR_TOO_MUCH_BOUNDS.value)
            OneDimMinimization.error_msg = ErrorMessage.ERROR_TOO_MUCH_BOUNDS.value
            return 0.

        if len(func.free_symbols) > 1:
            OneDimMinimization.logger.error(ErrorMessage.ERROR_WRONG_DIMENSION.value)
            OneDimMinimization.error_msg = ErrorMessage.ERROR_WRONG_DIMENSION.value
            return 0.

        if len(func.free_symbols) == 0:
            if draw:
                OneDimMinimization.drawer = PlaneMinimizationDrawer(func, interval)
                OneDimMinimization.check_images_folder(IMAGES_FOLDER)
                OneDimMinimization.const_minimization(interval)
            return float(func)

        variable = next(iter(func.free_symbols))

        left_bound, right_bound = interval[0], interval[1]
        x_center = (right_bound + left_bound) / 2

        iter_counter = count()  # iterations counter
        iter_next = next(iter_counter)

        images_for_gif = []

        if draw:
            OneDimMinimization.drawer = PlaneMinimizationDrawer(func, interval)
            OneDimMinimization.check_images_folder(IMAGES_FOLDER)
            OneDimMinimization.draw_current_iteration(iter_next, interval, images_for_gif)

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

            iter_next = next(iter_counter)

            if draw:
                OneDimMinimization.drawer.update_bounds([left_bound, right_bound])
                OneDimMinimization.draw_current_iteration(iter_next, interval, images_for_gif)

        if draw:
            OneDimMinimization.draw_result_image(iter_next, left_bound, right_bound, images_for_gif)

        res = (right_bound + left_bound) / 2
        return CONSTANT_ZERO if res < finfo(float).eps else res

    @staticmethod
    def fibonacci_method(func, interval: list = [], eps: float = 0., draw: bool = False) -> float:

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
            Minimum value of the function on the specified segment with the required accuracy
        """

        # processing exceptions, which can ruin work of one dimension minimization
        if len(interval) != BOUNDS_NUMBER:
            OneDimMinimization.logger.error(ErrorMessage.ERROR_TOO_MUCH_BOUNDS.value)
            OneDimMinimization.error_msg = ErrorMessage.ERROR_TOO_MUCH_BOUNDS.value
            return 0.

        if len(func.free_symbols) > 1:
            OneDimMinimization.logger.error(ErrorMessage.ERROR_WRONG_DIMENSION.value)
            OneDimMinimization.error_msg = ErrorMessage.ERROR_WRONG_DIMENSION.value
            return 0.

        images_for_gif = []

        if len(func.free_symbols) == 0:
            if draw:
                OneDimMinimization.drawer = PlaneMinimizationDrawer(func, interval)
                OneDimMinimization.check_images_folder(IMAGES_FOLDER)
                OneDimMinimization.const_minimization(interval)
            return float(func)

        variable = next(iter(func.free_symbols))

        left_bound, right_bound = interval[0], interval[1]

        # find the closest fibonacci number to the given
        f_n = fbn.nearest_fibonacci_number(int((right_bound - left_bound) / eps))
        n = fbn.index_of_fibonacci(f_n)  # find the number of a given fibonacci number in a row
        if fbn.error_msg:
            OneDimMinimization.error_msg = fbn.error_msg
            return 0.
        iter_num = 0

        lambda_k = left_bound + fbn.get_fibonacci_number(n - iter_num - 1) / fbn.\
            get_fibonacci_number(n - iter_num + 1) * (right_bound - left_bound)
        if fbn.error_msg:
            OneDimMinimization.error_msg = fbn.error_msg
            return 0.
        mu_k = left_bound + fbn.get_fibonacci_number(n - iter_num) / fbn.\
            get_fibonacci_number(n - iter_num + 1) * (right_bound - left_bound)
        if fbn.error_msg:
            OneDimMinimization.error_msg = fbn.error_msg
            return 0.

        if draw:
            OneDimMinimization.drawer = PlaneMinimizationDrawer(func, interval)
            OneDimMinimization.check_images_folder(IMAGES_FOLDER)
            OneDimMinimization.draw_current_iteration(iter_num, interval, images_for_gif)

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
                    return 0.
            else:
                right_bound = mu_k
                mu_k = lambda_k
                lambda_k = left_bound + fbn.get_fibonacci_number(n - k - 1) / fbn.\
                    get_fibonacci_number(n - k + 1) * (right_bound - left_bound)
                if fbn.error_msg:
                    OneDimMinimization.error_msg = fbn.error_msg
                    return 0.
            if draw:
                OneDimMinimization.drawer.update_bounds([left_bound, right_bound])
                OneDimMinimization.draw_current_iteration(k, interval, images_for_gif)

        if draw:
            OneDimMinimization.draw_result_image(n - 2, left_bound, right_bound, images_for_gif)

        res = (right_bound + left_bound) / 2
        return CONSTANT_ZERO if res < finfo(float).eps else res

    @staticmethod
    def draw_current_iteration(iter_num: int = 0, init_interval: list = None, images_for_gif: list = []):

        """
        Method for drawing the current iteration of the minimization algorithm
        Parameters:
        ----------

        iter_num: float
            Number of current iteration which drawing we draw
        l_bound: float
            Left bound of new interval on current iteration
        r_bound: float
            Right bound of new interval on current iteration
        init_interval: list
            Initial bounds of uncertainty interval for drawing axes on graph
        images_for_gif: list
            List of image names from which are built minimization animation
        """

        OneDimMinimization.drawer.draw_bounds(iter_num)
        OneDimMinimization.drawer.update_bounds([init_interval[0], init_interval[1]])
        OneDimMinimization.drawer.draw_colored_axes()
        OneDimMinimization.drawer.draw_graph_of_function()
        OneDimMinimization.save_iteration_img(iter_num, images_for_gif)
        OneDimMinimization.drawer.clear_figure()

    @staticmethod
    def draw_result_image(iter_num: int = 1, result_x: float = 0., result_y: float = 0., images_for_gif: list = []):

        """
        Method for drawing minimization result on function graph to show the user

        Parameters:
        ----------
        iter_num: int
            Iteration number at which the minimization result was found
        result_x: float
            Abscissa of the minimization result point
        result_y: float
            Ordinate of the point-result of minimization
        init_interval: list
            Initial bounds of uncertainty interval for drawing axes on graph
        images_for_gif: list
            List of image names from which are built minimization animation
        """

        OneDimMinimization.drawer.draw_graph_of_function()
        OneDimMinimization.drawer.draw_colored_axes()
        OneDimMinimization.drawer.draw_point(iter_num, "result point on iteration #{}".format(iter_num),
                                             result_x, result_y)
        OneDimMinimization.save_iteration_img(iter_num, images_for_gif)
        OneDimMinimization.result_gif = GifMaker.create_gif_result(images_for_gif, IMAGES_FOLDER)

    @staticmethod
    def const_minimization(interval: list):

        """
        Method for solving the problem of minimization on a constant function

        Parameters:
        ----------
        interval: list
            List of two boundaries of the uncertainty interval
        """

        iter_num = 1
        result_x = (interval[0] + interval[1]) / 2
        result_y = float(OneDimMinimization.drawer.func)
        images_for_gif = []
        OneDimMinimization.draw_result_image(iter_num, result_x=result_x,
                                             result_y=result_y, images_for_gif=images_for_gif)
        OneDimMinimization.save_iteration_img(iter_num, images_for_gif)
        OneDimMinimization.result_gif = GifMaker.create_gif_result(images_for_gif, IMAGES_FOLDER)

    @staticmethod
    def clear_minimization():

        """
        Method for updating static class variables for further minimization
        """

        OneDimMinimization.drawer = None
        OneDimMinimization.result_gif = EMPTY_STR
        OneDimMinimization.error_msg = EMPTY_STR
        OneDimMinimization.images_for_gif = []

    @staticmethod
    def save_iteration_img(iter_num: int = 0, images_list: list = None):

        """
        Method for saving the path to the image, along which it is planned to animate the minimization process,
         and adding it to the general set of such images

        Parameters:
        ----------
        iter_num: int
            Number of iteration
        images_list: list
            List of pictures that are supposed to be used to create GIF animation
        """

        image_name = "iter_{}".format(iter_num)
        image_path = OneDimMinimization.drawer.save_figure(IMAGES_FOLDER, image_name)
        images_list.append(image_path)

    @staticmethod
    def check_images_folder(folder_name: str = ""):

        """
        Method for checking a directory before filling it with temporary files

        Parameters:
        ----------
        folder_name: str
            Name of the folder, the presence and emptiness of which you want to check
        """

        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        else:
            GifMaker.clear_temp_images(folder_name)
