"""Module for building scales"""

# todo add MONTHS | QUARTERS | HALVES | YEARS
# todo if text size not set then calculated
# todo clean separator (e.g. only one or two chars or forbidden chars)
# todo ability to create custom interval (e.g. 20 days representing 1 month)
# todo key or label for each scale (e.g. Months)
# todo merge label type and fate format to create label format
# todo debug months where 1 day duration results in miscalculated overhang
# todo rebuild all iterators with new design
# todo redesign tuple of tuples such that is plain count and another variable indicates not whole
# todo rewrite weeks using same design as months but identifying interval starts with week_start

from shapes import Box, Text
from dataclasses import dataclass
from datetime import date, timedelta
from calendar import monthrange
import dates


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

    # defines first day of week as a string
    week_start: str = str(0)

    # defines interval type
    interval_type: str = str()  # DAYS | WEEKS | MONTHS | QUARTERS | HALVES | YEARS

    # defines label type
    label_type: str = str()  # count | hidden | date

    # defines minimum interval width for a label
    min_interval_width: int = 50

    # defines date format
    date_format: str = str()  # y | yyyy | m | mm | mmm | M | d | dd | a | aaa | A | n | nnn | w

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

        # clean label type
        if self.label_type in ['HIDDEN', 'hidden', 'hide', 'h']:
            self.label_type = 'hidden'
        elif self.label_type in ['COUNT', 'count', 'c', '']:
            self.label_type = 'count'
        elif self.label_type in ['DATE', 'DATES', 'date', 'dates', 'd']:
            self.label_type = 'date'
        else:
            raise ValueError(self.label_type)

        # set default scale end color if blank
        if self.scale_ends == str():
            self.scale_ends = self.box_fill

        # set default text_x if zero
        if self.text_x is None:
            self.text_x = 10  # arbitrary value

        # set default text_y if zero
        if self.text_y is None:
            self.text_y = self.height * 0.65  # 0.65 sets text in middle

        # set default date_format if blank
        if self.label_type == 'date' and self.date_format == str():
            if self.interval_type == 'DAYS':
                self.date_format = 'a'
            elif self.interval_type == 'WEEKS':
                self.date_format = 'w'
            elif self.interval_type == 'MONTHS':
                self.date_format = 'mmm'
            elif self.interval_type == 'QUARTERS':
                self.date_format = ''
            elif self.interval_type == 'HALVES':
                self.date_format = ''
            elif self.interval_type == 'YEARS':
                self.date_format = 'yyyy'
            else:
                raise ValueError(self.interval_type)

        # calculate resolution (pixels per day) (note, this is a private variable)
        self.resolution = self.width / (self.finish - self.start)  # // will reduce float (good) and precision (bad)

        # build interval data (note, this is a private variable)
        self.intervals = select(self.start, self.finish, self.interval_type, self.resolution, self._week_start)

    def build_boxes(self):

        box = Box()
        boxes = str()

        # unchanging variables
        box.y = self.y
        box.height = self.height
        box.rounding = self.box_rounding
        box.background_color = self.box_background_color
        box.border_color = self.box_border_color
        box.border_width = self.box_border_width

        # changing variables
        for i in self.intervals:
            box.x = i[0]
            box.width = i[1]
            if i[3] == 0:
                box.fill = self.scale_ends
            else:
                box.fill = self.box_fill
            boxes += box.get_box()

        return boxes

    def build_labels(self):

        label = Text()
        labels = str()

        # unchanging variables
        label.y = self.y
        label.translate_y = self.text_y
        label.translate_x = self.text_x
        label.font_fill = self.font_fill
        label.font_size = self.font_size
        label.font_weight = self.font_weight
        label.font_family = self.font_family
        label.font_style = self.font_style

        # set visibility
        if self.label_type == 'hidden':
            label.text_visibility = self.label_type

        # changing variables
        for i in self.intervals:
            label.x = i[0]
            if i[1] < self.min_interval_width:
                label.text = str()  # you could set visibility to hidden but more verbose
            elif i[3] == 0 and self.label_type == 'count':
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


def select(start, finish, interval_type='DAYS', resolution=1.0, week_start=0):
    """Selects appropriate iterable based on interval type"""

    # Iterable is a tuple of tuples
    # Each tuple: x (pixels), width (pixels), ordinal date (00:00hrs of date), count, whole (boolean)

    if interval_type == 'DAYS':
        return days(start, finish, resolution)
    elif interval_type == 'WEEKS':
        return weeks(start, finish, resolution, week_start)
    elif interval_type == 'MONTHS':
        return months(start, finish, resolution)
    elif interval_type == 'QUARTERS':
        return quarters(start, finish, resolution)
    elif interval_type == 'HALVES':
        return halves(start, finish, resolution)
    elif interval_type == 'YEARS':
        return years(start, finish, resolution)
    else:
        raise ValueError(interval_type)


