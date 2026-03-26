# Cambium

## Integrantes

| Nome              | GitHub                                                  |
|-------------------|---------------------------------------------------------|
| Henrique Pizzoni  | [henrique-pizzoni](https://github.com/henrique-pizzoni) |
| João Pedro Santos | [joaopedromsantos](https://github.com/joaopedromsantos) |
| Juliano Aleixo    | [JulianoAleixo](https://github.com/JulianoAleixo)       |
| Leonardo Ferreira | [LeonardoFerreira23](https://github.com/LeonardoFerreira23)                  |

## Sobre o projeto

O Cambium é uma API que permite converter valores entre diferentes moedas do mundo de forma simples e rápida. Basta informar o valor, a moeda de origem e a moeda de destino — a API consulta as taxas de câmbio atualizadas e devolve o valor convertido na hora.

Por exemplo: quanto vale 100 dólares em reais agora? Ou 50 euros em ienes? O Cambium responde isso em instantes, usando dados oficiais do Banco Central Europeu.

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
pip install -r requirements.txt
```

**4. Inicie a API**

```bash
python run.py
```

A API estará disponível em `http://localhost:5000`.

### Testando

Com a API rodando, acesse no navegador ou via terminal:

```bash
# Verificar se a API está no ar
curl http://localhost:5000/health
```