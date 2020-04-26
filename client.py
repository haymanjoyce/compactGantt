"""Classes representing different clients"""

# todo get screen size from something other than the Qt object

from dataclasses import dataclass
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
class Browser:
    """Represents the browser"""
    pass


@dataclass
class Printer:
    """Represents the printer"""
    pass

