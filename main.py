#!/usr/bin/env python3

# todo refactor scales module
# todo banners module
# todo columns module
# todo labels module
# todo plot module
# todo database module
# todo add controls to gui module

# REQUIREMENTS
# PySide2
# attrs

from datetime import date
from scales import Scale, Grid
from viewport import ViewPort
import browser
import gui
from shapes import Rectangle
from layout import Layout

# LAYOUT
layout = Layout()
layout.configure(plot_width=600)

# FEATURES
today = date.toordinal(date.today())
duration = 100
end = today + duration

chart_area = Rectangle(x=0, y=0, width=1000, height=500, fill_color='green', border_width=0)
rect_a = Rectangle(x=0, y=0, width=1000, height=50, fill_color='orange', border_width=0)
rect_b = Rectangle(x=0, y=50, width=1000, height=50, fill_color='blue', border_width=0)
# scale_a = Scale(window_width=1000, window_height=50, window_start=today, window_finish=end, scale_y=100).get_bar()
rect_c = Rectangle(x=0, y=0, width=50, height=600, fill_color='purple', border_width=0)

features = []

# VIEWPORT
viewport = ViewPort()
viewport.width = layout.chart.width
viewport.height = layout.chart.height
viewport.child_elements = [layout]
viewport.order_child_elements()
viewport.render_child_elements()

# DISPLAY
browser.display_chart(viewport.svg)
gui.display(viewport.svg)