def days(start, finish, resolution):
    """Returns iterable showing all days in a given range"""

    entries = tuple()
    total_days = finish - start
    x = 0
    width = 1 * resolution

    for day in range(total_days):

        entry = x, width, start + day, day + 1, True
        entries += (entry, )
        x += width

    return entries


def weeks(start, finish, resolution, week_start):
    """Returns iterable showing all weeks in a given range"""

    entries = tuple()
    intervals = [day for day in range(start, finish + 1) if date.fromordinal(day).weekday() == week_start or day == start or day == finish]
    interval = 0
    x = 0
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


def months(start, finish, resolution):
    """Returns iterable showing all months in given range"""

    entries = tuple()

    intervals = [i for i in range(1, 13)]

    # lists half starts and finish if it is also a half start (we need this to set count)
    starts = [day for day in range(start, finish + 1) if date.fromordinal(day).month in intervals and date.fromordinal(day).day == 1]

    # finish appears twice if finish is also a quarter end but while loop stops at first so no need to remove
    interval_dates = [start] + starts + [finish]

    count = 0
    item = 0

    while interval_dates[item] != finish:

        x = (interval_dates[item] - start) * resolution
        width = (interval_dates[item + 1] - interval_dates[item]) * resolution

        if interval_dates[item + 1] == finish and finish not in starts:
            count = 0  # sets count to 0 for overhang
        elif interval_dates[item] not in starts:
            count = 0  # sets count to 0 for underhang
        else:
            count += 1  # whole interval count

        entry = x, width, interval_dates[item], count
        entries += (entry, )

        item += 1

    return entries


def quarters(start, finish, resolution):
    """Returns iterable showing all halves in given range"""

    entries = tuple()

    # lists quarter starts and finish if it is also a quarter start (we need this to set count)
    quarter_starts = [day for day in range(start, finish + 1) if
                      date.fromordinal(day).month in [1, 4, 7, 10] and date.fromordinal(day).day == 1]

    # finish appears twice if finish is also a quarter end but while loop stops at first so no need to remove
    interval_dates = [start] + quarter_starts + [finish]

    count = 0
    item = 0

    while interval_dates[item] != finish:

        x = (interval_dates[item] - start) * resolution
        width = (interval_dates[item + 1] - interval_dates[item]) * resolution

        if interval_dates[item + 1] == finish and finish not in quarter_starts:
            count = 0  # sets count to 0 for overhang
        elif interval_dates[item] not in quarter_starts:
            count = 0  # sets count to 0 for underhang
        else:
            count += 1  # whole interval count

        entry = x, width, interval_dates[item], count
        entries += (entry, )

        item += 1

    return entries


def halves(start, finish, resolution):
    """Returns iterable showing all quarters in given range"""

    entries = tuple()

    # lists half starts and finish if it is also a half start (we need this to set count)
    half_starts = [day for day in range(start, finish + 1) if
                      date.fromordinal(day).month in [1, 7] and date.fromordinal(day).day == 1]

    # finish appears twice if finish is also a quarter end but while loop stops at first so no need to remove
    interval_dates = [start] + half_starts + [finish]

    count = 0
    item = 0

    while interval_dates[item] != finish:

        x = (interval_dates[item] - start) * resolution
        width = (interval_dates[item + 1] - interval_dates[item]) * resolution

        if interval_dates[item + 1] == finish and finish not in half_starts:
            count = 0  # sets count to 0 for overhang
        elif interval_dates[item] not in half_starts:
            count = 0  # sets count to 0 for underhang
        else:
            count += 1  # whole interval count

        entry = x, width, interval_dates[item], count
        entries += (entry, )

        item += 1

    return entries


def years(start, finish, resolution):
    """Returns iterable showing all years in given range"""

    entries = tuple()

    # lists half starts and finish if it is also a half start (we need this to set count)
    year_starts = [day for day in range(start, finish + 1) if
                   date.fromordinal(day).month in [1] and date.fromordinal(day).day == 1]

    # finish appears twice if finish is also a quarter end but while loop stops at first so no need to remove
    interval_dates = [start] + year_starts + [finish]

    count = 0
    item = 0

    while interval_dates[item] != finish:

        x = (interval_dates[item] - start) * resolution
        width = (interval_dates[item + 1] - interval_dates[item]) * resolution

        if interval_dates[item + 1] == finish and finish not in year_starts:
            count = 0  # sets count to 0 for overhang
        elif interval_dates[item] not in year_starts:
            count = 0  # sets count to 0 for underhang
        else:
            count += 1  # whole interval count

        entry = x, width, interval_dates[item], count
        entries += (entry, )

        item += 1

    return entries

