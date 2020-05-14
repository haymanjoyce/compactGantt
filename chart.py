# todo develop layout

from attr import attrs, attrib
from shapes import Rectangle


@attrs
class Chart:

    chart_objects = attrib(default=list())
    svg_string = attrib(default=str())

    viewPort_width = 800
    viewPort_height = 600

    def order_objects(self):
        pass

    def render_objects(self):
        for chart_object in self.chart_objects:
            self.svg_string += chart_object.svg

    def wrap_string(self):
        self.svg_string = f'<svg width="{self.viewPort_width}" height="{self.viewPort_height}" ' \
                          f'id="chart" overflow="auto"> ' \
                          f'{self.svg_string}' \
                          f'</svg>'


@attrs
class Layout:

    chart_width = attrib(default=800)
    chart_height = attrib(default=600)

    svg_strings = attrib(default=str())

    rect = Rectangle()

    def __attrs_post_init__(self):
        pass

    def chart_area(self):
        self.rect.width = self.chart_width
        self.rect.height = self.chart_height
        self.rect.border_width = 0
        self.rect.fill_color = 'black'

    def banner_areas(self):
        pass

    def column_areas(self):
        pass

    def scale_areas(self):
        pass

    def plot_area(self):
        pass

    @property
    def svg(self):
        return self.svg_strings

