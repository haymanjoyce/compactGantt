from dataclasses import dataclass, field


@dataclass
class Box:
    """
    A custom box model
    The border line does not bleed over the outer edge, as defined by width and height
    The border line does not bleed over the inner edge, as defined by inner_width and inner_height
    The inner dimensions are reduced to accommodate padding and border line width
    """

    x: float = 100
    y: float = 100

    width: float = 200
    height: float = 100

    padding_width: float = 10
    padding_width_doubled: float = field(init=False)
    padding_color: str = 'blue'

    border_width: float = 10
    border_width_halved: float = field(init=False)
    border_color: str = 'black'
    border_rounding: float = 5
    border_rx: float = field(init=False)
    border_ry: float = field(init=False)
    border_box_x: float = field(init=False)
    border_box_y: float = field(init=False)
    border_box_width: float = field(init=False)
    border_box_height: float = field(init=False)

    inner_box_x: float = field(init=False)
    inner_box_y: float = field(init=False)
    inner_box_width: float = field(init=False)
    inner_box_height: float = field(init=False)
    inner_box_color: str = 'red'

    def __post_init__(self):
        self.padding_width_doubled = self.padding_width * 2
        self.border_width_halved = self.border_width / 2
        self.border_rx = self.border_rounding
        self.border_ry = self.border_rounding
        self.border_box_x = self.padding_width + self.border_width_halved
        self.border_box_y = self.padding_width + self.border_width_halved
        self.border_box_width = self.width - self.padding_width_doubled - self.border_width
        self.border_box_height = self.height - self.padding_width_doubled - self.border_width
        self.inner_box_x = self.border_box_x + self.border_width_halved
        self.inner_box_y = self.border_box_y + self.border_width_halved
        self.inner_box_width = self.border_box_width - self.border_width
        self.inner_box_height = self.border_box_height - self.border_width

    def __str__(self):
        return f'<g transform="translate({self.x}, {self.y})">' \
               f'<rect x="0" y="0" width="{self.width}" height="{self.height}" fill="{self.padding_color}"></rect>' \
               f'<rect x="{self.border_box_x}" y="{self.border_box_y}" rx="{self.border_rx}" ry="{self.border_ry}" width="{self.border_box_width}" height="{self.border_box_height}" stroke="{self.border_color}" stroke-width="{self.border_width}" fill="{self.inner_box_color}"></rect>' \
               f'<rect x="{self.inner_box_x}" y="{self.inner_box_y}" width="{self.inner_box_width}" height="{self.inner_box_height}" fill="yellow"></rect>' \
               f'</g>'


@dataclass
class Diamond:
    """
    This class simply rotates a rectangle that has equal width and length
    """

    x: float = 100
    y: float = 100
    rx: float = 0
    ry: float = 0
    size: float = 50
    fill: str = 'blue'  # option to pass fill as SVG attribute

    stroke: str = 'rgb(0, 0, 0)'
    stroke_width: float = 1

    half_size: float = 0
    tx: float = 0
    ty: float = 0

    def __post_init__(self):
        self.half_size = self.size / 2
        self.tx = self.x + self.half_size
        self.ty = self.y + self.half_size

    def __str__(self):
        return f'<rect x="{self.x}" y="{self.y}" ' \
               f'rx="{self.rx}" ry="{self.ry}" ' \
               f'width="{self.size}" height="{self.size}" ' \
               f'fill="{self.fill}" ' \
               f'stroke="{self.stroke}" ' \
               f'stroke-width="{self.stroke_width}" ' \
               f'transform="rotate(45, {self.tx}, {self.ty})" ' \
               f'></rect>'


@dataclass
class Line:
    """
    This is a standard SVG line
    """

    x1: float = 0
    x2: float = 0
    y1: float = 0
    y2: float = 0
    style: str = None  # string created by Style class

    def __str__(self):
        return f'<line x1="{self.x1}" y1="{self.y1}" x2="{self.x2}" y2="{self.y2}" style="{self.style}" />'


@dataclass
class Circle:
    """
    This SVG circle has non-standard attributes
    If the circle was placed in a square, x and y would define its top-left corner
    Size, which is twice r, is used to keep language common across shape classes
    """

    size: float = 0
    r: float = field(init=False)
    x: float = 0
    y: float = 0
    cx: float = 0
    cy: float = 0
    style: str = None  # string created by Style class

    def __post_init__(self):
        self.r = self.size / 2
        self.cx = self.x + self.r
        self.cy = self.y + self.r

    def __str__(self):
        return f'<circle cx="{self.cx}" cy="{self.cy}" r="{self.r}" style="{self.style}"/>'

