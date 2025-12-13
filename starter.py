import subprocess
import time
import os

ROOT = os.path.abspath(os.path.dirname(__file__))

def run(cmd, cwd=ROOT):
    subprocess.Popen(cmd, cwd=cwd, shell=True)

print("🚀 Starting infrastructure (Postgres + Qdrant)...")
run("docker compose -f docker-compose.infra.yml up -d")
time.sleep(5)

print("⚙️ Starting backend...")
run(
    r'cmd /k "backend-venv\Scripts\activate && cd backend && python -m uvicorn app.main:app --reload"'
)
time.sleep(5)

print("🎨 Starting frontend...")
run(
    r'cmd /k "frontend-venv\Scripts\activate && cd frontend && streamlit run streamlit_app.py"'
)

print("\n✅ ALL SERVICES STARTED")
print("🌐 Backend → http://127.0.0.1:8000")
print("📘 Swagger → http://127.0.0.1:8000/docs")
print("🖥 Frontend → http://localhost:8501")
