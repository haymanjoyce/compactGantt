from shapes import Box
from dataclasses import dataclass, field
from datetime import date


@dataclass
class TimeBox(Box):
    """
    Builds Box using dates
    """

    # Class assumes it is receiving ordinal dates
    # We don't change the values of date attributes (good design imho)

    start: int = field(default=date.toordinal(date.today()))
    finish: int = None

    min: int = None  # defines lower limit such as left edge
    max: int = None  # defines upper limit such as right edge

    resolution: float = 1

    def __post_init__(self):

        # if no finish given then we create arbitrary finish
        if self.finish is None:
            self.finish = self.start + 800

        # if none given then we assume same as start and finish
        if self.min is None:
            self.min = self.start
        if self.max is None:
            self.max = self.finish

        # don't display if finish less than min
        if self.finish < self.min:
            self.x = 0
            self.width = 0
            self.visibility = 'hidden'
        # don't display if start more than max
        elif self.start > self.max:
            self.x = 0
            self.width = 0
            self.visibility = 'hidden'
        # crop left part if start less than min
        elif self.start < self.min:
            self.x = 0
            self.width = self.finish - self.min  # and converted to pixels
        # crop right part if finish more than max
        elif self.finish > self.max:
            self.x = self.start  # and converted to pixels
            self.width = self.max - self.start  # and converted to pixels
        # display whole box
        else:
            self.x = self.start - self.min  # and converted to pixels
            self.width = self.finish - self.start  # and converted to pixels


@dataclass
class Scale:
    """
    Arranges TimeBoxes to form scale
    """

    x: float = 100
    y: float = 100
    width: float = 800
    height: float = 100

    def __post_init__(self):
        pass

    def build_scale(self):
        # todo build this
        pass

    def get_element(self):
        return f'<g ' \
               f'transform="translate({self.x}, {self.y})"' \
               f'>' \
               f'{Box(y=200).get_element()}{Box(y=500).get_element()}' \
               f'</g>' \

