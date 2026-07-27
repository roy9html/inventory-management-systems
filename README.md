# Inventory Management System

A Flask-based REST API for managing inventory with OpenFoodFacts API integration. The application allows users to create, view, update, delete, and search inventory items while also retrieving product information from the OpenFoodFacts API.


# Table of Contents

* Features
* Technology Stack
* Installation
* API Endpoints
* CLI Commands
* Testing
* Project Structure
* Git Workflow
* Quick Start
* License



# Features

## Core Features

* Create, read, update, and delete inventory items
* Search inventory by product name, brand, or barcode
* Fetch product information from the OpenFoodFacts API
* Command-line interface for interacting with the application
* Unit tests covering application functionality
* Error handling for invalid requests and API failures



# Technology Stack

| Technology | Version  | Purpose                       |
| ---------- | -------- | ----------------------------- |
| Python     | 3.14.5   | Programming Language          |
| Flask      | 2.3.3    | Web Framework                 |
| Flask-CORS | 4.0.0    | Cross-Origin Resource Sharing |
| Requests   | 2.31.0   | HTTP Client                   |
| Click      | 8.1.7    | Command-Line Interface        |
| Tabulate   | 0.9.0    | Table Formatting              |
| Pytest     | 7.4.0    | Testing Framework             |
| Pipenv     | 2026.6.2 | Dependency Management         |


# Installation

# Prerequisites

* Python 3.14.5 or later
* Pipenv
* Git

# Clone the Repository

bash
git clone https://github.com/roy9html/inventory-management-systems.git
cd inventory-management-systems


## Set Up the Environment

bash
pyenv local 3.14.5

pipenv install

pipenv shell


## Install Dependencies

bash
pipenv install flask flask-cors requests tabulate click python-dotenv

pipenv install --dev pytest pytest-cov pytest-flask

## Run the Application

bash
python run.py


The application runs locally at:


http://127.0.0.1:5000


# API Endpoints

Base URL


http://localhost:5000/api


# Inventory

| Method | Endpoint                      | Description                      |
| ------ | ----------------------------- | -------------------------------- |
| GET    | `/inventory`                  | Retrieve all inventory items     |
| GET    | `/inventory/<id>`             | Retrieve a single inventory item |
| POST   | `/inventory`                  | Create a new inventory item      |
| PATCH  | `/inventory/<id>`             | Update an inventory item         |
| DELETE | `/inventory/<id>`             | Delete an inventory item         |
| GET    | `/inventory/search?q=<query>` | Search inventory                 |

# External API

| Method | Endpoint                    | Description                           |
| ------ | --------------------------- | ------------------------------------- |
| GET    | `/external/fetch/<barcode>` | Retrieve a product from OpenFoodFacts |
| GET    | `/external/search/<name>`   | Search OpenFoodFacts                  |



# Example API Requests

# Get All Items

bash
curl http://localhost:5000/api/inventory


# Create an Item

bash
curl -X POST http://localhost:5000/api/inventory \
  -H "Content-Type: application/json" \
  -d '{"name":"Organic Milk","brand":"Silk","price":4.99,"quantity":20}'


# Update an Item

bash
curl -X PATCH http://localhost:5000/api/inventory/<item_id> \
  -H "Content-Type: application/json" \
  -d '{"price":5.99,"quantity":25}'


## Delete an Item

bash
curl -X DELETE http://localhost:5000/api/inventory/<item_id>


# Search Inventory

bash
curl "http://localhost:5000/api/inventory/search?q=Milk"


# Fetch a Product

bash
curl http://localhost:5000/api/external/fetch/<barcode>

# CLI Commands

| Command                                  | Description                        
| `python cli.py list`                     | List all inventory items           |
| `python cli.py get <item_id>`            | View a single inventory item       |
| `python cli.py add`                      | Add a new inventory item           |
| `python cli.py update <item_id>`         | Update an inventory item           |
| `python cli.py delete <item_id>`         | Delete an inventory item           |
| `python cli.py search "query"`           | Search inventory                   |
| `python cli.py fetch-external <barcode>` | Fetch a product from OpenFoodFacts |
| `python cli.py search-external "name"`   | Search OpenFoodFacts               |

### Example

bash

python cli.py add --name "Organic Milk" --brand "Silk" --price 4.99 --quantity 20

python cli.py list

python cli.py search "Milk"

python cli.py update <item_id> --price 5.99 --quantity 25

python cli.py delete <item_id>

# Testing

Run all tests

bash
PYTHONPATH=. pytest tests/ -v
Run route tests

bash
PYTHONPATH=. pytest tests/test_routes.py -v

Run utility tests

bash
PYTHONPATH=. pytest tests/test_utils.py -v

Generate a coverage report

bash
PYTHONPATH=. pytest tests/ --cov=app --cov-report=term

# Project Structure

text
inventory-management-system/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_routes.py
│   └── test_utils.py
├── cli.py
├── run.py
├── requirements.txt
├── Pipfile
├── Pipfile.lock
├── pytest.ini
├── test_helper.py
├── run_tests_demo.py
├── README.md
└── .gitignore


# Git Workflow

Feature branches used during development

* feature/basic-api
* feature/external-api
* feature/cli
* feature/tests

All feature branches were merged into the `main` branch before deployment.



# Quick Start

bash
git clone https://github.com/roy9html/inventory-management-systems.git

cd inventory-management-systems

pipenv install
pipenv shell
python run.py
Open another terminal
bash
python cli.py add --name "Milk" --price 4.99 --quantity 20
python cli.py list
python cli.py search "Milk"
Run the test suite
bash
PYTHONPATH=. pytest tests/ -v
# Project Summary
This project demonstrates the development of a Flask REST API integrated with the OpenFoodFacts API. It includes CRUD functionality, a command-line interface, automated testing, and version control using Git feature branches.
# License
This project is licensed under the MIT License.
# Author
Roy
GitHub: https://github.com/roy9html

# Acknowledgements

* Flask
* OpenFoodFacts
* Click
* Pytest
* Tabulate
