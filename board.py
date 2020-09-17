import copy
from itertools import product


class Board:

    def __init__(self, board=None):
        if board is None:
            default_board_length = 9
            board = [[0 for _ in range(default_board_length)] for _ in range(default_board_length)]
            self.__board = board
            self.__length = len(self.__board)
            self.__square_length = int((self.__length ** 0.5))

        else:
            self.__board = board
            self.__length = len(self.__board)
            self.__square_length = int((self.__length ** 0.5))

        self.update_indices_to_be_solved()

    @property
    def indices_to_be_solved(self):
        return copy.deepcopy(self.__indices_to_be_solved)

    def get(self):
        return copy.deepcopy(self.__board)

    @property
    def length(self):
        return self.__length

    @property
    def square_length(self):
        return self.__square_length

    def __getitem__(self, item):
        return self.__board[item]

    def update_indices_to_be_solved(self):
        indices = []
        for i in range(self.length):
            for j in range(self.length):
                if self.__board[i][j] == 0:
                    indices.append((i, j))
        self.__indices_to_be_solved = indices

    def print_board(self):
        items_iterated_over = 0
        print("\n===================================", end='')
        for i in range(self.length):
            for j in range(self.length):
                items_iterated_over += 1
                if j == 0:
                    print()
                if j % self.square_length == 0:
                    print("| ", end='')

                if self.__board[i][j] == 0:
                    str_to_print = '  '
                elif not (i, j) in self.indices_to_be_solved:
                    str_to_print = '.' + str(self.__board[i][j])
                else:
                    str_to_print = ' ' + str(self.__board[i][j])

                print(str_to_print, end=' ')

                if j == self.length - 1:
                    print("| ", end='')

                if items_iterated_over == self.square_length * self.length:
                    print("\n===================================", end='')
                    items_iterated_over = 0
