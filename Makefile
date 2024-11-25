run:
	docker compose up -d
	poetry run schema
	poetry run start

test:
	poetry run tests

test_reload:
	fd ".*\.py$$" | entr -c poetry run tests

destroy:
	docker compose down -v --remove-orphans
