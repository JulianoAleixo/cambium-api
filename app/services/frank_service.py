import requests
from app.config.settings import Config

FRANKFURTER_BASE_URL = Config.FRANKFURTER_BASE_URL

def obter_taxa_de_cambio(base: str, dest: str) -> float:
    """Busca a taxa de câmbio atual na API do Frankfurter."""
    url = f'{FRANKFURTER_BASE_URL}/latest?from={base}&to={dest}'
    api_response = requests.get(url)
    
    #Se a API der erro (exemplo de moeda que não existe), isso levanta uma exceção
    api_response.raise_for_status() 
    
    dados = api_response.json()
    return float(dados["rates"][dest])