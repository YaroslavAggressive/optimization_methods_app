from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QStyleFactory
from PyQt5.QtGui import QMovie, QIcon, QPixmap
from PyQt5 import QtWidgets
from front.optimization_methods_gui import Ui_MainWindow
from backend.one_dimension_minimization import OneDimMinimization, EMPTY_STR
from backend.error_message import ErrorMessage
from sympy.parsing import parse_expr
import logging
import datetime


TARGET_FUNCTION_DEFAULT = 0.  # standard values for input fields of the one-dimensional minimization problem
LEFT_BORDER_DEFAULT = 0.
RIGHT_BORDER_DEFAULT = 1.
EPSILON_DEFAULT = 1e-6
FUNCTION_DIMENSIONS = [1, 2, 3]  # dimensions of spaces in which the optimization problem can be solved
ONE_DIM_MINIMIZATION_METHODS_NAMES = {"Golden Ratio Method": OneDimMinimization.golden_ratio_method,
                                      "Dichotomy Method": OneDimMinimization.dichotomy_method,
                                      "Bisection Method": OneDimMinimization.bisection_method,
                                      "Fibonacci Method": OneDimMinimization.fibonacci_method}
TABLE_COLUMNS = ["Target Function", "Interval", "Accuracy", "Result"]  # column names in the results table
INIT_ROWS_NUMBER = 1  # before starting work with minimization, the table must have one empty string
FIRST_COLUMN_INDEX = 0

DEFAULT_STYLESHEET_COLOR = "color:red;"
PAUSE_BTN_PLAY_TEXT = "continue gif"
PAUSE_BTN_PAUSE_TEXT = "pause gif"
PAUSE_BTN_INIT_TEXT = "No gif available"
LOGGER_NAME = "application_log.log"  # name for the application logger to collect error information
WINDOW_STYLE_NAME = 'Fusion'

LABEL_INIT_PIXMAP = "front/ui_src/your_advert.png"
LOADING_GIF = "front/ui_src/loading.gif"

STANDARD_ERROR_MSG = "Error in the formulation of the minimization problem"
ERROR_MSG_TITLE = "Critical error"
ERROR_WINDOW_ICON = "front/ui_src/message_box_icon.jpg"


