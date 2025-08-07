import gspread
from oauth2client.service_account import ServiceAccountCredentials
from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime

# авторизация
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)

# читаем таблицу
sheet = client.open("Magnets").sheet1
data = sheet.get_all_records()

# генерируем RSS
rss = Element("rss", version="2.0")
channel = SubElement(rss, "channel")
SubElement(channel, "title").text = "My Torrent Feed"
SubElement(channel, "link").text = "https://example.com"
SubElement(channel, "description").text = "Generated from Google Sheets"

for row in data:
    item = SubElement(channel, "item")
    SubElement(item, "title").text = "SOME"
    SubElement(item, "link").text = row['link']
    SubElement(item, "guid", isPermaLink="true").text = row['A']
    SubElement(item, "pubDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")

with open("feed.xml", "wb") as f:
    f.write(tostring(rss))
