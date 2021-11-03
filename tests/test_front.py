from PyQt5.QtWidgets import QLabel, QPushButton, QTextEdit
# from PyQt5 import QtWidgets
# import sys
from PyQt5.QtCore import Qt
from front.gui import AppWindow
from tests.test_front_data import LABELS_TEXT, BUTTONS_TEXT, EDITS_TEXT, RESULT


def test_correct_input(qtbot):

    """
    Method for testing correct creating application window labels and filling them with text

    Parameters:
    ----------
    qtbot: QtBot
        bot to simulate user keystrokes
    """
    test_app = AppWindow()

    qtbot.addWidget(test_app)

    line_edits = test_app.findChildren(QTextEdit)
    for editor in line_edits:
        editor.setText(EDITS_TEXT[editor.objectName()])

    qtbot.mouseClick(test_app.solution_button, Qt.LeftButton)
    assert test_app.results_table.rowCount() == 1

    concatenated_interval = "[" + test_app.bound_left.toPlainText() + ", " + test_app.right_bound.toPlainText() + "]"

    # processing each table cell manually so as not to write an interval gluer into one line of two numbers
    assert test_app.results_table.item(0, 0).text() == EDITS_TEXT[test_app.edit_target_function.objectName()]
    assert test_app.results_table.item(0, 1).text() == concatenated_interval
    assert test_app.results_table.item(0, 2).text() == EDITS_TEXT[test_app.edit_epsilon.objectName()]
    assert float(test_app.results_table.item(0, 3).text()) - RESULT < float(test_app.edit_epsilon.toPlainText())


def test_initializing_app():

    """
    Method for checking the correct filling of all fields of the program interface
    """

    test_app = AppWindow()

    # checking button and label correct filling
    labels = test_app.findChildren(QLabel)
    for label in labels:
        assert label.text() == LABELS_TEXT[label.objectName()]

    buttons = test_app.findChildren(QPushButton)
    for btn in buttons:
        assert btn.text() == BUTTONS_TEXT[btn.objectName()]

