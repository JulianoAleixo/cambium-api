import requests
from flask import Blueprint, jsonify, request

from app.config.settings import Config
from app.services.frankfurter import (
    calculate_performance,
    get_exchange_rate,
    validate_dates,
)

FRANKFURTER_BASE_URL = Config.FRANKFURTER_BASE_URL

frankfurter_bp = Blueprint("frankfurter", __name__)


@frankfurter_bp.route("/frankfurter", methods=["GET"])
def get_frankfurter_rate():
    base = request.args.get("base", default="", type=str)
    dest = request.args.get("dest", default="", type=str)

    try:
        rate = get_exchange_rate(base, dest)
        return jsonify({"exchange_rate": rate}), 200
    except Exception as e:
        return (
            jsonify({"error": "Could not retrieve exchange rate", "details": str(e)}),
            400,
        )


@frankfurter_bp.route("/currency-performance", methods=["GET"])
def get_currency_performance_route():
    """Analyses the appreciation/depreciation of a currency over a period.

    Query params:
        base       - Base currency (e.g. USD)
        dest       - Target currency (e.g. BRL)
        start_date - Start date (YYYY-MM-DD)
        end_date   - End date (YYYY-MM-DD)
    """
    base = request.args.get("base", default="", type=str)
    dest = request.args.get("dest", default="", type=str)
    start_date = request.args.get("start_date", default="", type=str)
    end_date = request.args.get("end_date", default="", type=str)

    try:
        validate_dates(start_date, end_date)

        url = (
            f"{FRANKFURTER_BASE_URL}/{start_date}..{end_date}"
            f"?base={base}&symbols={dest}"
        )
        api_response = requests.get(url)
        api_response.raise_for_status()

        data = api_response.json()
        rates = data.get("rates", {})

        if not rates:
            raise ValueError("No rates found for the given period")

        rate_values = [
            float(day_rates[dest])
            for day_rates in (rates[d] for d in sorted(rates.keys()))
            if dest in day_rates
        ]

        performance = calculate_performance(
            rate_values, base, dest, start_date, end_date
        )
        return jsonify(performance), 200
    except ValueError as e:
        return jsonify({"error": "Invalid input", "details": str(e)}), 400
    except Exception as e:
        return (
            jsonify({"error": "Failed to analyse performance", "details": str(e)}),
            400,
        )
