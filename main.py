#!/usr/bin/env python3

# ENV02
# pip (default)
# setuptools (default)
# oauth2client
# gspread
# mako
# selenium

import shapes
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from mako.template import Template
from selenium import webdriver


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

# SHAPE OBJECTS
box_a = shapes.Box(x=100, y=100, height=200, width=200)
diamond_a = shapes.Diamond(x=150, y=300, size=100)
circle_a = shapes.Circle(x=150, y=150, size=100)
box_b = shapes.Box(x=400, y=100, height=10, width=200, border_width=3, padding_width=0, border_color='rgba(0,0,0)', padding_color='blue', inner_box_color='green')

# CONVERT SHAPE OBJECTS TO SINGLE SVG STRING
shape_objects = [box_a]
full_string = ''
for string in shape_objects:
    full_string += (str(string))

# BUILD IMAGE FILE CONTENT AND WRITE TO IMAGE FILE
template_file = os.path.join(cwd, "template.html")
template_handler = Template(filename=template_file)
template_output = template_handler.render(myvar=full_string)
image_file = os.path.join(cwd, "image.html")
image_write = open(image_file, "w")
image_write.write(template_output)
image_write.close()

# REFRESH THE WEB PAGE
# use LivePage extension for Chrome

