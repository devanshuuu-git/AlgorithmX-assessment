# 📚 PDF‑based Retrieval‑Augmented Generation (RAG)

A powerful **Retrieval-Augmented Generation (RAG)** system that allows users to upload PDF documents and ask questions about their content. Powered by **Google Gemini**, **Qdrant**, and **FastAPI**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B)
![Gemini](https://img.shields.io/badge/AI-Gemini-8E75B2)

## 🚀 Features

- **📄 PDF Ingestion:** Upload and process PDF documents automatically.
- **🧠 Semantic Search:** Uses high-performance vector embeddings to find relevant context.
- **🤖 Generative AI:** Generates accurate answers using Google's Gemini models.
- **⚡ Real-time:** Fast retrieval and response generation.
- **🐳 Dockerized:** Easy infrastructure setup with Docker Compose.

## 📂 Project Structure

The project is organized into a backend API and a frontend user interface.

```plaintext
.
├── backend/                    # 🐍 FastAPI Backend
│   ├── app/
│   │   ├── db/                 # Database configuration & models
│   │   │   ├── crud.py         # Database CRUD operations
│   │   │   ├── init_db.py      # Database initialization
│   │   │   ├── models.py       # SQLAlchemy models
│   │   │   └── session.py      # Database session management
│   │   ├── routes/             # API Endpoints
│   │   │   ├── chat.py         # Chat/Question answering endpoints
│   │   │   └── ingest.py       # Document upload endpoints
│   │   ├── schemas/            # Pydantic Data Schemas
│   │   │   ├── chat.py         # Chat request/response schemas
│   │   │   └── ingest.py       # Ingestion schemas
│   │   ├── services/           # Core Business Logic
│   │   │   ├── llm.py          # Gemini LLM integration
│   │   │   ├── pdf_ingest.py   # PDF parsing logic
│   │   │   └── retriever.py    # Qdrant vector search logic
│   │   ├── utils/              # Helper Utilities
│   │   │   ├── logger.py       # Logging configuration
│   │   │   ├── text_splitter.py# Text chunking utilities
│   │   │   └── timing.py       # Performance timing decorators
│   │   ├── config.py           # Application configuration
│   │   └── main.py             # App entry point
│   └── requirements.txt        # Backend dependencies
│
├── frontend/                   # 🖥️ Streamlit Frontend
│   ├── api.py                  # API client for communicating with backend
│   ├── streamlit_app.py        # Main Streamlit application UI
│   └── requirements.txt        # Frontend dependencies
│
├── docker-compose.infra.yml    # 🐳 Infrastructure (Postgres, Qdrant)
├── starter.py                  # 🚀 Helper script to launch everything
├── .env.example                # 🔐 Environment variable template
└── README.md                   # 📖 Project documentation
```

## 🛠️ Tech Stack

- **Backend:** FastAPI, SQLAlchemy, Pydantic
- **Frontend:** Streamlit
- **AI/LLM:** Google Gemini (via `google-generativeai`)
- **Vector DB:** Qdrant
- **Database:** PostgreSQL
- **Infrastructure:** Docker, Docker Compose

## ⚡ Quick Start

### 1. Prerequisites

- Python 3.10+
- Docker & Docker Compose

### 2. Clone & Configure

```bash
git clone https://github.com/devanshuuu-git/AlgorithmX-assessment.git
cd AlgorithmX-assessment

# Create .env file
cp .env.example .env
```

**Important:** Open `.env` and add your `GEMINI_API_KEY`.

### 3. Run with One Command

We provide a starter script to set up the infrastructure and run both services.

```bash
python starter.py
```

This will:
1. Start Postgres & Qdrant containers.
2. Launch the FastAPI backend (port 8000).
3. Launch the Streamlit frontend (port 8501).

---

## 🔧 Manual Setup (Optional)

If you prefer running services individually:

**1. Start Infrastructure:**
```bash
docker-compose -f docker-compose.infra.yml up -d
```

**2. Backend Setup:**
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

**3. Frontend Setup:**
```bash
cd frontend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 📝 Usage Guide

1.  **Access the App:** Go to `http://localhost:8501`.
2.  **Upload:** Use the sidebar to upload a PDF file.
3.  **Process:** Click "Process PDF" to ingest the document into the vector database.
4.  **Ask:** Type your question in the chat input. The AI will answer based on the PDF content.

## 🤝 Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.
