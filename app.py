from flask import Flask, request, jsonify, render_template
import sqlite3
import datetime

app = Flask(__name__)

# --------- DATABASE INITIALIZATION ----------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --------- ROUTES ----------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/checkin", methods=["POST"])
def checkin():
    student_name = request.json.get("student_name")

    if not student_name:
        return jsonify({"error": "Student name is required"}), 400

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO attendance (student_name, timestamp) VALUES (?, ?)", 
              (student_name, timestamp))
    conn.commit()
    conn.close()

    return jsonify({"message": "Check-in successful"}), 200


@app.route("/attendance", methods=["GET"])
def attendance_list():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM attendance")
    rows = c.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "student_name": row[1],
            "timestamp": row[2]
        })

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
