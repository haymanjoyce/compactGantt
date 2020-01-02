from shapes import Box
from dataclasses import dataclass, field

# the shape is base
# text is base
# width is base
# x is base
# y can be base
# ordinal is child
# unit may be derived


def scale_a(layer=1):

    a1 = Box(x=100, y=0, width=50, height=50, border=1, rounding=0, padding=2, inner_color='pink')

    scale = str()

    for i in range(1, 4):

        a1.y = (i * 100)
        scale += a1.make_element()

    return layer, scale


@dataclass
class Scale:

    x: float = 100
    y: float = 100
    width: float = 800
    height: float = 100
    layer: int = 1
    intervals: int = 30
    # mask_width: float = field(init=False)
    # mask_height: float = field(init=False)
    # mask_start: float = field(init=False)
    # mask_finish: float = field(init=False)

    def __iter__(self):
        pass

    def __post_init__(self):
        pass

    def make_tuple(self):
        return self.layer, self.make_element()

    def make_element(self):
        return f'<g ' \
               f'transform="translate({self.x}, {self.y})"' \
               f'>' \
               f'{Box(y=200).make_element()}{Box(y=500).make_element()}' \
               f'</g>' \

