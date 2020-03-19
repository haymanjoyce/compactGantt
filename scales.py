# Module for building scales

# todo add MONTHS | QUARTERS | HALVES | YEARS
# todo fix WEEKS so does not break if period too small to pass assertions
# todo ability to set date format
# todo improve using map()
# todo put non-whole intervals into iterator
# todo change name of ends to partial
# todo what happens if week partial interval start and finish are same date (i.e. 1 day)
# todo what if range less than 1 week
# todo rewrite TimeBox to assume start is 00:00 and next argument adds days

from shapes import TimeBox
from dataclasses import dataclass
from datetime import date, datetime
from pprint import pprint


@dataclass
class Scale:
    """
    Builds scale out of TimeBoxes
    """

    # places the scale
    x: float = 0
    y: float = 0

    # sets scale dimensions
    width: float = 800  # used to calculate resolution
    height: float = 100

    # defines time window
    start: int = 0
    finish: int = 0

    # defines interval type for scale
    intervals: str = 'WEEKS'  # DAYS | WEEKS | MONTHS | QUARTERS | HALVES | YEARS
    week_start: int = 0  # 0 is Monday

    # scale styling
    background_color: str = 'black'
    border_color: str = 'black'
    border_width: float = 1
    rounding: int = 1
    fill: str = 'grey'
    ends: str = None

    # defines pixels per day
    resolution: float = None

    # text positioning
    translate_x: float = 2
    translate_y: float = None  # calculated if None

    # text styling
    font_fill: str = '#000'
    font_size: str = str(20)  # 2em | smaller | etc.
    font_family: str = str()  # "Arial, Helvetica, sans-serif"
    font_style: str = str()  # normal | italic | oblique
    font_weight: str = str()  # normal | bold | bolder | lighter | <number>

    # text visibility
    text_visibility: str = str()

    def build_scale(self):

        # create iterator
        iterator = get_iterator(self.start, self.finish, self.intervals.upper(), self.week_start)

        # create SVG string
        scale = str()

        # create TimeBox object
        time_box = TimeBox()

        # calculates total days
        total_days = self.finish - self.start

        # calculate resolution
        if self.resolution is None:
            self.resolution = self.width / total_days

        # calculate text vertical alignment
        if self.translate_y is None:
            self.translate_y = self.height - 3

        # set text visibility
        if self.font_size == str(0):
            self.text_visibility = 'hidden'

        # set color for non-whole intervals
        if self.ends is None:
            self.ends = self.fill

        # general settings for time_box object
        time_box.min = self.start
        time_box.max = self.finish
        time_box.height = self.height
        time_box.resolution = abs(self.resolution)
        time_box.background_color = self.background_color
        time_box.border_color = self.border_color
        time_box.border_width = self.border_width
        time_box.rounding = self.rounding
        time_box.fill = self.fill
        time_box.font_fill = self.font_fill
        time_box.font_size = self.font_size
        time_box.font_weight = self.font_weight
        time_box.font_family = self.font_family
        time_box.font_style = self.font_style
        time_box.text_visibility = self.text_visibility

        # changes to TimeBox object by iteration
        for interval in iterator:

            # we assume the date marks the end of the day
            time_box.start = interval[0] - 1
            time_box.finish = interval[1]

            # updates derived values in TimeBox object
            time_box.update()

            # needs to render before text
            scale += time_box.get_box()

            # position text relative to box
            time_box.translate_x = self.translate_x
            time_box.translate_y = self.translate_y

            # label box
            time_box.text = interval[2]

            # add text to scale
            scale += time_box.get_text()

        return scale

    def get_scale(self):
        return f'<g ' \
               f'transform="translate({self.x}, {self.y})"' \
               f'>' \
               f'{self.build_scale()}' \
               f'</g>'


def get_iterator(start, finish, interval='DAYS', week_start=0):
    """Creator method which decides which concrete implementation to use (a factory method design pattern)"""
    if interval == 'DAYS':
        return iterate_days(start, finish)
    elif interval == 'WEEKS':
        return iterate_weeks(start, finish, week_start)
    else:
        raise ValueError(interval)


def iterate_days(start, finish):
    """Returns iterator showing all days in a given range"""
    number_of_days = finish - start
    iterator = tuple()
    day_count = 1
    for day_number in range(0, number_of_days):
        day_start = start + day_number
        day_end = day_start + 1
        entry = ((day_start, day_end, day_count),)
        iterator += entry
        day_count += 1
    return iterator


def iterate_weeks(start, finish, week_start=0):

    iterator = tuple()
    week_count = 1

    # create iterator
    for day in range(start, finish + 1):
        week_day = date.fromordinal(day).weekday()
        if week_day == week_start:
            entry = tuple()
            entry += day,
            week_stop = day + 6
            entry += week_stop,
            entry += week_count,
            week_count += 1
            iterator += entry,

    # if first week start more than range start
    if iterator[0][0] > start:
        entry = start, iterator[0][0] - 1, 0,  # 0 denotes incomplete week
        iterator = (entry, ) + iterator

    # if last week finish more than range finish
    if iterator[-1][1] > finish:
        entry = iterator[-1][0], finish, 0,  # 0 denotes incomplete week
        iterator = iterator[:-1] + (entry, )

    assert date.fromordinal(iterator[1][0]).weekday() == week_start

    print("range start ", start)
    print("range finish", finish)
    print("iterator", iterator)
    print("first interval, start", datetime.fromordinal(iterator[0][0]))
    print("first interval, finish", datetime.fromordinal(iterator[0][1]))
    print("last interval, start", datetime.fromordinal(iterator[-1][0]))
    print("last interval, finish", datetime.fromordinal(iterator[-1][1]))

    return iterator

