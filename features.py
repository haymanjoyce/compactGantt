# todo add display layer to Base
# todo same line for {} things
# todo need window x and y
# todo pass objects to classes
# todo create layout classes in another module then pass their objects to features; features may need less of own vars
# todo rename TW variables such that tw.height

from dataclasses import dataclass
from shapes import Rectangle, Circle, Diamond, Line, Text


@dataclass
class Feature:
    """Feature variables used by many features"""

    # defines order in which feature is rendered
    layer: int = int()

    # identity field for feature (not all features need it)
    id: int = int()

    # used for container relationships
    parent: int = int()


@dataclass
class TextBox(Feature):
    pass


@dataclass
class Curtain(Feature):
    pass


@dataclass
class Bar(Feature):
    pass


@dataclass
class TimeLine(Feature, Rectangle):

    def get_timeline(self):
        return f'{self.get_rect()}'


@dataclass
class Task(Feature, Rectangle, Text):

    def get_task(self):
        return f'{self.get_rect()} ' \
               f'{self.get_text()}'


@dataclass
class Milestone(Feature, Circle, Diamond, Text):

    diamond: bool = True

    def get_milestone(self):

        if self.diamond:
            pass
        else:
            pass

        return f'{self.get_diamond()} ' \
               f'{self.get_text()}'


@dataclass
class Cell(Feature, Rectangle, Text):

    def get_cell(self):
        return f'{self.get_rect()} ' \
               f'{self.get_text()}'


@dataclass
class Row(Feature, Rectangle):

    def get_row(self):

        return f'{self.get_rect()}'


@dataclass
class SwimLane(Feature, Rectangle):

    def get_swimlane(self):
        return f'{self.get_rect()}'

