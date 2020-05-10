# todo fix aspect ratio
# todo window icon

import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtSvg import QSvgWidget, QSvgRenderer
from PySide2.QtCore import QByteArray, QRect


def display_chart(svg='No SVG code found.'):
    gui = QApplication(sys.argv)
    window = QSvgWidget()
    contents = QByteArray(bytearray(svg, encoding='utf-8'))  # will also accept svg file
    window.renderer().load(contents)
    window.setGeometry(0, 0, window.sizeHint().width(), window.sizeHint().height())  # sizeHint from viewPort
    window.renderer().setViewBox(QRect(-10, -10, window.sizeHint().width() + 20, window.sizeHint().height() + 20))
    # window.heightForWidth(True)  # does not fix aspect ratio
    window.setWindowTitle('CompactGantt')
    # window.setWindowIcon()
    window.show()
    sys.exit(gui.exec_())

