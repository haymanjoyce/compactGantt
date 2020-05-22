# todo fix aspect ratio
# todo window icon

import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtSvg import QSvgWidget
from PySide2.QtCore import QByteArray, QRect
from PySide2.QtGui import QColor


def display(svg='No SVG code found.'):
    gui = QApplication(sys.argv)
    window = QSvgWidget()
    contents = QByteArray(bytearray(svg, encoding='utf-8'))
    window.setPalette(QColor('#bbb'))
    window.renderer().load(contents)  # will also accept SVG file
    window.setGeometry(0, 0, window.sizeHint().width(), window.sizeHint().height())  # sizeHint reads viewPort
    window.renderer().setViewBox(QRect(-10, -10, window.sizeHint().width() + 20, window.sizeHint().height() + 20))
    # window.heightForWidth(True)  # does not fix aspect ratio
    window.setWindowTitle('CompactGantt')
    # window.setWindowIcon()
    window.show()
    sys.exit(gui.exec_())

