# OnlineShop-DB-Project
Here’s a concise and well-structured README for your project based on the documents provided for each phase:

---

# Online Shop Database Design

This project is a comprehensive database design for an online shop, created as part of a university database course at Amirkabir University of Technology. The design focuses on managing users, products, orders, and other crucial aspects of an online store.

## Project Overview

The project consists of four main phases:

### Phase 1: ERD Design
- **Objective:** Design an Entity-Relationship Diagram (ERD) for the online shop database.
The ERD includes tables for users, managers, products, categories, brands, orders, and more, detailing their relationships and attributes, ensuring all necessary components for the system are modeled effectively.

### Phase 2: Database Normalization
- **Objective:** Normalize the database up to the third normal form (3NF).
Tables were normalized to eliminate redundancy and ensure data integrity. A report was prepared explaining the normalization process, and an updated ERD reflecting these changes was created.

### Phase 3: Table Creation & Data Insertion
- **Objective:** Implement the database schema in MySQL and populate it with data.
The tables were created based on the normalized design, and data was inserted manually using SQL `INSERT` commands. Additionally, `Faker` was used to generate and insert random data.

### Phase 4: Queries & Reports
- **Objective:** Write and execute meaningful SQL queries on the database.
Various queries were written to retrieve useful insights, such as identifying users in specific regions with orders exceeding a certain amount. Queries were implemented and tested using Python scripts, connecting to the database.

## How to Use

1. Clone the repository:  
   `git clone https://github.com/AliGhasemi01/OnlineShop-DB-Project.git`
2. Set up the MySQL database using the provided SQL files.
3. Run the Python scripts to insert data and execute queries.
