from sudoko_solver import SudokuSolver
from board_generator import BoardGenerator
from board import Board
# board = Board([
#     [0, 9, 1, 4, 7, 0, 0, 0, 0],
#     [5, 7, 0, 0, 6, 0, 0, 0, 0],
#     [0, 8, 0, 0, 0, 0, 9, 0, 0],
#     [6, 0, 8, 0, 0, 0, 5, 0, 2],
#     [0, 0, 9, 0, 2, 0, 0, 6, 4],
#     [0, 0, 4, 5, 0, 0, 0, 8, 0],
#     [0, 0, 5, 6, 4, 0, 0, 3, 0],
#     [0, 0, 0, 3, 1, 0, 6, 0, 5],
#     [0, 0, 3, 9, 0, 0, 0, 0, 0]
# ])

b = BoardGenerator()
b.generate_unique().print_board()



arr = [
    [0, 9, 1, 4, 7, 0, 0, 0, 0],
    [5, 7, 0, 0, 6, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 9, 0, 0],
    [6, 0, 8, 0, 0, 0, 5, 0, 2],
    [0, 0, 9, 0, 2, 0, 0, 6, 4],
    [0, 0, 4, 5, 0, 0, 0, 8, 0],
    [0, 0, 5, 6, 4, 0, 0, 3, 0],
    [0, 0, 0, 3, 1, 0, 6, 0, 5],
    [0, 0, 3, 9, 0, 0, 0, 0, 0]
]