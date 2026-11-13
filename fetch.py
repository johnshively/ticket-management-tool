import requests
import json
from datetime import datetime, timezone
from pathlib import Path 

def fetch_events():
    URL = "https://api.fatsoma.com/v1/events"
    params = {
        "filter[status]": "active",
        "filter[page.id]": "cf1c5642-94c6-4078-a72a-125d49a7b90d",
        "filter[ends-at][gte]": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "include": "location,ticket-options",
        "page[number]": 1,
        "page[size]": 12,
        "sort": "starts-at-day,relevance",
        "with-co-promoted": "true",

        }
    r = requests.get(URL, params=params, timeout=10)
    
    r.raise_for_status()

    return r.json()


if __name__ == "__main__":
    result = fetch_events()
    
