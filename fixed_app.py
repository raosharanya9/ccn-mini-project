import sqlite3
import hashlib
from flask import Flask, request, render_template, flash, session

# Secure fixed app for Day-3 (Member C) — run separately from the vulnerable app.
app = Flask(__name__)
app.secret_key = "replace_this_with_a_random_secret"

DB = "app.db"

def hash_pw(p: str) -> str:
    return hashlib.sha256(p.encode()).hexdigest()

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','')

        # Only log the username attempt (no passwords, no raw SQL)
        print(f"[fixed_app] LOGIN ATTEMPT username={username}")

        db = get_db()
        cur = db.cursor()
        # Parameterized query — prevents SQL injection
        cur.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        db.close()

        if row:
            stored_hash = row["password_hash"]
            if hash_pw(password) == stored_hash:
                session["user_id"] = row["id"]
                return f"Welcome, {row['username']}!"
        # failed auth
        flash("Login failed")
        return render_template('login.html'), 401

    return render_template('login.html')

if __name__ == "__main__":
    # run this app separately: python fixed_app.py
    app.run(host="127.0.0.1", port=5001, debug=True)
