from flask import Blueprint, request, jsonify
from app.models import inventory_db, InventoryItem, find_item_by_id, find_item_by_barcode
import logging

logger = logging.getLogger(__name__)

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/inventory', methods=['GET'])
def get_all_items():
    """Get all inventory items"""
    items = [item.to_dict() for item in inventory_db]
    return jsonify({
        'status': 'success',
        'count': len(items),
        'data': items
    }), 200

@inventory_bp.route('/inventory/<string:item_id>', methods=['GET'])
def get_item(item_id):
    """Get a single inventory item by ID"""
    item = find_item_by_id(item_id)
    if item:
        return jsonify({
            'status': 'success',
            'data': item.to_dict()
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Item not found'
        }), 404

@inventory_bp.route('/inventory', methods=['POST'])
def create_item():
    """Create a new inventory item"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No data provided'
        }), 400
    
    # Validate required fields
    if 'name' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Name is required'
        }), 400
    
    # Check if item with same barcode exists
    if 'barcode' in data and data['barcode']:
        existing = find_item_by_barcode(data['barcode'])
        if existing:
            return jsonify({
                'status': 'error',
                'message': f"Item with barcode {data['barcode']} already exists"
            }), 409
    
    # Create new item
    item = InventoryItem(
        name=data['name'],
        brand=data.get('brand'),
        price=float(data.get('price', 0.0)),
        quantity=int(data.get('quantity', 0)),
        barcode=data.get('barcode'),
        category=data.get('category'),
        description=data.get('description')
    )
    
    inventory_db.append(item)
    
    return jsonify({
        'status': 'success',
        'message': 'Item created successfully',
        'data': item.to_dict()
    }), 201

@inventory_bp.route('/inventory/<string:item_id>', methods=['PATCH'])
def update_item(item_id):
    """Update an existing inventory item"""
    item = find_item_by_id(item_id)
    if not item:
        return jsonify({
            'status': 'error',
            'message': 'Item not found'
        }), 404
    
    data = request.get_json()
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No data provided'
        }), 400
    
    # Update item
    item.update(data)
    
    return jsonify({
        'status': 'success',
        'message': 'Item updated successfully',
        'data': item.to_dict()
    }), 200

@inventory_bp.route('/inventory/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an inventory item"""
    item = find_item_by_id(item_id)
    if not item:
        return jsonify({
            'status': 'error',
            'message': 'Item not found'
        }), 404
    
    inventory_db.remove(item)
    
    return jsonify({
        'status': 'success',
        'message': 'Item deleted successfully'
    }), 200

@inventory_bp.route('/inventory/search', methods=['GET'])
def search_items():
    """Search inventory items by name or barcode"""
    query = request.args.get('q')
    if not query:
        return jsonify({
            'status': 'error',
            'message': 'Search query is required'
        }), 400
    
    results = []
    for item in inventory_db:
        if query.lower() in item.name.lower() or \
           (item.barcode and query in item.barcode) or \
           (item.brand and query.lower() in item.brand.lower()):
            results.append(item.to_dict())
    
    return jsonify({
        'status': 'success',
        'count': len(results),
        'data': results
    }), 200
