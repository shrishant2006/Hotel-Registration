from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "f3a9c1e7b2d84f6a9e0c5b7d3a1f8e6c"  # Change this in production!

# --- Database Configuration ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DB_PATH = os.path.join(INSTANCE_DIR, "example.db")


def init_db():
    """Create instance folder, database, and table if they don't already exist."""
    if not os.path.exists(INSTANCE_DIR):
        os.makedirs(INSTANCE_DIR)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # CREATE TABLE IF NOT EXISTS ensures existing DB files are reused safely
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            owner TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            rooms INTEGER NOT NULL,
            phone TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# --- Routes ---

@app.route("/")
def index():
    conn = get_db_connection()
    hotels = conn.execute("SELECT * FROM hotels ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", hotels=hotels)


@app.route("/add", methods=["POST"])
def add_hotel():
    name = request.form.get("name", "").strip()
    owner = request.form.get("owner", "").strip()
    address = request.form.get("address", "").strip()
    city = request.form.get("city", "").strip()
    rooms = request.form.get("rooms", "").strip()
    phone = request.form.get("phone", "").strip()

    if not all([name, owner, address, city, rooms, phone]):
        flash("All fields are required.", "error")
        return redirect(url_for("index"))

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO hotels (name, owner, address, city, rooms, phone) VALUES (?, ?, ?, ?, ?, ?)",
        (name, owner, address, city, rooms, phone),
    )
    conn.commit()
    conn.close()
    flash("Hotel registered successfully.", "success")
    return redirect(url_for("index"))


@app.route("/edit/<int:hotel_id>", methods=["POST"])
def edit_hotel(hotel_id):
    name = request.form.get("name", "").strip()
    owner = request.form.get("owner", "").strip()
    address = request.form.get("address", "").strip()
    city = request.form.get("city", "").strip()
    rooms = request.form.get("rooms", "").strip()
    phone = request.form.get("phone", "").strip()

    conn = get_db_connection()
    conn.execute(
        """UPDATE hotels
           SET name = ?, owner = ?, address = ?, city = ?, rooms = ?, phone = ?
           WHERE id = ?""",
        (name, owner, address, city, rooms, phone, hotel_id),
    )
    conn.commit()
    conn.close()
    flash("Hotel updated successfully.", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:hotel_id>")
def delete_hotel(hotel_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM hotels WHERE id = ?", (hotel_id,))
    conn.commit()
    conn.close()
    flash("Hotel deleted successfully.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)