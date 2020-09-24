import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://tableau.ons.org.br/vizql/w/COVID-19Deaths/v/Deaths/bootstrapSession/sessions/"

url = "https://tableau.azdhs.gov/views/COVID-19Deaths/Deaths"
r = requests.get(
    url,
    params= {
        ":embed":"y",
        ":showAppBanner":"false",
        ":showShareOptions":"true",
        ":display_count":"no",
        "showVizHome": "no"
    }
)
soup = BeautifulSoup(r.text, "html.parser")

tableauData = json.loads(soup.find("textarea",{"id": "tsConfigContainer"}).text)

print(tableauData["vizql_root"])
print(tableauData["sessionid"])
print(tableauData["sheetId"])

dataUrl = f'https://tableau.azdhs.gov{tableauData["vizql_root"]}/bootstrapSession/sessions/{tableauData["sessionid"]}'
print(dataUrl)
r = requests.post(dataUrl, data= {
    "sheet_id": tableauData["sheetId"],
})
print(r)
dataReg = re.search('\d+;({.*})\d+;({.*})', r.text, re.MULTILINE)
info = json.loads(dataReg.group(1))
data = json.loads(dataReg.group(2))
print(data)
print(data["secondaryInfo"]["presModelMap"]["dataDictionary"]["presModelHolder"]["genDataDictionaryPresModel"]["dataSegments"]["0"]["dataColumns"])

