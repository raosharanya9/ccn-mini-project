from flask import Flask, render_template, request, redirect, url_for
import sqlite3, hashlib, os

app = Flask(__name__)
DB = os.path.join(os.path.dirname(__file__), "app.db")

def check_login(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (username, password_hash))
    user = c.fetchone()
    conn.close()
    return user is not None

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if check_login(username, password):
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid username or password.")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return "<h2>✅ Login successful! Welcome to your dashboard.</h2>"

if __name__ == "__main__":
    app.run(debug=True)
