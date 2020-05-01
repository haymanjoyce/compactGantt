#!/usr/bin/env python3

# todo hold data in database
# todo GUI interface to database
# todo page module
# todo chart module
# todo redo scales module

# REQUIREMENTS
# PySide2 - GUI under LGPL license
# attrs

import sys
from PySide2.QtWidgets import QApplication
from datetime import date
from scales import Scale, Grid
from gui import Display, ByteArray, Screen
from chart import Chart
from browser import update_web_page

# CHART
today = date.toordinal(date.today()) - 2
duration = 50
end = today + duration
scale_a = Scale(interval_type='DAYS', window_start=today, window_finish=end, window_width=1000, scale_ends='pink', scale_x=100, scale_y=0, window_height=50, label_type='dates', date_format='a', font_size='15', min_interval_width=30).get_bar()
scale_b = Scale(interval_type='WEEKS', window_start=today, window_finish=end, window_width=1000, scale_ends='pink', scale_x=100, scale_y=50, window_height=50, week_start_text='0').get_bar()
scale_c = Scale(interval_type='WEEKS', window_start=today, window_finish=end, window_width=1000, scale_ends='pink', scale_x=100, scale_y=100, window_height=50, week_start_text='6').get_bar()
scale_d = Scale(interval_type='MONTHS', window_start=today, window_finish=end, window_width=1000, scale_ends='pink', scale_x=100, scale_y=150, window_height=50, label_type='dates', date_format='mm', min_interval_width=40, text_x=10).get_bar()
scale_e = Scale(interval_type='QUARTERS', window_start=today, window_finish=end, window_width=1000, scale_ends='pink', scale_x=100, scale_y=200, window_height=50, label_type='dates', date_format='Q', separator="/").get_bar()
scale_f = Scale(interval_type='HALVES', window_start=today, window_finish=end, window_width=1000, scale_ends='pink', scale_x=100, scale_y=250, window_height=50, label_type='dates', date_format='H', separator="/").get_bar()
scale_g = Scale(interval_type='YEARS', window_start=today, window_finish=end, window_width=1000, scale_ends='pink', scale_x=100, scale_y=300, window_height=50, label_type='dates', date_format='Y', separator="/").get_bar()
grid_a = Grid(interval_type='WEEKS', window_start=today, window_finish=end, window_width=1000, scale_x=100, scale_y=350, window_height=200, week_start_text='0', line_dashing='6 2').get_grid_lines()
svg_elements = scale_a, scale_b, scale_c, scale_d, scale_e, scale_f, scale_g, grid_a
svg_elements = "".join(svg_elements)

# IMAGE
image = Chart(svg_elements)

# GUI
gui = QApplication(sys.argv)
display = Display()
display.load_renderer(ByteArray.get_byte_array(image.get_svg()))
display.set_screen_size(Screen.get_screen_size(display))
display.set_geometry()
display.show()
sys.exit(gui.exec_())

