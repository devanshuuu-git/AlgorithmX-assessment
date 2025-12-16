.PHONY: up down logs restart clean build help

help:
	@echo "PDF RAG Application - Makefile Commands"
	@echo "========================================"
	@echo "make up        - Start all services"
	@echo "make down      - Stop all services"
	@echo "make logs      - View logs (follow mode)"
	@echo "make restart   - Restart all services"
	@echo "make build     - Rebuild all containers"
	@echo "make clean     - Remove all containers, volumes, and images"
	@echo "make backend   - View backend logs"
	@echo "make frontend  - View frontend logs"

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

restart:
	docker compose restart

build:
	docker compose build --no-cache

clean:
	docker compose down -v --rmi all

backend:
	docker compose logs -f backend

frontend:
	docker compose logs -f frontend

postgres:
	docker compose logs -f postgres

qdrant:
	docker compose logs -f qdrant
