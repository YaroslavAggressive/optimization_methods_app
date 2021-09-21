import pytest
from tests.test_data import Case, ONE_DIM_MINIMIZATION_DATA
from backend.one_dimension_minimization import OneDimMinimization
from sympy import parse_expr


@pytest.mark.parametrize('test_example', ONE_DIM_MINIMIZATION_DATA, ids=str)
def test_golden_ratio_method(test_example: Case) -> None:

    """
    Testing Golden Ratio Method
    """

    result_golden = OneDimMinimization.golden_ratio_method(parse_expr(test_example.func),
                                                           test_example.interval,
                                                           test_example.accuracy)
    assert result_golden - test_example.expected < test_example.accuracy


@pytest.mark.parametrize('test_example', ONE_DIM_MINIMIZATION_DATA, ids=str)
def test_bisection_method(test_example: Case) -> None:

    """
    Testing Bisection Method
    """

    result_bisection = OneDimMinimization.bisection_method(parse_expr(test_example.func),
                                                           test_example.interval,
                                                           test_example.accuracy)
    assert result_bisection - test_example.expected < test_example.accuracy


@pytest.mark.parametrize('test_example', ONE_DIM_MINIMIZATION_DATA, ids=str)
def test_dichotomy_method(test_example: Case) -> None:

    """
    Testing Dichotomy Method
    """

    result_bisection = OneDimMinimization.dichotomy_method(parse_expr(test_example.func),
                                                           test_example.interval,
                                                           test_example.accuracy)
    assert result_bisection - test_example.expected < test_example.accuracy


@pytest.mark.parametrize('test_example', ONE_DIM_MINIMIZATION_DATA, ids=str)
def test_fibonacci_method(test_example: Case) -> None:

    """
    Testing Fibonacci Method
    """

    result_fibonacci = OneDimMinimization.fibonacci_method(parse_expr(test_example.func),
                                                           test_example.interval,
                                                           test_example.accuracy)
    assert result_fibonacci - test_example.expected < test_example.accuracy
