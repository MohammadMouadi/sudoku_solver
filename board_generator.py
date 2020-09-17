import copy

from board import Board
from sudoko_solver import SudokuSolver
from random import shuffle


class BoardGenerator:
    def __init__(self):
        self.__solved_board = None

    def generate_unique(self) -> Board:
        solver = SudokuSolver(Board())
        solver.solve()
        self.__solved_board = solver.board.get()

        indices = [(i, j) for i in range(solver.board.length) for j in range(solver.board.length)]
        shuffle(indices)
        for index in indices:
            tmp_board_value = solver.board[index[0]][index[1]]
            solver.board[index[0]][index[1]] = 0

            solver.board.update_indices_to_be_solved()
            if not solver.has_unique_solution():
                solver.board[index[0]][index[1]] = tmp_board_value
                solver.board.update_indices_to_be_solved()
        return solver.board

    @property
    def solved_board(self):
        return copy.deepcopy(self.__solved_board)
