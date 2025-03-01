from flask import Flask, jsonify, render_template, request, redirect, url_for
from dotenv import load_dotenv
load_dotenv()
import psycopg2
import os
import tkinter as tk

app = Flask(__name__)

def get_db_connections():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    return conn
def init_db():
    conn = get_db_connections()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            animal TEXT PRIMARY KEY,
            count INTEGER
        )
    ''')
    cur.execute("SELECT COUNT(*) FROM votes")
    if cur.fetchone()[0] == 0:
        default_votes = [("Kot", 0), ("Pies", 0), ("Ptak", 0), ("Ryba", 0)]
        cur.executemany("INSERT INTO votes (animal, count) VALUES (%s, %s)", default_votes)
    conn.commit()
    cur.close()
    conn.close()

init_db()

def get_votes():
    conn = get_db_connections()
    cur = conn.cursor()
    cur.execute("SELECT * FROM votes")
    votes = dict(cur.fetchall())
    cur.close()
    conn.close()
    return votes

def save_votes(animal):
    conn = get_db_connections()
    cur = conn.cursor()
    cur.execute("UPDATE votes SET count = count + 1 WHERE animal = %s", (animal,))
    conn.commit()
    cur.close
    conn.close

@app.route("/")
def index():
    return render_template("index.html", votes=get_votes())

@app.route("/vote", methods=["POST"])
def vote():
    animal = request.form["animal"]
    if animal in get_votes():
        save_votes(animal)
    return redirect(url_for("index"))
@app.route("/api/votes", methods=["GET"])
def api_get_votes():
    return jsonify(get_votes())

# API do oddawania głosu
@app.route("/api/vote", methods=["POST"])
def api_vote():
    data = request.get_json()
    animal = data.get("animal")
    if animal and animal in get_votes():
        save_votes(animal)
        return jsonify({"status": "success", "animal": animal})
    return jsonify({"status": "error", "message": "Invalid animal"}), 400
    
@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)

