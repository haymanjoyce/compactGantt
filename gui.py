"""Classes representing different GUI windows"""

from dataclasses import dataclass, field
from PySide2.QtSvg import QSvgWidget
from PySide2.QtCore import QByteArray
from collections import namedtuple


@dataclass
class Screen:
    """Represents the device screen"""

    screen_width: int = 800
    screen_height: int = 600

    @staticmethod
    def get_screen_size(widget):
        Size = namedtuple('Size', ['width', 'height'])
        size = Size(widget.screen().availableSize().width(), widget.screen().availableSize().height())
        return size


@dataclass
class ByteArray:

    @staticmethod
    def get_byte_array(svg):
        return QByteArray(bytearray(svg, encoding='utf-8'))


@dataclass
class Display(QSvgWidget):
    """Represents window on which image is displayed"""

    # display dimensions (system should provide this data)
    # display is the display area available on screen
    screen_width: int = 0
    screen_height: int = 0

    def load_renderer(self, byte_array):
        self.renderer().load(byte_array)

    def set_screen_size(self, screen_size):
        self.screen_width = screen_size.width
        self.screen_height = screen_size.height

    def set_geometry(self):
        window_x = int(0 * self.screen_width)
        window_y = int(0.2 * self.screen_height)
        window_width = int(0.4 * self.screen_width)
        window_height = int(0.6 * self.screen_height)
        window_geometry = window_x, window_y, window_width, window_height
        self.setGeometry(*window_geometry)  # the asterisk unpacks the tuple

