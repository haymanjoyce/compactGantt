from attr import attrs, attrib


@attrs
class ViewPort:
    """Objects represent the viewport, which is the SVG root element"""

    width = 800
    height = 600
    child_elements = attrib(default=list())
    svg_string = attrib(default=str())

    def order_child_elements(self):
        """Orders objects by their layer property"""
        pass

    def render_child_elements(self):
        """Builds SVG string; assumes all objects have an .svg property"""
        for child_element in self.child_elements:
            self.svg_string += child_element.svg

    def wrap_svg_string(self):
        """Wraps the SVG elements in the root SVG element"""
        return f'<svg width="{self.width}" height="{self.height}" ' \
               f'id="chart" overflow="auto">' \
               f'{self.svg_string}' \
               f'</svg>'

    @property
    def svg(self):
        """Returns SVG image which can be used by browser, GUI, and other clients"""
        return self.wrap_svg_string()

