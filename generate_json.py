import json
import ulid


data = {
    "model": "pen.Pen",
    "pk": ulid.new().str,
    "fields": {
            "name": "",
            "description": "",
            "category": 1,
            "price_yen": 1,
            "brand":1,
            "tag": [1],
            "image": "",
            "image_src": "",
            "created_at": "2021-02-20T12:00:00.000Z",
            "updated_at": "2021-02-20T12:00:00.000Z",
            "amazon_link_to_buy": "",
            "rakuten_link_to_buy": ""
        }
}
num = int(input("how many times? "))
for i in range(num):
    output = {
    "model": "pen.Pen",
    "pk": ulid.new().str,
    "fields": {
            "name": "",
            "description": "",
            "category": 1,
            "price_yen": 1,
            "brand":1,
            "tag": [1],
            "image": "",
            "image_src": "",
            "created_at": "2021-02-20T12:00:00.000Z",
            "updated_at": "2021-02-20T12:00:00.000Z",
            "amazon_link_to_buy": "",
            "rakuten_link_to_buy": ""
        }
    }
    