import streamlit as st
from api import ingest_pdf, chat
import uuid

st.set_page_config(
    page_title="AlgorithmX PDF RAG",
    page_icon="📄",
    layout="wide",
)

# -----------------------------
# Session state
# -----------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Sidebar – PDF Upload
# -----------------------------
st.sidebar.title("📂 PDF Ingestion")

uploaded_file = st.sidebar.file_uploader(
    "Upload a PDF",
    type=["pdf"],
)

if uploaded_file:
    if st.sidebar.button("📥 Ingest PDF"):
        with st.spinner("Indexing PDF into vector database..."):
            try:
                result = ingest_pdf(uploaded_file)
                st.sidebar.success(
                    f"Indexed {result['chunks_indexed']} chunks from {result['file']}"
                )
            except Exception as e:
                st.sidebar.error(f"Ingestion failed: {e}")

st.sidebar.divider()

st.sidebar.markdown("### ⚙️ Chat Settings")
top_k = st.sidebar.slider("Top K Chunks", 1, 10, 5)
only_if_sources = st.sidebar.checkbox("Answer only if sources found", value=False)

# -----------------------------
# Main Chat UI
# -----------------------------
st.title("🤖 AlgorithmX PDF RAG Assistant")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
query = st.chat_input("Ask a question about the uploaded PDFs...")

if query:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": query}
    )
    with st.chat_message("user"):
        st.markdown(query)

    # Call backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = chat(
                    {
                        "query": query,
                        "top_k": top_k,
                        "session_id": st.session_state.session_id,
                        "only_if_sources": only_if_sources,
                    }
                )

                answer = response.get("answer", "")
                sources = response.get("sources", [])

                st.markdown(answer)

                # Show sources
                if sources:
                    st.markdown("---")
                    st.markdown("### 📚 Sources")
                    for src in sources:
                        st.markdown(
                            f"- **{src['doc']}**, page {src['page']}"
                        )

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"Chat failed: {e}")
