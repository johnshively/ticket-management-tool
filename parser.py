from pathlib import Path
import json
from fetch import fetch_events

def build_ticket_lookup(payload):
    lookup = {}
    for item in payload.get("included", []):
        if item["type"] == "ticket-options":
            lookup[item["id"]] = item["attributes"]
    print(next(iter(lookup.values())))
    return lookup

if __name__ == "__main__":
    fetch = fetch_events()
    print(len(build_ticket_lookup(fetch)))
   
