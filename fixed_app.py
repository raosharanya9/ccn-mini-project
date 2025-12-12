import sqlite3
import hashlib
from flask import Flask, request, render_template, session, redirect, url_for

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

# Redirect root to the login page so users don't need to type /login manually
@app.route('/', methods=['GET'])
def root():
    return redirect(url_for('login'))

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
            # Secure check: compare the stored hash with the hash of provided password
            if hash_pw(password) == stored_hash:
                session["user_id"] = row["id"]
                # render your template in templates/secure_success.html
                return render_template("secure_success.html", username=row["username"])

        # failed auth — render templates/secure_failed.html
        return render_template("secure_failed.html"), 401

    # GET -> show login page
    return render_template('login.html')

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 FIXED APP STARTING (SECURE)...")
    print("="*50)
    print("📍 Server running at: http://127.0.0.1:5001")
    print("🔐 Using parameterized queries + hashing")
    print("Press Ctrl+C to stop")
    print("="*50 + "\n")
    app.run(host="127.0.0.1", port=5001, debug=True)
