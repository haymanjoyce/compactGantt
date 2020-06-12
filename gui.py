# todo fixed aspect ratio
# todo window icon

import sys
from PySide2.QtWidgets import QApplication, QTableWidget, QMainWindow
from PySide2.QtSvg import QSvgWidget
from PySide2.QtCore import QByteArray, QRect
from PySide2.QtGui import QColor


class Chart(QSvgWidget):
    def __init__(self, svg='No SVG passed.'):
        super().__init__()
        contents = QByteArray(bytearray(svg, encoding='utf-8'))
        self.setPalette(QColor('#bbb'))
        self.renderer().load(contents)  # will also accept SVG file
        self.setGeometry(0, 0, self.sizeHint().width(), self.sizeHint().height())  # sizeHint reads viewPort
        self.renderer().setViewBox(QRect(-10, -10, self.sizeHint().width() + 20, self.sizeHint().height() + 20))
        # self.heightForWidth(True)  # does not make aspect ratio fixed
        self.setWindowTitle('compactGantt')
        # self.setWindowIcon()
        self.show()


class Table(QTableWidget):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table = Table(10, 10)
        self.setCentralWidget(self.table)
        self.show()


class Application(QApplication):
    def __init__(self, svg):
        super().__init__()
        self.main_window = MainWindow()
        self.chart = Chart(svg)
        sys.exit(self.exec_())

