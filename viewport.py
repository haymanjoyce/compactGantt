from attr import attrs, attrib


@attrs
class ViewPort:

    width = 800
    height = 600
    child_elements = attrib(default=list())
    svg_string = attrib(default=str())

    def order_child_elements(self):
        pass

    def render_child_elements(self):
        for child_element in self.child_elements:
            self.svg_string += child_element.svg

    def wrap_svg_string(self):
        return f'<svg width="{self.width}" height="{self.height}" ' \
               f'id="chart" overflow="auto">' \
               f'{self.svg_string}' \
               f'</svg>'

    @property
    def svg(self):
        return self.wrap_svg_string()

