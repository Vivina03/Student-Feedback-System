from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"  # for sessions

def get_db():
    return sqlite3.connect("feedback.db")

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Student registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_pw = generate_password_hash(password)

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO students (username, password) VALUES (?, ?)", (username, hashed_pw))
            db.commit()
        except:
            return "Username already exists"
        return redirect(url_for("login"))
    return render_template("register.html")

# Student login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM students WHERE username=?", (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user[2], password):
            session["student_id"] = user[0]
            session["username"] = user[1]
            return redirect(url_for("feedback"))
        # Admin login
        elif username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect(url_for("admin"))
        else:
            return "Invalid login credentials"
    return render_template("login.html")

# Submit feedback (students only)
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if not session.get("student_id"):
        return redirect(url_for("login"))

    if request.method == "POST":
        message = request.form["message"]
        student_id = session["student_id"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO feedback (student_id, message) VALUES (?, ?)", (student_id, message))
        db.commit()

        return "Feedback submitted successfully!"
    return render_template("feedback.html", username=session["username"])

# Admin view feedback
@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("login"))

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
    SELECT feedback.id, students.username, feedback.message
    FROM feedback JOIN students ON feedback.student_id = students.id
    """)
    data = cursor.fetchall()
    return render_template("admin.html", data=data)

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
