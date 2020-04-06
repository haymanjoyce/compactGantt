"""Module for rows, groups, and swimlanes"""

# todo swimlanes
# todo ability to style SVG elements
# todo possible Rows class for building multiple rows with one interface


from dataclasses import dataclass
from shapes import Rect, Text


@dataclass
class Row:

    id: int = int()

    width: float = float()
    height: float = float()

    fill: str = 'red'
    border_color: str = 'black'
    border_width: int = 1
    rounding: int = 2
    visibility: str = str()

    parent: int = int()  # parent group

    def __post_init__(self):
        pass

    def build_group(self):
        pass

    def get_group(self):
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

