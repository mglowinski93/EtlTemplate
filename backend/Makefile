all: black-check isort-check ruff-check mypy-check bandit-check import-linter-check migrations-check tests
	echo "All checks passed!"

black-check:
	echo "Checking black..."
	black --check ./
	echo "Black passed."

isort-check:
	echo "Sorting imports ..."
	isort --settings-path .isort.cfg --check-only .
	echo "Isort passed."

ruff-check:
	echo "Checking ruff..."
	ruff check ./
	echo "Ruff passed."

mypy-check:
	echo "Checking mypy..."
	mypy ./ --explicit-package-bases
	echo "Mypy passed."

bandit-check:
	echo "Checking bandit..."
	find . -name '*.py' | grep -v tests | xargs bandit
	echo "Bandit passed."

import-linter-check:
	echo "Checking import linter..."
	lint-imports
	echo "Import linter passed."

migrations-check:
	echo "Running migrations check..."
	infrastructures/manage.py makemigrations --dry-run --check
	echo "Migrations check passed."

tests: unit-tests integrated-tests end-to-end-tests
	echo "All tests passed!"

unit-tests:
	echo "Running unit tests..."
	pytest tests/unit/
	echo "Unit tests passed."

integrated-tests:
	echo "Running integrated tests..."
	pytest tests/integrated/
	echo "Integrated tests passed."

end-to-end-tests:
	echo "Running end to end tests..."
	pytest tests/end_to_end/
	echo "End to end tests passed."
