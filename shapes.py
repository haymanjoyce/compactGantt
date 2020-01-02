from dataclasses import dataclass, field, astuple


@dataclass
class Box:
    """
    This is a custom box model
    The border line does not bleed over the outer edge, as defined by width and height
    You can apply padding, and color to the padding
    The 'layer' variable defines the order in which the SVG element is rendered
    """

    x: float = 100
    y: float = 100
    width: float = 200
    height: float = 100
    outer_color: str = 'red'
    inner_color: str = 'blue'
    border_color: str = 'green'
    padding: float = 10
    border: float = 10
    rounding: float = 5
    layer: int = 100
    inner_origin: float = field(init=False, repr=False)
    inner_size_reduction: float = field(init=False, repr=False)

    def __iter__(self):
        return self

    def __post_init__(self):
        self.inner_origin = self.padding + (self.border / 2)
        self.inner_size_reduction = (self.padding * 2) + self.border

    def make_tuple(self):
        return self.layer, self.make_element()

    def make_element(self):
        return f'<g ' \
               f'transform="translate({self.x}, {self.y})"' \
               f'><rect ' \
               f'x="0" y="0" ' \
               f'width="{self.width}" height="{self.height}" ' \
               f'fill="{self.outer_color}" ' \
               f'></rect><rect ' \
               f'x="{self.inner_origin}" y="{self.inner_origin}" ' \
               f'rx="{self.rounding}" ry="{self.rounding}" ' \
               f'width="{self.width - self.inner_size_reduction}" height="{self.height - self.inner_size_reduction}" ' \
               f'stroke="{self.border_color}" stroke-width="{self.border}" ' \
               f'fill="{self.inner_color}" ' \
               f'></rect>' \
               f'</g>'

# REWRITE CLASSES BELOW


@dataclass
class Diamond(Box):
    """
    TBC
    """

    size: float = 50
    orientation: int = field(default=45)
    tx: float = 0
    ty: float = 0

    def __post_init__(self):
        self.box_padding_doubled = self.padding * 2
        self.box_border_halved = self.border / 2
        self.box_inner_rx = self.rounding
        self.box_inner_ry = self.rounding
        self.box_inner_x = self.padding + self.box_border_halved
        self.box_inner_y = self.padding + self.box_border_halved
        self.box_inner_width = self.width - self.box_padding_doubled - self.border
        self.box_inner_height = self.height - self.box_padding_doubled - self.border
        self.box_inner_tx = self.width / 2
        self.box_inner_ty = self.height / 2
        self.box_inner_angle = 45

    def __str__(self):
        return f'<g transform="translate({self.x}, {self.y})">' \
               f'<rect x="0" y="0" width="{self.width}" height="{self.height}" fill="{self.outer_color}" ' \
               f'>' \
               f'</rect>' \
               f'<rect x="{self.box_inner_x}" y="{self.box_inner_y}" rx="{self.box_inner_rx}" ry="{self.box_inner_ry}" ' \
               f'width="{self.box_inner_width}" height="{self.box_inner_height}" stroke="{self.border_color}" ' \
               f'stroke-width="{self.border}" fill="{self.inner_color}" ' \
               f'transform="rotate({self.orientation}, {self.tx}, {self.ty})" ' \
               f'>' \
               f'</rect>' \
               f'</g>'


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


@dataclass
class Text:
    pass

