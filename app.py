#Part 1: Setup
from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey, Boolean, Select
from sqlalchemy.orm import sessionmaker, relationship, Mapped, mapped_column, declarative_base
from typing import List

# --- Database setup ---
engine = create_engine("sqlite:///shop.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# --- Association table for many-to-many (Order ↔ Product) ---
order_product = Table(
    "order_product",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("product_id", ForeignKey("products.id"), primary_key=True),
)

#Part 2: Define Tables
# --- Models ---
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(100), unique=True)

    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    price: Mapped[int] = mapped_column(Integer)

    orders: Mapped[List["Order"]] = relationship(
        "Order", secondary=order_product, back_populates="products"
    )

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    quantity: Mapped[int] = mapped_column(Integer)

    user: Mapped["User"] = relationship("User", back_populates="orders")
    products: Mapped[List["Product"]] = relationship(
        "Product", secondary=order_product, back_populates="orders"
    )
	#status = True(order shipped), False(order not shipped)
    status: Mapped[bool] = mapped_column(Boolean)

# Part 3: Create tables 
Base.metadata.create_all(engine)
#Base.metadata.drop_all(engine)

#Part 4: Insert Data
# --- Create 2 Users ---
user1 = User(name="Jack", email="jack@gmail.com")
user2 = User(name="Mary", email="mary@gmail.com")
session.add(user1)
session.add(user2)
session.commit()

# --- Create 3 products ---
product1 = Product(name="Desktop", price=899)
product2 = Product(name="Laptop", price=699)
product3 = Product(name="Printer", price=199)
session.add(product1)
session.add(product2)
session.add(product3)
session.commit()

# --- Create 4 orders ---
order1 = Order(user=user1, quantity=1, products=[product1], status=True)          
order2 = Order(user=user1, quantity=2, products=[product2], status=False)          
order3 = Order(user=user2, quantity=1, products=[product1, product2], status=False)  
order4 = Order(user=user2, quantity=3, products=[product2], status=True) 

session.add(order1)
session.add(order2)
session.add(order3)
session.add(order4)
session.commit()

#Part 5: Queries
#Retrieve all users and print their information
print("-----------------------------------------")
users = session.query(User).all()
for user in users:
    print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
	
#Retrieve all users and print their information.
print("-----------------------------------------")
products = session.query(Product).all()
for product in products:
    print(f"Product Name: {product.name}, Price: {product.price}")
	
#Retrieve all orders, showing the user’s name, product name, and quantity.
print("-----------------------------------------")
orders = session.query(Order).all()
for order in orders:
    print(f"User Name: {order.user.name}")
    for order.product in order.products:
        print(f"Product Name: {order.product.name}")
    print(f"Quantity: {order.quantity}")
	
#Update a product's price
product_to_update = session.get(Product, 1)
product_to_update.price = 499
session.commit()

#Delete a user by ID
user_to_delete = session.get(User, 1)
session.delete(user_to_delete)
session.commit()

#Part 6 - Bonus 
#Query all orders that are not shipped.
print("-----------------------------------------")
with session as session:
    stmt = Select(Order).where(Order.status == False)
    results = session.scalars(stmt).all()
	
    for order in results:
        print(f"User Name: {order.user.name}")  
        for product in order.products:
            print(f"Product Name: {product.name}")  
        print(f"Quantity: {order.quantity}")
		
#Count the total number of orders per user
users = session.query(User).all()
for user in users:
    num_order = len(user.orders) 
    print(f"{user.name} has {num_order} orders")
	



