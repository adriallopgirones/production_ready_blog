build:
	docker compose -f local.yml up --build -d --remove-orphans

up:
	docker compose -f local.yml up -d

down:
	docker compose -f local.yml down

down-remove:
	docker-compose -f local.yml down -v --rmi all
show-logs:
	docker compose -f local.yml logs

local-celery:
	celery -A production_ready_blog_project.celery worker --loglevel=info

local-redis:
	redis-server