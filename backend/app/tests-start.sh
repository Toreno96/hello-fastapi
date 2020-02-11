#! /usr/bin/env bash
set -e

# Let the DB start
python /app/app/tests_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python /app/app/initial_data.py

# Run tests
pytest $* /app/app/tests/
