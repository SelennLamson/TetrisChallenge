import numpy as np


class Grid:
    def __init__(self):
        self.__grid = np.zeros((30, 10))


class Model:
    EMPTY = 0
    TETRO_T = 1
    TETRO_L = 2
    TETRO_J = 3
    TETRO_O = 4
    TETRO_S = 5
    TETRO_Z = 6
    TETRO_I = 7

    def __init__(self):
        self.__grid = Grid()
        self.__held_tetro = None
        self.__current_tetro = None
        self.__current_tetro_rotation = None
        self.__current_tetro_position = None
        self.__next_tetro = None

    @property
    def grid(self):
        return self.__grid

    @property
    def next_tetro(self):
        return self.__next_tetro

    @property
    def current_tetro(self):
        return self.__current_tetro

    @property
    def current_tetro_position(self):
        return self.__current_tetro_position

    @property
    def current_tetro_rotation(self):
        return self.__current_tetro_rotation

    @property
    def time_counter(self):
        pass

    @property
    def score(self):
        pass

    def rotate(self):
        pass

    def left(self):
        pass

    def right(self):
        pass

    def hold(self):
        pass

    def fast_descent(self):
        pass

    def instant_descent(self):
        pass

    def tick(self):
        pass
