"""Module for building simple chart features"""

# todo add display layer to Base
# todo same line for {} things

from dataclasses import dataclass
from shapes import Rect, Circle, Diamond, Line, Text
from dates import select_scale, convert_ordinal


# BASE CLASSES

@dataclass
class Chart:
    """Base class for all features"""

    layer: int = int()


@dataclass
class Relationship(Chart):
    """Base class for all relational features"""

    id: int = int()
    parent: int = int()


@dataclass
class Scaly(Chart):
    """Base class for scale related features"""

    # places the image
    x: float = 0
    y: float = 0

    # sets image dimensions
    width: float = 800
    height: float = 600

    # defines time window
    start: int = 0  # note that ordinal dates are at 00:00hrs (day start)
    finish: int = 0  # we handle the missing 23:59 hours (you don't need to)

    # defines first day of week as string
    week_start_text: str = str(0)

    # defines first day of week as integer
    week_start_num: int = 0

    # defines interval type
    interval_type: str = str()  # DAYS | WEEKS | MONTHS | QUARTERS | HALVES | YEARS

    # private variable
    _pixels_per_day: float = float()

    # private variable
    _interval_data: tuple = tuple()

    def __post_init__(self):

        # if subclass overrides post_init then subclass will need to call these methods manually

        self.clean_scaly_data()
        self._pixels_per_day = self.get_pixels_per_day()
        self._interval_data = self.get_interval_data()

    def clean_scaly_data(self):

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

    def get_pixels_per_day(self):
        return self.width / (self.finish - self.start)  # // will reduce float (good) and precision (bad)

    def get_interval_data(self):
        return select_scale(self.x, self.start, self.finish, self.interval_type, self._pixels_per_day, self.week_start_num)


# SIMPLE FEATURES

@dataclass
class Annotation(Chart):
    pass


@dataclass
class Curtain(Chart):
    pass


@dataclass
class Bar(Chart):
    pass


# FEATURES WITH CONTAINER RELATIONSHIPS

@dataclass
class TimeLine(Relationship, Rect):

    def get_timeline(self):
        return f'{self.get_rect()}'


@dataclass
class Task(Relationship, Rect, Text):

    def get_task(self):
        return f'{self.get_rect()} ' \
               f'{self.get_text()}'


@dataclass
class Milestone(Relationship, Circle, Diamond, Text):

    diamond: bool = True

    def get_milestone(self):

        if self.diamond:
            pass
        else:
            pass

        return f'{self.get_diamond()} ' \
               f'{self.get_text()}'


@dataclass
class Cell(Relationship, Rect, Text):

    def get_cell(self):
        return f'{self.get_rect()} ' \
               f'{self.get_text()}'


@dataclass
class Row(Relationship, Rect):

    def get_row(self):

        return f'{self.get_rect()}'


@dataclass
class SwimLane(Relationship, Rect):

    def get_swimlane(self):
        return f'{self.get_rect()}'


@dataclass
class Group(Relationship, Rect, Text):

    def get_group(self):

        return f'{self.get_rect()} ' \
               f'{self.get_text()}'


# SCALE RELATED FEATURES

@dataclass
class GridLines(Scaly):
    """Builds vertical grid line feature"""

    # line styling
    line_color: str = 'black'
    line_width: int = 1
    line_dashing: str = str()  # dash gap dash gap

    def build_grid_lines(self):

        lines = str()
        line = Line()

        line.stroke = self.line_color
        line.stroke_width = self.line_width
        line.stroke_dasharray = self.line_dashing

        line.y = self.y
        line.dy = self.y + self.height

        for i in self._interval_data:
            line.x = i[0]
            line.dx = line.x
            lines += line.get_line()

        # last line
        last_line = self.x + ((self.finish - self.start) * self._pixels_per_day)
        line.x = last_line
        line.dx = last_line
        lines += line.get_line()

        return lines

    def get_grid_lines(self):
        return f'{self.build_grid_lines()}'


@dataclass
class Scale(Scaly):
    """Builds a scale feature"""

    # todo ability to label the scale (e.g. Months)
    # todo if text size not set then calculated (will need to know rendering medium and to be homed in separate module)

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

    def clean_scale_data(self):

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
            self.text_y = self.height * 0.65  # 0.65 sets text in middle

    def build_boxes(self):

        # set default scale end color if blank
        if self.scale_ends == str():
            self.scale_ends = self.box_fill

        # create Box object
        box = Rect()  # dropped Box class as internal bleed behaviour inconsistent with other SVG classes

        # create string for SVG
        boxes = str()

        # unchanging variables of Rect object
        box.y = self.y
        box.height = self.height
        box.rounding = self.box_rounding
        box.border_color = self.box_border_color
        box.border_width = self.box_border_width

        # changing variables for Rect object
        for i in self._interval_data:
            box.x = i[0]
            box.width = i[1]
            if i[4] is False:
                box.fill = self.scale_ends
            else:
                box.fill = self.box_fill
            boxes += box.get_rect()

        return boxes

    def build_labels(self):

        # create Text object
        label = Text()

        # create string for SVG
        labels = str()

        # unchanging variables for Text object
        label.y = self.y
        label.translate_y = self.text_y
        label.translate_x = self.text_x
        label.font_fill = self.font_fill
        label.font_size = self.font_size
        label.font_weight = self.font_weight
        label.font_family = self.font_family
        label.font_style = self.font_style

        if self.label_type == 'hidden':
            label.text_visibility = 'hidden'

        # changing variables for Text object
        for i in self._interval_data:
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

    def get_scale(self):

        self.clean_scale_data()

        return f'{self.build_boxes()} {self.build_labels()}'

