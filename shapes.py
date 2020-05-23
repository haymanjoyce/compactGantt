"""Classes whose objects represent shapes, which can return shapes as SVG elements"""

from attr import attrs
from math import sqrt


@attrs(auto_attribs=True)
class Line:

    x: float = 0
    y: float = 0
    dx: float = 200
    dy: float = 100
    stroke_color: str = 'black'
    stroke_width: int = 5
    stroke_line_cap: str = 'butt'  # butt | round | square
    stroke_dasharray: str = str()  # dash gap dash gap

    @property
    def svg(self):

        return f'<line ' \
               f'x1="{self.x}" y1="{self.y}" ' \
               f'x2="{self.dx}" y2="{self.dy}" ' \
               f'stroke="{self.stroke_color}" ' \
               f'stroke-width="{self.stroke_width}" ' \
               f'stroke-linecap="{self.stroke_line_cap}" ' \
               f'stroke-dasharray="{self.stroke_dasharray}" ' \
               f'></line>'


@attrs(auto_attribs=True)
class Circle:

    x: float = 0
    y: float = 0
    size: float = 50
    stroke_color: str = 'black'
    stroke_width: int = 1
    fill_color: str = 'red'

    @property
    def svg(self):

        r = self.size / 2
        cx = self.x + r
        cy = self.y + r

        return f'<circle ' \
               f'cx="{cx}" cy="{cy}" ' \
               f'r="{r}" ' \
               f'stroke="{self.stroke_color}" ' \
               f'stroke-width="{self.stroke_width}" ' \
               f'fill="{self.fill_color}" ' \
               f'></circle>'


@attrs(auto_attribs=True)
class Rectangle:

    x: float = 0
    y: float = 0
    width: float = 200
    height: float = 100
    fill_color: str = 'red'
    border_color: str = 'black'
    border_width: float = 1
    border_rounding: int = 2
    visibility: str = 'visible'

    @property
    def svg(self):

        return f'<rect ' \
               f'x="{self.x}" y="{self.y}" ' \
               f'rx="{self.border_rounding}" ry="{self.border_rounding}" ' \
               f'width="{self.width}" height="{self.height}" ' \
               f'stroke="{self.border_color}" stroke-width="{self.border_width}" ' \
               f'fill="{self.fill_color}" ' \
               f'visibility="{self.visibility}" ' \
               f'></rect>'


@attrs(auto_attribs=True)
class Diamond:

    x: float = 0
    y: float = 0
    size: float = 50
    fill_color: str = 'red'
    border_color: str = 'black'
    border_width: float = 1
    border_rounding: int = 2
    visibility: str = 'visible'

    @ property
    def svg(self):

        origin = self.size / 2
        resized = self.size / sqrt(2)
        repositioned = (self.size - resized) / 2

        return f'<rect ' \
               f'x="{self.x + repositioned}" y="{self.y + repositioned}" ' \
               f'rx="{self.border_rounding}" ry="{self.border_rounding}" ' \
               f'transform="rotate(45 {self.x + origin} {self.y + origin})" ' \
               f'width="{resized}" height="{resized}" ' \
               f'stroke="{self.border_color}" stroke-width="{self.border_width}" ' \
               f'fill="{self.fill_color}" ' \
               f'></rect>'


@attrs(auto_attribs=True)
class Text:

    text: str = str()
    text_x: float = 0
    text_y: float = 0
    text_translate_x: float = 0
    text_translate_y: float = 0  # add 0.35 of text size for middle align
    text_anchor: str = 'start'  # start | middle | end
    text_rotate: int = 0
    text_visibility: str = 'visible'  # visible | hidden
    font_fill_color: str = 'black'
    font_size: str = str(20)  # 2em | smaller | etc.
    font_family: str = str()  # "Arial, Helvetica, sans-serif"
    font_style: str = 'normal'  # normal | italic | oblique
    font_weight: str = 'normal'  # normal | bold | bolder | lighter | <number>

    @property
    def svg(self):

        return f'<text ' \
               f'x="{self.text_x}" y="{self.text_y}" ' \
               f'fill="{self.font_fill_color}" ' \
               f'transform="' \
               f'translate({self.text_translate_x}, {self.text_translate_y}) ' \
               f'rotate({self.text_rotate} {self.text_x} {self.text_y})" ' \
               f'font-size="{self.font_size}" ' \
               f'font-family="{self.font_family}" ' \
               f'text-anchor="{self.text_anchor}" ' \
               f'font-style="{self.font_style}" ' \
               f'font-weight="{self.font_weight}" ' \
               f'visibility="{self.text_visibility}" ' \
               f'>' \
               f'{self.text}' \
               f'</text>'

