up:
	docker compose up -d sonarqube

logs:
	docker compose logs -f sonarqube

scan:
	docker compose run --rm scanner

down:
	docker compose down
