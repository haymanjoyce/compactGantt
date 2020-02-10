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

    x: float = 0
    y: float = 0

    width: float = 800
    height: float = 100

    start: int = None
    finish: int = None

    duration: int = None
    resolution: float = None

    scale: str = str()

    def __post_init__(self):
        self.start = date.today().toordinal()
        self.finish = (date.today() + timedelta(days=365)).toordinal()
        self.duration = self.finish - self.start

        start = self.start
        finish = start + 7
        for day in range(self.duration):
            self.scale += TimeBox(min=self.start, max=self.finish, start=start, finish=finish, resolution=2, background_color="black", border_width=0.5).get_element()
            start += 7
            finish += 7

    def get_element(self):
        return f'<g ' \
               f'transform="translate({self.x}, {self.y})"' \
               f'>' \
               f'{self.scale}' \
               f'</g>' \

