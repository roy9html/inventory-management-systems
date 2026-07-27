#!/bin/bash
echo "=== Quick Test for Inventory System ==="
echo ""
echo "1. Adding items..."
python cli.py add --name "Milk" --brand "Silk" --price 4.99 --quantity 20
python cli.py add --name "Bread" --brand "Farm" --price 3.49 --quantity 15

echo ""
echo "2. Listing items (shows FULL IDs)..."
python cli.py list

echo ""
echo "3. Run automated tests..."
python run_tests_demo.py

echo ""
echo "✓ All tests complete!"
