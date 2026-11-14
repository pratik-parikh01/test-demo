import os

import requests
from flask import Flask, jsonify

app = Flask(__name__)

USERS = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
    3: {"id": 3, "name": "Carol", "email": "carol@example.com"},
}

PRODUCTS_SERVICE_URL = os.getenv("PRODUCTS_SERVICE_URL", "http://node-service:3000")


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "users"})


@app.route("/users")
def list_users():
    return jsonify(list(USERS.values()))


@app.route("/users/<int:user_id>")
def get_user(user_id):
    user = USERS.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)


@app.route("/users/<int:user_id>/products")
def get_user_products(user_id):
    user = USERS.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        resp = requests.get(f"{PRODUCTS_SERVICE_URL}/products?owner_id={user_id}", timeout=3)
        products = resp.json()
    except requests.RequestException as exc:
        return jsonify({"error": f"Could not reach products service: {exc}"}), 502

    return jsonify({"user": user, "products": products})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
