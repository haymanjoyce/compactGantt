from shapes import *
from dataclasses import dataclass, field
from datetime import *
from time import *


@dataclass
class TimeBox(Box):

    start: int = 737400
    finish: int = 737600
    min: int = 737450  # defines lower limit such as left edge
    max: int = 7374550  # defines upper limit such as right edge
    resolution: float = 2

    def __post_init__(self):
        if self.start < self.min:  # if off the left hand edge
            self.x = 0
            # self.width is...
            # convert to pixels
        elif self.start > self.max:  # if off the right hand edge
            self.x = 0
            self.width = 0
            self.visibility = 'hidden'
        else:
            self.x = self.start - self.min  # x in days if min was 0
            # width is...
            # convert to pixels


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

