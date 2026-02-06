"""
AI Chatbot Workshop - Build a chatbot with RAG and Google Search
This chatbot can:
1. Have conversations using a local AI model
2. Answer questions about documents you upload
3. Search Google for current information

Perfect for beginners! Every section is clearly commented.
"""

import streamlit as st
from ollama import chat
from sentence_transformers import SentenceTransformer
import chromadb
from duckduckgo_search import DDGS
import PyPDF2
import io

# ============================================================================
# PART 1: SETUP AND CONFIGURATION
# ============================================================================

# Set up the page
st.set_page_config(page_title="AI Chatbot Workshop", page_icon="🤖", layout="wide")
st.title("🤖 AI Chatbot with RAG & Search")
st.caption("Built from scratch in Python!")

# Initialize session state - this keeps data between page refreshes
if "messages" not in st.session_state:
    st.session_state.messages = []  # Stores chat history

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False  # Track if docs are uploaded


# ============================================================================
# PART 2: DOCUMENT PROCESSING (RAG - Retrieval Augmented Generation)
# ============================================================================

def extract_text_from_pdf(pdf_file):
    """
    Extract all text from a PDF file.
    
    Args:
        pdf_file: The uploaded PDF file
        
    Returns:
        str: All text from the PDF
    """
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def chunk_text(text, chunk_size=500, overlap=50):
    """
    Split long text into smaller chunks for better searching.
    Think of this like breaking a book into paragraphs.
    
    Args:
        text: The full text to split
        chunk_size: How many characters per chunk
        overlap: How many characters to overlap between chunks (helps with context)
        
    Returns:
        list: List of text chunks
    """
    chunks = []
    start = 0
    
    while start < len(text):
        # Get a chunk of text
        end = start + chunk_size
        chunk = text[start:end]
        
        # Add it to our list
        chunks.append(chunk)
        
        # Move forward, but overlap a bit
        start = end - overlap
    
    return chunks


def setup_vector_database(text_chunks):
    """
    Create a vector database from text chunks.
    This converts text into numbers (embeddings) so we can search by meaning.
    
    Args:
        text_chunks: List of text chunks to store
    """
    # Load the embedding model - this converts text to numbers
    st.info("📊 Converting text to embeddings (this might take a moment)...")
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Create a vector database
    client = chromadb.Client()
    
    # Delete old collection if it exists
    try:
        client.delete_collection("documents")
    except:
        pass
    
    # Create new collection
    collection = client.create_collection("documents")
    
    # Add each chunk to the database
    for i, chunk in enumerate(text_chunks):
        # Convert text to embedding (a list of numbers)
        embedding = embedding_model.encode(chunk).tolist()
        
        # Store in database
        collection.add(
            embeddings=[embedding],
            documents=[chunk],
            ids=[f"chunk_{i}"]
        )
    
    # Save to session state so we can use it later
    st.session_state.collection = collection
    st.session_state.embedding_model = embedding_model
    st.success(f"✅ Processed {len(text_chunks)} chunks!")


def search_documents(query, n_results=3):
    """
    Search the uploaded documents for relevant information.
    
    Args:
        query: The question to search for
        n_results: How many relevant chunks to return
        
    Returns:
        str: The most relevant text from the documents
    """
    if "collection" not in st.session_state:
        return None
    
    # Convert the query to an embedding
    query_embedding = st.session_state.embedding_model.encode(query).tolist()
    
    # Search the database
    results = st.session_state.collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    # Combine the results into one text
    relevant_text = "\n\n".join(results['documents'][0])
    return relevant_text


# ============================================================================
# PART 3: GOOGLE SEARCH TOOL
# ============================================================================

def google_search(query, max_results=3):
    """
    Search Google for current information.
    We use DuckDuckGo's API - it's free and doesn't need an API key!
    
    Args:
        query: What to search for
        max_results: How many results to return
        
    Returns:
        str: Formatted search results
    """
    try:
        # Create a search instance
        with DDGS() as ddgs:
            # Perform the search
            results = list(ddgs.text(query, max_results=max_results))
        
        # Format the results nicely
        formatted_results = "🔍 Google Search Results:\n\n"
        for i, result in enumerate(results, 1):
            formatted_results += f"{i}. {result['title']}\n"
            formatted_results += f"   {result['body']}\n"
            formatted_results += f"   Source: {result['href']}\n\n"
        
        return formatted_results
    
    except Exception as e:
        return f"Sorry, search failed: {str(e)}"


