# todo fixed aspect ratio
# todo window icon
# todo add .csv export and import
# todo try using QPaint
# todo splitter

import sys
from PySide2.QtWidgets import QApplication, QTableWidget, QMainWindow, QTableWidgetItem, QAction, QHBoxLayout, QFrame, QSplitter, QVBoxLayout, QLabel, QWidget
from PySide2.QtSvg import QSvgWidget
from PySide2.QtCore import QByteArray, QRect
from PySide2.QtGui import QColor


class Application(QApplication):
    def __init__(self):
        super().__init__()

    def build(self, svg):
        main_window = MainWindow()
        # chart = SvgWidget(svg)
        sys.exit(self.exec_())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.build()

    def build(self):

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')

        exit_action = QAction('Exit', parent=self)
        exit_action.setShortcut('Ctrl+E')
        file_menu.addAction(exit_action)
        exit_action.triggered.connect(self.exit_trigger)

        central_widget = QWidget()
        h_box = QHBoxLayout()

        table_1 = Table(2, 2)
        column_headers = ['A', 'B', 'C']
        table_1.setHorizontalHeaderLabels(column_headers)
        number = QTableWidgetItem('10')
        table_1.setCurrentCell(1, 1)
        table_1.setItem(1, 1, number)

        table_2 = Table(2, 2)
        column_headers = ['x', 'y', 'z']
        table_2.setHorizontalHeaderLabels(column_headers)

        # frame = QFrame()
        # frame.setFrameShape(QFrame.StyledPanel)

        # splitter = QSplitter()
        # splitter.addWidget(table)
        # splitter.addWidget(frame)

        h_box.addWidget(table_1)
        h_box.addWidget(table_2)

        central_widget.setLayout(h_box)

        self.setCentralWidget(central_widget)
        self.show()

    def exit_trigger(self):
        QApplication.quit()


class Table(QTableWidget):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.cellChanged.connect(self.change_current_cell)
        self.show()

    def change_current_cell(self):
        row = self.currentRow()
        column = self.currentColumn()
        value = self.item(row, column)
        value = value.text()


class SvgWidget(QSvgWidget):
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

