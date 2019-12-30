from dataclasses import dataclass, field


@dataclass
class Box:
    """
    This is a custom box model
    The border line does not bleed over the outer edge, as defined by width and height
    You can apply padding, and color to the padding
    The object is returned as a tuple
    The tuple exposes the SVG element and its position in the render order
    """

    x: float = field(default=100, repr=False)
    y: float = field(default=100, repr=False)
    width: float = field(default=200, repr=False)
    height: float = field(default=100, repr=False)
    outer_color: str = field(default='red', repr=False)
    inner_color: str = field(default='blue', repr=False)
    border_color: str = field(default='green', repr=False)
    padding: float = field(default=10, repr=False)
    border: float = field(default=10, repr=False)
    rounding: float = field(default=5, repr=False)
    position: int = 100
    element: str = field(init=False)

    def __post_init__(self):
        inner_origin = self.padding + (self.border / 2)
        inner_size_reduction = (self.padding * 2) + self.border
        self.element = f'<g ' \
                       f'transform="translate({self.x}, {self.y})">' \
                       f'<rect ' \
                       f'x="0" y="0" ' \
                       f'width="{self.width}" height="{self.height}" ' \
                       f'fill="{self.outer_color}" ' \
                       f'></rect>' \
                       f'<rect ' \
                       f'x="{inner_origin}" y="{inner_origin}" ' \
                       f'rx="{self.rounding}" ry="{self.rounding}" ' \
                       f'width="{self.width - inner_size_reduction}" height="{self.height - inner_size_reduction}" ' \
                       f'stroke="{self.border_color}" stroke-width="{self.border}" ' \
                       f'fill="{self.inner_color}" ' \
                       f'></rect>' \
                       f'</g>'

    def __iter__(self):
        return self.position, self.element


@dataclass
class Diamond(Box):
    """
    TBC
    """

    size: float = 50
    orientation: int = field(init=False, default=45)
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

