import uuid
from datetime import datetime

# Mock database - stored in memory
inventory_db = []

class InventoryItem:
    """Model for inventory items"""
    
    def __init__(self, name, brand=None, price=0.0, quantity=0, 
                 barcode=None, category=None, description=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.brand = brand
        self.price = price
        self.quantity = quantity
        self.barcode = barcode
        self.category = category
        self.description = description
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self):
        """Convert item to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'price': self.price,
            'quantity': self.quantity,
            'barcode': self.barcode,
            'category': self.category,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def update(self, data):
        """Update item attributes"""
        allowed_fields = ['name', 'brand', 'price', 'quantity', 
                         'barcode', 'category', 'description']
        for field in allowed_fields:
            if field in data and data[field] is not None:
                setattr(self, field, data[field])
        self.updated_at = datetime.now().isoformat()
        return self

def find_item_by_id(item_id):
    """Find an item by ID"""
    for item in inventory_db:
        if item.id == item_id:
            return item
    return None

def find_item_by_barcode(barcode):
    """Find an item by barcode"""
    for item in inventory_db:
        if item.barcode == barcode:
            return item
    return None
