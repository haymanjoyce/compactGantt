from dataclasses import dataclass, field
import shapes


@dataclass
class Geometry:

    # the SVG image to be rendered
    image: str = str()

    # todo you need to give the object the image size and then post init viewBox to match

    # sets top left corner of GUI window relative to display
    GUI_x: int = 10
    GUI_y: int = 100

    # sets dimensions of GUI window
    # advice is to select size based on display size (not image size)
    GUI_width: int = 300
    GUI_height: int = 300

    # should set the dimensions of the root SVG element but seems to have no effect in GUI
    viewPort_width: int = None
    viewPort_height: int = None

    # sets top left corner of viewBox
    # a negative x value will seem to move the SVG image right
    viewBox_x: int = 0
    viewBox_y: int = 0

    # sets viewBox size in GUI
    # defines proportion of visible image on initial rendering
    # the viewBox does not define size of image on screen
    # a 100x100 will show that much of a 300x300 image scaled up to fit, say, a 600x600 window
    # setting values to 0 will cause image to fill GUI window; aspect ration not preserved
    # setting values to more than 0 will cause image to fill to shortest dimension of GUI window; aspect ratio preserved
    # advice, for most applications, is to match size to image size
    viewBox_width: int = 300
    viewBox_height: int = 300

    def __post_init__(self):
        pass

    def get_elements(self):
        return f'<?xml version="1.0" encoding="UTF-8" standalone="no"?> ' \
               f'<svg width="{self.viewPort_width}" height="{self.viewPort_height}" ' \
               f'viewBox="{self.viewBox_x} {self.viewBox_y} {self.viewBox_width} {self.viewBox_height}" ' \
               f'id="" version="1.1" overflow="auto"> ' \
               f'{self.image}' \
               f'</svg>'

