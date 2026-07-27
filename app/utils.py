import logging
import requests
from typing import Optional, Dict, Any

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenFoodFactsAPI:
    """Wrapper for OpenFoodFacts API"""
    
    BASE_URL = "https://world.openfoodfacts.org/api/v0/product"
    
    @classmethod
    def get_product_by_barcode(cls, barcode: str) -> Optional[dict[str, Any]]:
        """
        Fetch product details from OpenFoodFacts API by barcode
        
        Args:
            barcode: Product barcode (EAN/UPC)
            
        Returns:
            Product data dict or None if not found
        """
        try:
            url = f"{cls.BASE_URL}/{barcode}.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 1:
                product = data.get('product', {})
                return cls._format_product_data(product)
            else:
                logger.warning(f"No product found for barcode: {barcode}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing API response: {e}")
            return None
    
    @classmethod
    def search_product_by_name(cls, name: str) -> Optional[Dict[str, Any]]:
        """
        Search for product by name using OpenFoodFacts API
        
        Args:
            name: Product name to search
            
        Returns:
            First matching product data or None
        """
        try:
            search_url = "https://world.openfoodfacts.org/cgi/search.pl"
            params = {
                'search_terms': name,
                'search_simple': 1,
                'action': 'process',
                'json': 1,
                'page_size': 1
            }
            response = requests.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            products = data.get('products', [])
            
            if products:
                return cls._format_product_data(products[0])
            else:
                logger.warning(f"No product found for name: {name}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing API response: {e}")
            return None
    
    @staticmethod
    def _format_product_data(product: Dict[str, Any]) -> Dict[str, Any]:
        """Format product data from API"""
        return {
            'name': product.get('product_name', 'Unknown'),
            'brand': product.get('brands', 'Unknown'),
            'barcode': product.get('code', ''),
            'category': product.get('categories', 'Unknown'),
            'description': product.get('ingredients_text', 'No description available'),
            'price': 0.0,
            'quantity': 0
        }
