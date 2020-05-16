# todo add chart
# todo give everything x, y, width, height
# todo add columns
# todo paint layout

from attr import attrs, attrib
from shapes import Rectangle
from viewport import ViewPort


@attrs
class Layout:

    parent = ViewPort

    banner_top_height = parent.height * 0.1
    banner_bottom_height = parent.height * 0.1

    scales_top_height = parent.height * 0.2
    _sales_top_y = banner_top_height

    scales_bottom_height = parent.height * 0.2
    _scales_bottom_y = parent.height - (scales_bottom_height + banner_bottom_height)

    _plot_y = banner_top_height + scales_top_height
    _plot_height = _scales_bottom_y - (banner_top_height + scales_top_height)

