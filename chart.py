# todo render layout

from attr import attrs, attrib


@attrs
class Chart:

    svg_elements = attrib()
    chart_width = attrib(default=800)
    chart_height = attrib(default=600)
    viewPort_width = attrib()
    viewPort_height = attrib()

    @viewPort_width.default
    def get_height(self):
        return self.chart_width

    @viewPort_height.default
    def get_height(self):
        return self.chart_height

    @property
    def svg(self):
        return f'<svg width="{self.viewPort_width}" height="{self.viewPort_height}" ' \
               f'id="chart" overflow="auto"> ' \
               f'{self.svg_elements}' \
               f'</svg>'

