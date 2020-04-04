"""Module for building scales"""

# todo ability to create custom interval (e.g. 20 days representing 1 month)
# todo ability to label the scale (e.g. Months)
# todo if text size not set then calculated (will need to know rendering medium and to be homed in separate module)
# todo vertical grid lines
# todo Base class for Scale and Grid

from shapes import Box, Text, Line
from dataclasses import dataclass
from datetime import date
import dates


@dataclass
class Grid:
    """Builds vertical grid lines which align with scale intervals"""

    # places the grid
    x: float = 0
    y: float = 0

    # sets grid dimensions
    width: float = 800
    height: float = 600

    # defines time window
    start: int = 0  # note that ordinal dates are at 00:00hrs (day start)
    finish: int = 0  # we handle the missing 23:59 hours (you don't need to)

    # defines first day of week
    week_start: str = str(0)

    # defines interval type
    interval_type: str = str()  # DAYS | WEEKS | MONTHS | QUARTERS | HALVES | YEARS

    # line styling
    line_color: str = 'black'
    line_width: int = 1
    line_dashing: str = str()  # dash gap dash gap

    def __post_init__(self):

        # clean start and finish dates
        if self.finish <= self.start or self.start >= self.finish:
            self.finish = self.start + 1

        # clean first day of week string and converts to integer
        if self.week_start in ['6', '7', 'S', 'Sun', 'Sunday', 'SUN', 'SUNDAY']:
            self._week_start = 6
        else:
            self._week_start = 0

        # clean interval type
        if self.interval_type.lower() in [item.lower() for item in ['days', 'day', 'd', '']]:  # blank indicates default
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

        # calculate resolution (pixels per day) (note, this is a private variable)
        self.resolution = self.width / (self.finish - self.start)  # // will reduce float (good) and precision (bad)

        # build interval data (note, this is a private variable)
        self.intervals = select(self.x, self.start, self.finish, self.interval_type, self.resolution, self._week_start)

    def build_grid(self):

        lines = str()
        line = Line()

        line.stroke = self.line_color
        line.stroke_width = self.line_width
        line.stroke_dasharray = self.line_dashing

        line.y = self.y
        line.dy = self.y + self.height

        for i in self.intervals:
            line.x = i[0]
            line.dx = line.x
            lines += line.get_line()

        return lines

    def get_grid(self):
        print(self.build_grid())
        return f'{self.build_grid()}'


@dataclass
class Scale:
    """Builds scales"""

    # places the scale
    x: float = 0
    y: float = 0

    # sets scale dimensions
    width: float = 800
    height: float = 50

    # defines time window
    start: int = 0  # note that ordinal dates are at 00:00hrs (day start)
    finish: int = 0  # we handle the missing 23:59 hours (you don't need to)

    # defines first day of week
    week_start: str = str(0)

    # defines interval type
    interval_type: str = str()  # DAYS | WEEKS | MONTHS | QUARTERS | HALVES | YEARS

    # defines minimum interval width for a label
    min_interval_width: int = 50

    # defines label type
    label_type: str = str()  # count | hidden | date

    # defines date format
    date_format: str = str()  # y | yyyy | Y | m | mm | mmm | M | d | dd | a | aaa | A | n | nnn | w | q | h

    # defines date format separator
    separator: str = " "

    # interval styling
    box_background_color: str = 'black'  # this fills the outer box which is revealed when using rounding
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

    def __post_init__(self):

        # clean start and finish dates
        if self.finish <= self.start or self.start >= self.finish:
            self.finish = self.start + 1

        # clean first day of week string and converts to integer
        if self.week_start in ['6', '7', 'S', 'Sun', 'Sunday', 'SUN', 'SUNDAY']:
            self._week_start = 6
        else:
            self._week_start = 0

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

        # clean interval type
        if self.interval_type.lower() in [item.lower() for item in ['days', 'day', 'd', '']]:  # blank indicates default
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

        # set default scale end color if blank
        if self.scale_ends == str():
            self.scale_ends = self.box_fill

        # set default text_x if None
        if self.text_x is None:
            self.text_x = 10  # arbitrary value

        # set default text_y if None
        if self.text_y is None:
            self.text_y = self.height * 0.65  # 0.65 sets text in middle

        # calculate resolution (pixels per day) (note, this is a private variable)
        self.resolution = self.width / (self.finish - self.start)  # // will reduce float (good) and precision (bad)

        # build interval data (note, this is a private variable)
        self.intervals = select(self.x, self.start, self.finish, self.interval_type, self.resolution, self._week_start)

    def build_boxes(self):

        box = Box()
        boxes = str()

        box.y = self.y
        box.height = self.height
        box.rounding = self.box_rounding
        box.background_color = self.box_background_color
        box.border_color = self.box_border_color
        box.border_width = self.box_border_width

        for i in self.intervals:
            box.x = i[0]
            box.width = i[1]
            if i[4] is False:
                box.fill = self.scale_ends
            else:
                box.fill = self.box_fill
            boxes += box.get_box()

        return boxes

    def build_labels(self):

        label = Text()
        labels = str()

        label.y = self.y
        label.translate_y = self.text_y
        label.translate_x = self.text_x
        label.font_fill = self.font_fill
        label.font_size = self.font_size
        label.font_weight = self.font_weight
        label.font_family = self.font_family
        label.font_style = self.font_style

        if self.label_type == 'hidden':
            label.text_visibility = self.label_type

        for i in self.intervals:
            label.x = i[0]
            if i[1] < self.min_interval_width:
                label.text = str()  # you could set visibility to hidden but more verbose
            elif self.label_type == 'count' and i[3] == 0:
                label.text = str()  # you could set visibility to hidden but more verbose
            elif self.label_type == 'date':
                label.text = dates.convert_ordinal(i[2], self.date_format, self._week_start, self.separator)
            else:
                label.text = i[3]  # references count in intervals entry
            labels += label.get_text()

        return labels

    def get_scale(self):
        return f'{self.build_boxes()}' \
               f'{self.build_labels()}'


