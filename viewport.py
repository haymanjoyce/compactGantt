from attr import attrs, attrib
from shapes import Rectangle


@attrs
class ViewPort:

    root_element = Rectangle(x=0, y=0, width=800, height=600, fill_color='#fff', border_width=0)
    child_elements = attrib(default=list())
    svg_string = attrib(default=str())

    def order_child_elements(self):
        pass

    def render_child_elements(self):
        for child_element in self.child_elements:
            self.svg_string += child_element.svg

    def wrap_svg_string(self):
        return f'<svg width="{self.root_element.width}" height="{self.root_element.height}" ' \
               f'id="chart" overflow="auto">' \
               f'{self.root_element.svg}{self.svg_string}' \
               f'</svg>'

    @property
    def svg(self):
        return self.wrap_svg_string()

