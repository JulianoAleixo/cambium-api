from flask import Blueprint, jsonify, request
from app.services.frankfurter import get_exchange_rate

exchange_bp = Blueprint("exchange", __name__)

@exchange_bp.route("/exchange", methods=["GET"])
def get_exchange():
    base = request.args.get('base', default='', type=str)
    dest = request.args.get('dest', default='', type=str)
    value = request.args.get('value', default=0.0, type=float)
    
    try:
        rate = get_exchange_rate(base, dest)
        converted_value = rate * value
        
        return jsonify({
            "base_currency": base,
            "target_currency": dest,
            "original_value": value,
            "exchange_rate": rate,
            "converted_value": converted_value
        }), 200
        
    except Exception as e:
        return jsonify({"error": "Conversion failed", "details": str(e)}), 400