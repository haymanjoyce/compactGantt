# Module extends shape classes

from shapes import Box
from dataclasses import dataclass


@dataclass
class TimeBox(Box):
    """Builds Box using ordinal dates"""

    # we keep the date values as ordinal dates (we don't convert them into pixels)
    start: int = 0
    finish: int = 0

    # defines lower and uppers limits (i.e. edges), as ordinal dates
    min: int = 0
    max: int = 0

    # pixels per day
    resolution: float = 1

    def update(self):
        """Updates all variables"""

        # reset start if start less than min
        if self.start < self.min:
            self.start = self.min

        # reset finish is finish more than max
        if self.finish > self.max:
            self.finish = self.max

        # don't display if finish less than min
        if self.finish < self.min:
            self.visibility = 'hidden'

        # don't display if start more than max
        if self.start > self.max:
            self.visibility = 'hidden'

        # subtracts days before min
        self.x = (self.start - self.min) * self.resolution

        # difference, in days, between start and finish
        self.width = (self.finish - self.start) * self.resolution
