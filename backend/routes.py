from flask import request, jsonify, render_template

from backend.app import app
from backend.renderer import render_black_hole

from pathlib import Path
from flask import send_from_directory


@app.route("/")
def home():
    return jsonify({
        "engine": "Stella Nova",
        "status": "running"
    })


@app.route("/renderer")
def renderer_page():
    return render_template(
        "hybrid_renderer.html"
    )


@app.route("/render", methods=["POST"])
def render_api():
    parameters = request.get_json(
        silent=True
    ) or {}

    filename = render_black_hole(
        parameters
    )

    return jsonify({
        "status": "complete",
        "image": filename
    })

@app.route("/renderer-v2")
def renderer_v2_page():
    return render_template("hybrid_renderer_v2.html")


# Add these imports to backend/routes.py


# Add this near the top of backend/routes.py, after app is imported.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_CANDIDATES = (
    PROJECT_ROOT / "frontend" / "frontend",
    PROJECT_ROOT / "frontend",
)
FRONTEND_DIR = next(
    (folder for folder in FRONTEND_CANDIDATES if (folder / "index.html").exists()),
    FRONTEND_CANDIDATES[0],
)

# Add these routes. They serve the teammate website and keep relative CSS/JS links working.
@app.route("/site")
@app.route("/site/")
def website_home():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/site/<path:filename>")
def website_file(filename):
    return send_from_directory(FRONTEND_DIR, filename)

# Keep the existing POST /render endpoint unchanged.
# Open the integrated website at:
# http://127.0.0.1:5000/site/
#
# Open the backend-connected renderer directly at:
# http://127.0.0.1:5000/site/engine.html
