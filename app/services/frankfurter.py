import requests
from datetime import datetime
from app.config.settings import Config

FRANKFURTER_BASE_URL = Config.FRANKFURTER_BASE_URL

def get_exchange_rate(base: str, dest: str) -> float:
    url = f'{FRANKFURTER_BASE_URL}/latest?from={base}&to={dest}'
    api_response = requests.get(url)
    
    api_response.raise_for_status() 
    
    data = api_response.json()
    return float(data["rates"][dest])



def validate_dates(start_date: str, end_date: str) -> None:
    """Validates the format and order of the given dates.

    Raises:
        ValueError: If the format is invalid or start_date > end_date.
    """
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Dates must be in YYYY-MM-DD format")

    if start_date > end_date:
        raise ValueError("Start date cannot be later than end date")


def calculate_performance(rates: list, base: str, quote: str, start_date: str, end_date: str) -> dict:
    """Calculates appreciation/depreciation metrics from an ordered list of rates.

    Args:
        rates: List of floats in chronological order.
        base, quote: Currencies involved.
        start_date, end_date: Period analysed (YYYY-MM-DD).

    Raises:
        ValueError: If the rates list is empty.
    """
    if not rates:
        raise ValueError("Insufficient data to analyse the period")

    initial_rate = rates[0]
    final_rate = rates[-1]
    absolute_change = final_rate - initial_rate
    percentage_change = (absolute_change / initial_rate) * 100 if initial_rate != 0 else 0

    return {
        "base_currency": base,
        "target_currency": quote,
        "start_date": start_date,
        "end_date": end_date,
        "initial_rate": round(initial_rate, 4),
        "final_rate": round(final_rate, 4),
        "percentage_change": round(percentage_change, 2),
        "absolute_change": round(absolute_change, 4),
        "highest_rate": round(max(rates), 4),
        "lowest_rate": round(min(rates), 4),
    }
