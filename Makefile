# Convenience commands for the Alzheimer's CDSS project

.PHONY: up down logs build train backend-local frontend-local clean

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

build:
	docker compose build

# Train the ML model inside the running backend container
train:
	docker compose exec backend python -m app.ml.train

# Stop and remove containers + volumes (wipes the database)
clean:
	docker compose down -v
