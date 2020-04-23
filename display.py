"""Renders SVG image in on different display types"""

from dataclasses import dataclass, field


@dataclass
class Window:
    """Sets up the GUI window in which the SVG image is displayed"""

    # display dimensions (system should provide this data)
    # display is the display area available on screen
    display_width: int = 800
    display_height: int = 600

    # sets top left corner of window relative to display
    window_x: int = field(init=False, default=10, repr=False)
    window_y: int = field(init=False, default=100, repr=False)

    # sets dimensions of GUI window
    # advice is to select size based on display size (not image size)
    window_width: int = field(init=False, default=800, repr=False)
    window_height: int = field(init=False, default=600, repr=False)

    def __post_init__(self):
        # todo change proportions are for production
        self.window_x = int(0 * self.display_width)
        self.window_y = int(0.2 * self.display_height)
        self.window_width = int(0.4 * self.display_width)
        self.window_height = int(0.6 * self.display_height)

    def get_geometry(self):
        return self.window_x, self.window_y, self.window_width, self.window_height