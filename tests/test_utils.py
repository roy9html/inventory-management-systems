import pytest
from unittest.mock import patch, Mock
from app.utils import OpenFoodFactsAPI

def test_get_product_by_barcode_success():
    """Test successful product fetch by barcode"""
    mock_response = Mock()
    mock_response.json.return_value = {
        'status': 1,
        'product': {
            'product_name': 'Test Product',
            'brands': 'Test Brand',
            'code': '1234567890123',
            'categories': 'Test Category',
            'ingredients_text': 'Test ingredients'
        }
    }
    mock_response.raise_for_status = Mock()
    
    with patch('requests.get', return_value=mock_response):
        result = OpenFoodFactsAPI.get_product_by_barcode('1234567890123')
        assert result is not None
        assert result['name'] == 'Test Product'
        assert result['brand'] == 'Test Brand'

def test_get_product_by_barcode_not_found():
    """Test product not found by barcode"""
    mock_response = Mock()
    mock_response.json.return_value = {'status': 0}
    mock_response.raise_for_status = Mock()
    
    with patch('requests.get', return_value=mock_response):
        result = OpenFoodFactsAPI.get_product_by_barcode('1234567890123')
        assert result is None

def test_search_product_by_name_success():
    """Test successful product search by name"""
    mock_response = Mock()
    mock_response.json.return_value = {
        'products': [{
            'product_name': 'Test Product',
            'brands': 'Test Brand',
            'code': '1234567890123'
        }]
    }
    mock_response.raise_for_status = Mock()
    
    with patch('requests.get', return_value=mock_response):
        result = OpenFoodFactsAPI.search_product_by_name('Test')
        assert result is not None
        assert result['name'] == 'Test Product'
        assert result['brand'] == 'Test Brand'
