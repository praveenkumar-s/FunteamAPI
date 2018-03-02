import requests
import threading
import json
from dateutil.parser import *


def get_latest_data(id):
    latestdate=None
    url=None
    HISTORY_DATA=requests.get(url="https://staging-admin.justickets.co/v2/history/{0}".format(id))
    data= json.loads(HISTORY_DATA.content)

    for items in data["orders"]:
        if(items["greeting"] is not None):
            if(latestdate is None):
                latestdate=parse(items["greeting"][0]["timestamp"])
            else:
                if(parse(items["greeting"][0]["timestamp"]) > latestdate):
                    latestdate=parse(items["greeting"][0]["timestamp"])
                    url=items["greeting"][0]["preview"]
    return url
   



