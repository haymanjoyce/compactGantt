"""Module for rows, groups, and swimlanes"""

# todo swimlanes
# todo ability to style SVG elements
# todo possible Rows class for building multiple rows with one interface


from dataclasses import dataclass
from shapes import Rect, Text


@dataclass
class Task(Rect):

    id: int = int()
    parent: int = int()  # parent group

    def __post_init__(self):
        pass

    def build_row(self):
        pass

    def get_row(self):
        pass


@dataclass
class Row(Rect):

    id: int = int()
    parent: int = int()  # parent group

    def __post_init__(self):
        pass

    def build_row(self):
        pass

    def get_row(self):
        pass


@dataclass
class Group:

    # it gets its height from sum of child rows or sum of child groups
    # it gets its width from group with greatest width in that level
    # if no children then height is 0

    name: str = 'Test'
    parent: int = int()
    width: float = float()

    def __post_init__(self):
        pass

    def build_group(self):
        pass

    def get_group(self):
        pass

