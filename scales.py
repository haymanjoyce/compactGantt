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
    Builds scale out of TimeBoxes
    """

    # Does not inherit TimeBox because it is a different kind of object

    # todo clean up comments
    # todo add in resolution calc based on width
    # todo add text
    # todo work out why build_scale not working

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

    # scale styling
    background_color: str = 'black'
    border_color: str = 'black'
    border_width: float = 1
    rounding: int = 1
    fill: str = 'grey'
    ends: str = None  # option to use different fill on scale ends

    # defines pixels per day
    # passed to TimeBox
    # value calculated, based on width, after initiation
    resolution: float = field(repr=False, init=False, default=4.0)

    # holds the final SVG code for the scale
    # value calculated after initiation
    scale: str = field(repr=False, init=False, default=str())

    def __post_init__(self):

        # convert interval value to upper case if not already upper case
        self.intervals = self.intervals.upper()

        # use today if start not given
        if self.start is None:
            self.start = date.today().toordinal()

        # use duration if no finish defined
        if self.finish is None:
            self.finish = self.start + self.duration

        # use fill if no end fill is defined
        if self.ends is None:
            self.ends = self.fill

        # build scale
        self.scale = self.build_scale()

    def build_scale(self):

        # iterator is not object specific
        iterator = get_iterator(self.start, self.finish, self.intervals)

        # NEW METHOD

        # SVG string
        scale = str()

        # create TimeBox object
        timebox = TimeBox()

        # general settings of TimeBox object
        timebox.min = self.start
        timebox.max = self.finish
        timebox.height = self.height
        timebox.resolution = self.resolution
        timebox.background_color = self.background_color
        timebox.border_color = self.border_color
        timebox.border_width = self.border_width
        timebox.rounding = self.rounding

        # first interval
        timebox.start = self.start
        timebox.finish = iterator[0][0]
        timebox.fill = self.ends
        scale += timebox.get_element()

        # last interval
        timebox.start = iterator[-1][1]
        timebox.finish = self.finish
        scale += timebox.get_element()

        # whole intervals
        timebox.fill = self.fill
        for interval in iterator:
            timebox.start = interval[0]
            timebox.finish = interval[1]
            scale += timebox.get_element()

        # OLD METHOD

        # first interval
        first_interval = TimeBox(min=self.start, max=self.finish,
                                 start=self.start, finish=iterator[0][0],
                                 height=self.height,
                                 resolution=self.resolution,
                                 background_color=self.background_color, fill='green', border_color=self.border_color,
                                 border_width=self.border_width, rounding=self.rounding).get_element()

        # last interval
        last_interval = TimeBox(min=self.start, max=self.finish,
                                start=iterator[-1][1], finish=self.finish,
                                height=self.height,
                                resolution=self.resolution,
                                background_color=self.background_color, fill='green', border_color=self.border_color,
                                border_width=self.border_width, rounding=self.rounding).get_element()

        # whole intervals
        whole_intervals = str()
        for interval in iterator:
            whole_intervals += TimeBox(min=self.start, max=self.finish,
                                       start=interval[0], finish=interval[1],
                                       height=self.height,
                                       resolution=self.resolution,
                                       background_color=self.background_color, fill=self.fill,
                                       border_color=self.border_color,
                                       border_width=self.border_width, rounding=self.rounding).get_element()

        return first_interval + last_interval + whole_intervals
        # return scale

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


