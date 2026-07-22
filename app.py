from flask import Flask
from flask_cors import CORS

from api.photon import photon_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(photon_bp)

@app.route("/")
def home():
    return {
        "project": "Stella Nova",
        "engine": "General Relativity Physics Engine",
        "status": "Running"
    }

if __name__ == "__main__":
    app.run(debug=True)