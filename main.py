#!/usr/bin/env python3

# todo database module
# todo add controls to gui module

# todo banners module
# todo columns module
# todo titles module
# todo plot module

# todo textbox module
# todo image module
# todo table module

# REQUIREMENTS
# PySide2
# attrs

from datetime import date
from scales import Scale
from grid import Grid
from plot import Plot
from viewport import ViewPort
from browser import display_chart
from gui import Application
from layout import Layout

# LAYOUT
layout = Layout()
layout.configure(plot_width=1200)

# TIME WINDOW
today = date.toordinal(date.today())
duration = 21
end = today + duration

# PLOT
plot = Plot()
plot.x = layout.plot.x
plot.y = layout.plot.y
plot.width = layout.plot.width
plot.height = layout.plot.height
plot.start = today
plot.finish = end
plot.clean_dates()
plot.calculate_resolution()

# SCALES
scale = Scale()
scale.x = layout.scales_top.x
scale.y = layout.scales_top.y
scale.width = layout.scales_top.width
scale.height = layout.scales_top.height / 4
scale.start = plot.start
scale.finish = plot.finish
scale.resolution = plot.resolution
scale.interval_type = 'days'
scale.week_start = 0
scale.min_label_width = 20
scale.box_fill = 'pink'
scale.ends = 'yellow'
scale.label_type = 'd'
scale.date_format = 'a w'
scale.separator = '-'
scale.font_size = 10
scale.text_x = 10
scale.text_y = scale.height * 0.65

# GRID
grid = Grid()
grid.interval_type = 'WEEKS'
grid.week_start = 0
grid.x = layout.plot.x
grid.y = layout.plot.y
grid.height = plot.height
grid.start = plot.start
grid.finish = plot.finish
grid.resolution = plot.resolution
grid.line_width = 0.5

# VIEWPORT
viewport = ViewPort()
viewport.width = layout.chart.width
viewport.height = layout.chart.height
viewport.child_elements = [layout, scale, grid]
viewport.order_child_elements()
viewport.render_child_elements()

# GUI
application = Application(viewport.svg)

# BROWSER
display_chart(viewport.svg)
