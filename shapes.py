"""Module for building SVG shapes"""

# todo if you need to update post init vars then declare vars in post init but move calcs to method

from dataclasses import dataclass
from math import sqrt


@dataclass
class Point:
    """Base coordinate for all shape classes"""

    x: float = 0
    y: float = 0


@dataclass
class Line(Point):

    dx: float = 200
    dy: float = 100
    stroke: str = 'black'
    stroke_width: int = 5
    stroke_line_cap: str = str('butt')  # butt | round | square
    stroke_dasharray: str = str()  # dash gap dash gap

    def get_line(self):
        return f'<line ' \
               f'x1="{self.x}" y1="{self.y}" ' \
               f'x2="{self.dx}" y2="{self.dy}" ' \
               f'stroke="{self.stroke}" ' \
               f'stroke-width="{self.stroke_width}" ' \
               f'stroke-line-cap="{self.stroke_line_cap}" ' \
               f'stroke-dasharray="{self.stroke_dasharray}" ' \
               f'></line>'


@dataclass
class Circle(Point):

    size: float = 50
    stroke: str = 'black'
    stroke_width: int = 1
    fill: str = 'red'

    def __post_init__(self):
        self.r = self.size / 2
        self.cx = self.x + self.r
        self.cy = self.y + self.r

    def get_circle(self):
        return f'<circle ' \
               f'cx="{self.cx}" cy="{self.cy}" ' \
               f'r="{self.r}" ' \
               f'stroke="{self.stroke}" ' \
               f'stroke-width="{self.stroke_width}" ' \
               f'fill="{self.fill}" ' \
               f'></circle>'


@dataclass
class Rect(Point):

    width: float = 200
    height: float = 100
    fill: str = 'red'
    border_color: str = 'black'
    border_width: int = 1
    rounding: int = 2
    visibility: str = str()

    def get_rect(self):
        return f'<rect ' \
               f'x="{self.x}" y="{self.y}" ' \
               f'rx="{self.rounding}" ry="{self.rounding}" ' \
               f'width="{self.width}" height="{self.height}" ' \
               f'stroke="{self.border_color}" stroke-width="{self.border_width}" ' \
               f'fill="{self.fill}" ' \
               f'visibility="{self.visibility}" ' \
               f'></rect>'


@dataclass
class Diamond(Rect):

    size: float = 50  # replaces height and width

    def __post_init__(self):
        self.origin = self.size / 2
        self.resized = self.size / sqrt(2)
        self.repositioned = (self.size - self.resized) / 2

    def get_diamond(self):
        return f'<rect ' \
               f'x="{self.x + self.repositioned}" y="{self.y + self.repositioned}" ' \
               f'rx="{self.rounding}" ry="{self.rounding}" ' \
               f'transform="rotate(45 {self.x + self.origin} {self.y + self.origin})" ' \
               f'width="{self.resized}" height="{self.resized}" ' \
               f'stroke="{self.border_color}" stroke-width="{self.border_width}" ' \
               f'fill="{self.fill}" ' \
               f'></rect>'


@dataclass
class Text(Point):

    rotate: int = 0
    rotate_x: float = None
    rotate_y: float = None
    translate_x: float = 0
    translate_y: float = 0  # add 0.35 of text size for middle align
    text: str = str()
    text_anchor: str = str()  # start | middle | end
    font_fill: str = 'black'
    font_size: str = str(20)  # 2em | smaller | etc.
    font_family: str = str()  # "Arial, Helvetica, sans-serif"
    font_style: str = str()  # normal | italic | oblique
    font_weight: str = str()  # normal | bold | bolder | lighter | <number>
    text_visibility: str = str()

    # scale_x: float = 1  # the app does not need this feature
    # scale_y: float = 1  # the app does not need this feature
    # skew_x: int = int()  # the app does not need this feature
    # skew_y: int = int()  # the app does not need this feature
    # text_decoration: str = field(init=False, repr=False, default=str())  # does not render on GUI
    # font_size_adjust: float = field(init=False, repr=False, default=float())  # does not render on GUI or browser
    # font_stretch: str = field(init=False, repr=False, default=str())  # does not render on GUI or browser
    # font_variant: str = field(init=False, repr=False, default=str())  # does not render on GUI
    # dx: float = field(init=False, repr=False, default=float())  # does not render on GUI
    # dy: float = field(init=False, repr=False, default=float())  # does not render on GUI
    # text_length: float = field(init=False, repr=False, default=float())  # does not render on GUI
    # length_adjust: str = field(init=False, repr=False, default=str())  # does not render on GUI
    # word_spacing: int = field(init=False, repr=False, default=int())  # does not render on GUI
    # letter_spacing: int = field(init=False, repr=False, default=int())  # does not render on GUI
    # dominant_baseline: str = field(init=False, repr=False, default=str())  # does not render on GUI
    # alignment_baseline: str = field(init=False, repr=False, default=str())  # only applies to tspan element

    def __post_init__(self):
        if self.rotate_x is None:
            self.rotate_x = self.x
        if self.rotate_y is None:
            self.rotate_y = self.y

    def get_text(self):
        return f'<text ' \
               f'x="{self.x}" y="{self.y}" ' \
               f'fill="{self.font_fill}" ' \
               f'transform="' \
               f'translate({self.translate_x}, {self.translate_y}) ' \
               f'rotate({self.rotate}, {self.rotate_x}, {self.rotate_y})" ' \
               f'font-size="{self.font_size}" ' \
               f'font-family="{self.font_family}" ' \
               f'text-anchor="{self.text_anchor}" ' \
               f'font-style="{self.font_style}" ' \
               f'font-weight="{self.font_weight}" ' \
               f'visibility="{self.text_visibility}" ' \
               f'>' \
               f'{self.text}' \
               f'</text>'

