from flask import request, jsonify

from backend.app import app
from backend.renderer import render_black_hole


@app.route("/")
def home():

    return jsonify({
        "engine": "Stella Nova",
        "status": "running"
    })


@app.route("/render", methods=["POST"])
def render():

    parameters = request.get_json()

    filename = render_black_hole(parameters)

    return jsonify({
        "status": "complete",
        "image": filename
    })

@app.route("/render", methods=["POST"])
def render():

    parameters = request.get_json()

    print(parameters)

    filename = render_black_hole(parameters)

    return jsonify({
        "status": "complete",
        "image": filename
    })