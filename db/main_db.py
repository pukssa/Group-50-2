import sqlite3
from db import queries

# db = sqlite3.connect('db/registered.sqlite3')
db = sqlite3.connect('db/store.sqlite3')
cursor = db.cursor()

async def create_db():
    if db:
        print('База данных подключена')
    # cursor.execute(queries.CREATE_TABLE_registered)
    cursor.execute(queries.CREATE_TABLE_store)
    cursor.execute(queries.CREATE_TABLE_store_detail)

async def sql_insert_registered(fullname, age, email, city, photo):
    cursor.execute(queries.INSERT_registered_query, (
        fullname, age, email, city, photo
    ))
    db.commit()


async def sql_insert_store(name_product, size, price, photo, product_id):
    cursor.execute(queries.INSERT_store_query, (
        name_product, size, price, photo, product_id
    ))
    db.commit()


async def sql_insert_detail(product_id, category, info_product):
    cursor.execute(queries.INSERT_store_detail_query, (
        product_id, category, info_product
    ))
    db.commit()


# CRUD - 1
# ==================================================================
def get_db_connection():
    conn = sqlite3.connect('db/store.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute("""
    SELECT * from store s
    INNER JOIN store_detail sd ON s.product_id = sd.product_id
    INNER JOIN collection c ON s.collection_id = c.collection_id
    """).fetchall()
    conn.close()
    return products

def delete_product(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM store WHERE product_id = ?', (product_id,))
    conn.execute('DELETE FROM store_detail WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()

async def get_product(product_id):
    query = "SELECT * FROM products WHERE product_id = %s"
    result = await db.fetch_one(query, (product_id,))
    return result


async def get_next_product(current_product_id):
    query = "SELECT * FROM products WHERE product_id > %s ORDER BY product_id LIMIT 1"
    result = await db.fetch_one(query, (current_product_id,))
    return result