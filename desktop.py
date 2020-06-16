# todo fixed aspect ratio
# todo window icon
# todo add .csv export and import
# todo try using QPaint
# todo splitter
# todo lamda
# todo QAction.trigger
# todo paint onto QScene

import sys
from PySide2.QtWidgets import QApplication, QTableWidget, QMainWindow, QTableWidgetItem, QAction, QHBoxLayout, QFrame, QSplitter, QVBoxLayout, QLabel, QWidget, QTabWidget, QStyleFactory, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide2.QtSvg import QSvgWidget
from PySide2.QtCore import QByteArray, QRect, QObject, Qt, QRectF
from PySide2.QtGui import QColor, QIcon, QKeySequence, QPainter, QFont, QPixmap, QBrush, QImage, QPaintEvent
from chart import build_chart


class Application(QApplication):
    def __init__(self):
        super().__init__()

    def run(self):
        print(QStyleFactory.keys())
        self.setStyle(QStyleFactory.create('windowsvista'))
        main_window = MainWindow()
        sys.exit(self.exec_())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.build_window()

    def build_window(self):

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('cG')
        self.setWindowIcon(QIcon())

        central_widget = CentralWidget()
        self.setCentralWidget(central_widget)

        exit_action = QAction(QIcon(), 'Exit', self)
        exit_action.triggered.connect(self.exit_application)

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(exit_action)

        self.show()

    @staticmethod
    def exit_application():
        Application.quit()


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.build()

    def build(self):

        table_1 = TableWidget(2, 2)
        table_1.setHorizontalHeaderLabels(['A', 'B', 'C'])
        table_1.setCurrentCell(1, 1)
        table_1.setItem(1, 1, QTableWidgetItem('10'))

        table_2 = TableWidget(3, 3)

        chart_1 = SvgWidget()

        chart_2 = Painter()

        char_3 = View()

        tabs = QTabWidget()
        tabs.addTab(table_1, 'Table 1')
        tabs.addTab(table_2, 'Table 2')

        splitter = QSplitter()
        splitter.addWidget(tabs)
        splitter.addWidget(char_3)
        splitter.setSizes([400, 400])

        layout = QHBoxLayout()
        layout.addWidget(splitter)

        self.setLayout(layout)


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
        self.build()

    def build(self):
        svg = build_chart()
        contents = QByteArray(bytearray(svg, encoding='utf-8'))
        self.setPalette(QColor('#bbb'))
        self.renderer().load(contents)  # will also accept SVG file
        # self.setGeometry(0, 0, self.sizeHint().width(), self.sizeHint().height())  # sizeHint reads viewPort
        self.renderer().setViewBox(QRect(-10, -10, self.sizeHint().width() + 20, self.sizeHint().height() + 20))
        # self.heightForWidth(True)  # does not make aspect ratio fixed
        # self.setWindowTitle('compactGantt')
        # self.setWindowIcon()


class Painter(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event: QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(Qt.red))
        qp.setFont(QFont('Arial', 20))

        qp.drawText(10, 50, "hello Python")
        qp.setPen(QColor(Qt.blue))
        qp.drawLine(10, 100, 100, 100)
        qp.drawRect(10, 150, 150, 100)

        qp.setPen(QColor(Qt.yellow))
        qp.drawEllipse(100, 50, 100, 50)
        qp.drawPixmap(220, 10, QPixmap("python.jpg"))
        qp.fillRect(200, 175, 150, 100, QBrush(Qt.SolidPattern))
        qp.end()


class View(QGraphicsView):
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        scene = QGraphicsScene(self)
        rect_a = QRectF(10, 10, 20, 20)
        rect_b = QRect(10, 40, 20, 20)
        rect_c = QRect(10, 70, 20, 20)
        scene.addRect(rect_a)
        scene.addRect(rect_b)
        scene.addRect(rect_c)
        svg_widget = SvgWidget()
        scene.addWidget(svg_widget)
        self.setScene(scene)
        self.setSceneRect(0, 0, svg_widget.sizeHint().width(), svg_widget.sizeHint().height())
        self.setFixedHeight(svg_widget.sizeHint().height())
        # self.setFixedSize(500, 500)

