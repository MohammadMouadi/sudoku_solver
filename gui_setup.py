from PyQt5 import QtGui, QtWidgets

from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QSlider
from PyQt5.Qt import Qt
from PyQt5.QtGui import QFont

from gui_solver_thread import GuiSolverThread
from board_generator import BoardGenerator


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setMouseTracking(True)
        self.__grid = Grid()
        self.__fixed_cells = []
        self.mouse_location = None
        self.__layout = QVBoxLayout()
        self.__layout.addLayout(self.__grid)

        self.__buttons_layout = QHBoxLayout()

        self.__new_game_button = QPushButton('New Game')
        self.__solve_button = QPushButton('Solve')

        self.__time_controlling_slider = QSlider(Qt.Horizontal, self)
        self.__time_controlling_slider.setRange(0, 10)
        self.__time_controlling_slider.setFocusPolicy(Qt.NoFocus)
        self.__time_controlling_slider.setPageStep(1)
        self.__slider_value = 1
        self.__time_controlling_slider.valueChanged.connect(self.__update_timer)

        self.__buttons_layout.addWidget(self.__new_game_button)
        self.__new_game_button.clicked.connect(self.__create_new_game)
        self.__solve_button.clicked.connect(self.__solve_board)
        self.__buttons_layout.addWidget(self.__solve_button)

        self.__layout.addLayout(self.__buttons_layout)
        self.__layout.addWidget(self.__time_controlling_slider)

        self.__board = None

        widget = QWidget()
        widget.setLayout(self.__layout)
        self.setCentralWidget(widget)

        self.__solver = None

    @property
    def new_game_button(self):
        return self.__new_game_button

    @property
    def grid(self):
        return self.__grid

    @property
    def slider(self):
        return self.__time_controlling_slider

    @property
    def solve_button(self):
        return self.__solve_button

    @property
    def fixed_cells(self):
        return self.__fixed_cells

    @property
    def board(self):
        return self._board

    def __update_timer(self):
        if self.__solver is not None:

            self.__slider_value = 1 - self.__time_controlling_slider.value() / 10
            self.__solver.timer = self.__slider_value

        else:
            self.__slider_value = 1 - self.__time_controlling_slider.value() / 10

    def __solve_board(self):
        if self.__solve_button.text() == 'Solve':
            self.__solver = GuiSolverThread(self)
            self.__solver.timer = self.__slider_value
            self.__solver.start()
        else:
            self.__solver.stop()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        pos = QtGui.QCursor.pos()
        widget = QtWidgets.qApp.widgetAt(pos)
        if isinstance(widget,Label) and widget not in self.__fixed_cells and self.__board:
            index=self.__grid.get_index(widget)
            self.__grid.grids[index[0]][index[1]].setText(str(self.__board[index[0]][index[1]]))

    def keyPressEvent(self, event):
        digits = list(map(str, range(10)))
        pos = QtGui.QCursor.pos()
        widget = QtWidgets.qApp.widgetAt(pos)
        if not isinstance(widget, Label):
            return
        try:
            if chr(event.key()) in digits and widget not in self.__fixed_cells:
                if chr(event.key()) != '0':
                    if self.__is_valid_state(chr(event.key()),widget):
                        widget.setText(chr(event.key()))
                else:
                    widget.setText('')
        except ValueError:
            pass

    def __is_valid_state(self,num,widget):
        index = self.__grid.get_index(widget)
        if not self.__is_num_in_row(num, index[0]) and not self.__is_num_in_column(num, index[1]) \
                and not self.__is_num_in_square(num, index):
            return True
        return False

    def __is_num_in_row(self, num, row):
        for i in range(9):
            if self.__grid.grids[row][i].text() == num:
                return True
        return False

    def __is_num_in_column(self, num, col):
        for i in range(9):
            if self.__grid.grids[i][col].text() == num:
                return True
        return False

    def __is_num_in_square(self, num, index):
        index = list(index)
        index[0] = index[0] - index[0] % 3
        index[1] = index[1] - index[1] % 3
        for k in range(3):
            for m in range(3):
                if self.__grid.grids[index[0] + k][index[1] + m].text() == num:
                    return True
        return False





    def __create_new_game(self):
        self.__fixed_cells = []
        self.__grid.initiate_grid_cells()
        board_generator = BoardGenerator()
        board = board_generator.generate_unique()

        self.__board = board_generator.solved_board
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    self.__grid.get_grid(i, j).change_stylesheet(Label.FIXED_CELL_STYLESHEET)
                    self.__grid.get_grid(i, j).setText(str(board[i][j]))
                    self.__fixed_cells.append(self.__grid.get_grid(i, j))


