import sqlite3

DB_NAME = "expenses.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            type TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_transaction(amount, category, txn_type, description, date):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO transactions (amount, category, type, description, date)
        VALUES (?, ?, ?, ?, ?)
    """, (amount, category, txn_type, description, date))
    conn.commit()
    conn.close()

def get_transactions():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, amount, category, type, description, date FROM transactions ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_transaction(txn_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM transactions WHERE id = ?", (txn_id,))
    conn.commit()
    conn.close()

def get_total_by_type(txn_type):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT SUM(amount) FROM transactions WHERE type = ?", (txn_type,))
    total = cur.fetchone()[0] or 0
    conn.close()
    return total

def get_category_wise_expense():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT category, SUM(amount) 
        FROM transactions 
        WHERE type='expense' 
        GROUP BY category
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_monthly_expense():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT SUBSTR(date, 1, 7) as month, SUM(amount) 
        FROM transactions 
        WHERE type='expense' 
        GROUP BY month
    """)
    rows = cur.fetchall()
    conn.close()
    return rows
