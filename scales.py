from shapes import *
from dataclasses import dataclass, field
from datetime import *
from time import *


@dataclass
class TimeBox(Box):

    # Class assumes it is receiving ordinal dates
    # We don't change the values of date attributes (good design imho)

    min: int = None  # defines lower limit such as left edge
    max: int = None  # defines upper limit such as right edge
    start: int = None
    finish: int = None
    resolution: float = 1

    def __post_init__(self):
        if self.start is None:
            self.start = date.toordinal(date.today())
        if self.min is None:
            self.min = self.start
        if self.finish is None:
            self.finish = self.start + 100
        if self.max is None:
            self.max = self.finish
        if self.finish < self.min:  # if finish off left edge
            self.x = 0
            self.width = 0
            self.visibility = 'hidden'
        elif self.start > self.max:  # if start off right edge
            self.x = 0
            self.width = 0
            self.visibility = 'hidden'
        elif self.start < self.min:  # if start off left edge
            self.x = 0
            self.width = self.finish - self.min  # and converted to pixels
        elif self.finish > self.max:  # if finish off right edge
            self.x = self.start  # and converted to pixels
            self.width = self.max - self.start  # and converted to pixels
        else:
            self.x = self.start - self.min  # and converted to pixels
            self.width = self.finish - self.start  # and converted to pixels


@dataclass
class Scale:

    x: float = 100
    y: float = 100
    width: float = 800
    height: float = 100
    layer: int = 1
    intervals: int = 30
    # mask_width: float = field(init=False)
    # mask_height: float = field(init=False)
    # mask_start: float = field(init=False)
    # mask_finish: float = field(init=False)

    def __iter__(self):
        pass

    def __post_init__(self):
        pass

    def make_tuple(self):
        return self.layer, self.make_element()

    def make_element(self):
        return f'<g ' \
               f'transform="translate({self.x}, {self.y})"' \
               f'>' \
               f'{Box(y=200).get_element()}{Box(y=500).get_element()}' \
               f'</g>' \

