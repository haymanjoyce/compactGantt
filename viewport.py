# todo improve the way this is written; make it a singleton?

from attr import attrs, attrib
from shapes import Rectangle


@attrs
class ViewPort:

    svg_objects = attrib(default=list())
    svg_elements = attrib(default=str())

    width = 800
    height = 600

    # style options
    fill_color = '#fff'

    def _paint_viewport(self):
        viewport = Rectangle(border_width=0)
        viewport.width = self.width
        viewport.height = self.height
        viewport.fill_color = self.fill_color
        return viewport.svg

    def order_objects(self):
        pass

    def render_objects(self):
        for svg_object in self.svg_objects:
            self.svg_elements += svg_object.svg

    def wrap_string(self):
        return f'<svg width="{self.width}" height="{self.height}" ' \
               f'id="chart" overflow="auto">' \
               f'{self._paint_viewport()}{self.svg_elements}' \
               f'</svg>'

    @property
    def svg(self):
        return self.wrap_string()

