from attr import attrs, attrib
from shapes import Rectangle


@attrs
class ViewPort:

    root_element = Rectangle()
    child_elements = attrib(default=list())
    svg_string = attrib(default=str())

    def __attrs_post_init__(self):
        self.root_element.width = 800
        self.root_element.height = 600
        self.root_element.fill_color = '#fff'
        self.root_element.border_width = 0

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

