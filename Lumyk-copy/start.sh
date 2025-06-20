#!/bin/bash

echo "Rodando migrations..."
flask --app manage db upgrade --directory backend/app/migrations

echo "Rodando seeders..."
PYTHONPATH=backend python -m backend.app.db.seeders.seeder

echo "Iniciando o servidor Flask..."
PORT=${PORT:-10000}  # se não existir PORT, usa 10000
gunicorn -b 0.0.0.0:$PORT wsgi:app
