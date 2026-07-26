import pytest
import json
from app import create_app
from app.models import inventory_db, InventoryItem

@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        inventory_db.clear()
        yield client

def test_get_all_items_empty(client):
    """Test getting all items when database is empty"""
    response = client.get('/api/inventory')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['count'] == 0

def test_create_item(client):
    """Test creating a new item"""
    item_data = {
        'name': 'Test Product',
        'brand': 'Test Brand',
        'price': 19.99,
        'quantity': 10,
        'barcode': '1234567890123'
    }
    response = client.post('/api/inventory', json=item_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['data']['name'] == 'Test Product'

def test_get_single_item(client):
    """Test getting a single item by ID"""
    item = InventoryItem('Test Product', 'Test Brand', 19.99, 10)
    inventory_db.append(item)
    
    response = client.get(f'/api/inventory/{item.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['data']['id'] == item.id

def test_update_item(client):
    """Test updating an existing item"""
    item = InventoryItem('Test Product', 'Test Brand', 19.99, 10)
    inventory_db.append(item)
    
    update_data = {'name': 'Updated Product', 'price': 29.99}
    response = client.patch(f'/api/inventory/{item.id}', json=update_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['name'] == 'Updated Product'

def test_delete_item(client):
    """Test deleting an item"""
    item = InventoryItem('Test Product', 'Test Brand', 19.99, 10)
    inventory_db.append(item)
    
    response = client.delete(f'/api/inventory/{item.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['message'] == 'Item deleted successfully'
    assert len(inventory_db) == 0

def test_search_items(client):
    """Test searching for items"""
    item1 = InventoryItem('Apple iPhone', 'Apple', 999.99, 5)
    item2 = InventoryItem('Samsung Galaxy', 'Samsung', 799.99, 3)
    inventory_db.extend([item1, item2])
    
    response = client.get('/api/inventory/search?q=iphone')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['count'] == 1
    assert data['data'][0]['name'] == 'Apple iPhone'

def test_create_item_duplicate_barcode(client):
    """Test creating an item with a duplicate barcode"""
    item = InventoryItem('Test Product', 'Test Brand', 19.99, 10, barcode='1234567890123')
    inventory_db.append(item)
    
    new_item_data = {
        'name': 'Another Product',
        'brand': 'Another Brand',
        'price': 29.99,
        'quantity': 5,
        'barcode': '1234567890123'
    }
    response = client.post('/api/inventory', json=new_item_data)
    assert response.status_code == 409
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'already exists' in data['message']
