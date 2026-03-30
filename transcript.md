# Transcript: Planejamento da API de Câmbio (Cambium)

**Data**: 29 de março de 2026  
**Projeto**: cambium-api (Flask + conversão de moedas)

---

## Conversa Inicial

### Usuário
> Gostaria de realizar um planejamento de etapas necessárias para os códigos desse projeto. 
> A ideia é fazer uma api que está consumindo de uma api externa, no caso frankfurter, 
> que mostra valores de câmbio, e por meio da nossa api realizar essa conversão no valor 
> de origem para o valor desejado.

### Resposta (Exploração)
Após explorar a estrutura do projeto, identificou-se:

- **Framework**: Flask 3.1.3
- **Linguagem**: Python 3.12+
- **Dependências existentes**: requests, pytest, pytest-cov
- **Estrutura atual**: Factory pattern em pp/__init__.py, endpoint /health existente
- **URL da API externa**: Configurada em settings.py (https://api.frankfurter.app)

---

## Clarificações de Escopo

### Pergunta 1: Quais endpoints você quer implementar?
**Resposta**: Completo: conversão, cotações e histórico

### Pergunta 2: Qual validação é importante?
**Resposta**: Rate limiting (limite de requisições por IP/token)

### Pergunta 3: Quer armazenar histórico de conversões?
**Resposta**: Sim, em um banco de dados

### Pergunta 4: Qual banco de dados?
**Resposta**: PostgreSQL (mais robusto que SQLite)

### Pergunta 5: Quer documentação interativa?
**Resposta**: Sim, Swagger/OpenAPI

---

## Decisões Tomadas

 **Endpoints**: 3 endpoints (conversão, cotações, histórico)  
 **Validações**: Rate limiting por IP (10 req/60s)  
 **Banco de Dados**: PostgreSQL  
 **Documentação**: Swagger/Flasgger  
 **Cache**: In-memory 1h na FrankfurterClient  
 **Sem autenticação**: Escopo inicial (pode ser adicionado depois)

---

## Resultado Final
Um plano detalhado em 8 fases foi criado, com:
- Arquitetura proposta (models, services, routes, utils)
- Passo-a-passo de implementação
- Dependências a instalar
- Verificações para validar cada fase
- Dependências entre fases (o que bloqueia o que)
