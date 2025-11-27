# --- Day2 vulnerable login (use this exact block) ---
import sqlite3
from flask import Flask, request, render_template

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username','')
        p = request.form.get('password','')

        # INTENTIONALLY VULNERABLE: uses actual DB column `password_hash`
        query = f"SELECT * FROM users WHERE username = '{u}' AND password_hash = '{p}';"
        print("EXECUTED QUERY:", query)   # copy this output as evidence

        db = get_db()
        cur = db.cursor()
        try:
            cur.execute(query)   # vulnerable to SQLi
            user = cur.fetchone()
        except Exception as e:
            print("SQL ERROR:", e)
            return "Server error", 500

        if user:
            return "Login success"
        else:
            return "Login failed", 401

    return render_template('login.html')
# --- end vulnerable login ---
if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 FLASK APP STARTING...")
    print("="*50)
    print("📍 Server running at: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop")
    print("="*50 + "\n")
    app.run(host='127.0.0.1', port=5000, debug=True)

