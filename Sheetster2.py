import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import copy
from pprint import pprint

global er
er = 0
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
# aditij@able-device-139019.iam.gserviceaccount.com
# adi-97@bubbly-repeater-345015.iam.gserviceaccount.com
creds = ServiceAccountCredentials.from_json_keyfile_name("bubbly-repeater-345015-5576db1c9381.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Cricket").sheet1
data = sheet.get_all_records()
print(data)
sheet.del_worksheet()
