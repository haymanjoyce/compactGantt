from dataclasses import dataclass, field
import shapes


@dataclass
class Geometry:

    # the SVG image to be rendered
    image: str = str()

    # image dimensions (user defined)
    image_width: int = 300
    image_height: int = 300

    # padding defines size of viewBox
    # more accurately, it is: "panning back so that you see this much pixels around image border"
    # todo make padding proportionate to display size
    padding: int = 100

    # display dimensions (system should provide this data)
    # todo https://stackoverflow.com/questions/3129322/how-do-i-get-monitor-resolution-in-python
    display_width: int = 600
    display_height: int = 600

    # sets top left corner of GUI window relative to display
    # todo make proportional to display size
    GUI_x: int = 10
    GUI_y: int = 100

    # sets dimensions of GUI window
    # advice is to select size based on display size (not image size)
    GUI_width: int = 300
    GUI_height: int = 300

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

        # this will expand the viewBox by value of padding
        self.viewBox_width = self.image_width + self.padding
        self.viewBox_height = self.image_height + self.padding

        # this will centre the image in the viewBox
        offset = int(self.padding * -0.5)
        self.viewBox_x = offset
        self.viewBox_y = offset

    def get_elements(self):
        return f'<?xml version="1.0" encoding="UTF-8" standalone="no"?> ' \
               f'<svg width="{self.viewPort_width}" height="{self.viewPort_height}" ' \
               f'viewBox="{self.viewBox_x} {self.viewBox_y} {self.viewBox_width} {self.viewBox_height}" ' \
               f'id="" version="1.1" overflow="auto"> ' \
               f'{self.image}' \
               f'</svg>'

