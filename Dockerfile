FROM python:3.9-slim

WORKDIR /api

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y netcat-openbsd postgresql-client && apt-get clean

COPY . .

EXPOSE 2341

RUN alembic --version

CMD ["sh", "-c", "while ! nc -z db 5432; do sleep 1; done; uvicorn main:app --host 0.0.0.0 --port 2341 --reload"]