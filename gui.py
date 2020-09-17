import sys
from PyQt5.QtWidgets import QApplication
from gui_setup import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.setWindowTitle("Sudoku Solver")
    main_window.setFixedHeight(495)
    main_window.setFixedWidth(495)

    main_window.show()
    main_window.setFocus(True)
    # Start the event loop.
    app.exec_()
