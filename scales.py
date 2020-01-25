from shapes import *
from dataclasses import dataclass, field
from datetime import date


@dataclass
class TimeBox(Box):

    start: int = 0
    finish: int = 100
    min: int = 0
    max: int = 100
    resolution: float = 2
    duration: float = field(init=False)

    def __post_init__(self):
        pass


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

