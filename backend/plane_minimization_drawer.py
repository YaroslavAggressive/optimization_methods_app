import numpy as np
from math import fabs
from sympy import Symbol, Expr
from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.figure import Figure, Axes
from backend.drawer_interface import DrawerInterface
from typing import List
from pure_protobuf.dataclasses_ import field, optional_field
from backend.gif_maker import GifMaker

# constants for minimization drawing and configuring plotting
POINTS_NUMBER = 1000
DOTS_NUMBER = 10  # number of points on the dotted border of the interval
ARROW_COLOR = "green"  # color for annotation arrow
ARROW_SHRINK = 0.01  # annotation arrow shrink
AXES_BOUND_MULTIPLIER = 2  # multiplier of the boundaries of coordinate axes of graph relative to graph of function
AXES_ARROW_WIDTH = 0.01  # width of arrows of the coordinate axes on unction graph
AXES_COLOR = "orange"  # color for axes lines on plot
BOUNDS_COLOR = "blue"  # border color to indicate uncertainty range
DOT_MARKER = "o"  # designation of a point on the border of the uncertainty interval
ANNOTATION_COLOR = "black"
BOUNDS_LINE_STYLE = "--"
ANNOTATION_INDENT = 3
FONT_SIZE = "xx-small"  # boundary and central points annotation size on each iteration
EMPTY_STR = ""

IMAGES_FOLDER = "front/images_for_gif"
RESULT_FILENAME = "minimization_image_"
RES_POSTFIX = ".jpg"
BOUNDS_LABEL_PREFIX = "iter #"
PATH_DELIMITER = "/"


