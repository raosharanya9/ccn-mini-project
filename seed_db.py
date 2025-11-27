import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), "app.db")

conn = sqlite3.connect(DB)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    password_hash TEXT
)
""")

c.execute("INSERT OR IGNORE INTO users(username, password, password_hash) VALUES(?,?,?)",
    ("admin", "admin123", "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9"))

conn.commit()
conn.close()

print("✅ DB created/updated at:", DB)
