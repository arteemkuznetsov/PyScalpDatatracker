FROM python:3.11-slim

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd postgresql-client && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . /app
