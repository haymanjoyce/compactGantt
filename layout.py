# todo calculate layout
# todo paint layout
# todo make each layout component a rectangle object
# todo there must be a better way of doing this
# todo make it a singleton where function only allows change to user vars

from attr import attrs, attrib
from shapes import Rectangle
from viewport import ViewPort


@attrs
class Layout:

    parent = ViewPort.root_element

    elements = []

    chart = Rectangle(border_width=0)
    header = Rectangle(border_width=0)
    footer = Rectangle(border_width=0)
    columns_left = Rectangle(border_width=0)
    columns_right = Rectangle(border_width=0)
    scales_top = Rectangle(border_width=0)
    scales_bottom = Rectangle(border_width=0)
    labels_top_left = Rectangle(border_width=0)
    labels_top_right = Rectangle(border_width=0)
    labels_bottom_left = Rectangle(border_width=0)
    labels_bottom_right = Rectangle(border_width=0)
    plot_area = Rectangle(border_width=0)

    svg_string = attrib(default=str())

    def configure_elements(self):

        self.chart.x = self.parent.x
        self.chart.y = self.parent.y
        self.chart.width = self.parent.width
        self.chart.height = self.parent.height
        self.chart.fill_color = '#333'

        self.header.x = self.chart.x
        self.header.y = self.chart.y
        self.header.width = self.chart.width
        self.header.height = self.chart.height * 0.1
        self.header.fill_color = 'violet'

        self.footer.x = self.chart.x
        self.footer.width = self.chart.width
        self.footer.height = self.chart.height * 0.1
        self.footer.y = self.chart.height - self.footer.height
        self.footer.fill_color = 'violet'

        self.columns_left.width = self.chart.width * 0.2
        self.columns_right.width = self.chart.width * 0.2

        self.columns_left.x = self.chart.x
        self.columns_right.x = self.chart.width - self.columns_right.width

        self.scales_top.x = self.columns_left.x + self.columns_left.width
        self.scales_top.y = self.header.y + self.header.height
        self.scales_top.width = self.columns_right.x - self.columns_left.width
        self.scales_top.height = self.chart.height * 0.2
        self.scales_top.fill_color = 'pink'

        self.labels_top_left.x = self.chart.x
        self.labels_top_left.y = self.chart.y + self.header.height
        self.labels_top_left.width = self.columns_left.width
        self.labels_top_left.height = self.scales_top.height
        self.labels_top_left.fill_color = 'blue'

        self.labels_top_right.x = self.columns_right.x
        self.labels_top_right.y = self.labels_top_left.y
        self.labels_top_right.width = self.columns_right.width
        self.labels_top_right.height = self.scales_top.height
        self.labels_top_right.fill_color = 'orange'

        self.scales_bottom.x = self.scales_top.x
        self.scales_bottom.width = self.scales_top.width
        self.scales_bottom.height = self.chart.height * 0.2
        self.scales_bottom.y = self.footer.y - self.scales_bottom.height
        self.scales_bottom.fill_color = 'pink'

        self.labels_bottom_left.x = self.labels_top_left
        self.labels_bottom_left.y = self.scales_bottom.y
        self.labels_bottom_left.width = self.labels_top_left.width
        self.labels_bottom_left.height = self.scales_bottom.height
        self.labels_bottom_left.fill_color = 'yellow'

        self.labels_bottom_right.x = self.labels_top_right.x
        self.labels_bottom_right.y = self.scales_bottom.y
        self.labels_bottom_right.width = self.labels_bottom_left.width
        self.labels_bottom_right.height = self.scales_bottom.height
        self.labels_bottom_right.fill_color = 'purple'

        self.plot_area.x = self.scales_top.x
        self.plot_area.y = self.scales_top.y + self.scales_top.height
        self.plot_area.width = self.scales_top.width
        self.plot_area.height = self.scales_bottom.y - (self.scales_top.y + self.scales_top.height)
        self.plot_area.fill_color = '#eee'

        self.columns_left.y = self.plot_area.y
        self.columns_left.height = self.plot_area.height
        self.columns_left.fill_color = 'indigo'

        self.columns_right.y = self.plot_area.y
        self.columns_right.height = self.plot_area.height
        self.columns_right.fill_color = 'indigo'

    def render_elements(self):
        self.svg_string += self.chart.svg
        self.svg_string += self.header.svg
        self.svg_string += self.footer.svg
        self.svg_string += self.columns_left.svg
        self.svg_string += self.columns_right.svg
        self.svg_string += self.scales_top.svg
        self.svg_string += self.scales_bottom.svg
        self.svg_string += self.labels_top_left.svg
        self.svg_string += self.labels_top_right.svg
        self.svg_string += self.labels_bottom_left.svg
        self.svg_string += self.labels_bottom_right.svg
        self.svg_string += self.plot_area.svg

    @property
    def svg(self):
        return self.svg_string

