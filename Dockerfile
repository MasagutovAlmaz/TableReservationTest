FROM python:3.9-slim

WORKDIR /api

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 2341

RUN alembic --version

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "2341", "--reload"]