#!/usr/bin/env python3

# todo hold data in database not spreadsheets
# todo GUI interface to database

# option to show overlay which shows all key measurements of layout; used for positioning text boxes
# paper size overlay showing how will fit on paper or slide

# REQUIREMENTS
# oauth2client - access Google Cloud Platform
# gspread - access Google Sheets
# Mako - templating engine
# PySide2 - GUI under LGPL license
# attrs

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from mako.template import Template
from operator import itemgetter
import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtSvg import QSvgWidget
from PySide2.QtSvg import QSvgRenderer
from PySide2.QtCore import QByteArray
from pprint import pprint
import display
from datetime import date, timedelta, datetime
from scales import Scale, Grid
from mixins import *
from shapes import Diamond, Text


# TEMP
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
grid_a = Grid(interval_type='HALVES', window_start=today, window_finish=end, window_width=1000, scale_x=100, scale_y=350, window_height=200, week_start_text='0', line_dashing='6 2').get_grid_lines()

svg_elements = scale_a, scale_b, scale_c, scale_d, scale_e, scale_f, scale_g, grid_a
svg_elements = "".join(svg_elements)

# PAGE.HTML
module_path = str(__file__)  # os.getcwd() was getting to wrong place
cwd = os.path.dirname(module_path)
template_file = os.path.join(cwd, "template.html")
template_handler = Template(filename=template_file)
template_output = template_handler.render(myvar=svg_elements)
image_file = os.path.join(cwd, "page.html")
image_write = open(image_file, "w")
image_write.write(template_output)
image_write.close()

# GUI
app = QApplication(sys.argv)
svgWidget = QSvgWidget()
image = display.Image(svg_elements)
image_in_bytes = QByteArray(bytearray(image.get_image(), encoding='utf-8'))
svgWidget.renderer().load(image_in_bytes)
display_size = svgWidget.screen().availableSize()
window_geometry = display.Window(display_width=display_size.width(), display_height=display_size.height()).get_geometry()
svgWidget.setGeometry(*window_geometry)  # the asterisk unpacks the tuple
svgWidget.show()
sys.exit(app.exec_())

