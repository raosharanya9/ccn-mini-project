import sqlite3
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

# Redirect root → /login
@app.route('/', methods=['GET'])
def root():
    return redirect(url_for('login'))

# Vulnerable login page
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username','')
        p = request.form.get('password','')

        # INTENTIONALLY VULNERABLE (string concat — SQLi enabled)
        query = f"SELECT * FROM users WHERE username = '{u}' AND password='{p}';"
        print("🚨 EXECUTED QUERY:", query)

        db = get_db()
        cur = db.cursor()
        try:
            cur.execute(query)
            user = cur.fetchone()
        except Exception as e:
            print("SQL ERROR:", e)
            return "Server error", 500

        if user:
            return render_template('vulnerable_success.html', username=user['username'])
        else:
            return render_template('vulnerable_failed.html'), 401

    # GET request → show form
    return render_template('login.html')

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 VULNERABLE APP STARTING...")
    print("="*50)
    print("📍 Server running at: http://127.0.0.1:5000")
    print("💀 SQL Injection Enabled")
    print("Press Ctrl+C to stop")
    print("="*50 + "\n")
    app.run(host='127.0.0.1', port=5000, debug=True)
