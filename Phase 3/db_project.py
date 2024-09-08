import sqlite3
import os
from faker import Faker
import random

conn = sqlite3.connect(os.path.expanduser("~/Desktop/DB/myDB.db"))
cursor = conn.cursor()

fake = Faker()

############################################
# Admin Authentication

def authenticate_manager(username, password):
    query = '''
    SELECT username FROM Manager WHERE username = ? AND password = ?;
    '''
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    return result is not None

def authorize_manager(func):
    def wrapper(username, password, *args, **kwargs):
        if authenticate_manager(username, password):
            return func(*args, **kwargs)
        else:
            raise PermissionError("Unauthorized: Manager access required")
    return wrapper
############################################


#@authorize_manager
def insert_users_and_shopping_carts(n):
    for _ in range(n):
        username = fake.user_name()
        email = fake.email()
        name = fake.name()
        phoneNumber = fake.phone_number()
        password = fake.password()
        cursor.execute("INSERT INTO User (username, email, name, phoneNumber, password) VALUES (?, ?, ?, ?, ?)", 
                       (username, email, name, phoneNumber, password))
        cursor.execute("INSERT INTO ShoppingCart (username) VALUES (?)", (username,))

#authorize_manager
def insert_managers(n):
    for _ in range(n):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        cursor.execute("INSERT INTO Manager (username, email, password) VALUES (?, ?, ?)", 
                       (username, email, password))

#@authorize_manager
def insert_addresses(n):
    cursor.execute("SELECT username FROM User")
    usernames = [row[0] for row in cursor.fetchall()]
    for _ in range(n):
        username = random.choice(usernames)
        state = fake.state()
        city = fake.city()
        street = fake.street_address()
        pin = fake.zipcode()
        cursor.execute("INSERT INTO Address (username, state, city, street, pin) VALUES (?, ?, ?, ?, ?)", 
                       (username, state, city, street, pin))

#@authorize_manager
def insert_brands(n):
    for _ in range(n):
        name = fake.company()
        cursor.execute("INSERT INTO Brand (name) VALUES (?)", (name,))

#@authorize_manager
def insert_categories(n):
    for _ in range(n):
        name = fake.word()
        cursor.execute("INSERT INTO Category (name) VALUES (?)", (name,))

#@authorize_manager
def insert_products(n):
    cursor.execute("SELECT brandID FROM Brand")
    brand_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT categoryID FROM Category")
    category_ids = [row[0] for row in cursor.fetchall()]
    for _ in range(n):
        name = fake.word()
        description = fake.text()
        stockQuantity = random.randint(0, 100)
        price = round(random.uniform(10.0, 100.0), 2)
        brandID = random.choice(brand_ids)
        categoryID = random.choice(category_ids)
        cursor.execute("INSERT INTO Product (name, description, stockQuantity, price, brandID, categoryID) VALUES (?, ?, ?, ?, ?, ?)", 
                       (name, description, stockQuantity, price, brandID, categoryID))

#@authorize_manager
def insert_selected_items(n):
    cursor.execute("SELECT cartID FROM ShoppingCart")
    cart_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT productID FROM Product")
    product_ids = [row[0] for row in cursor.fetchall()]

    # Generate all possible unique pairs (cartID, productID)
    all_pairs = [(cartID, productID) for cartID in cart_ids for productID in product_ids]
    random.shuffle(all_pairs)

    selected_pairs = all_pairs[:n]

    for cartID, productID in selected_pairs:
        quantity = random.randint(1, 5)
        cursor.execute("INSERT INTO SelectedItems (cartID, productID, quantity) VALUES (?, ?, ?)", 
                       (cartID, productID, quantity))

#@authorize_manager
def insert_discounts(n):
    cursor.execute("SELECT productID FROM Product")
    product_ids = [row[0] for row in cursor.fetchall()]
    for _ in range(n):
        productID = random.choice(product_ids)
        percentage = round(random.uniform(5.0, 50.0), 2)
        startDate = fake.date()
        endDate = fake.date()
        cursor.execute("INSERT INTO Discount (pID, percentage, startDate, endDate) VALUES (?, ?, ?, ?)", 
                       (productID, percentage, startDate, endDate))

#@authorize_manager
def insert_reviews(n):
    cursor.execute("SELECT username FROM User")
    usernames = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT productID FROM Product")
    product_ids = [row[0] for row in cursor.fetchall()]
    for _ in range(n):
        username = random.choice(usernames)
        productID = random.choice(product_ids)
        date = fake.date()
        context = fake.text()
        cursor.execute("INSERT INTO Review (username, pID, date, context) VALUES (?, ?, ?, ?)", 
                       (username, productID, date, context))

#@authorize_manager
def insert_orders_and_shipments():
    cursor.execute("""
        SELECT DISTINCT ShoppingCart.username, ShoppingCart.cartID 
        FROM ShoppingCart
        JOIN SelectedItems ON ShoppingCart.cartID = SelectedItems.cartID
    """)
    user_cart_map = cursor.fetchall()

    
    while(len(user_cart_map) > 0):
        
        username, cartID = user_cart_map.pop()
        
        date = fake.date()
        cursor.execute("INSERT INTO Orders (username, date, shoppingcartID) VALUES (?, ?, ?)", 
                       (username, date, cartID))
        orderID = cursor.lastrowid
        trackingNumber = fake.uuid4()
        carrier = fake.company()
        cost = round(random.uniform(5.0, 20.0), 2)
        status = random.choice(['Shipped', 'In Transit', 'Delivered'])
        sentDate = fake.date()
        receivedDate = fake.date()
        cursor.execute("INSERT INTO Shipment (trackingNumber, orderID, carrier, cost, status, sentDate, receivedDate) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                       (trackingNumber, orderID, carrier, cost, status, sentDate, receivedDate))
        cursor.execute("UPDATE Orders SET shipmentID = ? WHERE orderID = ?", (trackingNumber, orderID))


'''
insert_users_and_shopping_carts(5)
insert_addresses(5)
insert_managers(2)
insert_brands(4)
insert_categories(4)
insert_products(10)
insert_reviews(5)
insert_discounts(3)
insert_selected_items(6)
insert_orders_and_shipments()

conn.commit()
cursor.close()
conn.close()
'''
