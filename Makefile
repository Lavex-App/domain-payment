all:
	poetry run isort domain_payment/ tests/
	poetry run black domain_payment/ tests/
	poetry run flake8 domain_payment/ tests/
	poetry run mypy domain_payment/ tests/ --install-types --non-interactive --show-error-codes
	poetry run pylint domain_payment/ tests/
	poetry run wily build domain_payment/
	poetry run wily diff -a --no-detail domain_payment/

style:
	isort domain_payment/
	black --line-length 120 domain_payment/

run:
	uvicorn domain_payment.main:app --host 0.0.0.0 --reload
