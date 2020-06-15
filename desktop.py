# todo fixed aspect ratio
# todo window icon
# todo add .csv export and import
# todo try using QPaint
# todo splitter
# todo lamda
# todo QAction.trigger

import sys
from PySide2.QtWidgets import QApplication, QTableWidget, QMainWindow, QTableWidgetItem, QAction, QHBoxLayout, QFrame, QSplitter, QVBoxLayout, QLabel, QWidget
from PySide2.QtSvg import QSvgWidget
from PySide2.QtCore import QByteArray, QRect, QObject
from PySide2.QtGui import QColor, QIcon, QKeySequence
from chart import build_chart


class Application(QApplication):
    def __init__(self):
        super().__init__()

    def run(self):
        main_window = MainWindow()
        sys.exit(self.exec_())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.build()

    def build(self):

        exit_action = QAction(QIcon(), 'Exit', self)
        exit_action.triggered.connect(self.exit_application)

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(exit_action)

        central_widget = CentralWidget()

        self.setCentralWidget(central_widget)
        self.show()

    @staticmethod
    def exit_application():
        Application.quit()


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.build()

    def build(self):

        h_box = QHBoxLayout()

        table_widget = TableWidget(2, 2)
        column_headers = ['A', 'B', 'C']
        table_widget.setHorizontalHeaderLabels(column_headers)
        number = QTableWidgetItem('10')
        table_widget.setCurrentCell(1, 1)
        table_widget.setItem(1, 1, number)

        svg_widget = SvgWidget()

        # splitter = QSplitter()
        # splitter.addWidget(table)
        # splitter.addWidget(frame)

        h_box.addWidget(table_widget)
        h_box.addWidget(svg_widget)

        self.setLayout(h_box)


class TableWidget(QTableWidget):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.cellChanged.connect(self.change_current_cell)
        # self.show()

    def change_current_cell(self):
        row = self.currentRow()
        column = self.currentColumn()
        value = self.item(row, column)
        value = value.text()


class SvgWidget(QSvgWidget):
    def __init__(self):
        super().__init__()
        svg = build_chart()
        contents = QByteArray(bytearray(svg, encoding='utf-8'))
        self.setPalette(QColor('#bbb'))
        self.renderer().load(contents)  # will also accept SVG file
        self.setGeometry(0, 0, self.sizeHint().width(), self.sizeHint().height())  # sizeHint reads viewPort
        self.renderer().setViewBox(QRect(-10, -10, self.sizeHint().width() + 20, self.sizeHint().height() + 20))
        # self.heightForWidth(True)  # does not make aspect ratio fixed
        self.setWindowTitle('compactGantt')
        # self.setWindowIcon()

