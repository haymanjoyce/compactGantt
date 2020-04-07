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

    row_padding: float = float()
    task_margin: float = float()

    def __post_init__(self):

        if 0 < self.row_padding < (self.height * 0.5):
            self.y += self.row_padding
            self.height -= self.row_padding * 2


@dataclass
class Group(Text):

    id: int = int()
    parent: int = int()

    def build_group(self):
        pass

    def get_group(self):
        pass

