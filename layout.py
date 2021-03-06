# todo this module may become redundant if dimensions set at feature level

from attr import attrs, attrib
from shapes import Rectangle


@attrs
class Layout:
    """Objects represent chart layout, which can be rendered as SVG elements"""

    chart = Rectangle(x=0, y=0, width=0, height=0, border_width=0, border_rounding=0, fill_color='#ccc')
    header = Rectangle(x=0, y=0, width=0, height=0, border_width=0, border_rounding=0, fill_color='#ddd')
    footer = Rectangle(x=0, y=0, width=0, height=0, border_width=0, border_rounding=0, fill_color='#ddd')
    columns_left = Rectangle(x=0, y=0, width=0, height=0, border_width=0, border_rounding=0, fill_color='#eee')
    columns_right = Rectangle(x=0, y=0, width=0, height=0, border_width=0, border_rounding=0, fill_color='#eee')
    scales_top = Rectangle(x=0, y=0, width=0, height=0, border_width=0, border_rounding=0, fill_color='#eee')
    scales_bottom = Rectangle(x=0, y=0, width=0, height=0, border_width=0, border_rounding=0, fill_color='#eee')
    titles_top_left = Rectangle(x=0, y=0, width=0, height=0, border_width=0, border_rounding=0, fill_color='#fff')
    titles_top_right = Rectangle(x=0, y=0, width=0, height=0, border_width=0, border_rounding=0, fill_color='#fff')
    titles_bottom_left = Rectangle(x=0, y=0, width=0, height=0, border_width=0, border_rounding=0, fill_color='#fff')
    titles_bottom_right = Rectangle(x=0, y=0, width=0, height=0, border_width=0, border_rounding=0, fill_color='#fff')
    plot = Rectangle(x=0, y=0, width=0, height=0, border_width=0, border_rounding=0, fill_color='#fff')

    svg_string = attrib(default=str())

    def configure(self,
                  header_height=50,
                  scales_top_height=150,
                  plot_height=200,
                  scales_bottom_height=150,
                  footer_height=50,
                  columns_left_width=200,
                  plot_width=400,
                  columns_right_width=200,
                  ):

        self.chart.x = 0
        self.chart.y = 0
        self.chart.width = columns_left_width + plot_width + columns_right_width
        self.chart.height = header_height + scales_top_height + plot_height + scales_bottom_height + footer_height

        self.header.x = 0
        self.header.y = 0
        self.header.width = columns_left_width + plot_width + columns_right_width
        self.header.height = header_height

        self.footer.x = 0
        self.footer.y = header_height + scales_top_height + plot_height + scales_bottom_height
        self.footer.width = columns_left_width + plot_width + columns_right_width
        self.footer.height = footer_height

        self.scales_top.x = columns_left_width
        self.scales_top.y = header_height
        self.scales_top.width = plot_width
        self.scales_top.height = scales_top_height

        self.scales_bottom.x = columns_left_width
        self.scales_bottom.y = header_height + scales_top_height + plot_height
        self.scales_bottom.width = plot_width
        self.scales_bottom.height = scales_bottom_height

        self.columns_left.x = 0
        self.columns_left.y = header_height + scales_top_height
        self.columns_left.width = columns_left_width
        self.columns_left.height = plot_height

        self.columns_right.x = columns_left_width + plot_width
        self.columns_right.y = header_height + scales_top_height
        self.columns_right.width = columns_right_width
        self.columns_right.height = plot_height

        self.plot.x = columns_left_width
        self.plot.y = header_height + scales_top_height
        self.plot.width = plot_width
        self.plot.height = plot_height

        self.titles_top_left.x = 0
        self.titles_top_left.y = header_height
        self.titles_top_left.width = columns_left_width
        self.titles_top_left.height = scales_top_height

        self.titles_top_right.x = columns_left_width + plot_width
        self.titles_top_right.y = header_height
        self.titles_top_right.width = columns_right_width
        self.titles_top_right.height = scales_top_height

        self.titles_bottom_left.x = 0
        self.titles_bottom_left.y = header_height + scales_top_height + plot_height
        self.titles_bottom_left.width = columns_left_width
        self.titles_bottom_left.height = scales_bottom_height

        self.titles_bottom_right.x = columns_left_width + plot_width
        self.titles_bottom_right.y = header_height + scales_top_height + plot_height
        self.titles_bottom_right.width = columns_right_width
        self.titles_bottom_right.height = scales_bottom_height

    @property
    def svg(self):
        self.svg_string += self.chart.svg
        self.svg_string += self.header.svg
        self.svg_string += self.footer.svg
        self.svg_string += self.columns_left.svg
        self.svg_string += self.columns_right.svg
        self.svg_string += self.scales_top.svg
        self.svg_string += self.scales_bottom.svg
        self.svg_string += self.titles_top_left.svg
        self.svg_string += self.titles_top_right.svg
        self.svg_string += self.titles_bottom_left.svg
        self.svg_string += self.titles_bottom_right.svg
        self.svg_string += self.plot.svg
        return self.svg_string

