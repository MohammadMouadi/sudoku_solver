import random
import threading
import time
from board import Board
import copy


class GuiSolverThread:
    def __init__(self, window):

        self.__window = window
        self.__grid = window.grid
        self.__grids = self.__grid.grids
        self.__create_board_from_grids()
        self.__original_board = copy.deepcopy(self.__board)
        self.__thread = threading.Thread(target=self.__solve)
        self.__stop_thread = False
        self.__timer = 0.5

    @property
    def timer(self):
        return self.__timer

    @timer.setter
    def timer(self, timer):
        if timer < 0.05:
            timer = 0.05
        self.__timer = timer

    def start(self):
        self.__window.new_game_button.setDisabled(True)
        self.__stop_thread = False
        self.__set_highlighting(False)
        self.__window.solve_button.setText("Stop")
        self.__thread.start()

    def stop(self):
        self.__stop_thread = True
        self.__thread.join()
        self.__restore_original_board()
        self.__set_highlighting(True)

    def __create_board_from_grids(self):
        board = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                if self.__grid.get_grid(i, j) in self.__window.fixed_cells:
                    board[i][j] = int(self.__grid.get_grid(i, j).text()) if self.__grid.get_grid(i, j).text() else 0

        self.__board = Board(board)

    def __solve(self):

        def helper(self):
            if self.__stop_thread:
                return True
            index = self.__first_empty_grid()
            if index is not None:
                candidates = [k for k in range(1, self.__board.length + 1) if self.__is_valid_state(k, index)]
                if not candidates:
                    return False
                random.shuffle(candidates)

                while candidates:
                    candidate = candidates.pop()
                    self.__board[index[0]][index[1]] = candidate
                    self.__grids[index[0]][index[1]].setText(str(candidate))
                    self.__grids[index[0]][index[1]].change_stylesheet("border: 2px solid green;")
                    time.sleep(self.__timer)
                    if helper(self):
                        return True
                    time.sleep(self.__timer)
                    self.__board[index[0]][index[1]] = 0
                    self.__grids[index[0]][index[1]].setText('0')
                    self.__grids[index[0]][index[1]].change_stylesheet("border: 2px solid red;")
                return False
            return True

        helper(self)
        self.__window.new_game_button.setDisabled(False)
        self.__window.solve_button.setText("Solve")
        self.__set_highlighting(True)
        self.__board.update_indices_to_be_solved()

    def __is_valid_state(self, num, index):
        if not self.__is_num_in_row(num, index[0]) and not self.__is_num_in_column(num, index[1]) \
                and not self.__is_num_in_square(num, index):
            return True
        return False

    def __first_empty_grid(self):
        for i in self.__board.indices_to_be_solved:
            if self.__board[i[0]][i[1]] == 0:
                return i
        return None

    def __is_num_in_row(self, num, row):
        for i in range(self.__board.length):
            if self.__board[row][i] == num:
                return True
        return False

    def __is_num_in_column(self, num, col):
        for i in range(self.__board.length):
            if self.__board[i][col] == num:
                return True
        return False

    def __is_num_in_square(self, num, index):
        index = list(index)
        index[0] = index[0] - index[0] % self.__board.square_length
        index[1] = index[1] - index[1] % self.__board.square_length
        for k in range(self.__board.square_length):
            for m in range(self.__board.square_length):
                if self.__board[index[0] + k][index[1] + m] == num:
                    return True
        return False

    def __restore_original_board(self):
        for i in range(9):
            for j in range(9):
                if self.__original_board[i][j] == 0:
                    self.__grid.get_grid(i, j).setText('')
                else:
                    self.__grid.get_grid(i, j).setText(str(self.__original_board[i][j]))

    def __set_highlighting(self, val: bool):
        for i in range(9):
            for j in range(9):
                self.__grid.grids[i][j].highlight_enabled = val
