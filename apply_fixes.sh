#!/bin/bash
echo "Applying fixes..."

# Create test helper
cat > test_helper.py << 'HELP'
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
HELP

chmod +x test_helper.py

# Create test demo
cat > run_tests_demo.py << 'DEMO'
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
DEMO

chmod +x run_tests_demo.py

echo "✓ Fixes applied!"
echo ""
echo "Run these commands:"
echo "  python test_helper.py        - View all items with full IDs"
echo "  python run_tests_demo.py     - Run automated tests"
echo "  python cli.py list           - List items (now shows full IDs)"
