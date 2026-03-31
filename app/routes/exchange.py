from flask import Blueprint, jsonify, request
from app.services.frank_service import obter_taxa_de_cambio 

exchange_bp = Blueprint("exchange", __name__)

@exchange_bp.route("/exchange", methods=["GET"])
def get_exchange():
    base = request.args.get('base', default='', type=str)
    dest = request.args.get('dest', default='', type=str)
    value = request.args.get('value', default=0.0, type=float)
    
    try:
        rate = obter_taxa_de_cambio(base, dest)
        converted_value = rate * value
        
        return jsonify({
            "moeda_base": base,
            "moeda_destino": dest,
            "valor_original": value,
            "taxa_utilizada": rate,
            "valor_convertido": converted_value
        }), 200
        
    except Exception as e:
        return jsonify({"erro": "Falha na conversão", "detalhes": str(e)}), 400