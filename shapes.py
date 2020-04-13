from dataclasses import dataclass
from math import sqrt


@dataclass
class Point:
    """Base coordinate for all shape classes"""

    x: float = 0
    y: float = 0


@dataclass
class Line(Point):

    line_dx: float = 200
    line_dy: float = 100
    line_stroke_color: str = 'black'
    line_stroke_width: int = 5
    line_stroke_line_cap: str = str('butt')  # butt | round | square
    line_stroke_dasharray: str = str()  # dash gap dash gap

    def get_line(self):

        return f'<line ' \
               f'x1="{self.x}" y1="{self.y}" ' \
               f'x2="{self.line_dx}" y2="{self.line_dy}" ' \
               f'stroke="{self.line_stroke_color}" ' \
               f'stroke-width="{self.line_stroke_width}" ' \
               f'stroke-line-cap="{self.line_stroke_line_cap}" ' \
               f'stroke-dasharray="{self.line_stroke_dasharray}" ' \
               f'></line>'


@dataclass
class Circle(Point):

    circle_size: float = 50
    circle_stroke_color: str = 'black'
    circle_stroke_width: int = 1
    circle_fill_color: str = 'red'

    def get_circle(self):

        r = self.circle_size / 2
        cx = self.x + r
        cy = self.y + r

        return f'<circle ' \
               f'cx="{cx}" cy="{cy}" ' \
               f'r="{r}" ' \
               f'stroke="{self.circle_stroke_color}" ' \
               f'stroke-width="{self.circle_stroke_width}" ' \
               f'fill="{self.circle_fill_color}" ' \
               f'></circle>'


@dataclass
class Rectangle(Point):

    rectangle_width: float = 200
    rectangle_height: float = 100
    rectangle_fill_color: str = 'red'
    rectangle_border_color: str = 'black'
    rectangle_border_width: float = 1
    rectangle_border_rounding: int = 2
    rectangle_visibility: str = str()

    def get_rect(self):

        return f'<rect ' \
               f'x="{self.x}" y="{self.y}" ' \
               f'rx="{self.rectangle_border_rounding}" ry="{self.rectangle_border_rounding}" ' \
               f'width="{self.rectangle_width}" height="{self.rectangle_height}" ' \
               f'stroke="{self.rectangle_border_color}" stroke-width="{self.rectangle_border_width}" ' \
               f'fill="{self.rectangle_fill_color}" ' \
               f'visibility="{self.rectangle_visibility}" ' \
               f'></rect>'


@dataclass
class Diamond(Rectangle):

    diamond_size: float = 50  # replaces height and width

    def get_diamond(self):

        origin = self.diamond_size / 2
        resized = self.diamond_size / sqrt(2)
        repositioned = (self.diamond_size - resized) / 2

        return f'<rect ' \
               f'x="{self.x + repositioned}" y="{self.y + repositioned}" ' \
               f'rx="{self.rectangle_border_rounding}" ry="{self.rectangle_border_rounding}" ' \
               f'transform="rotate(45 {self.x + origin} {self.y + origin})" ' \
               f'width="{resized}" height="{resized}" ' \
               f'stroke="{self.rectangle_border_color}" stroke-width="{self.rectangle_border_width}" ' \
               f'fill="{self.rectangle_fill_color}" ' \
               f'></rect>'


@dataclass
class Text(Point):

    text: str = str()

    text_rotate: int = 0
    text_translate_x: float = 0
    text_translate_y: float = 0  # add 0.35 of text size for middle align
    text_anchor: str = str()  # start | middle | end
    text_visibility: str = str()

    font_fill_color: str = 'black'
    font_size: str = str(20)  # 2em | smaller | etc.
    font_family: str = str()  # "Arial, Helvetica, sans-serif"
    font_style: str = str()  # normal | italic | oblique
    font_weight: str = str()  # normal | bold | bolder | lighter | <number>

    def get_text(self):

        return f'<text ' \
               f'x="{self.x}" y="{self.y}" ' \
               f'fill="{self.font_fill_color}" ' \
               f'transform="' \
               f'translate({self.text_translate_x}, {self.text_translate_y}) ' \
               f'rotate({self.text_rotate} {self.x} {self.y})" ' \
               f'font-size="{self.font_size}" ' \
               f'font-family="{self.font_family}" ' \
               f'text-anchor="{self.text_anchor}" ' \
               f'font-style="{self.font_style}" ' \
               f'font-weight="{self.font_weight}" ' \
               f'visibility="{self.text_visibility}" ' \
               f'>' \
               f'{self.text}' \
               f'</text>'

