from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# -------------------------
# 1️⃣ Database Init
# -------------------------
def init_db():
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            location TEXT NOT NULL,
            complaint TEXT NOT NULL,
            anonymous BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()

init_db()  # Run once when app starts

# -------------------------
# 2️⃣ Home / Complaint Form
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -------------------------
# 3️⃣ Form Submit
# -------------------------
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    location = request.form.get("location")
    complaint = request.form.get("complaint")
    anonymous = True if request.form.get("anonymous") else False

    # If user checks anonymous → show "Anonymous"
    if anonymous or not name:
        name = "Anonymous"

    # Save in DB
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute(
        'INSERT INTO complaints (name, location, complaint, anonymous) VALUES (?, ?, ?, ?)',
        (name, location, complaint, anonymous)
    )
    conn.commit()
    conn.close()

    return redirect("/")  # redirect to home after submission

# -------------------------
# 4️⃣ Admin Login
# -------------------------
@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")  # create this in templates

@app.route("/admin_dashboard", methods=["POST"])
def admin_dashboard():
    username = request.form.get("username")
    password = request.form.get("password")

    # Simple hardcoded admin login
    if username == "admin" and password == "1234":
        # Fetch all complaints
        conn = sqlite3.connect('complaints.db')
        c = conn.cursor()
        c.execute('SELECT * FROM complaints')
        complaints = c.fetchall()
        conn.close()
        return render_template("admin_dashboard.html", complaints=complaints)
    else:
        return "Invalid credentials! Please go back."

# -------------------------
# 5️⃣ Run Server
# -------------------------
if __name__ == "__main__":
    # ---------- Ngrok Optional ----------
    # Uncomment below lines if you want temporary public URL via Ngrok
    # from pyngrok import ngrok
    # public_url = ngrok.connect(5000)
    # print("Ngrok public URL:", public_url)

    # Local/private server
    app.run(host="0.0.0.0", port=5000, debug=True)