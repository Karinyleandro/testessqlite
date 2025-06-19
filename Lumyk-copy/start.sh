#!/bin/bash

echo "Rodando migrations..."
flask --app manage.py db upgrade --directory backend/app/migrations

echo "Rodando seeders..."
PYTHONPATH=backend python -m backend.app.db.seeders.seeder

echo "Iniciando o servidor Flask..."
exec gunicorn -b 0.0.0.0:10000 backend.app.main:app