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

        # INTENTIONALLY VULNERABLE: uses string concat WITHOUT hashing (vulnerable to SQLi)
        query = f"SELECT * FROM users WHERE username = '{u}' AND password='{p}';"
        print("EXECUTED QUERY:", query)   # copy this output as evidence

        db = get_db()
        cur = db.cursor()
        try:
            cur.execute(query)   # vulnerable to SQLi
            user = cur.fetchone()
        except Exception as e:
            print("SQL ERROR:", e)
            return """
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Server Error</title>
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
                    <div class="error-icon">⚠️</div>
                    <h1>Server Error</h1>
                    <p>Something went wrong. Please try again later.</p>
                    <a href="/login" class="btn">Back to Login</a>
                </div>
            </body>
            </html>
            """, 500

        if user:
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
                    <h1>Login Successful!</h1>
                    <p>Welcome back,</p>
                    <div class="username">""" + user['username'] + """</div>
                    <p>You have successfully logged in.</p>
                    <a href="/login" class="btn">Back to Login</a>
                </div>
            </body>
            </html>
            """
        else:
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
                    <div class="error-icon">❌</div>
                    <h1>Login Failed</h1>
                    <p>Invalid username or password</p>
                    <p style="font-size: 14px; color: #999;">Please try again</p>
                    <a href="/login" class="btn">Back to Login</a>
                </div>
            </body>
            </html>
            """, 401

    return render_template('login.html')
# --- end vulnerable login ---

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 VULNERABLE APP STARTING...")
    print("="*50)
    print("📍 Server running at: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop")
    print("="*50 + "\n")
    app.run(host='127.0.0.1', port=5000, debug=True)
