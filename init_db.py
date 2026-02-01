import sqlite3

conn = sqlite3.connect("feedback.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    message TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id)
)
""")

conn.commit()
conn.close()

print("Database initialized successfully")
