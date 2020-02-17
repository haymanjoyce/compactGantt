from shapes import Box
from dataclasses import dataclass, field
from datetime import date, timedelta
from pprint import pprint


@dataclass
class TimeBox(Box):
    """
    Builds Box using ordinal dates
    """

    # we keep the date values as ordinal dates (we don't convert them into pixels)
    start: int = None
    finish: int = None
    min: int = None  # defines lower limit such as left edge
    max: int = None  # defines upper limit such as right edge

    # an optional way to define finish if no finish available
    duration: int = 150

    # pixels per day
    resolution: float = 1

    def __post_init__(self):

        # if no start given then we assume start is today
        if self.start is None:
            self.start = date.toordinal(date.today())

        # if no finish given then we create finish based on duration
        if self.finish is None:
            self.finish = self.start + self.duration

        # if no min given then we assume same as start
        if self.min is None:
            self.min = self.start

        # if no max given then we assume same as finish
        if self.max is None:
            self.max = self.finish

        # don't display if finish less than min
        if self.finish < self.min:
            self.visibility = 'hidden'

        # don't display if start more than max
        if self.start > self.max:
            self.visibility = 'hidden'

        # reset start if start less than min
        if self.start < self.min:
            self.start = self.min

        # reset finish is finish more than max
        if self.finish > self.max:
            self.finish = self.max

        # set x
        self.x = (self.start - self.min) * self.resolution

        # set width
        self.width = (self.finish - self.start) * self.resolution


@dataclass
class Scale:
    """
    Arranges TimeBoxes to form scale
    """

    # todo get boxes to abut
    # todo tidy up Scale - does it need duration? - self.finish calc is verbose
    # todo solve partial boxes at scale ends
    # todo clean up comments

    # this method needs iterator that shows start and finish dates and various kinds of interval dates
    # it's got enough to work out the rest (e.g. resolution or finish from duration absence of finish)
    # iterator needs dates in ordinals; other classes can convert ordinals to other formats as required

    # places the scale
    x: float = 0
    y: float = 0

    # sets scale dimensions
    width: float = 800  # used to calculate resolution
    height: float = 100  # passed to TimeBox

    # defines time window
    # passed to TimeBox as min and max
    start: int = None
    finish: int = None

    # defines interval type for scale
    # passed to .get_iterator function
    intervals: str = 'WEEKS'  # DAYS | WEEKS | MONTHS | QUARTERS | HALVES | YEARS

    # defines pixels per day
    # passed to TimeBox
    # value calculated post initiation
    resolution: float = field(repr=False, init=False, default=float())

    # holds the final SVG code for the scale
    # value calculated post initiation
    scale: str = field(repr=False, init=False, default=str())

    def __post_init__(self):

        if self.start is None:
            self.start = date.today().toordinal()

        if self.finish is None:
            self.finish = (date.today() + timedelta(days=200)).toordinal()

        for unit in get_iterator(self.start, self.finish, self.intervals):
            self.scale += TimeBox(min=self.start, max=self.finish, start=unit[0], finish=unit[1], resolution=2, background_color="black", border_width=0.5).get_element()

    def get_element(self):
        return f'<g ' \
               f'transform="translate({self.x}, {self.y})"' \
               f'>' \
               f'{self.scale}' \
               f'</g>'


def get_iterator(start, finish, interval='DAYS'):
    """Creator method which decides which concrete implementation to use (i.e. factory method design pattern)"""
    if interval == 'DAYS':
        return iterate_days(start, finish)
    elif interval == 'WEEKS':
        print(start, finish)
        print(iterate_weeks(start, finish))
        return iterate_weeks(start, finish)
    else:
        raise ValueError(interval)


def iterate_days(start, finish):
    """Returns iterator showing all days in a given range"""
    number_of_days = finish - start
    iterator = tuple()
    for day_number in range(1, number_of_days):
        entry = ((start + day_number, day_number),)
        iterator += entry
    return iterator


def iterate_weeks(start, finish, week_start=0):
    """Returns iterator showing whole weeks in a given range"""

    # calculate number of days in range
    number_of_days = finish - start

    # find start of first whole week
    first_seven_days = [date.fromordinal(start + day).weekday() for day in range(0, number_of_days)[:7]]
    first_week_start = first_seven_days.index(week_start)

    # build iterator
    iterator = tuple()
    week_count = 1
    for day_number in range(first_week_start, number_of_days, 7):
        start_week = start + day_number
        end_week = start_week + 6  # first day and another 6 days
        entry = ((start_week, end_week, week_count), )
        iterator += entry
        week_count += 1
    return iterator


