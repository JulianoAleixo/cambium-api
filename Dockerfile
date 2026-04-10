FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --upgrade pip && pip install --no-cache-dir .

COPY app/ ./app/
COPY run.py .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "run.py"]