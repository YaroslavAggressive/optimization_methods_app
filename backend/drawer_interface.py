from abc import abstractmethod


class DrawerInterface:

    """
    Interface for minimization renderer classes
    to separate implementations of rendering minimization on a plane, in space and in n-dimensional space
    """

    @abstractmethod
    def draw_graph_of_function(self): raise NotImplementedError

    @abstractmethod
    def draw_colored_axes(self): raise NotImplementedError

    @abstractmethod
    def draw_point(self, iteration: int, annotation: str, point_x: float, point_y: float): raise NotImplementedError

    @abstractmethod
    def update_bounds(self, bounds: list): raise NotImplementedError

    @abstractmethod
    def calculate_function_graph(self): raise NotImplementedError
