@echo off
echo ========================================
echo 📊 Checking PostgreSQL Database State
echo ========================================

echo.
echo [1/5] Users Table:
docker exec rag_postgres psql -U postgres -d rag_db -c "SELECT * FROM users;"

echo.
echo [2/5] Sessions Table:
docker exec rag_postgres psql -U postgres -d rag_db -c "SELECT id, user_id, title, created_at FROM sessions;"

echo.
echo [3/5] Documents Table:
docker exec rag_postgres psql -U postgres -d rag_db -c "SELECT id, filename, status, created_at FROM documents;"

echo.
echo [4/5] Messages Table (Last 5):
docker exec rag_postgres psql -U postgres -d rag_db -c "SELECT id, role, left(content, 50) as content_preview FROM messages ORDER BY created_at DESC LIMIT 5;"

echo.
echo [5/5] Metrics Table (Last 5):
docker exec rag_postgres psql -U postgres -d rag_db -c "SELECT id, query, latency_ms, model_used FROM metrics ORDER BY created_at DESC LIMIT 5;"

echo.
echo ========================================
echo ✅ Check Complete
echo ========================================
pause
