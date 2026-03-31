import requests
from app.config.settings import Config

FRANKFURTER_BASE_URL = Config.FRANKFURTER_BASE_URL

def get_exchange_rate(base: str, dest: str) -> float:
    url = f'{FRANKFURTER_BASE_URL}/latest?from={base}&to={dest}'
    api_response = requests.get(url)
    
    api_response.raise_for_status() 
    
    dados = api_response.json()
    return float(dados["rates"][dest])