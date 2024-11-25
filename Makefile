run:
	docker compose up -d
	# TODO sleeps should be replaced by maging the migration wait for the DB
	sleep 2
	poetry run schema
	poetry run start

test:
	poetry run tests

test_reload:
	fd ".*\.py$$" | entr -c poetry run tests
