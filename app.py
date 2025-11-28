from flask import Flask, request, jsonify
import os

# If you also want to use Drive paths later, adjust BASE_DIR accordingly.
BASE_DIR = os.environ.get("RAMAYANA_BASE", os.path.abspath("."))

SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
os.makedirs(SCRIPTS_DIR, exist_ok=True)

app = Flask(__name__)

def load_script(episode_id="ep001"):
    path = os.path.join(SCRIPTS_DIR, f"{episode_id}.txt")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@app.route("/script", methods=["GET"])
def get_script_api():
    episode_id = request.args.get("episode_id", "ep001")
    text = load_script(episode_id)
    if text is None:
        return jsonify({"error": "script_not_found", "episode_id": episode_id}), 404
    return jsonify({
        "episode_id": episode_id,
        "text": text
    })

@app.route("/")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
