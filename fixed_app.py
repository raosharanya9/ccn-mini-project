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
        cur.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))

        row = cur.fetchone()
        db.close()

        if row:
            stored_password = row["password"]
            if password == stored_password:
                session["user_id"] = row["id"]
                return """
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Login Successful</title>
                    <style>
                        * { margin: 0; padding: 0; box-sizing: border-box; }
                        body {
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                            min-height: 100vh;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            padding: 20px;
                        }
                        .success-card {
                            background: white;
                            border-radius: 15px;
                            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                            padding: 60px 40px;
                            text-align: center;
                            max-width: 400px;
                            animation: slideIn 0.5s ease-out;
                        }
                        @keyframes slideIn {
                            from { opacity: 0; transform: translateY(20px); }
                            to { opacity: 1; transform: translateY(0); }
                        }
                        .success-icon { font-size: 60px; margin-bottom: 20px; }
                        h1 { color: #28a745; font-size: 28px; margin-bottom: 10px; }
                        p { color: #666; font-size: 16px; margin-bottom: 20px; }
                        .username {
                            background: #f0f0f0;
                            padding: 10px;
                            border-radius: 5px;
                            font-weight: bold;
                            color: #333;
                            margin: 20px 0;
                        }
                        .security-badge {
                            background: #d4edda;
                            color: #155724;
                            padding: 10px;
                            border-radius: 5px;
                            margin: 15px 0;
                            font-size: 13px;
                            border: 1px solid #c3e6cb;
                        }
                        .btn {
                            display: inline-block;
                            margin-top: 20px;
                            padding: 12px 30px;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            text-decoration: none;
                            border-radius: 8px;
                            font-weight: 600;
                            transition: all 0.3s ease;
                        }
                        .btn:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3); }
                    </style>
                </head>
                <body>
                    <div class="success-card">
                        <div class="success-icon">✅</div>
                        <h1>Welcome, """ + row['username'] + """!</h1>
                        <p>Secure login successful</p>
                        <div class="security-badge">🔐 Parameterized query protected</div>
                        <a href="/login" class="btn">Back to Login</a>
                    </div>
                </body>
                </html>
                """

        # failed auth - show error directly
        return """
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Login Failed</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding: 20px;
                }
                .error-card {
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                    padding: 60px 40px;
                    text-align: center;
                    max-width: 400px;
                    animation: slideIn 0.5s ease-out;
                }
                @keyframes slideIn {
                    from { opacity: 0; transform: translateY(20px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                .error-icon { font-size: 60px; margin-bottom: 20px; }
                h1 { color: #dc3545; font-size: 28px; margin-bottom: 10px; }
                p { color: #666; font-size: 16px; margin-bottom: 20px; }
                .security-note {
                    background: #f8d7da;
                    color: #721c24;
                    padding: 10px;
                    border-radius: 5px;
                    margin: 15px 0;
                    font-size: 13px;
                    border: 1px solid #f5c6cb;
                }
                .btn {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 12px 30px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: 600;
                    transition: all 0.3s ease;
                }
                .btn:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3); }
            </style>
        </head>
        <body>
            <div class="error-card">
                <div class="error-icon">🔒</div>
                <h1>Login Failed</h1>
                <p>Invalid username or password</p>
                <div class="security-note">✓ SQL injection attempt blocked by parameterized queries</div>
                <p style="font-size: 14px; color: #999;">Please try again</p>
                <a href="/login" class="btn">Back to Login</a>
            </div>
        </body>
        </html>
        """, 401

    return render_template('login.html')

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 FIXED APP STARTING (SECURE)...")
    print("="*50)
    print("📍 Server running at: http://127.0.0.1:5001")
    print("🔐 Using parameterized queries")
    print("Press Ctrl+C to stop")
    print("="*50 + "\n")
    app.run(host="127.0.0.1", port=5001, debug=True)
