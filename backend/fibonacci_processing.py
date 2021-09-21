from enum import Enum
from logging import Logger


class ErrorFibonacci(Enum):
    ERROR_NEGATIVE_INDEX = "Fibonacci numbers in a sequence cannot have negative indices"
    ERROR_NEGATIVE_NUMBER = "There are no negative numbers in the fibonacci sequence"
    ERROR_MATRIX_DIMENSIONS = "Cannot be raised to a power of a non-square matrix"
    ERROR_EMPTY_MATRIX = "Empty matrix was passed"
    ERROR_NEGATIVE_POWER = "Matrices cannot be raised to negative powers"


EMPTY_STR = ""
FIBONACCI_ZERO = 0
FIBONACCI_ONE = 1
FIBONACCI_INDEX_OF_ZERO = 1
FIBONACCI_SECOND_ONE_INDEX = 2
FIBONACCI_INITIALS = 3
FIBONACCI_MATRIX_SIZE = 2
FIBONACCI_INIT_MATRIX = [[1, 1],
                         [1, 0]]  # to optimize calculation of the Fibonacci number in terms of time and memory,
# we use matrices, in particular, [[1, 1], [1, 0]]


class FibonacciMethods:

    """
    Class that combines methods of working with fibonacci numbers

    Parameters:
    ----------
    error_msg: str

    """

    error_msg = EMPTY_STR
    logger = Logger(EMPTY_STR)

    @staticmethod
    def nearest_fibonacci_number(n: int = 0) -> int:

        """
        Method of obtaining the fibonacci number closest to the given human number

        Parameters:
        ----------
        n: int
            Fibonacci number to get

        Returns:
        -------
            Fibonacci number index in a row
        """

        if n < 0:
            FibonacciMethods.logger.error(ErrorFibonacci.ERROR_NEGATIVE_NUMBER.value)
            FibonacciMethods.error_msg = ErrorFibonacci.ERROR_NEGATIVE_NUMBER.value
            return 0
        f_2 = FIBONACCI_ONE
        f_3 = f_2 + f_2

        while f_3 < n:
            f_1 = f_2
            f_2 = f_3
            f_3 = f_2 + f_1

        return f_3

    @staticmethod
    def index_of_fibonacci(n: int) -> int:

        """
        Method of obtaining the index of the number of fibonacci in a row

        Parameters:
        ----------
        n: int
            Fibonacci number to get

        Returns:
        -------
            Fibonacci number index in a row
        """
        if n < 0:
            FibonacciMethods.logger.error(ErrorFibonacci.ERROR_NEGATIVE_INDEX.value)
            FibonacciMethods.error_msg = ErrorFibonacci.ERROR_NEGATIVE_INDEX.value
            return 0
        elif n == FIBONACCI_ZERO:
            return FIBONACCI_INDEX_OF_ZERO
        elif n == FIBONACCI_ONE:
            return FIBONACCI_SECOND_ONE_INDEX
        else:
            f_2 = FIBONACCI_ONE
            f_3 = f_2 + f_2
            i = FIBONACCI_INITIALS
            while f_3 <= n:
                f_1 = f_2
                f_2 = f_3
                f_3 = f_2 + f_1
                i += 1

            return i

    @staticmethod
    def matrix_to_pow(matrix: list = None, n: int = 0) -> list:

        """
        Method of raising the matrix "matrix" to the power "n"

        Parameters:
        ----------
        matrix: list
            Matrix to be raised to the power
        n: int
            Power of matrix

        Returns:
        -------
            Matrix in entered power in list-of-lists format
        """
        if not matrix:
            FibonacciMethods.logger.error(ErrorFibonacci.ERROR_EMPTY_MATRIX.value)
            FibonacciMethods.error_msg = ErrorFibonacci.ERROR_EMPTY_MATRIX.value
            return []
        elif n < 0:
            FibonacciMethods.logger.error(ErrorFibonacci.ERROR_NEGATIVE_POWER.value)
            FibonacciMethods.error_msg = ErrorFibonacci.ERROR_NEGATIVE_POWER.value
            return []
        elif len(matrix) != len(matrix[0]):
            FibonacciMethods.logger.error(ErrorFibonacci.ERROR_MATRIX_DIMENSIONS.value)
            FibonacciMethods.error_msg = ErrorFibonacci.ERROR_MATRIX_DIMENSIONS.value
            return []
        elif n == 0:
            return FibonacciMethods.identity_matrix(FIBONACCI_MATRIX_SIZE)
        elif n == 1:
            return matrix
        else:
            matrix_in_power = FibonacciMethods.matrix_to_pow(matrix, n // 2)
            matrix_in_power = FibonacciMethods.matrix_multiply(matrix_in_power, matrix_in_power)
            if n % 2:
                matrix_in_power = FibonacciMethods.matrix_multiply(matrix, matrix_in_power)
            return matrix_in_power

    @staticmethod
    def identity_matrix(n) -> list:

        """
        Method for creating an n-by-n identity matrix

        Parameters:
        ----------
        n: int
            Matrix ros/column size

        Returns:
        -------
            n x n identity matrix
        """

        r = list(range(n))
        return [[1 if i == j else 0 for i in r] for j in r]

    @staticmethod
    def matrix_multiply(matrix_1: list, matrix_2: list) -> list:

        """
        Matrix multiplication method

        Parameters:
        ----------
        matrix_1: list
            First matrix for multiplication
        matrix_2: list
            Second  matrix for multiplication

        Returns:
        -------
            New matrix - result of multiplication
        """

        matrix_2_t = list(zip(*matrix_2))
        result = []
        for row_1 in matrix_1:
            new_col = []
            for col_2 in matrix_2_t:
                new_col.append(sum(elem_1 * elem_2 for elem_1, elem_2 in zip(row_1, col_2)))
            result.append(new_col)
        return result

    @staticmethod
    def get_fibonacci_number(n: int = 0) -> int:

        """
        Helper fibonacci method (for separating recursion and returning the result)

        Parameters:
        ----------
        n: int
            Number of fibonacci number in sequence

        Returns:
        -------
            Fibonacci number in the sequence under the entered number
        """
        if n < 0:
            FibonacciMethods.logger.error(ErrorFibonacci.ERROR_NEGATIVE_NUMBER.value)
            FibonacciMethods.error_msg = ErrorFibonacci.ERROR_NEGATIVE_NUMBER.value
            return 1
        fibonacci = FibonacciMethods.matrix_to_pow(FIBONACCI_INIT_MATRIX, n)
        return fibonacci[0][1]
