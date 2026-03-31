# arquivo: frankfurter_routes.py (ou onde estiver seu frankfurter_bp)
from flask import Blueprint, jsonify, request
# Importe a função que você acabou de criar (ajuste o caminho do import conforme sua pasta)
from app.services.frank_service import obter_taxa_de_cambio 

frankfurter_bp = Blueprint("frankfurter", __name__)

@frankfurter_bp.route("/frankfurter", methods=["GET"])
def get_frankfurter_rate():
    base = request.args.get('base', default='', type=str)
    dest = request.args.get('dest', default='', type=str)
    
    try:
        rate = obter_taxa_de_cambio(base, dest)
        return jsonify(rate), 200
    except Exception as e:
        return jsonify({"erro": "Não foi possível obter a taxa", "detalhes": str(e)}), 400