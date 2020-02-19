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

    # defines lower and uppers limits (i.e. edges)
    min: int = None
    max: int = None

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

    # todo tidy up Scale - does it need duration? - self.finish calc is verbose
    # todo solve partial boxes at scale ends
    # todo clean up comments
    # todo add in resolution
    # todo how to define Box and TimeBox attributes in Scale

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

    # an optional way to define finish if no finish available
    duration: int = 200

    # defines interval type for scale
    # passed to .get_iterator function
    intervals: str = 'WEEKS'  # DAYS | WEEKS | MONTHS | QUARTERS | HALVES | YEARS

    # defines pixels per day
    # passed to TimeBox
    # value calculated, based on width, after initiation
    resolution: float = field(repr=False, init=False, default=1.0)

    # holds the final SVG code for the scale
    # value calculated post initiation
    scale: str = field(repr=False, init=False, default=str())

    def __post_init__(self):

        # convert interval value to upper case if not already upper case
        self.intervals = self.intervals.upper()

        # use today if start not given
        if self.start is None:
            self.start = date.today().toordinal()

        # use duration if no finish defined
        if self.finish is None:
            self.finish = (date.today() + timedelta(days=self.duration)).toordinal()

        # build scale
        self.scale = self.build_scale()

    def build_scale(self):
        iterator = get_iterator(self.start, self.finish, self.intervals)

        first_interval = TimeBox(min=self.start, max=self.finish, start=self.start, finish=iterator[0][0], resolution=2, background_color="black", border_width=0.5, fill='blue').get_element()
        last_interval = TimeBox(min=self.start, max=self.finish, start=iterator[-1][1], finish=self.finish, resolution=2, background_color="black", border_width=0.5, fill='blue').get_element()

        whole_intervals = str()
        for interval in iterator:
            whole_intervals += TimeBox(min=self.start, max=self.finish, start=interval[0], finish=interval[1], resolution=2, background_color="black", border_width=0.5).get_element()

        return first_interval + whole_intervals + last_interval

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

    # find start of first whole week in range
    first_seven_days = [date.fromordinal(start + day).weekday() for day in range(0, number_of_days)[:7]]
    first_week_start_day = first_seven_days.index(week_start)

    # build iterator
    range_start = first_week_start_day - 1  # start of first day is end of preceding day
    range_end = number_of_days - first_week_start_day  # cut range length proportionate to new range_start
    range_interval = 7  # weekly
    iterator = tuple()
    week_count = 1  # the first whole week counts as 1 (not 0 or 2)
    for day_number in range(range_start, range_end, range_interval):
        start_week = start + day_number  # first day_number value is 0
        end_week = start_week + 7
        entry = ((start_week, end_week, week_count), )
        iterator += entry
        week_count += 1  # prepare week_count for next entry
    return iterator


