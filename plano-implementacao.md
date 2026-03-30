# Plano de Implementação: API de Câmbio (Cambium)

**Projeto**: cambium-api  
**Objetivo**: API completa para conversão de moedas usando Frankfurter API  
**Data de Criação**: 29 de março de 2026

---

## TL;DR

Implementar uma API Flask que:
1.  Consome API Frankfurter para taxas de câmbio
2.  Oferece 3 endpoints: conversão, cotações, histórico
3.  Armazena histórico em PostgreSQL
4.  Valida moedas e amounts
5.  Rate limit: 10 requisições por 60 segundos por IP
6.  Documentação interactive via Swagger

---

## Arquitetura Proposta

\\\
cambium-api/
app/
 __init__.py                    (factory pattern - MODIFICAR)
 config/
    settings.py                (MODIFICAR - adicionar DB, rate limit config)
 database.py                    (NOVO - setup SQLAlchemy)
 models/
    conversion.py              (NOVO - ORM ConversionHistory)
 services/
    frankfurter.py             (NOVO - client HTTP com cache)
    converter.py               (NOVO - lógica de conversão)
    rate_limiter.py            (NOVO - middleware rate limit)
 routes/
    health.py                  (existente)
    convert.py                 (NOVO - POST /convert)
    rates.py                   (NOVO - GET /rates/{from}/{to})
    history.py                 (NOVO - GET /history)
 utils/
     validators.py              (NOVO - validações)

tests/
 test_frankfurter.py            (NOVO)
 test_converter.py              (NOVO)
 test_routes.py                 (NOVO)
 test_rate_limiter.py           (NOVO)

ROOT/
 requirements.txt               (MODIFICAR - adicionar dependências)
 run.py                         (existente)
 README.md                      (existente)
\\\

---

## Endpoints Resumo

| Método | Rota | Descrição | Rate Limit |
|--------|------|-----------|-----------|
| \POST\ | \/convert\ | Converter valor entre moedas |  10/min |
| \GET\ | \/rates/{from}/{to}\ | Obter taxa atual (ou histórica com \?date=\) |  Sem limite |
| \GET\ | \/health\ | Health check |  Sem limite |
| \GET\ | \/history\ | Histórico de conversões com filtros e paginação |  10/min |

---

## Dependências Finais para requirements.txt

\\\
Flask==3.1.3
Werkzeug==3.1.7
requests==2.33.0
SQLAlchemy==2.0.23
Flask-SQLAlchemy==3.1.1
psycopg2-binary==2.9.9
Flask-Limiter==3.5.0
flasgger==0.9.7.1
pytest==9.0.2
pytest-cov==7.1.0
\\\

---

## Plano: 8 Fases

### Fase 1: Setup do Banco de Dados e ORM
**Bloqueador para**: Fase 2

**Tarefas**:
1. Adicionar ao \equirements.txt\:
   - \SQLAlchemy==2.0.23\
   - \Flask-SQLAlchemy==3.1.1\
   - \psycopg2-binary==2.9.9\

2. Criar \pp/database.py\
3. Atualizar \pp/config/settings.py\ com SQLALCHEMY_DATABASE_URI e rate limit config
4. Criar DB PostgreSQL local

---

### Fase 2: Modelos e Persistência
**Depende de**: Fase 1  
**Bloqueador para**: Fase 4, 6, 8

- Criar \pp/models/conversion.py\ com ConversionHistory ORM
- Atualizar \pp/__init__.py\ com SQLAlchemy init

---

### Fase 3: Integração com API Frankfurter
**Pode rodar em paralelo com**: Fase 4, 5

- Criar \pp/services/frankfurter.py\ com cache 1h
- Criar \pp/utils/validators.py\ com validações ISO 4217 e amounts

---

### Fase 4: Lógica de Negócio
**Depende de**: Fase 2  
**Pode rodar em paralelo com**: Fase 3, 5  
**Bloqueador para**: Fase 6, 8

- Criar \pp/services/converter.py\ com lógica de conversão
- Registrar conversões no banco de dados

---

### Fase 5: Rate Limiting
**Pode rodar em paralelo com**: Fase 3, 4

- Adicionar Flask-Limiter ao requirements.txt
- Criar \pp/services/rate_limiter.py\
- Integrar em \pp/__init__.py\

---

### Fase 6: Endpoints (Routes)
**Depende de**: Fase 2, 4, 5  
**Bloqueador para**: Fase 7, 8

- Criar \pp/routes/convert.py\ (POST /convert com rate limit)
- Criar \pp/routes/rates.py\ (GET /rates/{from}/{to})
- Criar \pp/routes/history.py\ (GET /history com paginação e rate limit)
- Registrar blueprints em \pp/__init__.py\

---

### Fase 7: Documentação Swagger/OpenAPI
**Depende de**: Fase 6

- Adicionar flasgger ao requirements.txt
- Integrar Flasgger em \pp/__init__.py\
- Adicionar docstrings YAML em cada endpoint
- Verificar http://localhost:5000/apidocs

---

### Fase 8: Testes Unitários
**Depende de**: Fase 4, 5, 6

- Criar \	ests/test_frankfurter.py\
- Criar \	ests/test_converter.py\
- Criar \	ests/test_routes.py\
- Criar \	ests/test_rate_limiter.py\
- Rodar \pytest -v --cov=app\ (almejar >80% cobertura)

---

## Decisões de Design

| Decisão | Justificativa |
|---------|-------------|
| **PostgreSQL** | Escalabilidade, robustez, melhor para produção |
| **Flask-Limiter** | Simples, em-memória, sem dependência externa |
| **Flasgger** | Mais leve que Flask-RESTX, menos boilerplate |
| **Cache in-memory** | Balanço entre performance (1h TTL) e dados frescos |
| **Sem autenticação** | Escopo inicial, pode ser adicionada com JWT depois |
| **ISO 4217** | Validação padrão internacional para moedas |

---

## Timeline Esperada

- **Fase 1-2** (Setup + Models): ~2-3 horas
- **Fase 3-5** (Services): ~3-4 horas
- **Fase 6** (Endpoints): ~2-3 horas
- **Fase 7** (Swagger): ~1 hora
- **Fase 8** (Testes): ~2-3 horas
- **Total**: ~11-16 horas de desenvolvimento

---

## Notas Importantes

1. **PostgreSQL Setup**:
\\\ash
psql -U postgres
CREATE DATABASE cambium_db;
CREATE USER cambium WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE cambium_db TO cambium;
\\\

2. **Environment Variables** (.env):
\\\
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=postgresql://cambium:password@localhost:5432/cambium_db
FRANKFURTER_BASE_URL=https://api.frankfurter.app
REQUEST_TIMEOUT=5
\\\

3. **Rodar a Aplicação**:
\\\ash
pip install -r requirements.txt
python run.py
# Access http://localhost:5000
\\\

4. **Melhorias Futuras**:
   - Autenticação com JWT
   - Webhook para notificações
   - Cache distribuído (Redis)
   - Logging estruturado
   - CI/CD pipeline
   - Containerização (Docker)
