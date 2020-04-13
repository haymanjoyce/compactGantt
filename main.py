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
from assembly import Item
import display
from datetime import date, timedelta, datetime
from scales import Scale, Grid
from features import Circle, Row
from shapes import Diamond, Text

# EXTRACT DATA FROM GOOGLE SHEETS
# https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
module_path = str(__file__)  # os.getcwd() was getting to wrong place
cwd = os.path.dirname(module_path)
client_secret = os.path.join(cwd, "client_secret.json")
creds = ServiceAccountCredentials.from_json_keyfile_name(client_secret, scope)
# client = gspread.authorize(creds)
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
# sheet = client.open("data").sheet1
# print(client.list_spreadsheet_files())
# Extract and print all of the values
# list_of_hashes = sheet.get_all_records()
# print(list_of_hashes)

# TEMP
today = date.toordinal(date.today()) - 2
duration = 50
end = today + duration

shape_a = Circle()
shape_b = Diamond(rectangle_fill_color='green')
shape_c = Text(text='Text', x=50, y=50, text_rotate=90)

scale_a = Scale(interval_type='DAYS', window_start=today, window_finish=end, window_width=1000, scale_ends='pink', scale_x=100, scale_y=0, window_height=50, label_type='dates', date_format='a', font_size='15', min_interval_width=30)
scale_b = Scale(interval_type='WEEKS', window_start=today, window_finish=end, window_width=1000, scale_ends='pink', scale_x=100, scale_y=50, window_height=50, week_start_text='0')
scale_c = Scale(interval_type='WEEKS', window_start=today, window_finish=end, window_width=1000, scale_ends='pink', scale_x=100, scale_y=100, window_height=50, week_start_text='6')
scale_d = Scale(interval_type='MONTHS', window_start=today, window_finish=end, window_width=1000, scale_ends='pink', scale_x=100, scale_y=150, window_height=50, label_type='dates', date_format='mm', min_interval_width=40, text_x=10)
scale_e = Scale(interval_type='QUARTERS', window_start=today, window_finish=end, window_width=1000, scale_ends='pink', scale_x=100, scale_y=200, window_height=50, label_type='dates', date_format='Q', separator="/")
scale_f = Scale(interval_type='HALVES', window_start=today, window_finish=end, window_width=1000, scale_ends='pink', scale_x=100, scale_y=250, window_height=50, label_type='dates', date_format='H', separator="/")
scale_g = Scale(interval_type='YEARS', window_start=today, window_finish=end, window_width=1000, scale_ends='pink', scale_x=100, scale_y=300, window_height=50, label_type='dates', date_format='Y', separator="/")
grid_a = Grid(interval_type='HALVES', window_start=today, window_finish=end, window_width=1000, scale_x=100, scale_y=350, window_height=200, week_start_text='0', line_dashing='6 2')

row_a = Row(x=100, y=350, rectangle_height=100, rectangle_width=1000, rectangle_border_rounding=0, rectangle_fill_color='light blue', rectangle_border_width=0.2)
row_b = Row(x=100, y=350, rectangle_height=100, rectangle_width=1000, rectangle_border_rounding=0, rectangle_fill_color='blue', rectangle_border_width=0)

# GET ALL TUPLES
unsorted_items = list()

shape_a = Item(element=shape_a.get_circle(), layer=400).get_item()
shape_b = Item(element=shape_b.get_diamond(), layer=400).get_item()
shape_c = Item(element=shape_c.get_text(), layer=400).get_item()
item_a = Item(element=scale_a.get_bar(), layer=300).get_item()
item_b = Item(element=scale_b.get_bar(), layer=300).get_item()
item_c = Item(element=scale_c.get_bar(), layer=300).get_item()
item_d = Item(element=scale_d.get_bar(), layer=300).get_item()
item_e = Item(element=scale_e.get_bar(), layer=300).get_item()
item_f = Item(element=scale_f.get_bar(), layer=300).get_item()
item_g = Item(element=scale_g.get_bar(), layer=300).get_item()
item_h = Item(element=grid_a.get_grid_lines(), layer=300).get_item()
item_i = Item(element=row_a.get_rect(), layer=200).get_item()
item_j = Item(element=row_b.get_rect(), layer=201).get_item()

unsorted_items.extend((shape_a, shape_b, shape_c))
unsorted_items.extend((item_a, item_b, item_c, item_d, item_e, item_f, item_g, item_h, item_i, item_j))

# SORT TUPLES BY POSITION
sorted_items = sorted(unsorted_items, key=itemgetter(0))

# BUILD SINGLE SVG STRING OF ELEMENTS
svg_elements = ''
for item in sorted_items:
    svg_elements += item[1]

# BUILD IMAGE FILE CONTENT AND WRITE TO IMAGE FILE
template_file = os.path.join(cwd, "template.html")
template_handler = Template(filename=template_file)
template_output = template_handler.render(myvar=svg_elements)
image_file = os.path.join(cwd, "image.html")
image_write = open(image_file, "w")
image_write.write(template_output)
image_write.close()

# REFRESH THE WEB PAGE
# use LivePage extension for Chrome

# RENDER TO GUI DISPLAY
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

