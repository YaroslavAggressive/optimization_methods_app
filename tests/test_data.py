from math import sin, fabs
from scipy.optimize import minimize_scalar
from dataclasses import dataclass
from typing import List


@dataclass
class Case:
    name: str
    func: str
    interval: list
    accuracy: float
    expected: float

    def __str__(self) -> str:
        return 'test_{}'.format(self.name)


def get_test_cases(func_for_scipy: List, func_for_test: List[str], intervals: List[list],
                   accurs: List[float], names: List):

    """
    Method for generating test cases for testing methods (so far only one-dimensional minimization)

    Parameters:
    ----------
        func_for_scipy: List[function]
            List of function objects to pass to test methods in scipy module
        func_for_test: List[str]
            String functions to pass to sympy module methods
        intervals: List[List]
            Uncertainty intervals for minimization problems
        accurs: List[float]
            List with computational precision with which you want to find the minimum of a function
        names: List[str]
            Test names

    Returns:
    -------
        List of Case-object each of which contains the necessary data for testing methods
    """

    output = []
    for scipy_func, test_func, bounds, name in zip(func_for_scipy, func_for_test, intervals, names):
        for accuracy in accurs:
            expected = minimize_scalar(scipy_func, bounds=bounds, method='bounded', options={'xatol': accuracy}).x
            output.append(Case(name=name + " with accuracy {}".format(accuracy),
                               func=test_func,
                               interval=bounds,
                               accuracy=accuracy,
                               expected=expected))

    return output


multiplier = 10  # initial values for creating a test dataset
orders_number = 14

accuracies = [multiplier**(-i) for i in range(orders_number)]  # list of accuracies for tests


# functions for use in method validation by solving minimization problems using methods from scipy

def func_1(x: float) -> float:
    return x**2


def func_2(x: float) -> float:
    return sin(x)


def func_3(x: float) -> float:
    return fabs(x)


test_functions_for_scipy = [func_1, func_2, func_3]

intervals = [[-2, 2], [3, 5], [0, 1]]  # uncertainty intervals for finding the minimum
# functions similar to previous ones for passing to the implemented minimization methods
test_functions_for_minimize = ["x**2", "sin(x)", "Abs(x)"]

test_names = ["test is always positive function",
              "periodic function test",
              "undifferentiable function test"]

ONE_DIM_MINIMIZATION_DATA = get_test_cases(func_for_scipy=test_functions_for_scipy,
                                           func_for_test=test_functions_for_minimize,
                                           intervals=intervals,
                                           accurs=accuracies,
                                           names=test_names)
print(ONE_DIM_MINIMIZATION_DATA)
