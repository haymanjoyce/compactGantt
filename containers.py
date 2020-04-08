"""Module for building features with container relationships"""

# todo possible renaming and redefining of this module
# todo each feature needs to be placement ready
# todo add display layer to Base
# todo add Scale and Grid but put cleaning and tuple of tuples elsewhere
# todo add other features like annotation

from dataclasses import dataclass
from shapes import Rect, Circle, Diamond, Text


@dataclass
class Base:

    id: int = int()
    parent: int = int()


@dataclass
class Row(Base, Rect):

    def get_row(self):

        return f'{self.get_rect()}'


@dataclass
class TimeLine(Base, Rect):

    def get_timeline(self):

        return f'{self.get_rect()}'


@dataclass
class SwimLane(Base, Rect):

    def get_swimlane(self):

        return f'{self.get_rect()}'


@dataclass
class Task(Base, Rect, Text):

    def get_task(self):

        return f'{self.get_rect()} ' \
               f'{self.get_text()}'


@dataclass
class Milestone(Base, Circle, Diamond, Text):

    diamond: bool = True

    def get_milestone(self):

        if self.diamond:
            pass
        else:
            pass

        return f'{self.get_diamond()} ' \
               f'{self.get_text()}'


@dataclass
class Group(Base, Rect, Text):

    def get_group(self):

        return f'{self.get_rect()} ' \
               f'{self.get_text()}'


@dataclass
class Cell(Base, Rect, Text):

    def get_cell(self):
        return f'{self.get_rect()} ' \
               f'{self.get_text()}'

