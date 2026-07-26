# Testing Instructions

## Quick Start

1. Start the server: `python run.py`
2. In another terminal, test commands:
   - `python cli.py list` - View all items
   - `python cli.py add --name "Milk" --price 4.99 --quantity 20` - Add item
   - `python test_helper.py` - View items with full IDs
   - `python run_tests_demo.py` - Run automated tests

## All CLI Commands
- `python cli.py list` - List all items (shows full IDs)
- `python cli.py get <id>` - Get item by full ID
- `python cli.py add --name "X" --price Y --quantity Z` - Add item
- `python cli.py update <id> --price Y --quantity Z` - Update item
- `python cli.py delete <id>` - Delete item
- `python cli.py search "query"` - Search items
- `python cli.py fetch-external <barcode>` - Fetch from OpenFoodFacts
- `python cli.py search-external "query"` - Search OpenFoodFacts
