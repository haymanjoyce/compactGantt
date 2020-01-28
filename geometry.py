from dataclasses import dataclass, field
import shapes


@dataclass
class Geometry:

    elements: str = str()

    # sets dimensions of SVG element
    # has no effect on elements it contains
    # GUI appears to ignore it (values do not seem to affect behaviour)
    viewPort_width: int = None
    viewPort_height: int = None

    # offsets viewBox
    # a negative x value will offset it left causing SVG to apparently move right
    viewBox_x: int = 0
    viewBox_y: int = 0

    # sets viewBox size in GUI
    # below this size the SVG elements scale down but aspect ratio is maintained
    # above this size the SVG elements stay the same and padding automatically takes up slack (centre aligned)
    viewBox_width: int = 800
    viewBox_height: int = 400

    # sets top left corner of GUI window relative to display
    x: int = 50
    y: int = 50

    # defines "padding" (my conception) between GUI window edge and SVG element edge
    padding: int = field(default=100)

    # sets dimensions of GUI window
    GUI_width: int = field(default=800, init=False)
    GUI_height: int = field(default=600, init=False)

    def __post_init__(self):
        self.GUI_width = self.viewBox_width + self.padding
        self.GUI_height = self.viewBox_height + self.padding

    def get_elements(self):
        return f'<?xml version="1.0" encoding="UTF-8" standalone="no"?> ' \
               f'<svg width="{self.viewPort_width}" height="{self.viewPort_height}" ' \
               f'viewBox="{self.viewBox_x} {self.viewBox_y} {self.viewBox_width} {self.viewBox_height}" ' \
               f'id="" version="1.1" overflow="auto"> ' \
               f'{self.elements}' \
               f'</svg>'

