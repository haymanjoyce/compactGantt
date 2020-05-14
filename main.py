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
from chart import Chart, Layout
import browser
import gui
from shapes import Rectangle

# CREATE CHART LAYOUT
# layout = Layout()

# CREATE CHART FEATURES
today = date.toordinal(date.today())
duration = 100
end = today + duration

chart_area = Rectangle(x=0, y=0, width=1000, height=500, fill_color='green', border_width=0)
rect_a = Rectangle(x=0, y=0, width=1000, height=50, fill_color='orange', border_width=0)
rect_b = Rectangle(x=0, y=50, width=1000, height=50, fill_color='blue', border_width=0)
# scale_a = Scale(window_width=1000, window_height=50, window_start=today, window_finish=end, scale_y=100).get_bar()
rect_c = Rectangle(x=0, y=0, width=50, height=600, fill_color='purple', border_width=0)

chart_objects = [chart_area, rect_a, rect_b, rect_c]

# BUILD CHART
chart = Chart()
chart.viewPort_width = 1000  # will come from layout
chart.viewPort_height = 600  # will come from layout
chart.chart_objects = chart_objects
chart.render_objects()
chart.wrap_string()

# DISPLAY
browser.display_chart(chart.svg_string)
gui.display_chart(chart.svg_string)
