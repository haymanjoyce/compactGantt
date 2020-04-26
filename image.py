"""Classes for converting the image format"""

from dataclasses import dataclass, field
from PySide2.QtCore import QByteArray


@dataclass
class HTML:
    pass


@dataclass
class ByteArray:

    @staticmethod
    def get_byte_array(svg):
        return QByteArray(bytearray(svg, encoding='utf-8'))

