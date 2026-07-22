from flask import Blueprint, jsonify

from services.photon_service import simulate_circular_photon

photon_bp = Blueprint("photon", __name__)


@photon_bp.route("/api/photon")
def photon():

    result = simulate_circular_photon()

    return jsonify(result)