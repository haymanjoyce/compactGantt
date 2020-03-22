"""Module for building scales"""

# todo add MONTHS | QUARTERS | HALVES | YEARS
# todo ability to set label format
# todo ability to choose to show count or date

from shapes import Box, Text
from dataclasses import dataclass
from datetime import date


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

    # defines interval type (cannot use "type" as it shadows a builtin)
    kind: str = 'WEEKS'  # DAYS | WEEKS | MONTHS | QUARTERS | HALVES | YEARS

    # defines first day of week
    week_start: int = 0  # 0 is Monday

    # interval styling
    box_background_color: str = 'black'
    box_border_color: str = 'black'
    box_border_width: float = 0.2
    box_rounding: int = 1
    box_fill: str = 'grey'

    # defines non-whole interval color
    scale_ends: str = None

    # text styling
    font_fill: str = '#000'
    font_size: str = str(20)  # 2em | smaller | etc.
    font_family: str = str()  # "Arial, Helvetica, sans-serif"
    font_style: str = str()  # normal | italic | oblique
    font_weight: str = str()  # normal | bold | bolder | lighter | <number>

    # text visibility
    text_visibility: str = str()  # hidden

    # text positioning relative to x and y
    text_x: float = None
    text_y: float = None

    def __post_init__(self):

        # clean start and finish dates
        if self.finish <= self.start or self.start >= self.finish:
            self.finish = self.start + 1

        # calculate resolution (pixels per day)
        self.resolution = self.width / (self.finish - self.start)  # // will reduce float (good) and precision (bad)

        # build interval data
        self.intervals = select(self.start, self.finish, self.kind, self.resolution, self.week_start)

        # set default scale end color if None
        if self.scale_ends is None:
            self.scale_ends = self.box_fill

        # set default text_x if None
        if self.text_x is None:
            try:
                self.text_x = self.intervals[1][1] * 0.15  # we take second entry as first may not be a whole interval
            except IndexError:
                self.text_x = 0  # if no second entry available

        # set default text_y if None
        if self.text_y is None:
            self.text_y = self.height * 0.65

        # ensure kind is in right format
        self.kind = self.kind.upper()

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
        label.text_visibility = self.text_visibility

        # changing variables
        for i in self.intervals:
            label.x = i[0]
            if i[3] == 0:
                label.text = str()
            else:
                label.text = i[3]
            labels += label.get_text()

        return labels

    def get_scale(self):
        return f'{self.build_boxes()}' \
               f'{self.build_labels()}'


def select(start, finish, kind='DAYS', resolution=1.0, week_start=0):
    """Selects appropriate iterable based on kind"""
    if kind == 'DAYS':
        return days(start, finish, resolution)
    elif kind == 'WEEKS':
        return weeks(start, finish, resolution, week_start)
    else:
        raise ValueError(kind)


def days(start, finish, resolution):
    """Returns iterable showing all days in a given range"""

    entries = tuple()

    total_days = finish - start
    box_width = 1 * resolution
    x = 0
    ordinal = start
    day_count = 1

    for day in range(total_days):
        entry = x, box_width, ordinal, day_count,
        entries += (entry, )
        x += box_width
        ordinal += 1
        day_count += 1

    return entries


def weeks(start, finish, resolution, week_start):
    """Returns iterable showing all weeks in a given range"""

    try:  # requires a week_start to be found

        entries = tuple()
        total_days = finish - start
        first_weekday = [date.fromordinal(day).weekday() for day in range(start, finish)[:20]].index(week_start)
        box_width = 7 * resolution
        week_commencing = start + first_weekday
        week_count = 1

        # create entries
        while first_weekday < total_days:
            x = first_weekday * resolution
            entries += (x, box_width, week_commencing, week_count),
            first_weekday += 7
            week_commencing += 7
            week_count += 1

        # underhang
        if entries[0][2] > start:
            underhang = (entries[0][2] - start) * resolution
            entry = 0, underhang, start, 0,  # a week number of 0 means not a whole week
            entries = (entry,) + entries

        # overhang
        if entries[-1][2] + 7 > finish:
            overhang = ((entries[-1][2] + 7) - finish) * resolution
            overhang = box_width - overhang
            entry = entries[-1][0], overhang, entries[-1][2], 0  # a week number of 0 means not a whole week
            entries = entries[:-1] + (entry, )

        return entries

    except ValueError:  # if no week_start found (i.e. range too short)

        entries = tuple()
        total_days = finish - start
        box_width = total_days * resolution
        entry = 0, box_width, start, 0
        entries += (entry, )

        return entries

