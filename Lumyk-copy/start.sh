#!/bin/bash

echo "Rodando migrations..."
flask --app manage db upgrade --directory backend/app/migrations

echo "Rodando seeders..."
PYTHONPATH=backend python -m backend.app.db.seeders.seeder

echo "Iniciando o servidor Flask..."
gunicorn -b 0.0.0.0:10000 wsgi:app
