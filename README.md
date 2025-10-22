# Relational-Databases-with-SQLAlchemy

This is a simple Python project demonstrating how to use SQLAlchemy ORM with SQLite to manage users, products, and orders in a database.

It supports many-to-many relationships between orders and products, and includes basic CRUD operations and queries.

Features
- Create and relate Users, Products, and Orders
- Many-to-many relationship between Orders and Products
- Boolean status for tracking shipped/unshipped orders
- Update and delete records
- Print user, product, and order info
- Bonus queries: View unshipped orders and count total orders per user

Setup Instructions
1. Download app.py and this README.md in the same folder.
2. Create a virtual environment (optional but recommended)
python3 -m venv venv
On MAC: source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies
Only SQLAlchemy is needed:
pip install sqlalchemy

How to Run the App
Just run the Python script:
python app.py
This will:
Create the shop.db SQLite database (if it doesn't exist)
Create users, products, and orders
Perform several queries and print results to the terminal

What Happens in app.py
Database and Models Setup
Uses SQLAlchemy ORM with type hinting (Mapped, mapped_column)
Defines User, Product, and Order models
Creates an order_product association table for many-to-many

Data Inserted
2 users: Jack, Mary
3 products: Desktop, Laptop, Printer
4 orders with different users, products, and status (True = shipped)

Queries Performed
- List all users
- List all products
- List all orders showing:
  1) User's name
  2) Product(s) in the order
  3) Quantity
- Delete user with ID 1 (Jack)
- Show all unshipped orders (status = False)
- Count and display total orders per user

Notes
The database is stored in shop.db. Delete it to reset.
If you run the script multiple times, you'll get IntegrityError because of duplicate emails or primary keys.
Uncomment Base.metadata.drop_all(engine) to drop tables before re-creating them if needed.
You must keep the session open while accessing relationships.

