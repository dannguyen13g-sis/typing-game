from flask import Flask, render_template, jsonify
from wordfreq import top_n_list
import random
import time
import sqlite3

app = Flask(__name__)
we_still_playing = True
string = ""
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
    return jsonify({"string": string})

# Example leaderboard scores
leaderboard = [
    {"username": "MangoMan", "time": 8.52},
    {"username": "SpeedKing", "time": 9.71},
    {"username": "FastTyper", "time": 11.24}
]

@app.route("/leaderboard")
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
