import sqlite3

DB_NAME = "database.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Table orders
    c.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_name TEXT,
        price INTEGER,
        access_granted TEXT,
        status TEXT
    )
    ''')

    # Table menu items
    c.execute('''
    CREATE TABLE IF NOT EXISTS menu_items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER,
        access_type TEXT,
        payment_type TEXT,
        payment_number TEXT,
        payment_owner TEXT,
        payment_link TEXT
    )
    ''')

    conn.commit()
    conn.close()

def add_order(user_id, item_name, price, access_granted, status="PENDING"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
    INSERT INTO orders (user_id, item_name, price, access_granted, status)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, item_name, price, access_granted, status))
    conn.commit()
    conn.close()

def get_menu_items():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM menu_items')
    data = c.fetchall()
    conn.close()
    return data

def add_menu_item(name, price, access_type, payment_type, payment_number="", payment_owner="", payment_link=""):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
    INSERT INTO menu_items (name, price, access_type, payment_type, payment_number, payment_owner, payment_link)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, price, access_type, payment_type, payment_number, payment_owner, payment_link))
    conn.commit()
    conn.close()
