up:
	docker compose up -d sonarqube

logs:
	docker compose logs -f sonarqube

scan:
	docker compose run --rm scanner

down:
	docker compose down

coverage:
	PYTHONPATH=. pytest --cov=generator --cov-report=xml --cov-report=html --cov-config=.coveragerc
