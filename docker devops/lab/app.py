import os
from flask import Flask, request, jsonify
import requests as http_requests

app = Flask(__name__)
ROLE = os.environ.get("ROLE", "web")
DATA_DIR = "/data"

@app.route("/health")
def health():
    return jsonify(status="ok", role=ROLE)

if ROLE == "api":
    @app.route("/requests", methods=["POST"])
    def add_request():
        data = request.get_json() or {}
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(os.path.join(DATA_DIR, "requests.log"), "a") as f:
            f.write(str(data) + "\n")
        return jsonify(status="saved"), 201

    @app.route("/requests", methods=["GET"])
    def list_requests():
        try:
            with open(os.path.join(DATA_DIR, "requests.log")) as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = []
        return jsonify(requests=lines)
else:
    @app.route("/")
    def index():
        try:
            r = http_requests.get("http://api:8000/health", timeout=2)
            api_status = r.json()
        except Exception as e:
            api_status = {"error": str(e)}
        return jsonify(web="ok", api=api_status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)