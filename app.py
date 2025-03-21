from flask import Flask, request, jsonify
import csv
import random
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(get_remote_address, app=app, default_limits=["50 per second", "100 per minute"])

def load_quotes():
    quotes = []
    with open("Quotes.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for i, row in enumerate(reader):
            quotes.append((i, row))  # Store index alongside each dictionary
    return quotes

quotes_data = load_quotes()

@app.route("/")
@limiter.limit("100 per minute")
def random_quote():
    random_index, random_entry = random.choice(quotes_data)
    random_quote = {
        "quote": random_entry["QUOTE"],
        "author": random_entry["AUTHOR"],
        "genre": random_entry["GENRE"],
        "private": {
            "random_line": random_index,
            "author": "superhenryman"
        }
    }
    return jsonify(random_quote)

if __name__ == "__main__":
    app.run(debug=True)
