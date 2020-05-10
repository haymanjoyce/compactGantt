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
from chart import Chart
import browser
import gui
from shapes import Rectangle

# CHART
today = date.toordinal(date.today()) - 2
duration = 100
end = today + duration

chart_area = Rectangle(x=0, y=0, width=1000, height=500, fill_color='green', border_width=0).svg
rect_a = Rectangle(x=0, y=0, width=1000, height=50, fill_color='orange', border_width=0).svg
rect_b = Rectangle(x=0, y=50, width=1000, height=50, fill_color='blue', border_width=0).svg
scale_a = Scale(window_width=1000, window_height=50, window_start=today, window_finish=end, scale_y=100).get_bar()
rect_c = Rectangle(x=0, y=0, width=50, height=600, fill_color='purple', border_width=0).svg

svg_elements = chart_area, rect_a, rect_b, scale_a, rect_c
svg_elements = "".join(svg_elements)

# IMAGE
chart = Chart(svg_elements=svg_elements, chart_width=1000, chart_height=600)
browser.display_chart(chart.svg)
gui.display_chart(chart.svg)
