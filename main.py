#!/usr/bin/env python3

# ENV02
# pip (default)
# setuptools (default)
# oauth2client - access Google Cloud Platform
# gspread - access Google Sheets
# mako - templating engine
# PySide2 - GUI under LGPL license

import shapes
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
import scales
import pprint
import arrange
import display

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

# GET ALL TUPLES
unsorted_items = list()
unsorted_items.extend((
    arrange.Item(element=shapes.Box(x=0, y=0, width=100, height=100, background_color='grey').get_element(), layer=100).get_item(),
    arrange.Item(element=shapes.Box(x=200, width=100, height=100, fill='green', background_color='grey').get_element(), layer=100).get_item(),
    arrange.Item(element=shapes.Box(x=0, y=200, width=100, height=100, fill='blue', background_color='grey').get_element(), layer=100).get_item(),
    arrange.Item(element=shapes.Box(x=200, y=200, width=100, height=100, fill='yellow', background_color='grey').get_element(), layer=100).get_item(),
    arrange.Item(element=shapes.Box(x=0, y=0, width=300, height=300, fill='grey', background_color='grey').get_element(), layer=50).get_item(),
))

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
# todo split image from gui
app = QApplication(sys.argv)


svgWidget = QSvgWidget()

image = display.Image(svg_elements)
image_in_bytes = QByteArray(bytearray(image.get_image(), encoding='utf-8'))
svgWidget.renderer().load(image_in_bytes)

print(svgWidget.screen().availableSize())
ab = display.Window()
print(ab.set_geometry())
svgWidget.setGeometry(*ab.set_geometry())  # the asterisk unpacks the tuple
# svgWidget.setGeometry(image.GUI_x, image.GUI_y, image.GUI_width, image.GUI_height)

svgWidget.show()
sys.exit(app.exec_())



