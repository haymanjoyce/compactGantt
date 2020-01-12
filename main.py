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

# EXTRACT DATA FROM GOOGLE SHEETS
# https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
module_path = str(__file__)  # os.getcwd() was getting to wrong place
cwd = os.path.dirname(module_path)
client_secret = os.path.join(cwd, "client_secret.json")
creds = ServiceAccountCredentials.from_json_keyfile_name(client_secret, scope)
client = gspread.authorize(creds)
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
# sheet = client.open("data").sheet1
# print(client.list_spreadsheet_files())
# Extract and print all of the values
# list_of_hashes = sheet.get_all_records()
# print(list_of_hashes)

# GET ALL TUPLES
unsorted_items = list()
unsorted_items.extend((scales.scale_a(),
                       scales.Scale().make_tuple(),
                       shapes.Box(x=300, y=100, layer=400, height=50, width=200, fill='pink', rounding=0).get_item(),
                       shapes.Line().get_item(),
                       shapes.Circle().get_item(),
                       shapes.Rect(x=100, y=100, layer=299, fill='blue', width=100, height=100).get_item(),
                       shapes.Diamond(fill='green', layer=300, size=100, y=100).get_item(),
                       shapes.Text(x=300, y=100, text='50 by 200 text', layer=410, fill='grey').get_item(),
                       shapes.Text(x=300, y=100, text='50 by 200 text', layer=500, rotate=45).get_item(),
                       ))

pprint.pprint(unsorted_items)

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
svg_string = f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>' \
            f'<svg width="800" height="800" viewBox="0 0 800 800" id="smile" version="1.1">' \
            f'{svg_elements}' \
            f'</svg>'

svg_bytes = QByteArray(bytearray(svg_string, encoding='utf-8'))

app = QApplication(sys.argv)
svgWidget = QSvgWidget()
svgWidget.renderer().load(svg_bytes)
svgWidget.setGeometry(10, 100, 300, 600)
svgWidget.show()
sys.exit(app.exec_())



