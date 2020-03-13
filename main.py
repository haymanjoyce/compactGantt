#!/usr/bin/env python3

# todo hold data in database not spreadsheets
# todo GUI interface to database

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
from scales import Scale
from shapes import TimeBox
from pprint import pprint
from arrange import Item
import display
from datetime import date, timedelta

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
timebox_a = TimeBox(fill='pink', start=100, finish=400, min=0, max=500, resolution=1, height=50)
timebox_b = TimeBox(fill='green', start=0, finish=300, min=0, max=500, resolution=1, y=50)
scale_a = Scale(intervals='WEEKS', border_width=0.2, y=400, start=737300, finish=737390, ends='pink', height=50, width=800)

# GET ALL TUPLES
unsorted_items = list()

item_a = Item(element=timebox_a.get_box(), layer=200).get_item()
item_b = Item(element=timebox_b.get_box(), layer=300).get_item()
item_c = Item(element=scale_a.get_scale(), layer=300).get_item()

unsorted_items.extend((item_a, item_b, item_c))

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



