"""
Dairi-O Nutrition Assistant (Unofficial Demo)
A fun AI-powered nutrition chatbot for exploring Dairi-O menu items.

DISCLAIMER: This is an unofficial educational demo, not affiliated with Dairi-O.
Created for AI workshop demonstration purposes.
"""

import streamlit as st
from ollama import chat
from sentence_transformers import SentenceTransformer
import chromadb
import PyPDF2

# ============================================================================
# CUSTOM STYLING - Dairi-O Brand Colors
# ============================================================================

st.set_page_config(
    page_title="Dairi-O Nutrition Assistant",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dairi-O branding
st.markdown("""
    <style>
    /* Dairi-O Green Theme */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Custom header styling */
    .dairi-header {
        background: linear-gradient(135deg, #8BC34A 0%, #689F38 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .dairi-title {
        color: white;
        font-size: 3rem;
        font-weight: bold;
        margin: 0;
        text-align: center;
    }
    
    .dairi-subtitle {
        color: #f0f0f0;
        font-size: 1.2rem;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f0f4f0;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #8BC34A;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #689F38;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Info boxes */
    .nutrition-tip {
        background-color: #E8F5E9;
        border-left: 4px solid #8BC34A;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Quick stats boxes */
    .stat-box {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #8BC34A;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
    <div class="dairi-header">
        <h1 class="dairi-title">🍔 Dairi-O Nutrition Assistant</h1>
        <p class="dairi-subtitle">Your AI-powered guide to making informed choices</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; padding: 1rem; background-color: #FFF3CD; border-radius: 5px; margin-bottom: 2rem;">
        <strong>⚠️ Educational Demo Only</strong><br>
        This is an unofficial AI assistant created for workshop demonstration purposes.
        Not affiliated with Dairi-O. Always verify nutritional information with official sources.
    </div>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Hi! I'm your Dairi-O Nutrition Assistant! I can help you:\n\n"
                      "🔍 Find nutritional info for menu items\n"
                      "⚖️ Compare different options\n"
                      "🥗 Suggest items based on your dietary goals\n"
                      "📊 Answer questions about calories, protein, carbs, and more!\n\n"
                      "What would you like to know?"
        }
    ]

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False

if "menu_stats" not in st.session_state:
    st.session_state.menu_stats = None

# ============================================================================
# DOCUMENT PROCESSING (RAG)
# ============================================================================

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF with special handling for tables."""
    try:
        import pdfplumber
        
        all_text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                
                if tables:
                    for table in tables:
                        if table and len(table) > 0:
                            headers = table[0]
                            
                            for row in table[1:]:
                                if row and any(row):
                                    row_text = []
                                    for i, cell in enumerate(row):
                                        if cell and i < len(headers) and headers[i]:
                                            row_text.append(f"{headers[i]}: {cell}")
                                    
                                    all_text += " | ".join(row_text) + "\n\n"
                
                page_text = page.extract_text()
                if page_text:
                    all_text += page_text + "\n\n"
        
        return all_text
    
    except ImportError:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n\n"
        return text


def chunk_text(text, chunk_size=1000, overlap=100):
    """Split text into chunks while preserving context."""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        if end < len(text):
            newline_pos = text.rfind('\n', end - 100, end)
            if newline_pos != -1:
                end = newline_pos + 1
        
        chunk = text[start:end].strip()
        
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap
    
    return chunks


def setup_vector_database(text_chunks):
    """Create vector database from text chunks."""
    with st.spinner("🔍 Analyzing nutritional data..."):
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


def search_documents(query, n_results=5):
    """Search documents for relevant information."""
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
# CHATBOT LOGIC
# ============================================================================

def chat_with_ai(user_message):
    """Main chatbot function with nutrition-specific prompting."""
    
    system_message = """You are a helpful nutrition assistant for Dairi-O restaurant. 
    
Your role:
- Help customers understand nutritional information about menu items
- Compare different options when asked
- Suggest items based on dietary goals (high protein, low carb, etc.)
- Be accurate with numbers from the nutritional data
- Be friendly and encouraging about healthy choices

When answering about nutritional information:
- Always cite specific numbers (calories, protein, carbs, fat, sodium, etc.)
- If comparing items, present info in an easy-to-read format
- Highlight key differences when comparing
- Use emojis occasionally to be friendly (but don't overdo it)

Important:
- You have access to the official Dairi-O nutritional information
- Look carefully at the data to match items to their exact nutritional values
- If you're not sure, say so rather than guessing
- Remind users this is for informational purposes

Be helpful, accurate, and supportive!"""
    
    # Search documents if available
    context = ""
    if st.session_state.documents_loaded:
        doc_context = search_documents(user_message)
        if doc_context:
            context += f"\n\nNUTRITIONAL DATA:\n{doc_context}"
    
    if context:
        system_message += f"\n\nRELEVANT INFORMATION:{context}"
    
    # Prepare messages
    messages = [
        {"role": "system", "content": system_message}
    ]
    
    for msg in st.session_state.messages:
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    messages.append({"role": "user", "content": user_message})
    
    # Call AI
    response = chat(
        model='llama3.2',
        messages=messages
    )
    
    return response['message']['content']


# ============================================================================
# SIDEBAR - QUICK ACTIONS
# ============================================================================

with st.sidebar:
    st.markdown("### 🍽️ Menu Navigator")
    
    # Upload nutritional data
    st.markdown("#### 📊 Load Nutritional Data")
    uploaded_file = st.file_uploader(
        "Upload Dairi-O nutritional PDF",
        type=["pdf"],
        help="Upload the official Dairi-O nutritional information PDF"
    )
    
    if uploaded_file and st.button("🔄 Process Menu Data", use_container_width=True):
        text = extract_text_from_pdf(uploaded_file)
        chunks = chunk_text(text)
        setup_vector_database(chunks)
        st.session_state.documents_loaded = True
        st.success("✅ Menu data loaded!")
        st.balloons()
    
    if st.session_state.documents_loaded:
        st.success("✅ Nutritional data ready!")
    
    st.divider()
    
    # Quick questions
    st.markdown("#### ⚡ Quick Questions")
    st.caption("Click to ask:")
    
    quick_questions = [
        "🏋️ What's the highest protein item?",
        "🥗 What are the healthiest options?",
        "🔥 Show me low-calorie choices",
        "🍔 Compare burger vs. chicken",
        "🌱 What vegetarian options exist?"
    ]
    
    for question in quick_questions:
        if st.button(question, use_container_width=True):
            # Add to chat
            st.session_state.messages.append({"role": "user", "content": question})
            with st.spinner("Thinking..."):
                response = chat_with_ai(question)
                st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    st.divider()
    
    # Dietary filters (visual only for demo)
    st.markdown("#### 🎯 Dietary Preferences")
    st.multiselect(
        "Filter by:",
        ["High Protein", "Low Carb", "Low Calorie", "Vegetarian", "Under 500 Cal"],
        help="These filters are for demo purposes"
    )
    
    st.divider()
    
    # Clear chat
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [st.session_state.messages[0]]  # Keep welcome message
        st.rerun()
    
    st.divider()
    
    # Info
    st.markdown("""
        <div style="background-color: #E8F5E9; padding: 1rem; border-radius: 5px;">
            <strong>💡 Tips:</strong><br>
            • Ask about specific items<br>
            • Request comparisons<br>
            • Ask for recommendations<br>
            • Inquire about macros
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN CHAT INTERFACE
# ============================================================================

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask about nutrition, compare items, or get recommendations..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)
    
    # Get AI response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            response = chat_with_ai(prompt)
            st.write(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# ============================================================================
# FOOTER
# ============================================================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="stat-box">
            <div class="stat-number">AI</div>
            <div class="stat-label">Powered Assistant</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="stat-box">
            <div class="stat-number">100%</div>
            <div class="stat-label">Unofficial & Fun</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="stat-box">
            <div class="stat-number">🎓</div>
            <div class="stat-label">Educational Demo</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #666;">
        <p>Built with ❤️ for AI Literacy Workshop</p>
        <p style="font-size: 0.8rem;">
            This chatbot uses RAG (Retrieval Augmented Generation) to answer questions<br>
            based on uploaded nutritional data. Not affiliated with Dairi-O.
        </p>
    </div>
""", unsafe_allow_html=True)
