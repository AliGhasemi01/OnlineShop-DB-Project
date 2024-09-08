/*
SELECT DISTINCT User.username, User.email, User.name, User.phoneNumber
FROM User
JOIN ShoppingCart ON User.username = ShoppingCart.username
JOIN SelectedItems ON ShoppingCart.cartID = SelectedItems.cartID
JOIN Product ON SelectedItems.productID = Product.productID;
*/

/*
SELECT User.username, User.email, User.name, User.phoneNumber, COUNT(Address.addressID) as address_count
FROM User
JOIN Address ON User.username = Address.username
GROUP BY User.username
HAVING COUNT(Address.addressID) > 1;
*/

/*
SELECT DISTINCT Product.name
FROM Product
JOIN Discount ON Product.productID = Discount.pID
WHERE Discount.percentage > 10;
*/

/*
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
*/

/*
UPDATE Discount
SET percentage = percentage * 0.5
WHERE pID IN (
    SELECT DISTINCT Product.productID
    FROM Product
    JOIN SelectedItems ON Product.productID = SelectedItems.productID
    JOIN Discount ON Product.productID = Discount.pID
);
*/

/*
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
    User.username = 'tlewis';
*/

/*
DELETE FROM Address
WHERE username IN (
    SELECT ShoppingCart.username
    FROM ShoppingCart
    WHERE ShoppingCart.username = 'X'
);
*/

/*
UPDATE Product
SET 
    categoryID = (SELECT categoryID FROM Category WHERE name = 'Y')
WHERE 
    categoryID = (SELECT categoryID FROM Category WHERE name = 'X');
*/

/*
SELECT Review.context
FROM Review
JOIN Product ON Review.pID = Product.productID
WHERE Product.name = 'X';
*/

/*
SELECT Brand.brandID, Brand.name, AVG(Product.price) AS avg_cost
FROM Brand
JOIN Product ON Brand.brandID = Product.brandID
GROUP BY Brand.brandID;
*/