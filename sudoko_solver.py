import random
import copy


class SudokuSolver:
    BOARD_LENGTH = 9
    SQUARE_LENGTH = int(BOARD_LENGTH ** 0.5)

    def __init__(self, board):
        self.__board = board

    @property
    def board(self):
        return self.__board

    def __is_valid_state(self, num, index):
        if not self.__is_num_in_row(num, index[0]) and not self.__is_num_in_column(num, index[1]) \
                and not self.__is_num_in_square(num, index):
            return True
        return False

    def __first_empty_grid(self):
        for i in self.board.indices_to_be_solved:
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

    def __is_valid_board(self):
        for i in self.__board.indices_to_be_solved:
            if self.__board.get_num_at(i) != 0:
                tmp_num = self.__board[i[0]][i[1]]
                self.__board[i[0]][i[1]] = 0
                if not self.__is_valid_state(tmp_num, i):
                    self.__board[i[0]][i[1]] = tmp_num
                    return False
                self.__board[i[0]][i[1]] = tmp_num
        return True

    def solve(self):

        def helper(self):
            index = self.__first_empty_grid()
            if index is not None:
                candidates = [k for k in range(1, self.__board.length + 1) if self.__is_valid_state(k, index)]

                if not candidates:
                    return False

                random.shuffle(candidates)

                while candidates:
                    candidate = candidates.pop()
                    self.__board[index[0]][index[1]] = candidate
                    if helper(self):
                        return True
                    self.__board[index[0]][index[1]] = 0
                return False
            return True

        helper(self)
        self.board.update_indices_to_be_solved()

    def has_unique_solution(self):
        def helper(self, solutions_num=0):
            index = self.__first_empty_grid()
            if index is None:
                solutions_num += 1
                if solutions_num > 1:
                    return False
                return solutions_num
            else:
                candidates = [k for k in range(1, self.__board.length + 1) if self.__is_valid_state(k, index)]
                while candidates:
                    candidate = candidates.pop()
                    self.__board[index[0]][index[1]] = candidate
                    solutions_num = helper(self, solutions_num)
                    self.__board[index[0]][index[1]] = 0
                    if not solutions_num:
                        return False
                return solutions_num == 1

        result = helper(self)
        self.board.update_indices_to_be_solved()
        return result

    def hint(self, index):
        if not self.__is_valid_board():
            return None

        board_tmp = copy.deepcopy(self.__board)
        self.solve()
        hint = self.__board[index[0]][index[1]]
        self.__board = copy.deepcopy(board_tmp)
        return hint

    def is_solved(self):
        if self.__is_valid_board() and self.__first_empty_grid() is None:
            return True
