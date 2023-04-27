from flask import Flask, jsonify
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()


@app.route("/api/status")
def status():
    return jsonify({"status": "online", "version": 0.1})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT"))
