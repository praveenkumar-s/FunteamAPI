import requests
import threading
import json
from dateutil.parser import *
import dbservice

def get_latest_data(id):
    latestdate=None
    url="https://data.justickets.co/assets/cheers_tagline.svg"
    HISTORY_DATA=requests.get(url="https://staging-admin.justickets.co/v2/history/{0}".format(id))
    data= json.loads(HISTORY_DATA.content)

    for items in data["orders"]:
        if(len(items["greeting"])!=0):
            if(latestdate is None):
                latestdate=parse(items["greeting"][0]["timestamp"])
                url=items["greeting"][0]["preview"]
            else:
                if(parse(items["greeting"][0]["timestamp"]) > latestdate):
                    latestdate=parse(items["greeting"][0]["timestamp"])
                    url=items["greeting"][0]["preview"]
    return url
   







#print get_latest_data('77e4b846-2bc1-479b-89b5-9a8763c2ff7a')