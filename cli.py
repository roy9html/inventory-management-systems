#!/usr/bin/env python
import click
import requests
import json
from tabulate import tabulate

BASE_URL = "http://localhost:5000/api"

class Colors:
    """ANSI color codes for CLI output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

@click.group()
def cli():
    """Inventory Management System CLI"""
    pass

@cli.command()
def list():
    """List all inventory items"""
    try:
        response = requests.get(f"{BASE_URL}/inventory")
        if response.status_code == 200:
            data = response.json()
            if data['count'] == 0:
                click.echo(f"{Colors.WARNING}No items in inventory{Colors.END}")
                return
            
            items = data['data']
            table_data = []
            for item in items:
                table_data.append([
                    item['id'][:8],
                    item['name'],
                    item.get('brand', 'N/A'),
                    f"${item['price']:.2f}",
                    item['quantity'],
                    item.get('barcode', 'N/A')
                ])
            
            headers = ['ID', 'Name', 'Brand', 'Price', 'Qty', 'Barcode']
            click.echo(f"\n{Colors.BOLD}{Colors.HEADER}Inventory Items{Colors.END}")
            click.echo(tabulate(table_data, headers=headers, tablefmt='grid'))
            click.echo(f"\nTotal items: {data['count']}")
        else:
            click.echo(f"{Colors.FAIL}Error: Failed to fetch items{Colors.END}")
    except requests.exceptions.ConnectionError:
        click.echo(f"{Colors.FAIL}Error: Could not connect to server. Make sure the Flask app is running.{Colors.END}")

@cli.command()
@click.argument('item_id')
def get(item_id):
    """Get details of a single item by ID"""
    try:
        response = requests.get(f"{BASE_URL}/inventory/{item_id}")
        if response.status_code == 200:
            item = response.json()['data']
            click.echo(f"\n{Colors.BOLD}{Colors.HEADER}Item Details{Colors.END}")
            click.echo(f"ID:          {item['id']}")
            click.echo(f"Name:        {item['name']}")
            click.echo(f"Brand:       {item.get('brand', 'N/A')}")
            click.echo(f"Price:       ${item['price']:.2f}")
            click.echo(f"Quantity:    {item['quantity']}")
            click.echo(f"Barcode:     {item.get('barcode', 'N/A')}")
            click.echo(f"Category:    {item.get('category', 'N/A')}")
            click.echo(f"Description: {item.get('description', 'N/A')}")
            click.echo(f"Created:     {item['created_at']}")
            click.echo(f"Updated:     {item['updated_at']}")
        elif response.status_code == 404:
            click.echo(f"{Colors.FAIL}Item not found{Colors.END}")
        else:
            click.echo(f"{Colors.FAIL}Error: Failed to fetch item{Colors.END}")
    except requests.exceptions.ConnectionError:
        click.echo(f"{Colors.FAIL}Error: Could not connect to server.{Colors.END}")

@cli.command()
@click.option('--name', prompt='Product name', help='Name of the product')
@click.option('--brand', help='Brand of the product')
@click.option('--price', type=float, prompt='Price', help='Price of the product')
@click.option('--quantity', type=int, prompt='Quantity', help='Quantity in stock')
@click.option('--barcode', help='Barcode of the product')
@click.option('--category', help='Category of the product')
@click.option('--description', help='Description of the product')
def add(name, brand, price, quantity, barcode, category, description):
    """Add a new item to inventory"""
    data = {
        'name': name,
        'brand': brand,
        'price': price,
        'quantity': quantity,
        'barcode': barcode,
        'category': category,
        'description': description
    }
    data = {k: v for k, v in data.items() if v is not None}
    
    try:
        response = requests.post(f"{BASE_URL}/inventory", json=data)
        if response.status_code == 201:
            item = response.json()['data']
            click.echo(f"{Colors.GREEN}✓ Item added successfully!{Colors.END}")
            click.echo(f"ID: {item['id']}")
        elif response.status_code == 409:
            click.echo(f"{Colors.WARNING}Item with this barcode already exists{Colors.END}")
        else:
            click.echo(f"{Colors.FAIL}Error: {response.json().get('message', 'Failed to add item')}{Colors.END}")
    except requests.exceptions.ConnectionError:
        click.echo(f"{Colors.FAIL}Error: Could not connect to server.{Colors.END}")

@cli.command()
@click.argument('item_id')
@click.option('--name', help='New name')
@click.option('--brand', help='New brand')
@click.option('--price', type=float, help='New price')
@click.option('--quantity', type=int, help='New quantity')
@click.option('--barcode', help='New barcode')
@click.option('--category', help='New category')
@click.option('--description', help='New description')
def update(item_id, name, brand, price, quantity, barcode, category, description):
    """Update an existing item"""
    data = {
        'name': name,
        'brand': brand,
        'price': price,
        'quantity': quantity,
        'barcode': barcode,
        'category': category,
        'description': description
    }
    data = {k: v for k, v in data.items() if v is not None}
    
    if not data:
        click.echo(f"{Colors.WARNING}No fields to update{Colors.END}")
        return
    
    try:
        response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=data)
        if response.status_code == 200:
            click.echo(f"{Colors.GREEN}✓ Item updated successfully!{Colors.END}")
        elif response.status_code == 404:
            click.echo(f"{Colors.FAIL}Item not found{Colors.END}")
        else:
            click.echo(f"{Colors.FAIL}Error: Failed to update item{Colors.END}")
    except requests.exceptions.ConnectionError:
        click.echo(f"{Colors.FAIL}Error: Could not connect to server.{Colors.END}")

@cli.command()
@click.argument('item_id')
def delete(item_id):
    """Delete an item from inventory"""
    if not click.confirm(f"Are you sure you want to delete item {item_id}?"):
        click.echo("Operation cancelled")
        return
    
    try:
        response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
        if response.status_code == 200:
            click.echo(f"{Colors.GREEN}✓ Item deleted successfully!{Colors.END}")
        elif response.status_code == 404:
            click.echo(f"{Colors.FAIL}Item not found{Colors.END}")
        else:
            click.echo(f"{Colors.FAIL}Error: Failed to delete item{Colors.END}")
    except requests.exceptions.ConnectionError:
        click.echo(f"{Colors.FAIL}Error: Could not connect to server.{Colors.END}")

@cli.command()
@click.argument('query')
def search(query):
    """Search inventory by name or barcode"""
    try:
        response = requests.get(f"{BASE_URL}/inventory/search", params={'q': query})
        if response.status_code == 200:
            data = response.json()
            if data['count'] == 0:
                click.echo(f"{Colors.WARNING}No items found matching '{query}'{Colors.END}")
                return
            
            items = data['data']
            click.echo(f"\n{Colors.BOLD}{Colors.HEADER}Search Results ({data['count']} items){Colors.END}")
            for item in items:
                click.echo(f"\n{Colors.BOLD}ID:{Colors.END} {item['id']}")
                click.echo(f"{Colors.BOLD}Name:{Colors.END} {item['name']}")
                if item.get('brand'):
                    click.echo(f"{Colors.BOLD}Brand:{Colors.END} {item['brand']}")
                click.echo(f"{Colors.BOLD}Price:{Colors.END} ${item['price']:.2f}")
                click.echo(f"{Colors.BOLD}Qty:{Colors.END} {item['quantity']}")
                click.echo("-" * 40)
        else:
            click.echo(f"{Colors.FAIL}Error: Failed to search items{Colors.END}")
    except requests.exceptions.ConnectionError:
        click.echo(f"{Colors.FAIL}Error: Could not connect to server.{Colors.END}")

@cli.command()
@click.argument('barcode')
def fetch_external(barcode):
    """Fetch product from OpenFoodFacts API by barcode and add to inventory"""
    try:
        click.echo(f"Fetching product with barcode: {barcode}...")
        response = requests.get(f"{BASE_URL}/external/fetch/{barcode}")
        
        if response.status_code == 201:
            item = response.json()['data']
            click.echo(f"{Colors.GREEN}✓ Product fetched and added to inventory!{Colors.END}")
            click.echo(f"Name: {item['name']}")
            click.echo(f"Brand: {item.get('brand', 'N/A')}")
            click.echo(f"ID: {item['id']}")
        elif response.status_code == 200:
            data = response.json()
            click.echo(f"{Colors.WARNING}Product already exists in inventory{Colors.END}")
            click.echo(f"ID: {data['data']['id']}")
        elif response.status_code == 404:
            click.echo(f"{Colors.FAIL}Product not found in external API{Colors.END}")
        else:
            click.echo(f"{Colors.FAIL}Error: {response.json().get('message', 'Failed to fetch product')}{Colors.END}")
    except requests.exceptions.ConnectionError:
        click.echo(f"{Colors.FAIL}Error: Could not connect to server.{Colors.END}")

@cli.command()
@click.argument('name')
def search_external(name):
    """Search for a product by name in OpenFoodFacts API"""
    try:
        click.echo(f"Searching for: {name}...")
        response = requests.get(f"{BASE_URL}/external/search/{name}")
        
        if response.status_code == 200:
            data = response.json()
            product = data['data']
            
            click.echo(f"\n{Colors.BOLD}{Colors.HEADER}Product Found{Colors.END}")
            click.echo(f"Name:        {product['name']}")
            click.echo(f"Brand:       {product.get('brand', 'N/A')}")
            click.echo(f"Barcode:     {product.get('barcode', 'N/A')}")
            click.echo(f"Category:    {product.get('category', 'N/A')}")
            click.echo(f"Description: {product.get('description', 'N/A')}")
            
            if data.get('in_inventory'):
                click.echo(f"\n{Colors.GREEN}This product is already in your inventory!{Colors.END}")
                click.echo(f"Inventory ID: {data['inventory_item']['id']}")
            else:
                click.echo(f"\n{Colors.WARNING}This product is not in your inventory.{Colors.END}")
                if click.confirm("Would you like to add it?"):
                    add_response = requests.post(f"{BASE_URL}/inventory", json={
                        'name': product['name'],
                        'brand': product.get('brand'),
                        'barcode': product.get('barcode'),
                        'category': product.get('category'),
                        'description': product.get('description'),
                        'price': 0.0,
                        'quantity': 0
                    })
                    if add_response.status_code == 201:
                        click.echo(f"{Colors.GREEN}✓ Product added to inventory!{Colors.END}")
                    else:
                        click.echo(f"{Colors.FAIL}Failed to add product{Colors.END}")
        elif response.status_code == 404:
            click.echo(f"{Colors.FAIL}Product '{name}' not found in external API{Colors.END}")
        else:
            click.echo(f"{Colors.FAIL}Error: Failed to search product{Colors.END}")
    except requests.exceptions.ConnectionError:
        click.echo(f"{Colors.FAIL}Error: Could not connect to server.{Colors.END}")

if __name__ == '__main__':
    cli()
