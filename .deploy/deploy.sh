#!/bin/bash
# Path: /opt/gem-hub-backend/.deploy/deploy.sh
set -e

echo "🚀 Starting Deployment..."

docker compose build web

docker compose up -d --no-deps web

docker compose exec -T web uv run python manage.py migrate --noinput

docker compose exec -T web uv run python manage.py collectstatic --noinput

docker image prune -f

echo "✅ Deployment Successful!"