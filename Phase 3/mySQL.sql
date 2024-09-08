CREATE TABLE User (
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    phoneNumber TEXT,
    password TEXT,
    PRIMARY KEY (username, email)
);

CREATE TABLE Manager (
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT,
    PRIMARY KEY (username, email)
);

CREATE TABLE Address (
    addressID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    state TEXT,
    city TEXT,
    street TEXT,
    pin TEXT,
    FOREIGN KEY (username) REFERENCES User(username)
);

CREATE TABLE Review (
    reviewID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    pID TEXT,
    date TEXT,
    context TEXT,
    FOREIGN KEY (username) REFERENCES User(username),
    FOREIGN KEY (pID) REFERENCES Product(productID)
);

CREATE TABLE Orders (
    orderID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    date TEXT,
    shipmentID TEXT,
    shoppingcartID INTEGER,
    FOREIGN KEY (username) REFERENCES User(username),
    FOREIGN KEY (shipmentID) REFERENCES Shipment(trackingNumber),
    FOREIGN KEY (shoppingcartID) REFERENCES ShoppingCart(cartID)
);

CREATE TABLE Product (
    productID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    stockQuantity INTEGER,
    price REAL,
    brandID INTEGER,
    categoryID INTEGER,
    FOREIGN KEY (brandID) REFERENCES Brand(brandID),
    FOREIGN KEY (categoryID) REFERENCES Category(categoryID)
);

CREATE TABLE ShoppingCart (
    cartID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    FOREIGN KEY (username) REFERENCES User(username)
);

CREATE TABLE SelectedItems (
    itemID INTEGER PRIMARY KEY AUTOINCREMENT,
    cartID INTEGER,
    productID INTEGER,
    quantity INTEGER,
    FOREIGN KEY (cartID) REFERENCES ShoppingCart(cartID),
    FOREIGN KEY (productID) REFERENCES Product(productID)
);

CREATE TABLE Brand (
    brandID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE Category (
    categoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE Discount (
    discountID INTEGER PRIMARY KEY AUTOINCREMENT,
    pID INTEGER,
    percentage REAL,
    startDate TEXT,
    endDate TEXT,
    FOREIGN KEY (pID) REFERENCES Product(productID)
);

CREATE TABLE Shipment (
    trackingNumber TEXT PRIMARY KEY,
    orderID INTEGER,
    carrier TEXT,
    cost REAL,
    status TEXT,
    sentDate TEXT,
    receivedDate TEXT
);
