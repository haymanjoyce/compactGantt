# todo get rid of base class; switch from inheritance to composition
# todo switch to attrs; get rid of post_init; use attrs features like validation
# todo develop Scales with interface: placement, number of scales, grids to show
# todo make Interval class
# todo add order in as mixin to Scales
# todo add ability to label a scale to Scale
# todo use @property to render svg
# todo test other datetime libraries

from dataclasses import dataclass
from shapes import Rectangle, Line, Text
from labels import date_label
from intervals import select_intervals


@dataclass
class Base:
    """Base class for features"""

    # time window dimensions
    width: float = 800
    height: float = 600

    # time window start and finish in ordinals
    start: int = 0  # note that ordinal dates are at 00:00hrs (day start)
    finish: int = 0  # we handle the missing 23:59 hours (you don't need to)

    # time window resolution (pixels per day)
    window_resolution: float = float()

    # places the scale
    x: float = 0
    y: float = 0

    # defines first day of week as string
    week_start_text: str = str(0)

    # defines first day of week as integer
    week_start_num: int = 0

    # defines interval type
    interval_type: str = str()  # DAYS | WEEKS | MONTHS | QUARTERS | HALVES | YEARS

    # private variable
    interval_data: tuple = tuple()

    def __post_init__(self):

        # if subclass overrides post_init then subclass will need to call these methods manually

        self.clean_scale_data()
        self._pixels_per_day = self.get_window_resolution()
        self.interval_data = self.get_interval_data()

    def clean_scale_data(self):

        # clean start and finish dates
        if self.finish <= self.start or self.start >= self.finish:
            self.finish = self.start + 1

        # clean first day of week string, if given, and converts to integer
        if self.week_start_text in ['6', '7', 'S', 'Sun', 'Sunday', 'SUN', 'SUNDAY']:
            self.week_start_num = 6
        else:
            self.week_start_num = 0

        # clean interval type
        if self.interval_type.lower() in [item.lower() for item in
                                          ['days', 'day', 'd', '']]:  # blank indicates default
            self.interval_type = 'DAYS'
        elif self.interval_type.lower() in [item.lower() for item in ['weeks', 'week', 'wk', 'w']]:
            self.interval_type = 'WEEKS'
        elif self.interval_type.lower() in [item.lower() for item in ['months', 'mon', 'month', 'm']]:
            self.interval_type = 'MONTHS'
        elif self.interval_type.lower() in [item.lower() for item in ['quarters', 'quarts', 'qts', 'q']]:
            self.interval_type = 'QUARTERS'
        elif self.interval_type.lower() in [item.lower() for item in ['halves', 'half', 'halfs', 'halve', 'h']]:
            self.interval_type = 'HALVES'
        elif self.interval_type.lower() in [item.lower() for item in ['years', 'year', 'yrs', 'yr', 'y']]:
            self.interval_type = 'YEARS'
        else:
            raise ValueError(self.interval_type)

    def get_interval_data(self):
        return select_intervals(self.x, self.start, self.finish, self.interval_type, self._pixels_per_day, self.week_start_num)

    def get_window_resolution(self):
        return self.width / (self.finish - self.start)


@dataclass
class Grid(Base):
    """Builds a grid feature"""

    # line styling
    line_color: str = 'black'
    line_width: int = 1
    line_dashing: str = str()  # dash gap dash gap

    def build_grid_lines(self):

        lines = str()
        line = Line()

        line.stroke_color = self.line_color
        line.stroke_width = self.line_width
        line.stroke_dasharray = self.line_dashing

        line.y = self.y
        line.dy = self.y + self.height

        for i in self.interval_data:
            line.x = i[0]
            line.dx = line.x
            lines += line.svg

        # last line
        last_line = self.x + ((self.finish - self.start) * self._pixels_per_day)
        line.x = last_line
        line.dx = last_line
        lines += line.svg

        return lines

    def get_grid_lines(self):
        return f'{self.build_grid_lines()}'

    @property
    def svg(self):
        return self.get_grid_lines()

