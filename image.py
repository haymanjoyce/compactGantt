"""Classes for handling the image"""

from dataclasses import dataclass, field
from PySide2.QtCore import QByteArray


@dataclass
class Image:
    """Handles image and creates images of chart in various formats"""

    # the SVG image to be rendered
    image: str = str()

    # image dimensions (user defined)
    image_width: int = 800
    image_height: int = 600

    # margin (around image) defines size of viewBox
    # more accurately, it is: "panning back so that you see this much pixels around image border"
    margin: int = field(init=False, repr=False, default=100)

    # should set the dimensions of the root SVG element but seems to have no effect in GUI
    viewPort_width: int = field(default=None, repr=False, init=False)
    viewPort_height: int = field(default=None, repr=False, init=False)

    # sets top left corner of viewBox
    # a negative x value will seem to move the SVG image right
    viewBox_x: int = field(init=False, repr=False)
    viewBox_y: int = field(init=False, repr=False)

    # sets viewBox size in GUI
    # defines proportion of visible image on initial rendering
    # the viewBox does not define size of image on screen
    # 100x100 will show that much of a 300x300 image scaled up to fit, say, a 600x600 window
    # 400 x 400 will show a 200x200 image taking up 0.5x0.5 (i.e. 0.25 area) of the window
    # setting values to 0 will cause image to fill GUI window; aspect ration not preserved
    # setting values to more than 0 will cause image to fill to shortest dimension of GUI window; aspect ratio preserved
    viewBox_width: int = field(init=False, repr=False)
    viewBox_height: int = field(init=False, repr=False)

    def __post_init__(self):

        # this will calculate margin n pixels
        self.margin = int(0.1 * self.image_width)

        # this will expand the viewBox by value of padding
        self.viewBox_width = int(self.image_width + self.margin)
        self.viewBox_height = int(self.image_height + self.margin)

        # this will centre the image in the viewBox
        offset = int(self.margin * -0.5)
        self.viewBox_x = offset
        self.viewBox_y = offset

    def get_svg(self):
        return f'<svg width="{self.viewPort_width}" height="{self.viewPort_height}" ' \
               f'viewBox="{self.viewBox_x} {self.viewBox_y} {self.viewBox_width} {self.viewBox_height}" ' \
               f'id="" version="1.1" overflow="auto"> ' \
               f'{self.image}' \
               f'</svg>'

    def get_byte_array(self):
        return QByteArray(bytearray(self.get_svg(), encoding='utf-8'))

