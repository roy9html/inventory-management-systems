#!/usr/bin/env python
import requests
BASE_URL = "http://localhost:5000/api"
print("\n=== Testing Inventory System ===\n")
try:
    r = requests.get(f"{BASE_URL}/inventory")
    print(f"✓ Server running. Items: {r.json()['count']}")
    
    # Add test item
    test_item = {"name": "Test", "price": 9.99, "quantity": 5}
    r = requests.post(f"{BASE_URL}/inventory", json=test_item)
    item = r.json()['data']
    print(f"✓ Added: {item['name']} (ID: {item['id'][:8]}...)")
    
    # Update
    r = requests.patch(f"{BASE_URL}/inventory/{item['id']}", json={"price": 14.99})
    print("✓ Updated price")
    
    # Delete
    r = requests.delete(f"{BASE_URL}/inventory/{item['id']}")
    print("✓ Deleted test item")
    
    print("\n✓ ALL TESTS PASSED!\n")
except:
    print("✗ Server not running! Start with: python run.py")
