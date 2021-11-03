from scipy.optimize import minimize_scalar
from tests.test_data import func_2

LABELS_TEXT = {'label': "Choose number of variables",
               'label_epsilon': "Enter calculation accuracy",
               'label_target_function': "Enter target function",
               'label_bounds': "Enter uncertainty interval",
               'label_minimization_method': "Choose optimization method",
               'gif_label': ""}

BUTTONS_TEXT = {'pause_button': "No gif available",
                'restart_prog_button': "New problem",
                'solution_button': "Calculate",
                'exit_button': "Exit"}

EDITS_TEXT = {'edit_target_function': "sin(x)",
              'edit_epsilon': "0.01",
              'bound_left': "1",
              'right_bound': "2"}

RESULT = minimize_scalar(func_2, bounds=[1, 2], method='bounded', options ={'xatol': 0.01}).x
print(RESULT)
