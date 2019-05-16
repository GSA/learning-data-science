from datetime import datetime

import requests

def get_resource(uri):
    r = requests.get(uri)
    response_text = r.text

    return response_text

def get_now():
    now = datetime.now().strftime("%Y-%d-%m")
    return now

def get_resource_by_date(uri, date = None):
    if not date:
        date = get_now()
    uri += f"?date={date}"
    r = requests.get(uri)
    response_text = r.text

    return response_text