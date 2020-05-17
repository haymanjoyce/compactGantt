# todo calculate layout
# todo paint layout
# todo make each layout component a rectangle object

from attr import attrs, attrib
from shapes import Rectangle
from viewport import ViewPort


@attrs
class Layout:

    parent = ViewPort.root_element

    chart = Rectangle()
    header = Rectangle()
    footer = Rectangle()
    columns_left = Rectangle()
    columns_right = Rectangle()
    scales_top = Rectangle()
    scales_bottom = Rectangle()
    labels_top_left = Rectangle()
    labels_top_right = Rectangle()
    labels_bottom_left = Rectangle()
    labels_bottom_right = Rectangle()
    plot_area = Rectangle()

    def configure_elements(self):
        pass