# ============================================================================
# PART 4: THE CHATBOT BRAIN
# ============================================================================

def chat_with_ai(user_message):
    """
    This is the main chatbot function that:
    1. Checks if it should search documents
    2. Checks if it should search Google
    3. Sends everything to the AI model
    4. Returns the response
    
    Args:
        user_message: What the user typed
        
    Returns:
        str: The AI's response
    """
    
    # Build the system message - this tells the AI how to behave
    system_message = """You are a helpful AI assistant. 
    
You have access to two tools:
1. Uploaded documents (if available) - search these for questions about the documents
2. Google search - use this for current events, facts, or things not in the documents

Be conversational and helpful!"""
    
    # Check if we should search the documents
    context = ""
    if st.session_state.documents_loaded:
        doc_context = search_documents(user_message)
        if doc_context:
            context += f"\n\nRELEVANT DOCUMENT CONTENT:\n{doc_context}"
    
    # Check if we should search Google
    # Simple logic: if message contains certain words, search
    search_keywords = ["current", "latest", "today", "news", "search", "google", "find"]
    should_search = any(keyword in user_message.lower() for keyword in search_keywords)
    
    if should_search:
        search_results = google_search(user_message)
        context += f"\n\n{search_results}"
    
    # Add context to the system message if we have any
    if context:
        system_message += f"\n\nADDITIONAL CONTEXT:{context}"
    
    # Prepare the messages for the AI
    messages = [
        {"role": "system", "content": system_message}
    ]
    
    # Add chat history
    for msg in st.session_state.messages:
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    # Add the new user message
    messages.append({"role": "user", "content": user_message})
    
    # Call the AI model
    # We're using Ollama with a local model (no API keys needed!)
    response = chat(
        model='llama3.2',  # You can change this to any model you have in Ollama
        messages=messages
    )
    
    return response['message']['content']


# ============================================================================
# PART 5: THE USER INTERFACE
# ============================================================================

# Sidebar for document upload
with st.sidebar:
    st.header("📄 Upload Documents")
    st.write("Upload PDFs or text files to give the chatbot knowledge!")
    
    uploaded_files = st.file_uploader(
        "Choose files",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        help="Upload PDFs or text files"
    )
    
    if uploaded_files and st.button("Process Documents"):
        all_text = ""
        
        # Process each uploaded file
        for uploaded_file in uploaded_files:
            if uploaded_file.type == "application/pdf":
                text = extract_text_from_pdf(uploaded_file)
            else:  # txt file
                text = uploaded_file.read().decode()
            
            all_text += text + "\n\n"
        
        # Break into chunks and create vector database
        chunks = chunk_text(all_text)
        setup_vector_database(chunks)
        st.session_state.documents_loaded = True
    
    # Show status
    if st.session_state.documents_loaded:
        st.success("✅ Documents loaded!")
    
    st.divider()
    
    # Clear chat button
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
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_with_ai(prompt)
            st.write(response)
    
    # Add AI response to chat
    st.session_state.messages.append({"role": "assistant", "content": response})

# Instructions at the bottom
with st.expander("ℹ️ How to use this chatbot"):
    st.markdown("""
    **Basic Chat:**
    - Just type a message and press Enter!
    
    **Using Documents (RAG):**
    1. Upload PDF or TXT files in the sidebar
    2. Click "Process Documents"
    3. Ask questions about your documents!
    
    **Using Google Search:**
    - Ask about current events or use words like "search", "latest", "news"
    - Example: "What's the latest news about AI?"
    
    **How it works:**
    - Your documents are split into chunks and converted to embeddings
    - When you ask a question, we search for relevant chunks
    - We can also search Google for current information
    - Everything is sent to a local AI model (Llama) that generates a response
    """)
