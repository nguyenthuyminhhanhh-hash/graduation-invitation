from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "wishes.db"


# ==========================================
# DATABASE
# ==========================================

def init_database():
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ==========================================
# SAVE WISH
# ==========================================

def save_wish(name, message):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO wishes
        (name, message, created_at)
        VALUES (?, ?, ?)
    """, (
        name,
        message,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# ==========================================
# HOME
# ==========================================

@app.route("/", methods=["GET", "POST"])
def home():

    success = False

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        message = request.form.get("message", "").strip()

        # Giới hạn dữ liệu
        name = name[:100]
        message = message[:500]

        if name and message:

            save_wish(name, message)

            success = True

    return render_template(
        "index.html",
        success=success
    )


# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":

    init_database()

    app.run(
        debug=True
    )