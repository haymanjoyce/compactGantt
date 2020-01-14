from dataclasses import dataclass, field
from math import sqrt


@dataclass
class Meta:
    """
    Lets you add meta-data to the shape
    """

    layer: int = 100

    def get_meta(self):
        return self.layer


@dataclass
class Rect(Meta):

    x: float = 100
    y: float = 100
    width: float = 200
    height: float = 100
    fill: str = 'red'
    border_color: str = 'black'
    border_width: int = 1
    rounding: int = 2

    def get_item(self):
        return self.get_meta(), self.get_element()

    def get_element(self):
        return f'<rect ' \
               f'x="{self.x}" y="{self.y}" ' \
               f'rx="{self.rounding}" ry="{self.rounding}" ' \
               f'width="{self.width}" height="{self.height}" ' \
               f'stroke="{self.border_color}" stroke-width="{self.border_width}" ' \
               f'fill="{self.fill}" ' \
               f'></rect>'


@dataclass
class Line(Meta):

    x1: float = 50
    x2: float = 200
    y1: float = 100
    y2: float = 100
    stroke: str = 'black'
    stroke_width: int = 5
    stroke_line_cap: str = str()
    stroke_dasharray: str = str()  # dash gap dash gap

    def get_item(self):
        return self.get_meta(), self.get_element()

    def get_element(self):
        return f'<line ' \
               f'x1="{self.x1}" y1="{self.y1}" ' \
               f'x2="{self.x2}" y2="{self.y2}" ' \
               f'stroke="{self.stroke}" ' \
               f'stroke-width="{self.stroke_width}" ' \
               f'stroke-line-cap="{self.stroke_line_cap}" ' \
               f'stroke-dasharray="{self.stroke_dasharray}" ' \
               f'></line>'


@dataclass
class Circle(Meta):

    size: float = 50
    x: float = 100
    y: float = 100
    stroke: str = 'black'
    stroke_width: int = 1
    fill: str = 'red'
    r: float = field(init=False, repr=False)
    cx: float = field(init=False, repr=False)
    cy: float = field(init=False, repr=False)

    def __post_init__(self):
        self.r = self.size / 2
        self.cx = self.x + self.r
        self.cy = self.y + self.r

    def get_item(self):
        return self.get_meta(), self.get_element()

    def get_element(self):
        return f'<circle ' \
               f'cx="{self.cx}" cy="{self.cy}" ' \
               f'r="{self.r}" ' \
               f'stroke="{self.stroke}" ' \
               f'stroke-width="{self.stroke_width}" ' \
               f'fill="{self.fill}" ' \
               f'></circle>'


@dataclass
class Box(Meta):
    """
    Rectangle where the border line does not bleed over the outer edge
    Define the background color if rectangle rounded
    """

    x: float = 100
    y: float = 100
    width: float = 200
    height: float = 100
    fill: str = 'red'
    background_color: str = 'white'
    border_color: str = 'black'
    border_width: int = 1
    rounding: int = 2

    def get_item(self):
        return self.get_meta(), self.get_element()

    def get_element(self):
        return f'<g ' \
               f'transform="translate({self.x}, {self.y})"' \
               f'><rect ' \
               f'x="0" y="0" ' \
               f'width="{self.width}" height="{self.height}" ' \
               f'fill="{self.background_color}" ' \
               f'></rect><rect ' \
               f'x="{self.border_width / 2}" y="{self.border_width / 2}" ' \
               f'rx="{self.rounding}" ry="{self.rounding}" ' \
               f'width="{self.width - self.border_width}" height="{self.height - self.border_width}" ' \
               f'stroke="{self.border_color}" stroke-width="{self.border_width}" ' \
               f'fill="{self.fill}" ' \
               f'></rect>' \
               f'</g>'


@dataclass
class Diamond(Rect):
    """
    Rotates and shrink-fits a square
    """

    size: float = 100  # overrides height and width
    height: float = field(init=False, repr=False)
    width: float = field(init=False, repr=False)
    rotate: int = field(default=45)
    origin: float = field(init=False, repr=False)
    resized: float = field(init=False, repr=False)
    repositioned: float = field(init=False, repr=False)

    def __post_init__(self):
        self.origin = self.size / 2
        self.resized = self.size / sqrt(2)
        self.repositioned = (self.size - self.resized) / 2

    def get_element(self):
        return f'<rect ' \
               f'x="{self.x + self.repositioned}" y="{self.y + self.repositioned}" ' \
               f'rx="{self.rounding}" ry="{self.rounding}" ' \
               f'transform="rotate({self.rotate} {self.x + self.origin} {self.y + self.origin})" ' \
               f'width="{self.resized}" height="{self.resized}" ' \
               f'stroke="{self.border_color}" stroke-width="{self.border_width}" ' \
               f'fill="{self.fill}" ' \
               f'></rect>'


@dataclass
class Text(Meta):

    x: float = 100
    y: float = 100
    rotate: int = 0
    rotate_x: float = None
    rotate_y: float = None
    translate_x: float = 0
    translate_y: float = 0  # add 0.35 of text size for middle align
    text: str = str()
    text_anchor: str = str()  # start | middle | end
    fill: str = 'black'
    font_size: str = str(50)  # 2em | smaller | etc.
    font_family: str = str()  # "Arial, Helvetica, sans-serif"
    font_style: str = str()  # normal | italic | oblique
    font_weight: str = str()  # normal | bold | bolder | lighter | <number>

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

    def get_item(self):
        return self.get_meta(), self.get_element()

    def get_element(self):
        return f'<text ' \
               f'x="{self.x}" y="{self.y}" ' \
               f'fill="{self.fill}" ' \
               f'transform="' \
               f'translate({self.translate_x}, {self.translate_y}) ' \
               f'rotate({self.rotate}, {self.rotate_x}, {self.rotate_y})" ' \
               f'font-size="{self.font_size}" ' \
               f'font-family="{self.font_family}" ' \
               f'text-anchor="{self.text_anchor}" ' \
               f'font-style="{self.font_style}" ' \
               f'font-weight="{self.font_weight}" ' \
               f'>' \
               f'{self.text}' \
               f'</text>'

