deploy:
	docker network create maillog || true && docker-compose up -d --build

down:
	docker-compose down

db_upgrade:
	docker-compose exec api python cli.py rdbs:upgrade

db_downgrade:
	docker-compose exec api python cli.py rdbs:downgrade

parse:
	docker-compose exec api python cli.py parse:log