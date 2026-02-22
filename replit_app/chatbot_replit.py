"""
AI Chatbot Workshop - Replit Version
This version uses the Anthropic API instead of Ollama so it works in cloud environments.

To use in Replit:
1. Add ANTHROPIC_API_KEY to Secrets (left sidebar, lock icon)
2. Click Run!
"""

import streamlit as st
from anthropic import Anthropic
from sentence_transformers import SentenceTransformer
import chromadb
from duckduckgo_search import DDGS
import PyPDF2
import os

# ============================================================================
# SETUP
# ============================================================================

st.set_page_config(page_title="AI Chatbot Workshop", page_icon="🤖", layout="wide")
st.title("🤖 AI Chatbot with RAG & Search")
st.caption("Built from scratch in Python! (Replit Version)")

# Initialize Anthropic client
# In Replit, set ANTHROPIC_API_KEY in Secrets
try:
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
except:
    st.error("⚠️ Please add ANTHROPIC_API_KEY to Secrets (lock icon in left sidebar)")
    st.stop()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False


# ============================================================================
# DOCUMENT PROCESSING (RAG)
# ============================================================================

def extract_text_from_pdf(pdf_file):
    """Extract all text from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def chunk_text(text, chunk_size=500, overlap=50):
    """Split long text into smaller chunks for better searching."""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    
    return chunks


def setup_vector_database(text_chunks):
    """Create a vector database from text chunks."""
    st.info("📊 Converting text to embeddings...")
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    client = chromadb.Client()
    
    try:
        client.delete_collection("documents")
    except:
        pass
    
    collection = client.create_collection("documents")
    
    for i, chunk in enumerate(text_chunks):
        embedding = embedding_model.encode(chunk).tolist()
        collection.add(
            embeddings=[embedding],
            documents=[chunk],
            ids=[f"chunk_{i}"]
        )
    
    st.session_state.collection = collection
    st.session_state.embedding_model = embedding_model
    st.success(f"✅ Processed {len(text_chunks)} chunks!")


def search_documents(query, n_results=3):
    """Search the uploaded documents for relevant information."""
    if "collection" not in st.session_state:
        return None
    
    query_embedding = st.session_state.embedding_model.encode(query).tolist()
    
    results = st.session_state.collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    relevant_text = "\n\n".join(results['documents'][0])
    return relevant_text


# ============================================================================
# GOOGLE SEARCH
# ============================================================================

def google_search(query, max_results=3):
    """Search Google using DuckDuckGo API."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        formatted_results = "🔍 Google Search Results:\n\n"
        for i, result in enumerate(results, 1):
            formatted_results += f"{i}. {result['title']}\n"
            formatted_results += f"   {result['body']}\n"
            formatted_results += f"   Source: {result['href']}\n\n"
        
        return formatted_results
    
    except Exception as e:
        return f"Sorry, search failed: {str(e)}"


# ============================================================================
# CHATBOT BRAIN (using Anthropic API instead of Ollama)
# ============================================================================

def chat_with_ai(user_message):
    """
    Main chatbot function using Claude API.
    
    KEY DIFFERENCE FROM OLLAMA VERSION:
    - Uses Anthropic API instead of local Ollama
    - This works in cloud environments like Replit
    - Requires API key (free tier available)
    """
    
    # Build the system message
    system_message = """You are a helpful AI assistant. 
    
You have access to two tools:
1. Uploaded documents (if available) - search these for questions about the documents
2. Google search - use this for current events, facts, or things not in the documents

Be conversational and helpful!"""
    
    # Check if we should search documents
    context = ""
    if st.session_state.documents_loaded:
        doc_context = search_documents(user_message)
        if doc_context:
            context += f"\n\nRELEVANT DOCUMENT CONTENT:\n{doc_context}"
    
    # Check if we should search Google
    search_keywords = ["current", "latest", "today", "news", "search", "google", "find"]
    should_search = any(keyword in user_message.lower() for keyword in search_keywords)
    
    if should_search:
        search_results = google_search(user_message)
        context += f"\n\n{search_results}"
    
    # Add context to system message
    if context:
        system_message += f"\n\nADDITIONAL CONTEXT:{context}"
    
    # Prepare messages for Claude API
    # Note: Claude API format is slightly different from Ollama
    api_messages = []
    
    for msg in st.session_state.messages:
        api_messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    api_messages.append({
        "role": "user",
        "content": user_message
    })
    
    # Call Claude API
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",  # Using Claude 3.5 Sonnet
        max_tokens=1024,
        system=system_message,
        messages=api_messages
    )
    
    return response.content[0].text


# ============================================================================
# USER INTERFACE
# ============================================================================

# Sidebar for document upload
with st.sidebar:
    st.header("📄 Upload Documents")
    st.write("Upload PDFs or text files to give the chatbot knowledge!")
    
    uploaded_files = st.file_uploader(
        "Choose files",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )
    
    if uploaded_files and st.button("Process Documents"):
        all_text = ""
        
        for uploaded_file in uploaded_files:
            if uploaded_file.type == "application/pdf":
                text = extract_text_from_pdf(uploaded_file)
            else:
                text = uploaded_file.read().decode()
            
            all_text += text + "\n\n"
        
        chunks = chunk_text(all_text)
        setup_vector_database(chunks)
        st.session_state.documents_loaded = True
    
    if st.session_state.documents_loaded:
        st.success("✅ Documents loaded!")
    
    st.divider()
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.write("### Chat")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_with_ai(prompt)
            st.write(response)
    
    # Add AI response
    st.session_state.messages.append({"role": "assistant", "content": response})

# Instructions
with st.expander("ℹ️ How to use this chatbot"):
    st.markdown("""
    **This is the Replit version** - it uses the Claude API instead of local models.
    
    **Basic Chat:**
    - Just type a message and press Enter!
    
    **Using Documents (RAG):**
    1. Upload PDF or TXT files in the sidebar
    2. Click "Process Documents"
    3. Ask questions about your documents!
    
    **Using Google Search:**
    - Ask about current events or use words like "search", "latest", "news"
    
    **Key Difference from Local Version:**
    - This uses the Anthropic Claude API (cloud-based)
    - The local version uses Ollama (runs on your computer)
    - Both do the same thing, just different infrastructure!
    """)

# Teaching note
st.sidebar.divider()
st.sidebar.caption("💡 **For Instructors:** This version uses Claude API instead of Ollama so it works in cloud environments like Replit, Colab, or shared servers.")
