import streamlit as st
import requests
import os

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
API_BASE = f"{BACKEND_URL}/api"

st.set_page_config(
    page_title="PDF RAG Chat",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Session State Initialization ---
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "sessions" not in st.session_state:
    st.session_state.sessions = []

# --- API Helper Functions ---
def get_sessions():
    try:
        response = requests.get(f"{API_BASE}/sessions")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Failed to fetch sessions: {e}")
    return []

def create_session():
    try:
        response = requests.post(f"{API_BASE}/sessions")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Failed to create session: {e}")
    return None

def get_messages(session_id):
    try:
        response = requests.get(f"{API_BASE}/sessions/{session_id}/messages")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Failed to fetch messages: {e}")
    return []

def upload_file(file):
    files = {"file": (file.name, file, file.type)}
    try:
        response = requests.post(f"{API_BASE}/upload", files=files)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Upload failed: {response.text}")
    except Exception as e:
        st.error(f"Upload error: {e}")
    return None

def send_chat_message(query, session_id, model_name, top_k, doc_filter):
    payload = {
        "query": query, 
        "session_id": session_id,
        "model_name": model_name,
        "top_k": top_k,
        "doc_filter": doc_filter
    }
    try:
        response = requests.post(f"{API_BASE}/chat", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Chat failed: {response.text}")
    except Exception as e:
        st.error(f"Chat error: {e}")
    return None

def list_documents():
    try:
        response = requests.get(f"{API_BASE}/documents")
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return []

# --- Sidebar ---
with st.sidebar:
    st.title("📚 PDF RAG")
    
    # 1. Document Upload
    st.subheader("Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        if st.button("Upload & Index"):
            with st.spinner("Uploading and indexing..."):
                result = upload_file(uploaded_file)
                if result:
                    st.success(f"Indexed: {result['filename']}")
                    st.rerun()

    # 2. Document List
    st.subheader("Indexed Documents")
    docs = list_documents()
    doc_map = {"All Documents": "All Documents"}
    if docs:
        for doc in docs:
            status_icon = "✅" if doc['status'] == 'indexed' else "⏳"
            st.text(f"{status_icon} {doc['filename']}")

            
            file_ext = os.path.splitext(doc['filename'])[1]
            stored_filename = f"{doc['file_hash']}{file_ext}"
            doc_map[doc['filename']] = stored_filename
    else:
        st.info("No documents indexed yet.")

    st.divider()

    # 3. Settings Drawer
    with st.expander("⚙️ Settings"):
        model_name = st.selectbox(
            "Model", 
            ["gemini-2.5-flash", "gemini-2.5-pro"],
            index=0
        )
        top_k = st.slider("Top K (Chunks)", min_value=1, max_value=10, value=4)
        
        selected_doc_name = st.selectbox("Filter by Document", list(doc_map.keys()))
        doc_filter = doc_map[selected_doc_name]

    st.divider()
    
    # 4. Session Management
    st.subheader("Chat Sessions")
    if st.button("➕ New Chat"):
        new_sess = create_session()
        if new_sess:
            st.session_state.session_id = new_sess['id']
            st.session_state.messages = []
            st.rerun()

    sessions = get_sessions()
    if sessions:
        for sess in sessions:
            if st.button(f"💬 {sess['title']}", key=sess['id']):
                st.session_state.session_id = sess['id']
                st.session_state.messages = get_messages(sess['id'])
                st.rerun()

# --- Main Chat Interface ---
st.header("Chat with your PDFs")

if not st.session_state.session_id:
    st.info("Please create a new chat or select an existing session from the sidebar.")
else:
    # Display Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])
            # We don't persist context in DB messages for simplicity in this version,
            # so history messages won't show context. Only new ones will.

    # Chat Input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # 1. Display User Message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 2. Get AI Response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_data = send_chat_message(
                    prompt, 
                    st.session_state.session_id,
                    model_name,
                    top_k,
                    doc_filter
                )
                
                if response_data:
                    answer = response_data['response']
                    st.markdown(answer)
                    
                    # Display Collapsible Context
                    context = response_data.get('context')
                    if context:
                        with st.expander("📄 View Source Context"):
                            for i, chunk in enumerate(context):
                                st.markdown(f"**Chunk {i+1}** (Page {chunk['metadata'].get('page', 'N/A')})")
                                st.text(chunk['page_content'])
                                st.divider()
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer})
