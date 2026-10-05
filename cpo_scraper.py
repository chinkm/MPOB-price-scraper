import pywhatkit as pwk
import keyboard
from datetime import datetime, timedelta, date
import datetime
import requests
import os
import sys
from bs4 import BeautifulSoup as bs

# Safely manage authorization or group identifiers via Environment variables
WHATSAPP_GROUP_ID = os.environ.get("WHATSAPP_GROUP_ID")

datetime_object = str(date.today()).split("-")
convertedDate = f"{datetime_object[-1]}/{datetime_object[-2]}/{datetime_object[-3]}"

URL = f"https://mpob.gov.my{convertedDate}"        # FFB Price
URL2 = f"https://mpob.gov.my{convertedDate}"   # CPO Price

varCPOPrice = requests.get(URL2)
soup = bs(varCPOPrice.content, "html.parser")
result = soup.find_all("td", {"class": "text-center"})

tagString = []
resultSet = []
for tag in result:
    tagString.append(tag.text.strip())

try:
    target_idx = tagString.index(str(int(datetime_object[-1]) - 1)) + 1
    for i in range(target_idx, target_idx + 12):
        resultSet.append(tagString[i])
        
    popResult = resultSet.pop(int(datetime_object[-2]) - 1)
    resultDate1 = datetime.datetime.now() - timedelta(days=1)

    # Dispatches messaging utilizing target variable channel
    pwk.sendwhatmsg_to_group(WHATSAPP_GROUP_ID, f"CPO Price for {str(resultDate1)[:11]} RM{popResult.strip('*')}", 13, 57, 30)
    keyboard.press_and_release('enter')
except ValueError:
    print("Error parsing target date metrics from price feed.")
except Exception as e:
    print(f"Error in execution framework: {e}")