def select(x, start, finish, interval_type='DAYS', resolution=1.0, week_start=0):
    """Selects appropriate iterable based on interval type"""

    # Iterable is a tuple of tuples
    # Each tuple: x (pixels), width (pixels), ordinal date (00:00hrs of date), count, whole (boolean)

    if interval_type == 'DAYS':
        return days(x, start, finish, resolution)

    elif interval_type == 'WEEKS':
        return weeks(x, start, finish, resolution, week_start)

    elif interval_type == 'MONTHS':
        start_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        whole_intervals = whole_periods(start, finish, start_months)
        return gregorian_periods(x, start, finish, resolution, whole_intervals)

    elif interval_type == 'QUARTERS':
        start_months = [1, 4, 7, 10]
        whole_intervals = whole_periods(start, finish, start_months)
        return gregorian_periods(x, start, finish, resolution, whole_intervals)

    elif interval_type == 'HALVES':
        start_months = [1, 7]
        whole_intervals = whole_periods(start, finish, start_months)
        return gregorian_periods(x, start, finish, resolution, whole_intervals)

    elif interval_type == 'YEARS':
        start_months = [1]
        whole_intervals = whole_periods(start, finish, start_months)
        return gregorian_periods(x, start, finish, resolution, whole_intervals)

    else:
        raise ValueError(interval_type)


def days(x, start, finish, resolution):
    """Returns iterable showing all days in a given range"""

    entries = tuple()
    total_days = finish - start
    width = 1 * resolution

    for day in range(total_days):

        entry = x, width, start + day, day + 1, True
        entries += (entry, )
        x += width

    return entries


def weeks(x, start, finish, resolution, week_start):
    """Returns iterable showing all weeks in a given range"""

    entries = tuple()
    intervals = [day for day in range(start, finish + 1) if date.fromordinal(day).weekday() == week_start or day == start or day == finish]
    interval = 0
    width = 0
    count = 0

    while intervals[interval] != finish:

        x += width
        duration = intervals[interval + 1] - intervals[interval]
        if duration == 7:
            whole = True
            count += 1
        else:
            whole = False
            count = 0
        width = duration * resolution

        entry = x, width, intervals[interval], count, whole
        entries += (entry, )

        interval += 1

    return entries


def gregorian_periods(x, start, finish, resolution, whole_intervals):
    """Returns iterable showing all Gregorian periods (greater or equal to one month) in a given range"""

    entries = tuple()

    starts = whole_intervals.copy()

    if start not in starts:
        starts = [start] + starts

    if finish not in starts:
        starts = starts + [finish]

    interval = 0

    count = 0

    while starts[interval] != finish:

        current_start = starts[interval]

        next_start = starts[interval + 1]

        width = (next_start - current_start) * resolution

        if current_start == start and start not in whole_intervals:
            count += 0
            whole = False
        elif next_start == finish and finish not in whole_intervals:
            count += 1
            whole = False
        else:
            count += 1
            whole = True

        entry = x, width, current_start, count, whole
        entries += (entry, )

        x += width

        interval += 1

    return entries


def whole_periods(start, finish, start_months):
    """Returns start dates for all Gregorian periods in given range, including last day in range"""

    return [day for day in range(start, finish + 1) if date.fromordinal(day).month in start_months and date.fromordinal(day).day == 1]

