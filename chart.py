# todo develop layout

from attr import attrs, attrib
from shapes import Rectangle


@attrs
class Chart:

    svg_elements = attrib(default=str())

    # this defines dimensions of root node in DOM
    chart_width = attrib(default=800)
    chart_height = attrib(default=600)

    # viewPort pretty much always the same as chart dimensions but make distinction anyway
    viewPort_width = attrib()
    viewPort_height = attrib()

    # chart node is abstract but option to render as rectangle
    rect = Rectangle()

    @viewPort_width.default
    def get_height(self):
        return self.chart_width

    @viewPort_height.default
    def get_height(self):
        return self.chart_height

    def __attrs_post_init__(self):
        self.rect.width = self.chart_width
        self.rect.height = self.chart_height
        self.rect.border_width = 0
        self.rect.fill_color = 'black'

    @property
    def svg(self):
        return f'<svg width="{self.viewPort_width}" height="{self.viewPort_height}" ' \
               f'id="chart" overflow="auto"> ' \
               f'{self.rect.svg}{self.svg_elements}' \
               f'</svg>'

