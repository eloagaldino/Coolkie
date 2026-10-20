cd ~/Coolkie
cp app.py app.py.bak
cat > app.py << 'EOF'
import os

from flask import Flask, abort, jsonify, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=None)

PAGES = {"index.html", "cliente.html", "sabores.html"}


@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/<path:page>.html")
def pages(page):
    filename = f"{page}.html"
    if filename not in PAGES:
        abort(404)
    return send_from_directory(BASE_DIR, filename)


@app.route("/css/<path:filename>")
def css(filename):
    return send_from_directory(os.path.join(BASE_DIR, "css"), filename)


@app.route("/image/<path:filename>")
def image(filename):
    return send_from_directory(os.path.join(BASE_DIR, "image"), filename)


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
EOF
