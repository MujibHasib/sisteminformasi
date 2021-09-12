import requests
from requests.structures import CaseInsensitiveDict

api = "69eaa41b2ae7bcb3b3a9eebb30009849e3df97b1"
url = "https://starsender.online/api/sendFile"

data = {
    "tujuan": "085215230460",
    "message": "What the Hell Man"
    "file": "https://cdn0-production-images-kly.akamaized.net/tAr72vTJCpF4IF9O5L493CD79kE=/640x360/smart/filters:quality(75):strip_icc():format(jpeg)/kly-media-production/medias/2754932/original/005940800_1552970791-fotoHL_kucing.jpg"
    }

headers = CaseInsensitiveDict()
headers["apikey"] = api

res = requests.post(url, json=data, headers=headers)
print(res.text)