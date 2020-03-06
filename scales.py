# Module for building scales

# todo add text to scales
# todo add MONTHS | QUARTERS | HALVES | YEARS
# todo fix WEEKS so does not break if period too small to pass assertions

from shapes import TimeBox, TimeText
from dataclasses import dataclass
from datetime import date
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
    height: float = 100  # passed to TimeBox

    # defines time window
    # passed to TimeBox as min and max
    start: int = 0
    finish: int = 0

    # defines interval type for scale
    # passed to .get_iterator function
    intervals: str = 'WEEKS'  # DAYS | WEEKS | MONTHS | QUARTERS | HALVES | YEARS

    # scale styling
    background_color: str = 'black'
    border_color: str = 'black'
    border_width: float = 1
    rounding: int = 1
    fill: str = 'grey'
    ends: str = None

    # defines pixels per day
    # passed to TimeBox
    resolution: float = 1

    def build_scale(self):

        # iterator is not object specific
        iterator = get_iterator(self.start, self.finish, self.intervals.upper())

        # SVG string
        scale = str()

        # create TimeBox object
        timebox = TimeBox()

        # create TimeText object
        timetext = TimeText()

        # general settings of TimeBox object
        timebox.min = self.start
        timebox.max = self.finish
        timebox.height = self.height
        timebox.resolution = abs(self.resolution)

        # style settings
        timebox.background_color = self.background_color
        timebox.border_color = self.border_color
        timebox.border_width = self.border_width
        timebox.rounding = self.rounding

        # setting a color for non-whole intervals
        if self.ends is None:
            self.ends = self.fill
        timebox.fill = self.ends

        # first non-whole interval
        timebox.start = self.start
        timebox.finish = iterator[0][0]
        timebox.update()
        scale += timebox.get_element()

        # last non-whole interval
        timebox.start = iterator[-1][1]
        timebox.finish = self.finish
        timebox.update()
        scale += timebox.get_element()

        # setting color for for whole intervals
        timebox.fill = self.fill

        # general settings for TimeText object
        timetext.min = self.start
        timetext.max = self.finish
        timetext.resolution = abs(self.resolution)
        timetext.fill = 'black'

        # whole intervals
        for interval in iterator:

            # timebox
            timebox.start = interval[0]
            timebox.finish = interval[1]
            timebox.update()
            scale += timebox.get_element()

            # timetext
            timetext.start = interval[0]
            timetext.text = interval[2]
            timetext.update()
            scale += timetext.get_element()

        return scale

    def get_element(self):
        return f'<g ' \
               f'transform="translate({self.x}, {self.y})"' \
               f'>' \
               f'{self.build_scale()}' \
               f'</g>'


def get_iterator(start, finish, interval='DAYS'):
    """Creator method which decides which concrete implementation to use (i.e. factory method design pattern)"""
    if interval == 'DAYS':
        return iterate_days(start, finish)
    elif interval == 'WEEKS':
        return iterate_weeks(start, finish)
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
    """Returns iterator showing whole weeks in a given range"""

    # calculate number of days in range
    number_of_days = finish - start

    # list days as datetime objects
    days = [date.fromordinal(start + day) for day in range(0, number_of_days)]

    # find position of start of whole week in range
    first_week = days[:7]
    first_week_day_numbers = [day.weekday() for day in first_week]
    range_start = (first_week_day_numbers.index(week_start)) - 1  # day before first week day

    # find position of end of last whole week in range
    over_hang = (number_of_days - range_start) % 7
    range_end = number_of_days - over_hang

    range_interval = 7  # weekly
    week_count = 1  # the first whole week counts as 1 (not 0 or 2)
    iterator = tuple()

    for day_number in range(range_start, range_end, range_interval):
        start_week = start + day_number  # first day_number value is 0
        end_week = start_week + 7
        entry = ((start_week, end_week, week_count), )
        iterator += entry
        week_count += 1  # prepare week_count for next entry

    assert date.fromordinal(iterator[0][0]).weekday() == 6  # first day of first whole week is last day of previous week
    assert date.fromordinal(iterator[-1][1]).weekday() == 6  # last day of last whole week is last day of current week

    return iterator


