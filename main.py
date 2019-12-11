#!/usr/bin/env python3

# ENV02
# pip (default)
# setuptools (default)
# oauth2client
# gspread

import shapes
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
# use creds to create a client to interact with the Google Drive API
# scope = ['https://spreadsheets.google.com/feeds']
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("data").sheet1
print(client.list_spreadsheet_files())
# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
print(list_of_hashes)


diamond = shapes.Diamond()
print(diamond)
