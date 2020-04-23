"""Is the main chart features"""

# todo develop Layout and features
# todo render main boxes which other modules render in more detail


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


class Window:
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
