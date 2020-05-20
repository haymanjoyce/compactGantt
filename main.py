#!/usr/bin/env python3

# todo hold data in database
# todo GUI interface to database
# todo page module
# todo chart module
# todo redo scales module
# todo drop mixins
# todo try gui using another framework

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

# CREATE VIEWPORT
viewport = ViewPort()
viewport.root_element.width = 1000
viewport.root_element.height = 600
viewport.root_element.fill_color = '#ddd'

# CREATE LAYOUT
layout = Layout()
layout.parent = viewport.root_element
layout.chart.width = 1000
layout.update_elements()
layout.render_elements()

# CREATE CHART FEATURES
today = date.toordinal(date.today())
duration = 100
end = today + duration

chart_area = Rectangle(x=0, y=0, width=1000, height=500, fill_color='green', border_width=0)
rect_a = Rectangle(x=0, y=0, width=1000, height=50, fill_color='orange', border_width=0)
rect_b = Rectangle(x=0, y=50, width=1000, height=50, fill_color='blue', border_width=0)
# scale_a = Scale(window_width=1000, window_height=50, window_start=today, window_finish=end, scale_y=100).get_bar()
rect_c = Rectangle(x=0, y=0, width=50, height=600, fill_color='purple', border_width=0)

elements = [layout]

# POPULATE SVG ELEMENT
viewport.child_elements = elements
viewport.order_child_elements()
viewport.render_child_elements()

# DISPLAY CHART
browser.display_chart(viewport.svg)
gui.display_chart(viewport.svg)
