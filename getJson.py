import requests
import os
import json

URL = "http://qweqwrtqwew.atwebpages.com/load.php"
LOCAL_DIR = "data"
os.makedirs(LOCAL_DIR, exist_ok=True)

response = requests.get(URL)

if response.status_code == 200:
    data_list = response.json()

    for idx, entry in enumerate(data_list, start=1):
        filename = os.path.join(LOCAL_DIR, f"{idx}.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(entry, f, indent=2)
        print(f" {filename} gespeichert.")
else:
    print(f" Fehler beim Abrufen: {response.status_code}")
