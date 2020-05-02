# todo https://wiki.python.org/moin/PyQt/Creating%20a%20widget%20with%20a%20fixed%20aspect%20ratio

import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtSvg import QSvgWidget
from PySide2.QtCore import QByteArray


def update_gui(svg='No SVG code found.'):
    gui = QApplication(sys.argv)
    window = QSvgWidget()
    window.renderer().load(QByteArray(bytearray(svg, encoding='utf-8')))
    geometry = 100, 100, 800, 600  # x, y, width, height
    window.setGeometry(*geometry)
    window.show()
    sys.exit(gui.exec_())

