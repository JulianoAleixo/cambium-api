# Cambium

![CI Status](https://github.com/JulianoAleixo/cambium-api/actions/workflows/cicd.yaml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.12%2B-blue?logo=python&logoColor=white)
![Repo Size](https://img.shields.io/github/repo-size/JulianoAleixo/cambium-api)

---

## Integrantes

| Nome              | GitHub                                                  |
|-------------------|---------------------------------------------------------|
| Henrique Pizzoni  | [henrique-pizzoni](https://github.com/henrique-pizzoni) |
| João Pedro Santos | [joaopedromsantos](https://github.com/joaopedromsantos) |
| Juliano Aleixo    | [JulianoAleixo](https://github.com/JulianoAleixo)       |
| Leonardo Ferreira | [LeonardoFerreira23](https://github.com/LeonardoFerreira23)                  |

---

## Sobre o projeto

O Cambium é uma API que permite converter valores entre diferentes moedas do mundo de forma simples e rápida. Basta informar o valor, a moeda de origem e a moeda de destino — a API consulta as taxas de câmbio atualizadas e devolve o valor convertido na hora.

Por exemplo: quanto vale 100 dólares em reais agora? Ou 50 euros em ienes? O Cambium responde isso em instantes, usando dados oficiais do Banco Central Europeu.

---

## Instalação

### Pré-requisitos

- [Python 3.12+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)

### Passo a passo

**1. Clone o repositório**

```bash
git clone https://github.com/JulianoAleixo/cambium-api.git
cd cambium-api
```

**2. Crie e ative o ambiente virtual**

```bash
python -m venv .venv
```

```bash
# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

**3. Instale as dependências**

```bash
pip install -e ".[dev]"
```

**4. Inicie a API**

```bash
python run.py
```

A API estará disponível em `http://localhost:5000`.

### Testando

Com a API rodando, você pode testar de duas formas:

**Via navegador ou terminal:**

```bash
# Verificar se a API está no ar
curl http://localhost:5000/health
```

**Rodar testes com cobertura (serviços):**

```bash
pytest
```

Isso gerará um relatório de cobertura em `htmlcov/index.html` com visualização interativa.

---

## Tecnologias Utilizadas

### Core
* **Linguagem:** [Python 3.12+](https://www.python.org/)
* **Framework Web:** [Flask 3.1.3](https://flask.palletsprojects.com/)
* **Requisições HTTP:** [Requests](https://requests.readthedocs.io/)

### Qualidade de Código e Padronização
* **Formatação:** [Black](https://black.readthedocs.io/en/stable/) 
* **Linting:** [Flake8](https://flake8.pycqa.org/en/latest/)
* **Organização ded Imports:** [isort](https://pycqa.github.io/isort/)

### Testes e Cobertura
* **Suíte de Testes:** [Pytest](https://docs.pytest.org/en/stable/)
* **Cobertura:** [Pytest-cov](https://pytest-cov.readthedocs.io/en/latest/)
* **Relatórios Visuais:** [Pytest-html](https://pytest-html.readthedocs.io/en/latest/)

---

## Estrutura do Projeto

```bash
├───.github
│   └───workflows       # Automação de CI/CD
├───app                 # Código principal da aplicação
│   ├───config          # Configurações globais
│   ├───routes          # Definição dos endpoints
│   └───services        # Regra de negócio e integrações
└───tests               # Suíte de testes
```

---

## Variáveis de Ambiente

As variáveis de ambiente foram definidas como `secrets` no github. As variáveis são:
* FLASK_DEBUG
* FRANKFURTER_BASE_URL
* MAIL_PASSWORD
* MAIL_TO
* MAIL_USERNAME
* RAILWAY_SERVICE_ID
* RAILWAY_TOKEN
* REQUEST_TIMEOUT

## Rotas

### Converter de moeda base para moeda destino

GET `http://localhost:5000/exchange?base=<base>&dest=<dest>&value=<value>`

Exemplo: 
```bash
# Chamada
http://localhost:5000/exchange?base=EUR&dest=USD&value=100

# Retorno
{
    "base_currency": "EUR",
    "converted_value": 114.84,
    "exchange_rate": 1.1484,
    "original_value": 100.0,
    "target_currency": "USD"
}
```

### Obter taxa de conversão entre moedas

GET `http://localhost:5000/frankfurter?base=<base>&dest=<dest>`

Exemplo:
```bash
# Chamada: 
http://localhost:5000/frankfurter?base=EUR&dest=USD

# Retorno: 
{
    "exchange_rate": 1.1484
}
```

### Obter a variação dos valores a partir de duas datas

GET `http://localhost:5000/currency-performance?base=<base>&dest=<dest>&start_date=<start_date>&end_date=<end_date>`

Exemplo:
```bash
# Chamada
http://localhost:5000/currency-performance?base=EUR&dest=USD&start_date=2025-10-09&end_date=2026-01-05

# Retorno
{
    "absolute_change": 0.0053,
    "base_currency": "EUR",
    "end_date": "2026-01-05",
    "final_rate": 1.1664,
    "highest_rate": 1.1787,
    "initial_rate": 1.1611,
    "lowest_rate": 1.1491,
    "percentage_change": 0.46,
    "start_date": "2025-10-09",
    "target_currency": "USD"
}
```

### Rotas em Produção

Para testar os endpoints em produção, basta substituir nas URLs `http://localhost:5000` por `https://cambium-api-production.up.railway.app`

---

## Import de Endpoints no Postman

Para testar os endpoints de uma melhor forma, basta importar o `cambium-postman.json` no Postman. Isso cria 2 pastas, uma para endpoints em Dev, usando localhost e outra com os endpoints em Produção, usando a Railway. 

---

## Prompts Utilizados

Ao longo do desenvolvimento do projeto, foi utilizado o uso de IA para pesquisa e guias em itens específicos. Todo o resumo de histórico de prompts pode ser acessado no arquivo `PROMPTS.md`.