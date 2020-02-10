#! /usr/bin/env bash
set -e

alembic upgrade head

python /app/app/tests_pre_start.py

pytest $* /app/app/tests/
