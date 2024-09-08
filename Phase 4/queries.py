import sqlite3
import os
# from db_project import authorize_manager

# Connect to the database 
conn = sqlite3.connect(os.path.expanduser("~/Desktop/DB/myDB.db"))
cursor = conn.cursor()


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


# Show users who have added products to their shopping carts.
@authorize_manager
def get_users_with_products_in_cart():
    query = '''
    SELECT DISTINCT User.username, User.email, User.name, User.phoneNumber
    FROM User
    JOIN ShoppingCart ON User.username = ShoppingCart.username
    JOIN SelectedItems ON ShoppingCart.cartID = SelectedItems.cartID
    JOIN Product ON SelectedItems.productID = Product.productID;
    '''
    cursor.execute(query)
    return cursor.fetchall()

# Show users who have more than one address.
#@authorize_manager
def get_users_with_multiple_addresses():
    query = '''
    SELECT User.username, User.email, User.name, User.phoneNumber, COUNT(Address.addressID) as address_count
    FROM User
    JOIN Address ON User.username = Address.username
    GROUP BY User.username
    HAVING COUNT(Address.addressID) > 1;
    '''
    cursor.execute(query)
    return cursor.fetchall()

# Show the names of the products that have more than a 10% discount.
#@authorize_manager
def get_discounted_products():
    query = '''
    SELECT DISTINCT Product.name
    FROM Product
    JOIN Discount ON Product.productID = Discount.pID
    WHERE Discount.percentage > 10;
    '''
    cursor.execute(query)
    return cursor.fetchall()

# Show the Orders table with three additional columns: 
# "fee" as the total cost of all products ordered (considering the discount), 
# "shipment fee" as the cost of order shipment, 
# and "total cost" as the sum of "fee" and "shipment fee".
#@authorize_manager
def get_orders_with_costs():
    query = '''
    SELECT 
        Orders.orderID,
        Orders.username,
        Orders.date,
        Orders.shipmentID,
        Orders.shoppingcartID,
        (
            SELECT SUM(
                CASE
                    WHEN Discount.percentage IS NOT NULL THEN (Product.price * (1 - Discount.percentage / 100.0)) * SelectedItems.quantity
                    ELSE Product.price * SelectedItems.quantity
                END
            )
            FROM SelectedItems
            JOIN Product ON SelectedItems.productID = Product.productID
            LEFT JOIN Discount ON Product.productID = Discount.pID
            WHERE SelectedItems.cartID = Orders.shoppingcartID
        ) AS fee,
        Shipment.cost AS shipment_fee,
        (
            (
                SELECT SUM(
                    CASE
                        WHEN Discount.percentage IS NOT NULL THEN (Product.price * (1 - Discount.percentage / 100.0)) * SelectedItems.quantity
                        ELSE Product.price * SelectedItems.quantity
                    END
                )
                FROM SelectedItems
                JOIN Product ON SelectedItems.productID = Product.productID
                LEFT JOIN Discount ON Product.productID = Discount.pID
                WHERE SelectedItems.cartID = Orders.shoppingcartID
            ) 
            + Shipment.cost
        ) AS total_cost
    FROM Orders
    JOIN Shipment ON Orders.shipmentID = Shipment.trackingNumber;
    '''
    cursor.execute(query)
    return cursor.fetchall()

# Find products that have been added to at least one shopping cart. If any product has a discount, reduce the discount by 50%.
#@authorize_manager
def update_discount():
    query = '''
    UPDATE Discount
    SET percentage = percentage * 0.5
    WHERE pID IN (
        SELECT DISTINCT Product.productID
        FROM Product
        JOIN SelectedItems ON Product.productID = SelectedItems.productID
        JOIN Discount ON Product.productID = Discount.pID
    );
    '''
    cursor.execute(query)
    conn.commit()

# Select the name of the product that a specific user has added to their shopping cart.
#@authorize_manager
def get_product_name_for_user(user_username):
    query = '''
    SELECT 
        Product.name AS product_name
    FROM 
        SelectedItems
    JOIN 
        ShoppingCart ON SelectedItems.cartID = ShoppingCart.cartID
    JOIN 
        User ON ShoppingCart.username = User.username
    JOIN 
        Product ON SelectedItems.productID = Product.productID
    WHERE 
        User.username = ?;
    '''
    cursor.execute(query, (user_username,))
    return cursor.fetchall()

# Delete every address associated with the a specific user.
#@authorize_manager
def delete_addresses_for_user(user_username):
    query = '''
    DELETE FROM Address
    WHERE username IN (
        SELECT ShoppingCart.username
        FROM ShoppingCart
        WHERE ShoppingCart.username = ?
    );
    '''
    cursor.execute(query, (user_username,))
    conn.commit()

# Find all products that are in category "X" and change their category to "Y".
#@authorize_manager
def update_product_category(old_category_name, new_category_name):
    query = '''
    UPDATE Product
    SET 
        categoryID = (SELECT categoryID FROM Category WHERE name = ?)
    WHERE 
        categoryID = (SELECT categoryID FROM Category WHERE name = ?);
    '''
    cursor.execute(query, (new_category_name, old_category_name))
    conn.commit()

# Show the context of every review written for a specific product.
#@authorize_manager
def get_reviews_for_product(product_name):
    query = '''
    SELECT Review.context
    FROM Review
    JOIN Product ON Review.pID = Product.productID
    WHERE Product.name = ?;
    '''
    cursor.execute(query, (product_name,))
    return cursor.fetchall()

# Calculate the average cost of each brand's products and show it as a separate column in the brands table.
#@authorize_manager
def get_average_cost_per_brand():
    query = '''
    SELECT Brand.brandID, Brand.name, AVG(Product.price) AS avg_cost
    FROM Brand
    JOIN Product ON Brand.brandID = Product.brandID
    GROUP BY Brand.brandID;
    '''
    cursor.execute(query)
    return cursor.fetchall()


print(get_users_with_products_in_cart("jessicaolson", ")V5IJMRz2F"))
print(get_users_with_multiple_addresses())
print(get_discounted_products())
print(get_orders_with_costs())
update_discount()
print(get_product_name_for_user('tlewis'))
delete_addresses_for_user('X')
update_product_category('X', 'Y')
print(get_reviews_for_product('X'))
print(get_average_cost_per_brand())

conn.close()