class Grid(QGridLayout):
    BOARD_LENGTH = 9

    def __init__(self, ):
        super(Grid, self).__init__()
        self.__grids = [[None for _ in range(9)] for _ in range(9)]
        self.__create_grids(Grid.BOARD_LENGTH)
        self.setSpacing(0)
        lines = QtGui.QPainter()
        lines.drawLine(20, 20, 200, 200)

    def __create_grids(self, length):
        for i in range(length):
            for j in range(length):
                label = Label()
                font = QFont('Arial font')
                font.setBold(True)
                label.setFont(font)
                self.addWidget(label, i, j)
                self.__grids[i][j] = label

    def initiate_grid_cells(self):
        for i in range(9):
            for j in range(9):
                self.__grids[i][j].setText('')
                self.__grids[i][j].change_stylesheet(Label.DEFAULT_STYLESHEET)

    def get_grid(self, i, j):
        return self.__grids[i][j]

    def get_index(self, grid):
        for i in range(9):
            for j in range(9):
                if self.__grids[i][j] == grid:
                    return i, j

    @property
    def grids(self):
        return self.__grids

    def get_index_from_grid_number(self, num):
        i = (num - 1) // Label.BOARD_LENGTH
        j = (num - 1) % Label.BOARD_LENGTH
        return (i, j)


class Label(QLabel):
    BOARD_LENGTH = 9
    HIGHLIGHTED_COLOR_STYLESHEET = "background-color: lightblue;"
    DEFAULT_STYLESHEET = "border: 2px solid black;"
    FIXED_CELL_STYLESHEET = "border: 2px solid blue;"
    TARGET_STYLESHEET = "border: 2px solid Green;"

    def __init__(self):
        super(Label, self).__init__()
        self.setAlignment(Qt.AlignCenter)
        self.__stylesheet = Label.DEFAULT_STYLESHEET
        self.__highlighted_stylesheet = self.__stylesheet + Label.HIGHLIGHTED_COLOR_STYLESHEET
        self.setStyleSheet(self.__stylesheet)
        self.__highlight_enabled = True

    @property
    def highlight_enabled(self):
        return self.__highlight_enabled

    @highlight_enabled.setter
    def highlight_enabled(self, val: bool):
        self.__highlight_enabled = val

    def change_stylesheet(self, stylesheet):
        self.__stylesheet = stylesheet
        self.__highlighted_stylesheet = self.__stylesheet + Label.HIGHLIGHTED_COLOR_STYLESHEET
        self.setStyleSheet(self.__stylesheet)

    @property
    def stylesheet(self):
        return self.__stylesheet

    @property
    def highlight_stylesheet(self):
        return self.__highlighted_stylesheet

    def enterEvent(self, event):
        if self.__highlight_enabled:
            self.setStyleSheet(self.__highlighted_stylesheet)
            self.highlight_related_cells(True)

    def leaveEvent(self, event):
        if self.__highlight_enabled:
            self.setStyleSheet(self.__stylesheet)
            self.highlight_related_cells(False)

    def highlight_related_cells(self, enter: bool):
        index = self.parent().children().index(self)
        row = (index - 1) // Label.BOARD_LENGTH
        col = (index - 1) % Label.BOARD_LENGTH
        square = (row - row % 3, col - col % 3)
        for i in range(9):
            if isinstance(self.parent().children().__getitem__(row * 9 + i + 1), Label):
                label = self.parent().children().__getitem__(row * 9 + i + 1)
                if enter:
                    label.setStyleSheet(label.highlight_stylesheet)
                else:
                    label.setStyleSheet(label.stylesheet)
            if isinstance(self.parent().children().__getitem__(i * 9 + col + 1), Label):
                label = self.parent().children().__getitem__(i * 9 + col + 1)
                if enter:
                    label.setStyleSheet(label.highlight_stylesheet)
                else:
                    label.setStyleSheet(label.stylesheet)

        for i in range(3):
            for j in range(3):
                if isinstance(self.parent().children().__getitem__(((square[0] + i) * 9) + (square[1] + j) + 1), Label):
                    label = self.parent().children().__getitem__(((square[0] + i) * 9) + (square[1] + j) + 1)
                    if enter:
                        label.setStyleSheet(label.highlight_stylesheet)
                    else:
                        label.setStyleSheet(label.stylesheet)
