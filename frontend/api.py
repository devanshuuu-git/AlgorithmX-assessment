import requests

BACKEND_URL = "http://127.0.0.1:8000"


def ingest_pdf(file):
    response = requests.post(
        f"{BACKEND_URL}/ingest/",
        files={"file": (file.name, file, "application/pdf")},
        timeout=300,
    )
    response.raise_for_status()
    return response.json()


def chat(payload: dict):
    response = requests.post(
        f"{BACKEND_URL}/chat/",
        json=payload,
        timeout=300,
    )
    response.raise_for_status()
    return response.json()
