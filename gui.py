# todo https://wiki.python.org/moin/PyQt/Creating%20a%20widget%20with%20a%20fixed%20aspect%20ratio

import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtSvg import QSvgWidget
from PySide2.QtCore import QByteArray, QRect


def update_gui(svg='No SVG code found.'):
    gui = QApplication(sys.argv)
    window = QSvgWidget()
    contents = QByteArray(bytearray(svg, encoding='utf-8'))  # will also accept svg file
    window.renderer().load(contents)
    geometry = 100, 100, 800, 600  # x, y, width, height
    window.setGeometry(*geometry)
    print(window.sizeHint())
    print(window.renderer())
    print(window.renderer().matrixForElement('chart'))
    print(window.renderer().boundsOnElement('chart'))  # Returns bounding rectangle of the item with the given id
    # print(window.renderer().framesPerSecond())
    print(window.renderer().viewBox())
    print(window.renderer().viewBoxF())
    window.renderer().setViewBox(QRect(width=200))
    window.show()
    sys.exit(gui.exec_())

