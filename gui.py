# todo https://wiki.python.org/moin/PyQt/Creating%20a%20widget%20with%20a%20fixed%20aspect%20ratio

from attr import attrs, attrib
import sys
from PySide2.QtWidgets import QApplication, QSizePolicy
from PySide2.QtSvg import QSvgWidget
from PySide2.QtCore import QByteArray


@attrs  # https://bugreports.qt.io/browse/PYSIDE-1177
class Display(QSvgWidget):

    screen_width = 800
    screen_height = 600

    def load_renderer(self, byte_array):
        self.renderer().load(byte_array)

    def set_screen_size(self):
        self.screen_width = self.screen().availableVirtualSize().width()
        self.screen_height = self.screen().availableVirtualSize().height()

    def set_geometry(self):
        window_x = int(0 * self.screen_width)
        window_y = int(0.2 * self.screen_height)
        window_width = int(0.4 * self.screen_width)
        window_height = int(0.6 * self.screen_height)
        window_geometry = window_x, window_y, window_width, window_height
        self.setGeometry(*window_geometry)  # the asterisk unpacks the tuple


def update_gui(svg='No SVG code found.'):
    gui = QApplication(sys.argv)
    display = Display()
    display.load_renderer(QByteArray(bytearray(svg, encoding='utf-8')))
    display.set_screen_size()
    display.set_geometry()
    display.show()
    sys.exit(gui.exec_())

