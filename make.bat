@echo off
if "%1" == "" goto help

if "%1" == "up" goto up
if "%1" == "build up" goto build up
if "%1" == "down" goto down
if "%1" == "volume down" goto volume down
if "%1" == "logs" goto logs
if "%1" == "restart" goto restart
if "%1" == "build" goto build
if "%1" == "clean" goto clean
if "%1" == "backend" goto backend
if "%1" == "frontend" goto frontend
if "%1" == "postgres" goto postgres
if "%1" == "qdrant" goto qdrant
if "%1" == "db-check" goto db-check
if "%1" == "help" goto help

echo Unknown command: %1
goto help

:db-check
call check_db.bat
goto end

:build up
docker compose up --build -d
goto end

:up
docker compose up -d
goto end

:down
docker compose down
goto end

:volume down
docker compose down -v
goto end

:logs
docker compose logs -f
goto end

:restart
docker compose restart
goto end

:build
docker compose build --no-cache
goto end

:clean
docker compose down -v --rmi all
goto end

:backend
docker compose logs -f backend
goto end

:frontend
docker compose logs -f frontend
goto end

:postgres
docker compose logs -f postgres
goto end

:qdrant
docker compose logs -f qdrant
goto end

:help
echo PDF RAG Application - Make Commands
echo ========================================
echo .\make up        - Start all services
echo .\make down      - Stop all services
echo .\make logs      - View logs (follow mode)
echo .\make restart   - Restart all services
echo .\make build     - Rebuild all containers
echo .\make clean     - Remove all containers, volumes, and images
echo .\make backend   - View backend logs
echo .\make frontend  - View frontend logs
echo .\make db-check  - Check database tables
goto end

:end
