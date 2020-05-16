# todo develop layout

from attr import attrs, attrib
from shapes import Rectangle


@attrs
class Chart:

    svg_objects = attrib(default=list())
    svg_elements = attrib(default=str())

    # we assume the chart (the root rectangle) and the viewPort (the SVG element) are the same size
    width = 800
    height = 600

    # style options
    fill_color = '#fff'
    border_color = '#000'
    border_width = 0

    def _paint_chart(self):
        chart = Rectangle()
        chart.width = self.width
        chart.height = self.height
        chart.fill_color = self.fill_color
        chart.border_color = self.border_color
        chart.border_width = self.border_width
        return chart.svg

    def order_objects(self):
        pass

    def render_objects(self):
        for svg_object in self.svg_objects:
            self.svg_elements += svg_object.svg

    def wrap_string(self):
        return f'<svg width="{self.width}" height="{self.height}" ' \
               f'id="chart" overflow="auto">' \
               f'{self._paint_chart()}{self.svg_elements}' \
               f'</svg>'

    @property
    def svg(self):
        return self.wrap_string()


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

