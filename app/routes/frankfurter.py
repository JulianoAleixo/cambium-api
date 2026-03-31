from flask import Blueprint, jsonify, request
from app.services.frankfurter import get_exchange_rate 

frankfurter_bp = Blueprint("frankfurter", __name__)

@frankfurter_bp.route("/frankfurter", methods=["GET"])
def get_frankfurter_rate():
    base = request.args.get('base', default='', type=str)
    dest = request.args.get('dest', default='', type=str)
    
    try:
        rate = get_exchange_rate(base, dest)
        return jsonify({"exchange_rate": rate}), 200
    except Exception as e:
        return jsonify({"error": "It was not possible to obtain the rate.", "details": str(e)}), 400