@dataclass
class PlaneMinimizationDrawer(DrawerInterface):

    """
    Class for drawing sequential processing of the function graph using one-dimensional minimization methods

    Parameters:
    ----------
    func: Expr
        Target function in sympy format to render
    bounds: List
        Optimization interval boundaries
    x_values: List
        Dividing the uncertainty interval by the optimization variable
    y_values: List
        Value of the function on the uncertainty interval
    variable: Symbol
        Variable for optimization
    """

    func: Expr = field(1, default="")
    bounds: List = field(2, default_factory=list)
    x_values: List = optional_field(3)
    y_values: List = optional_field(4)
    variable: Symbol = optional_field(5)
    fig: Figure = optional_field(6)
    axes: Axes = optional_field(7)

    def __post_init__(self):
        try:
            symbols = self.func.free_symbols
            if len(symbols) != 0:
                self.variable = next(iter(self.func.free_symbols))
        except SyntaxError:
            raise Exception("Error: invalid target function syntax")  ####
        self.fig, self.axes = plt.subplots()
        self.calculate_function_graph()

    def render_optimization_image(self):

        """
        Method for drawing initial picture of the optimization process
        """

        self.draw_colored_axes()
        self.draw_bounds()

    def calculate_function_graph(self):

        """
        Method for plotting a function graph in an easy-to-draw format
        """

        self.x_values = list(np.linspace(self.bounds[0], self.bounds[1], POINTS_NUMBER))
        self.y_values = []
        for component in self.x_values:
            self.y_values.append(float(self.func.subs(self.variable, component)))

    def draw_graph_of_function(self):

        """
        Method for drawing function with matplotlib
        """

        self.axes.plot(self.x_values, self.y_values, "r", label="target function")
        self.axes.legend()
        plt.draw()

    def draw_colored_axes(self):

        """
        Method for drawing colored coordinate axes on the graph
        """

        plt.xlabel(str(self.variable))
        plt.ylabel("f({})".format(self.variable))

        right_bound = fabs(max(self.bounds)) if fabs(max(self.bounds)) > fabs(min(self.bounds)) \
            else fabs(min(self.bounds))
        left_bound = -right_bound
        top_bound = fabs(max(self.y_values)) if fabs(max(self.y_values)) > fabs(min(self.y_values)) \
            else fabs(min(self.y_values))
        bottom_bound = -top_bound

        self.axes.arrow(left_bound, 0, right_bound - left_bound, 0, color=AXES_COLOR,
                        length_includes_head=True,
                        width=AXES_ARROW_WIDTH)
        self.axes.arrow(0, bottom_bound, 0, top_bound - bottom_bound, color=AXES_COLOR,
                        length_includes_head=True,
                        width=AXES_ARROW_WIDTH)

        self.axes.grid()
        plt.draw()

    def draw_bounds(self, iteration: int = 1):

        """
        Method for drawing dashed lines limiting the uncertainty interval at the moment

        Parameters:
        ----------
        iteration: int
            Iteration number of the minimization algorithm, at which the new bounds
             of the uncertainty interval should be drawn
        """

        f_left = self.func.subs(self.variable, self.bounds[0])  # consider the value of the function at the boundaries
        f_right = self.func.subs(self.variable, self.bounds[1])  # of the uncertainty interval

        # drawing right bound
        self.draw_point(iteration=iteration,
                        annotation="left border #{}".format(iteration),
                        point_x=self.bounds[0],
                        point_y=f_left)

        # drawing left bound
        self.draw_point(iteration=iteration,
                        annotation="right border #{}".format(iteration),
                        point_x=self.bounds[1],
                        point_y=f_right)

    def update_bounds(self, bounds: list):

        """
        Method for changing (updating) the value of the boundaries of the uncertainty interval

        Parameters:
        ----------
        bounds: list
            New values of interval borders
        """

        self.bounds = bounds

    def draw_point(self, iteration: int = 1, annotation: str = "", point_x: float = 0., point_y: float = 0.):

        """
        Method for drawing point of function graph

        Parameters:
        ----------
        iteration: int
            Iteration number of the minimization algorithm, at which the new point
             of the uncertainty interval should be drawn
        annotation: str
            Dot label text
        point_x: float
            Abscissa for the point being drawn
        point_y: float
            Ordinate for the point to draw
        """

        # putting dot
        self.axes.plot(point_x, point_y, color=BOUNDS_COLOR, marker=DOT_MARKER)
        # putting dot on x-axis
        self.axes.plot(point_x, 0, color=BOUNDS_COLOR, marker=DOT_MARKER)
        if point_y < 0:
            point_line = np.linspace(float(point_y), 0, DOTS_NUMBER)
        else:
            point_line = np.linspace(0, float(point_y), DOTS_NUMBER)

        self.axes.plot([point_x] * len(point_line), point_line,
                       linestyle='--',
                       color=BOUNDS_COLOR)

        # making annotation of center point of interval
        self.annotate_point(point_x, point_y, annotation)

        # self.axes.legend()
        plt.draw()

    def annotate_point(self, x_point: float, y_point: float, text: str):

        """
        Method for annotating point on function graph

        Parameters:
        ----------
        x_point: float
            X coordinate of the point
        y_point: float
            Y coordinate of the point
        text: str:
            Dot label text
        text_x: float
            X-coordinate of text annotation to point
        text_y: float
            Y-coordinate of text annotation to point
        """
        annotation_indent = max(self.y_values) / ANNOTATION_INDENT
        plt.annotate(text, xy=(x_point, y_point), xytext=(x_point, y_point + annotation_indent), color=ANNOTATION_COLOR,
                     arrowprops=dict(facecolor=ARROW_COLOR, shrink=ARROW_SHRINK), fontsize="xx-small")
        plt.draw()

    def get_fig(self):
        return self.fig

    def clear_figure(self):
        self.axes.cla()

    def draw_minimization(self, x_optimum: float = 0., f_x_optimum: float = 0., borders: dict = {}) -> list:
        """

        Parameters:
        ----------
        x_optimum: float
            Point at which the minimum of the function was found
        f_x_optimum: float
            Value of the function at the point at which the minimum of the function was found
        borders: dict
            Dictionary with all intervals of uncertainty in the minimization process, numbered by the iteration index

        Returns:
        -------
            List of paths to images for gif creation
        """

        images_for_gif = []
        init_iter = 0
        for iter_num in borders.keys():
            self.update_bounds(list(borders[iter_num]))
            images_for_gif.append(self.draw_current_iteration(iter_num, borders[init_iter]))
        images_for_gif.append(self.draw_result_image(len(borders.keys()), result_x=x_optimum, result_y=f_x_optimum))
        return images_for_gif

    def draw_current_iteration(self, iter_num: int = 0, init_interval: tuple = ()) -> str:

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

        Returns:
        -------
            Path to result image
        """

        self.draw_bounds(iter_num)
        self.update_bounds([init_interval[0], init_interval[1]])
        self.draw_colored_axes()
        self.draw_graph_of_function()
        image_path = PlaneMinimizationDrawer.save_iteration_img(iter_num)
        self.clear_figure()
        return image_path

    def draw_result_image(self, iter_num: int = 1, result_x: float = 0., result_y: float = 0.) -> str:

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

        Returns:
        -------
            Path to result image
        """

        self.draw_graph_of_function()
        self.draw_colored_axes()
        self.draw_point(iter_num, "result point on iteration #{}".format(iter_num), result_x, result_y)
        return PlaneMinimizationDrawer.save_iteration_img(iter_num)

    def const_minimization(self, interval: list) -> str:

        """
        Method for solving the problem of minimization on a constant function

        Parameters:
        ----------
        interval: list
            List of two boundaries of the uncertainty interval

        Returns:
        -------
            Path for gif with result minimization
        """

        iter_num = 1
        result_x = (interval[0] + interval[1]) / 2
        result_y = float(self.func)
        images_for_gif = [self.draw_result_image(iter_num, result_x, result_y)]
        return GifMaker.create_gif_result(images_for_gif, IMAGES_FOLDER)

    @staticmethod
    def save_iteration_img(iter_num: int = 0) -> str:

        """
        Method for saving the path to the image, along which it is planned to animate the minimization process,
         and adding it to the general set of such images

        Parameters:
        ----------
        iter_num: int
            Number of iteration

        Returns:
        -------
            Path to current saved image
        """

        image_name = "iter_{}".format(iter_num)
        full_path = IMAGES_FOLDER + PATH_DELIMITER + RESULT_FILENAME + image_name + RES_POSTFIX
        plt.savefig(full_path)
        return full_path
