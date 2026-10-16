from flask import Flask, render_template, jsonify, request
from wordfreq import top_n_list
import random
import time
import sqlite3
import os
import secrets
import threading

app = Flask(__name__)
we_still_playing = True
string = ""
challenges = {}
challenge_lock = threading.Lock()
words = [
    word for word in top_n_list("en", 50000)
    if len(word) == 5 and word.isalpha()
][:2000]
def create_database():
    conn = sqlite3.connect("leaderboard.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            username TEXT,
            seconds REAL
        )
    """)
    conn.commit()
    conn.close()

create_database()
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/new-game")

@app.route("/submit-score", methods=["POST"])
def submit_score():
    data = request.get_json(silent=True) or {}

    username = data.get("username", "")
    answer = data.get("answer", "")
    challenge_id = data.get("challenge_id", "")

    if not isinstance(username, str) or not 1 <= len(username.strip()) <= 20:
        return jsonify({"error": "Invalid username"}), 400

    if not isinstance(answer, str) or not isinstance(challenge_id, str):
        return jsonify({"error": "Invalid submission"}), 400

    with challenge_lock:
        challenge = challenges.pop(challenge_id, None)

    if challenge is None:
        return jsonify({"error": "Game expired or already submitted"}), 400

    elapsed = time.monotonic() - challenge["start"]

    if answer != challenge["string"]:
        return jsonify({
            "correct": False,
            "elapsed": elapsed
        })

    conn = sqlite3.connect("leaderboard.db")
    conn.execute(
        "INSERT INTO scores (username, seconds) VALUES (?, ?)",
        (username.strip(), elapsed)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "correct": True,
        "elapsed": elapsed
    })
def new_game():
    # Each visitor gets a fresh string; don't store shared game state.
    for i in range(1):
        word = random.choice(words)
        word1 = random.choice(words)
        word2 = random.choice(words)
        word3 = random.choice(words)
        word4 = random.choice(words)
        word5 = random.choice(words)
        word6 = random.choice(words)
        word7 = random.choice(words)
        word8 = random.choice(words)
        word9 = random.choice(words)
        string = word + " " + word1 + " " + word2 + " " + word3 + " " + word4 + " " + word5 + " " + word6 + " " + word7 + " " + word8 + " " + word9
    challenge_id = secrets.token_urlsafe(24)

with challenge_lock:
    challenges[challenge_id] = {
        "string": string,
        "start": time.monotonic()
    }

return jsonify({
    "string": string,
    "challenge_id": challenge_id
})

# Example leaderboard scores

@app.route("/leaderboard")
def show_leaderboard():
    conn = sqlite3.connect("leaderboard.db")

    scores = conn.execute("""
        SELECT username, MIN(seconds) AS best
        FROM scores
        GROUP BY username
        ORDER BY best ASC
        LIMIT 20
    """).fetchall()

    conn.close()

    return render_template(
        "leaderboard.html",
        leaderboard=scores
    )

def show_leaderboard():
    sorted_scores = sorted(
        leaderboard,
        key=lambda player: player["time"]
    )

    return render_template(
        "leaderboard.html",
        leaderboard=sorted_scores
    )

if __name__ == "__main__":
    app.run(debug=False)
