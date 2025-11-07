import sqlite3, os, hashlib

DB = os.path.join(os.path.dirname(__file__), "app.db")

def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()

conn = sqlite3.connect(DB)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hash TEXT
)
""")

c.execute("INSERT OR IGNORE INTO users(username, password_hash) VALUES(?,?)",
          ("admin", hash_pw("admin123")))

conn.commit()
conn.close()

print("✅ DB created/updated at:", DB)
