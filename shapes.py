from dataclasses import dataclass


@dataclass
class Style:
    fill: str = None
    stroke: int = None
    stroke_width: int = None
    opacity: int = None

    def __str__(self):
        return f'{self.fill}'

    def __post_init__(self):
        pass


@dataclass
class Rectangle:
    x: int = 0
    y: int = 0
    rx: int = 0
    ry: int = 0
    width: int = 200
    height: int = 100
    style: str = None  # string created by Style class

    def __str__(self):
        return f'{self.height}'

    def __post_init__(self):
        pass


@dataclass
class Frame:
    """
    Replicates CSS box model
    """

    def __str__(self):
        return f'<g transform="translate(100, 100)">' \
               f'<rect x="0" y="0" width="100" height="100" style="fill: green; stroke: black; stroke-width: 10px; stroke-dasharray: 20px, 20px;"></rect>' \
               f'<rect x="0" y="0" width="100" height="100" style="fill: red;"></rect>' \
               f'</g>'

    def __post_init__(self):
        pass


@dataclass
class Circle:
    pass


@dataclass
class Diamond:  # rotate square
    pass


@dataclass
class Line:
    pass