class AppWindow(QMainWindow, Ui_MainWindow):

    """
    Main class of minimization gui application
    """

    def __init__(self, parent=0, *args, **kwargs):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setStyle(QStyleFactory.create(WINDOW_STYLE_NAME))
        self.minimization_movie = QMovie()  # for drawing gif result to user

        # handling keystrokes
        self.restart_prog_button.clicked.connect(self.restart_button_clicked)
        self.exit_button.clicked.connect(self.close)
        self.solution_button.clicked.connect(self.solution_button_clicked)
        self.pause_button.clicked.connect(self.pause_animation)
        self.pause_button.setEnabled(False)

        logging.basicConfig(filename=LOGGER_NAME, level=logging.INFO)  # initializing application logger
        logging.info("Program started at {}".format(datetime.datetime.now()))
        # initialize drop-down button with dimensions of spaces
        self.init_variables_editor()
        # initialize minimization methods list
        self.init_minimization_methods()
        # initializing results table
        self.init_results_table()
        # now init all tables and task edits
        self.init_application()

        logging.info("Application initialization was completed")

    def restart_button_clicked(self):

        """
        Method of handling pressing the program restart key
        """

        # AppWindow.clear_layout(self.graph_rendering_layout)
        self.clear_gif_label()
        self.init_application()
        self.pause_button.setEnabled(False)
        logging.info("Application interface was successfully reinitialized")

    def clear_gif_label(self):

        """
        Method for deleting current gif from label for drawing next minimization process
        """

        self.gif_label.clear()
        self.minimization_movie.stop()
        self.minimization_movie.setFileName(EMPTY_STR)
        logging.info("Problem edit labels were reinitialized")

    def init_application(self):

        """
        Method for initializing the UI fields
        """

        # initialize the initial values of the input fields
        self.init_task_edits()
        # filling gif label with init picture
        self.gif_label.setPixmap(QPixmap(LABEL_INIT_PIXMAP))
        self.gif_label.setScaledContents(True)
        logging.info("Problem edit labels were reinitialized")

    def solution_button_clicked(self):

        """
        Method of handling pressing the search key for a solution to the problem
        """

        err_msg = self.process_init_mistakes()
        if err_msg:
            logging.error(err_msg)
            AppWindow.show_user_error_mess(err_msg)
            return
        # get all information about the task from the input fields
        function = self.edit_target_function.toPlainText()
        eps = self.edit_epsilon.toPlainText()
        bound_left = self.bound_left.toPlainText()
        bound_right = self.right_bound.toPlainText()
        method_name = self.minimization_methods_box.currentText()

        # translate information into a convenient format for transfer to the optimization method
        try:
            function = parse_expr(function)
            eps = float(eps)
            bound_right = float(bound_right)
            bound_left = float(bound_left)
        except ValueError:  # error in filling numeric parameters of minimization problem
            logging.error(ErrorMessage.ERROR_INVALID_VALUE.value)
            AppWindow.show_user_error_mess(ErrorMessage.ERROR_INVALID_VALUE.value)
        except SyntaxError:  # error in filling target function of minimization problem
            logging.error(ErrorMessage.ERROR_INCORRECT_TARGET_FUNCTION.value)
            AppWindow.show_user_error_mess(ErrorMessage.ERROR_INCORRECT_TARGET_FUNCTION.value)

        logging.info("All data on the minimization problem are entered correctly")

        interval = [bound_left, bound_right]

        # check if the minimization process has been started before clicking and match clear the gif if it was playing
        if self.gif_label.movie() or self.gif_label.pixmap():
            self.clear_gif_label()

        # adopt the minimization method and draw the process
        # self.draw_result_gif(LOADING_GIF)
        OneDimMinimization.logger = logging.getLogger()
        result = ONE_DIM_MINIMIZATION_METHODS_NAMES[method_name](function, interval, eps, draw=True)

        # self.clear_gif_label()
        if OneDimMinimization.error_msg:
            AppWindow.show_user_error_mess(OneDimMinimization.error_msg)
            return

        self.draw_result_gif(OneDimMinimization.result_gif)
        self.draw_result_table(result)

    def init_task_edits(self):

        """
        Method for filling in the input fields of the optimization task with default values
         displaying it on the screen to the user
        """

        self.edit_epsilon.setText(str(EPSILON_DEFAULT))
        self.bound_left.setText(str(LEFT_BORDER_DEFAULT))
        self.right_bound.setText(str(RIGHT_BORDER_DEFAULT))
        self.edit_target_function.setText(str(TARGET_FUNCTION_DEFAULT))
        self.pause_button.setText(PAUSE_BTN_INIT_TEXT)
        logging.info("Initial values of input fields are correctly initialized")

    def draw_result_gif(self, result_gif_path: str):

        """
        Method for initializing the means of drawing the graph of the function to be minimized

        Parameters:
        ----------
        result_gif_path: str
            Full path to the GIF image with rendering of the minimization process
        """

        self.minimization_movie = QMovie(result_gif_path)

        self.gif_label.setMovie(self.minimization_movie)
        self.minimization_movie.start()

        self.pause_button.setText(PAUSE_BTN_PAUSE_TEXT)
        self.pause_button.setEnabled(True)
        logging.info("Result animation was successfully drawn")

    def pause_animation(self):
        # if self.minimization_movie
        if self.minimization_movie.state() == QMovie.Paused:
            self.minimization_movie.setPaused(False)
            self.pause_button.setText(PAUSE_BTN_PAUSE_TEXT)
            logging.info("Animation of minimization successfully paused")
        else:
            self.minimization_movie.setPaused(True)
            self.pause_button.setText(PAUSE_BTN_PLAY_TEXT)
            logging.info("Animation of minimization successfully continued")

    def draw_result_table(self, minimization_result: float = 0):

        """
        Method for drawing minimization result information to user of application

        Parameters:
        ----------
        minimization_result: float
            Result of minimization in given as real number
        """
        row_index = self.results_table.rowCount() - 1
        # check the previous cell for filling
        last_item = self.results_table.item(row_index, FIRST_COLUMN_INDEX)
        if not last_item:
            self.table_cell_filling(row_index,
                                    cell_values=[self.edit_target_function.toPlainText(),
                                                 "[" + self.bound_left.toPlainText() + ", " +
                                                 self.right_bound.toPlainText() + "]",
                                                 self.edit_epsilon.toPlainText(),
                                                 str(minimization_result)])
        else:
            self.results_table.insertRow(self.results_table.rowCount())  # inserting new row at the end of the table
            self.table_cell_filling(row_index + 1,
                                    cell_values=[self.edit_target_function.toPlainText(),
                                                 "[" + self.bound_left.toPlainText() + ", " +
                                                 self.right_bound.toPlainText() + "]",
                                                 self.edit_epsilon.toPlainText(),
                                                 str(minimization_result)])

        # resizing table columns
        header = self.results_table.horizontalHeader()
        for column in range(self.results_table.columnCount() - 1):
            header.setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
        # resizing last column manually
        header.setSectionResizeMode(self.results_table.columnCount() - 1, QtWidgets.QHeaderView.ResizeToContents)

    def table_cell_filling(self, row_index: int = 0, cell_values: list = None):

        """
        Method for filling the row of the result table with the values obtained in the last minimization process

        Parameters:
        ----------
        row_index: int
            Index of row on which position it is necessary to insert new values
        cell_values: list
            Values to insert into table cells
        """

        if len(cell_values) != len(TABLE_COLUMNS):
            raise Exception("Error while table cell filling: not enough or too much input arguments")
        else:
            for index, column_value in enumerate(cell_values):
                self.results_table.setItem(row_index, index, QTableWidgetItem(column_value))

        logging.info("Minimization result successfully added to table")

    def init_variables_editor(self):

        """
        Method for adding dimensions of spaces to the combobox for solving optimization problems
        """

        for dimension in FUNCTION_DIMENSIONS:
            self.variables_number.addItem(str(dimension))
        logging.info("Combo box with minimization dimensions successfully initialized")

    def init_minimization_methods(self):

        """
        Method of filling the drop-down button with the names of the methods available for use in the minimization task
        """

        for name in ONE_DIM_MINIMIZATION_METHODS_NAMES.keys():
            self.minimization_methods_box.addItem(name)

    def init_results_table(self):

        """
        Method for initializing table widget for showing to user results of minimization
        """

        self.results_table.setColumnCount(len(TABLE_COLUMNS))
        self.results_table.setRowCount(INIT_ROWS_NUMBER)
        self.results_table.setHorizontalHeaderLabels(TABLE_COLUMNS)
        self.results_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # resizing table columns
        header = self.results_table.horizontalHeader()
        for column in range(self.results_table.columnCount() - 1):
            header.setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)

        logging.info("Result table was successfully drawn")

    def process_init_mistakes(self) -> str:

        """
        Method for handling user input errors for optimization problems

        Returns:
        -------
            Error message, if one was found (for creating Error Message Window after it)
        """
        try:
            eps_float = float(self.edit_epsilon.toPlainText())
            bound_left = float(self.bound_left.toPlainText())
            bound_right = float(self.right_bound.toPlainText())
        except ValueError:
            logging.error(ErrorMessage.ERROR_INVALID_VALUE.value)
            return ErrorMessage.ERROR_INVALID_VALUE.value
        func_value = self.edit_target_function.toPlainText()  # str here
        if AppWindow.is_number(func_value):
            if float(func_value) < eps_float:  # here comparing float, because we that such a cast wont cause mistakes
                logging.error(ErrorMessage.ERROR_INCORRECT_TARGET_FUNCTION.value)
                return ErrorMessage.ERROR_INCORRECT_TARGET_FUNCTION.value
        if eps_float <= 0:
            logging.error(ErrorMessage.ERROR_NOT_APPLICABLE_ACCURACY.value)
            return ErrorMessage.ERROR_NOT_APPLICABLE_ACCURACY.value
        if bound_left > bound_right:
            logging.error(ErrorMessage.ERROR_INCORRECT_BOUNDS.value)
            return ErrorMessage.ERROR_INCORRECT_BOUNDS.value
        logging.info("No errors found in current minimization problem")
        return EMPTY_STR

    @staticmethod
    def is_number(str_with_number: str = EMPTY_STR) -> bool:

        """
        Method for determining whether a string is a number
        (advantage compared to isdigit () - correlated processing of real numbers, including in scientific notation)
        """

        try:
            float(str_with_number)
            return True
        except ValueError:
            return False

    @staticmethod
    def show_user_error_mess(error_info: str = EMPTY_STR):

        """
        Method for showing user error message in qt box
        """

        msg = QMessageBox()
        msg.setText(STANDARD_ERROR_MSG)
        msg.setWindowTitle(ERROR_MSG_TITLE)
        msg.setWindowIcon(QIcon(ERROR_WINDOW_ICON))
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)

        msg.setDetailedText(error_info)
        msg.exec_()
