# PDF RAG Application

This is a Retrieval-Augmented Generation (RAG) application designed to process PDF documents and answer questions based on their content. It leverages Google's Gemini models for generation and embeddings, Qdrant for vector storage, and PostgreSQL for metadata management. The frontend is built with Streamlit, and the backend is powered by FastAPI.

## 🚀 Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI (Python)
- **LLM & Embeddings:** Google Gemini
- **Vector Database:** Qdrant
- **Database:** PostgreSQL
- **Infrastructure:** Docker & Docker Compose

## 📂 Project Structure

```
.
├── backend/                # FastAPI backend application
│   ├── app/                # Application source code
│   └── requirements.txt    # Backend dependencies
├── frontend/               # Streamlit frontend application
│   ├── streamlit_app.py    # Main Streamlit app
│   └── requirements.txt    # Frontend dependencies
├── docker-compose.infra.yml # Docker Compose for infrastructure (Postgres, Qdrant)
├── starter.py              # Helper script to start the application
├── .env.example            # Example environment variables
└── README.md               # Project documentation
```

## 🛠️ Setup & Installation

### Prerequisites

- [Python 3.10+](https://www.python.org/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Environment Configuration

Create a `.env` file in the root directory by copying the example file:

```bash
cp .env.example .env
```

Open `.env` and update the `GEMINI_API_KEY` with your actual API key.

### 3. Start Infrastructure

Start the required databases (PostgreSQL and Qdrant) using Docker Compose:

```bash
docker-compose -f docker-compose.infra.yml up -d
```

### 4. Install Dependencies

It is recommended to use virtual environments for both backend and frontend.

**Backend:**

```bash
# Create virtual environment
python -m venv backend-venv

# Activate (Windows)
.\backend-venv\Scripts\activate
# Activate (Mac/Linux)
# source backend-venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

**Frontend:**

```bash
# Create virtual environment
python -m venv frontend-venv

# Activate (Windows)
.\frontend-venv\Scripts\activate
# Activate (Mac/Linux)
# source frontend-venv/bin/activate

# Install dependencies
pip install -r frontend/requirements.txt
```

## ▶️ Running the Application

You can use the provided `starter.py` script or run services manually.

### Option A: Using Starter Script

```bash
python starter.py
```

### Option B: Manual Start

**1. Start Backend:**

```bash
# Ensure backend-venv is activated
cd backend
uvicorn app.main:app --reload --port 8000
```

**2. Start Frontend:**

```bash
# Ensure frontend-venv is activated (in a new terminal)
cd frontend
streamlit run streamlit_app.py
```

## 📝 Usage

1.  Open the Streamlit app in your browser (usually `http://localhost:8501`).
2.  Upload a PDF document.
3.  Ask questions related to the document content.
4.  The system will retrieve relevant context and generate an answer using Gemini.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
