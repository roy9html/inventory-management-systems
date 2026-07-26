#!/usr/bin/env python
import requests
BASE_URL = "http://localhost:5000/api"
try:
    r = requests.get(f"{BASE_URL}/inventory")
    data = r.json()
    print(f"\nTotal items: {data['count']}")
    for item in data['data']:
        print(f"\nID: {item['id']}")
        print(f"Name: {item['name']}")
        print(f"Brand: {item.get('brand', 'N/A')}")
        print(f"Price: ${item['price']:.2f}")
        print(f"Qty: {item['quantity']}")
        print("-"*40)
except:
    print("Server not running! Start with: python run.py")
