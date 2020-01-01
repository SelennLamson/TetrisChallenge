import numpy as np
import random as rd


class Tetrominos:
    def __init__(self, id, array):
        self.__id = id
        self.__array = array

    @property
    def id(self):
        return self.__id

    @property
    def array(self):
        return self.__array

    @array.setter
    def array(self, array):
        self.__array = array



class Model:
    EMPTY = 0
    TETRO_I = Tetrominos(1, np.array([[0, 0, 1, 0],
                                      [0, 0, 1, 0],
                                      [0, 0, 1, 0],
                                      [0, 0, 1, 0]]))
    TETRO_J = Tetrominos(2, np.array([[0, 0, 1],
                                      [0, 0, 1],
                                      [0, 1, 1]]))
    TETRO_L = Tetrominos(3, np.array([[0, 1, 0],
                                      [0, 1, 0],
                                      [0, 1, 1]]))
    TETRO_O = Tetrominos(4, np.array([[1, 1],
                                      [1, 1]]))
    TETRO_S = Tetrominos(5, np.array([[0, 0, 0],
                                      [0, 1, 1],
                                      [1, 1, 0]]))
    TETRO_T = Tetrominos(6, np.array([[0, 0, 1],
                                      [0, 1, 1],
                                      [0, 0, 1]]))
    TETRO_Z = Tetrominos(7, np.array([[0, 0, 0],
                                      [1, 1, 0],
                                      [0, 1, 1]]))
    TETROS = [TETRO_I, TETRO_J, TETRO_L, TETRO_O, TETRO_S, TETRO_T, TETRO_Z]

    def __init__(self):
        self.__grid = np.zeros((30, 10), dtype=np.uint8)
        self.__held_tetro = None
        self.__current_tetro = None
        self.__current_tetro_position = None
        self.__current_tetro_rotation = 0
        self._play_tetro(rd.choice(Model.TETROS))
        self.__next_tetro = rd.choice(Model.TETROS)
        self.__score = 0
        self.__time_counter = 0

    @property
    def grid(self):
        grid = self.__grid.copy()
        tetro_height, tetro_width = self.current_tetro.array.shape
        tetro_x, tetro_y = self.current_tetro_position
        grid[tetro_x:tetro_x + tetro_width, tetro_y:tetro_y + tetro_height] += self.current_tetro.array

        return grid

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
    def held_tetro(self):
        return self.__held_tetro

    @property
    def time_counter(self):
        return self.__time_counter

    @property
    def score(self):
        return self.__score

    def rotate(self):
        self.__current_tetro.array = np.rot90(self.__current_tetro.array)

    def left(self):
        pos = list(self.current_tetro_position)
        pos[1] -= 1
        if not self.collide(pos):
            self.__current_tetro_position = pos

    def right(self):
        pos = list(self.current_tetro_position)
        pos[1] += 1
        if not self.collide(pos):
            self.__current_tetro_position = pos

    def hold(self):
        if self.held_tetro is None:
            self.__held_tetro = self.current_tetro
            self._play_tetro(self.next_tetro)
            self.__next_tetro = rd.choice(Model.TETROS)
        else:
            tetro = self.held_tetro
            self.__held_tetro = self.current_tetro
            self._play_tetro(tetro)

    def instant_descent(self):
        pass

    def tick(self):
        pos = list(self.current_tetro_position)
        pos[0] -= 1
        if not self.collide(pos):
            self.__current_tetro_position = pos

        self.__time_counter += 1

    def collide(self, pos=None):
        if pos is None:
            pos = self.current_tetro_position
        return False

    def _play_tetro(self, tetro):
        self.__current_tetro = tetro
        self.__current_tetro_position = [23, 4]
        self.__current_tetro_rotation = 0
