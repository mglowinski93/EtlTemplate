#!/bin/bash
set -e

# Install python packages.
python -m pip install --upgrade --user --disable-pip-version-check pip
pip install -r /app/requirements/development.txt

# Navigate to the entrypoints directory.
cd infrastructures/

# Run database migrations.
./manage.py migrate

# Load users from fixture.
./manage.py loaddata fixtures/users.json

# Run the development server.
exec ./manage.py runserver 0.0.0.0:8000
