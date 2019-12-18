from dataclasses import dataclass


@dataclass
class Box:
    """
    Somewhat like the CSS box model
    """

    x: float = 100
    y: float = 600

    width: float = 200
    height: float = 100

    background_color: str = 'blue'

    padding: float = 10

    stroke_width: float = 10
    stroke: str = 'black'
    fill: str = 'red'
    style: str = ''

    rx: int = 10
    ry: int = 10

    inner_x: float = 0
    inner_y: float = 0

    inner_width: float = 0
    inner_height: float = 0

    def __post_init__(self):
        self.inner_x = self.padding + (self.stroke_width / 2)
        self.inner_y = self.padding + (self.stroke_width / 2)
        self.inner_width = self.width - (self.padding * 2) - self.stroke_width
        self.inner_height = self.height - (self.padding * 2) - self.stroke_width

    def __str__(self):
        return f'<g transform="translate({self.x}, {self.y})">' \
               f'<rect x="0" y="0" width="{self.width}" height="{self.height}" fill="{self.background_color}"></rect>' \
               f'<rect x="{self.inner_x}" y="{self.inner_y}" rx="{self.rx}" ry="{self.ry}" width="{self.inner_width}" height="{self.inner_height}" stroke="{self.stroke}" stroke-width="{self.stroke_width}" fill="{self.fill}" style="{self.style}"></rect>' \
               f'</g>'


@dataclass
class Rectangle:
    """
    Standard SVG rectangle
    """
    x: float = 100
    y: float = 100
    rx: int = 0
    ry: int = 0
    width: float = 200
    height: float = 100
    style: str = None  # string created by Style class

    def __str__(self):
        return f'<rect x="{self.x}" y="{self.y}" ' \
               f'rx="{self.rx}" ry="{self.ry}" ' \
               f'width="{self.width}" height="{self.height}" ' \
               f'style="{self.style}"></rect>'


@dataclass
class Diamond:
    """
    This class simply rotates an SVG rectangle that has equal width and length
    """

    x: float = 200
    y: float = 200
    x2: float = 0
    y2: float = 0
    rx: int = 0
    ry: int = 0
    size: float = 10
    half_size: float = 0
    fill: str = 'blue'  # option to pass fill as SVG attribute
    style: str = ''  # string created by Style class

    def __post_init__(self):
        self.half_size = self.size / 2
        self.x2 = self.x + self.half_size
        self.y2 = self.y + self.half_size

    def __str__(self):
        return f'<rect x="{self.x}" y="{self.y}" ' \
               f'rx="{self.rx}" ry="{self.ry}" ' \
               f'width="{self.size}" height="{self.size}" ' \
               f'fill="{self.fill}" ' \
               f'style="{self.style}" ' \
               f'transform="rotate(45, {self.x2}, {self.y2})" ' \
               f'></rect>'


@dataclass
class Line:
    """
    Standard SVG line
    """
    pass


@dataclass
class Circle:
    """
    Standard SVG circle
    """
    pass


@dataclass
class Style:
    """
    Pumps out CSS attributes to put into the SVG style attribute
    Tip: Surround object with str() if passing as argument
    """

    fill: str = None
    stroke: int = None
    stroke_width: float = None
    opacity: int = None

    def __str__(self):
        return f'fill: {self.fill}; ' \
               f'stroke: {self.stroke}; ' \
               f'stroke-width: {self.stroke_width}' \
               f'opacity: {self.opacity}'

