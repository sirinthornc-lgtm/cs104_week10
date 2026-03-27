from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# ✅ แก้ path database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'coffee_shop.db')

def get_db():
    return sqlite3.connect(db_path)

@app.route("/")
def register():
    return render_template("register.html")

@app.route("/add_customer", methods=["POST"])
def add_customer():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    level = request.form["member_level"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM customers")
    count = cur.fetchone()[0]
    customer_id = f"CUST{count + 1:04d}"

    cur.execute("""
        INSERT INTO customers
        (customer_id, name, email, phone, member_level)
        VALUES (?, ?, ?, ?, ?)
    """, (customer_id, name, email, phone, level))

    conn.commit()
    conn.close()

    return redirect("/customers")

@app.route("/customers")
def customers():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM customers")
    data = cur.fetchall()

    conn.close()

    return render_template("customers.html", customers=data)

@app.route("/menu")
def menu():
    return render_template("menu.html")
