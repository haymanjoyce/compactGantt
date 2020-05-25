#!/usr/bin/env python3

# todo refactor scales module
# todo banners module
# todo columns module
# todo titles module
# todo plot module
# todo database module
# todo add controls to gui module

# REQUIREMENTS
# PySide2
# attrs

from datetime import date
from scales import Scale
from grid import Grid
from plot import Plot
from viewport import ViewPort
import browser
import gui
from layout import Layout
import intervals

# LAYOUT
layout = Layout()
layout.configure(plot_width=600)

# TIME WINDOW
today = date.toordinal(date.today())
duration = 10
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

# INTERVALS
days = intervals.select_intervals(plot.x, today, end, 'DAYS', resolution=plot.resolution)
weeks = intervals.select_intervals(plot.x, today, end, 'WEEKS', resolution=plot.resolution)

# SCALES

scale = Scale(x=layout.scales_top.x, y=layout.scales_top.y,
              width=layout.scales_top.width, height=layout.scales_top.height,
              start=plot.start, finish=plot.finish, interval_type='days', window_resolution=plot.resolution)

scale.min_interval_width = 20
scale.text_x = 10
scale.box_fill = 'pink'
scale.height = layout.scales_top.height / 4
scale.interval_data = days
scale.label_type = 'date'

# GRIDS

grid = Grid(x=layout.plot.x, y=layout.plot.y,
            width=layout.plot.width, height=layout.plot.height,
            start=today, finish=end, interval_type='days')

# VIEWPORT
viewport = ViewPort()
viewport.width = layout.chart.width
viewport.height = layout.chart.height
viewport.child_elements = [layout, scale, grid]
viewport.order_child_elements()
viewport.render_child_elements()

# DISPLAY
browser.display_chart(viewport.svg)
gui.display(viewport.svg)
