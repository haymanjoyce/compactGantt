"""Classes for building the SVG"""

# todo develop Layout and features
# todo render main boxes which other modules render in more detail

from dataclasses import dataclass, field


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


class Chart:
    """Represents the area where all scale related features are displayed"""

    # equivalent to chart x
    layout_x: float = 100  # we get value from chart.Layout object

    # equivalent to header height
    layout_y: float = 50  # we get value from banners.Layout object

    # equivalent to chart width
    layout_width: float = 1000  # we get value from chart.Layout object

    # equivalent to chart height less sum of banner heights
    layout_height: float = 600  # we  calculate based on data from banners.Layout and chart.Layout

    def clean_layout_data(self):
        pass

    def build_layout(self):
        pass

    def get_layout_object(self):
        return self

    def get_layout_svg(self):
        pass


class TimeWindow:
    """Represents the area where tasks and milestones are displayed"""

    # equivalent to chart width less sum of column widths
    window_width: float = 800  # we get value from Columns.layout

    # equivalent to layout height less sum of scale heights
    window_height: float = 400

    # window start and finish in ordinals
    window_start: int = 0  # note that ordinal dates are at 00:00hrs (day start)
    window_finish: int = 0  # we handle the missing 23:59 hours (you don't need to)

    # equivalent to window width divided by total days (i.e. pixels per day)
    window_resolution: float = float()

    def clean_window_data(self):
        pass

    def build_window(self):
        pass

    def get_window_object(self):
        return self

    def get_window_svg(self):
        pass

