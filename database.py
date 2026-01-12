import sqlite3

DB_NAME= "expenses.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   amount REAL NOT NULL,
                   category TEXT NOT NULL,
                   type TEXT CHECK(type IN ('income','expense')) NOT NULL,
                   description TEXT,
                   date TEXT NOT NULL
                   )
                   """)
    conn.commit()
    conn.close()

def add_transaction(amount,category,txn_type,description,date):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""
        INSERT INTO transactions(amount,category,type,description,date) VALUES(?,?,?,?,?)
                   """,(amount,category,txn_type,description,date))
    conn.commit()
    conn.close()

def get_all_transactions():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows=cursor.fetchall()

    conn.close()
    return rows

def get_total_by_type(txn_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE type = ?
    """, (txn_type,))

    total = cursor.fetchone()[0]
    conn.close()
    return total

def get_category_wise_expense():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE type = 'expense'
        GROUP BY category
    """)

    data = cursor.fetchall()
    conn.close()
    return data

def get_monthly_expense():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT substr(date, 1, 7) AS month, SUM(amount)
        FROM transactions
        WHERE type = 'expense'
        GROUP BY month
        ORDER BY month
    """)

    data = cursor.fetchall()
    conn.close()
    return data

def delete_all_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions")

    conn.commit()
    conn.close()