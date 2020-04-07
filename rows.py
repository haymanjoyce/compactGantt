"""Module for rows, groups, and swimlanes"""

# todo possible swimlane class
# todo possible data column class
# todo possible renaming of this module

from dataclasses import dataclass
from shapes import Rect, Circle, Diamond, Text


@dataclass
class Task(Rect, Text):

    id: int = int()
    parent: int = int()  # parent row

    def build_task(self):
        pass

    def get_task(self):
        pass


@dataclass
class Milestone(Circle, Diamond, Text):

    id: int = int()
    parent: int = int()  # parent row

    def build_milestone(self):
        pass

    def get_milestone(self):
        pass


@dataclass
class Row(Rect):

    id: int = 1
    parent: int = int()  # parent group

    padding: float = float()  # reduces height of child tasks and milestones
    margin: float = float()  # reduces height of rectangle (but not row)


@dataclass
class Group(Text):

    id: int = int()
    parent: int = int()

    def build_group(self):
        pass

    def get_group(self):
        pass

