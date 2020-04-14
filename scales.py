# todo add ability to label a scale to Scale
# todo drop post_init
# todo add placement and order to Scale
# todo lift work from Base and children to Layout
# todo create interval object

from dataclasses import dataclass
from shapes import Rectangle, Line, Text
from dates import select_scale, convert_ordinal


@dataclass
class Layout:
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


@dataclass
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


@dataclass
class Base:
    """Base class for features"""

    # time window dimensions
    window_width: float = 800
    window_height: float = 600

    # time window start and finish in ordinals
    window_start: int = 0  # note that ordinal dates are at 00:00hrs (day start)
    window_finish: int = 0  # we handle the missing 23:59 hours (you don't need to)

    # time window resolution (pixels per day)
    window_resolution: float = float()

    # places the scale
    scale_x: float = 0
    scale_y: float = 0

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
        if self.window_finish <= self.window_start or self.window_start >= self.window_finish:
            self.window_finish = self.window_start + 1

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
        return select_scale(self.scale_x, self.window_start, self.window_finish, self.interval_type, self._pixels_per_day, self.week_start_num)

    def get_window_resolution(self):
        return self.window_width / (self.window_finish - self.window_start)


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

        line.line_stroke_color = self.line_color
        line.line_stroke_width = self.line_width
        line.line_stroke_dasharray = self.line_dashing

        line.y = self.scale_y
        line.line_dy = self.scale_y + self.window_height

        for i in self.interval_data:
            line.x = i[0]
            line.line_dx = line.x
            lines += line.get_line()

        # last line
        last_line = self.scale_x + ((self.window_finish - self.window_start) * self._pixels_per_day)
        line.x = last_line
        line.line_dx = last_line
        lines += line.get_line()

        return lines

    def get_grid_lines(self):
        return f'{self.build_grid_lines()}'


@dataclass
class Scale(Base):
    """Builds a scale feature"""

    # defines minimum interval width for a label
    min_interval_width: int = 50

    # defines label type
    label_type: str = str()  # count | hidden | date

    # defines date format
    date_format: str = str()  # y | yyyy | Y | m | mm | mmm | M | d | dd | a | aaa | A | n | nnn | w | q | h

    # defines date format separator
    separator: str = " "

    # interval styling
    box_rounding: int = 0
    box_border_width: float = 0.2
    box_border_color: str = 'black'
    box_fill: str = 'grey'

    # defines non-whole interval color
    scale_ends: str = str()

    # text styling
    font_fill: str = '#000'
    font_size: str = str(20)  # 2em | smaller | etc.
    font_family: str = str()  # "Arial, Helvetica, sans-serif"
    font_style: str = str()  # normal | italic | oblique
    font_weight: str = str()  # normal | bold | bolder | lighter | <number>

    # text positioning relative to x and y
    text_x: float = None
    text_y: float = None

    def clean_bar_data(self):

        # clean date format separator
        if len(self.separator) < 1 or self.separator in ['%', '#', '?', '*', '\"'] or self.separator is self.separator.isdigit():
            self.separator = " "  # default

        # clean label type
        if self.label_type in ['HIDDEN', 'hidden', 'hide', 'h', None]:
            self.label_type = 'hidden'
        elif self.label_type in ['COUNT', 'count', 'c', '']:  # default if blank
            self.label_type = 'count'
        elif self.label_type in ['DATE', 'DATES', 'date', 'dates', 'd']:
            self.label_type = 'date'
        else:
            raise ValueError(self.label_type)

        # set default date_format if blank
        if self.label_type == 'date' and self.date_format == str():
            if self.interval_type == 'DAYS':
                self.date_format = 'a'
            elif self.interval_type == 'WEEKS':
                self.date_format = 'w'
            elif self.interval_type == 'MONTHS':
                self.date_format = 'mmm'
            elif self.interval_type == 'QUARTERS':
                self.date_format = 'q'
            elif self.interval_type == 'HALVES':
                self.date_format = 'h'
            elif self.interval_type == 'YEARS':
                self.date_format = 'yyyy'
            else:
                raise ValueError(self.interval_type)

        # set default text_x if None
        if self.text_x is None:
            self.text_x = 10  # arbitrary value

        # set default text_y if None
        if self.text_y is None:
            self.text_y = self.window_height * 0.65  # 0.65 sets text in middle

    def build_boxes(self):

        # set default scale end color if blank
        if self.scale_ends == str():
            self.scale_ends = self.box_fill

        # create Box object
        box = Rectangle()  # dropped Box class as internal bleed behaviour inconsistent with other SVG classes

        # create string for SVG
        boxes = str()

        # unchanging variables of Rect object
        box.y = self.scale_y
        box.rectangle_height = self.window_height
        box.rectangle_border_rounding = self.box_rounding
        box.rectangle_border_color = self.box_border_color
        box.rectangle_border_width = self.box_border_width

        # changing variables for Rect object
        for i in self.interval_data:
            box.x = i[0]
            box.rectangle_width = i[1]
            if i[4] is False:
                box.rectangle_fill_color = self.scale_ends
            else:
                box.rectangle_fill_color = self.box_fill
            boxes += box.get_rect()

        return boxes

    def build_labels(self):

        # create Text object
        label = Text()

        # create string for SVG
        labels = str()

        # unchanging variables for Text object
        label.y = self.scale_y
        label.text_translate_y = self.text_y
        label.text_translate_x = self.text_x
        label.font_fill_color = self.font_fill
        label.font_size = self.font_size
        label.font_weight = self.font_weight
        label.font_family = self.font_family
        label.font_style = self.font_style

        if self.label_type == 'hidden':
            label.text_visibility = 'hidden'

        # changing variables for Text object
        for i in self.interval_data:
            label.x = i[0]
            if i[1] < self.min_interval_width:
                label.text = str()  # you could set visibility to hidden but more verbose
            elif self.label_type == 'count' and i[3] == 0:
                label.text = str()  # you could set visibility to hidden but more verbose
            elif self.label_type == 'date':
                label.text = convert_ordinal(i[2], self.date_format, self.week_start_num, self.separator)
            else:
                label.text = i[3]  # references count in intervals entry
            labels += label.get_text()

        return labels

    def get_bar(self):

        self.clean_bar_data()

        return f'{self.build_boxes()} {self.build_labels()}'

