# AI Chatbot Workshop - Complete Guide

## 🎯 Workshop Overview

**Duration:** ~2 hours  
**Level:** Complete beginners welcome  
**What attendees will build:** A fully functional chatbot with document upload (RAG) and Google search capabilities

## 📋 Pre-Workshop Setup (Send to Attendees 1 Week Before)

### Required Software

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, CHECK "Add Python to PATH"

2. **Ollama** (for running AI models locally)
   - Download from: https://ollama.com/download
   - After installing, open terminal and run: `ollama pull llama3.2`
   - This downloads the AI model we'll use (~2GB, do this before the workshop!)

3. **Code Editor** (choose one)
   - VS Code: https://code.visualstudio.com/
   - Or any text editor they're comfortable with

### Installation Steps (For Attendees)

```bash
# 1. Create a folder for the workshop
mkdir chatbot-workshop
cd chatbot-workshop

# 2. Download the files from GitHub (you'll share this link)
# Or manually create the files from the workshop materials

# 3. Install required packages
pip install -r requirements.txt

# 4. Test that Ollama is working
ollama list
# You should see llama3.2 in the list
```

## 🎓 Workshop Teaching Flow

### Part 0: Introduction (10 minutes)

**What to cover:**
- What we're building today
- What is a chatbot? (simple: software that talks with you)
- What is RAG? (giving the chatbot information to work with)
- What are embeddings? (turning text into numbers the computer can compare)

**Show the finished product:**
- Run the complete chatbot
- Demo uploading a document
- Demo asking questions about it
- Demo Google search
- This gets everyone excited!

### Part 1: Build Basic Chatbot (30 minutes)

**Teaching Goal:** Get a simple conversation working first!

**What to explain:**
1. What Streamlit does (makes web apps from Python)
2. What Ollama does (runs AI models on your computer)
3. How chat history works (storing messages in a list)

**Simplified starter code to build together:**

```python
import streamlit as st
from ollama import chat

st.title("My First Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Type a message..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get AI response
    response = chat(
        model='llama3.2',
        messages=st.session_state.messages
    )
    
    # Show and save AI response
    ai_message = response['message']['content']
    st.session_state.messages.append({"role": "assistant", "content": ai_message})
    
    # Refresh to show new messages
    st.rerun()
```

**Run it:**
```bash
streamlit run simple_chatbot.py
```

**Key concepts to emphasize:**
- Session state = memory between page refreshes
- Messages = a list of dictionaries (role + content)
- The AI needs to see all previous messages to have context

### Part 2: Add Document Upload (RAG) (45 minutes)

**Teaching Goal:** Show how to give the chatbot knowledge it didn't have before

**Concepts to explain (using analogies):**

1. **Text chunking** = "Like breaking a book into paragraphs so you can find the right section"
   
2. **Embeddings** = "Converting text into coordinates in space - similar meanings are close together"
   - Show visual: words like "dog" and "puppy" would be close in this space
   - Words like "dog" and "car" would be far apart

3. **Vector database** = "Like a really smart search engine that understands meaning, not just keywords"

**Walk through the code step-by-step:**

```python
# Show them the PDF reading function
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text
```

**Explain:** "We're just reading each page and combining all the text"

```python
# Show them chunking
def chunk_text(text, chunk_size=500):
    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start:start + chunk_size]
        chunks.append(chunk)
        start += chunk_size
    return chunks
```

**Explain:** "We break the text into 500-character pieces so the AI doesn't get overwhelmed"

**Demo the embedding process:**
- Upload a simple document (like a PDF about your local YMCA)
- Watch it process
- Ask a question about the document
- Show how it finds the right chunk

**Important:** Emphasize that this is what RAG means - Retrieval (finding the right chunk) + Augmented (adding it to the prompt) + Generation (AI creates the answer)

### Part 3: Add Google Search (30 minutes)

**Teaching Goal:** Give the chatbot access to current information

**Explain the problem:**
- "The AI model was trained on data from the past"
- "It doesn't know what happened yesterday or today"
- "We need to give it a tool to search for current info"

**Show the search function:**

```python
def google_search(query, max_results=3):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
    
    # Format results
    formatted = ""
    for result in results:
        formatted += f"{result['title']}\n{result['body']}\n"
    
    return formatted
```

**Explain:** 
- We're using DuckDuckGo (it's free, no API key needed)
- We format the results as text
- We add them to the prompt before sending to the AI

**Demo:**
- Ask "What's the weather today in Winston-Salem?"
- Ask "What's the latest news about AI?"
- Show how the search results get added to the context

### Part 4: Putting It All Together (15 minutes)

**Show the complete flow:**

```
User asks a question
    ↓
Is it about the documents? → Search documents
    ↓
Is it about current events? → Search Google
    ↓
Combine everything into one prompt
    ↓
Send to AI model
    ↓
Get response back
    ↓
Display to user
```

**Let attendees experiment:**
- Upload their own documents
- Ask questions
- Try different search queries
- See what works and what doesn't

## 🎁 Portfolio Enhancement Tips

**Help attendees customize their chatbot:**

1. **Change the AI model:**
   - Try different Ollama models: `llama3.2`, `mistral`, `phi`
   - Explain: different models have different personalities and capabilities

2. **Add more document types:**
   - CSV files
   - Word documents (.docx)
   - Websites

3. **Improve the search logic:**
   - Use sentiment analysis to detect when to search
   - Let users toggle search on/off

4. **Add memory:**
   - Save conversations to a file
   - Load previous conversations

## 🐛 Common Issues and Solutions

### Ollama not found
```bash
# Make sure Ollama is running
ollama serve
# In another terminal, check if models are downloaded
ollama list
```

### Embeddings slow
**Solution:** This is normal! Explain that:
- First time loads the model (~100MB)
- After that, it's cached and faster
- For workshops, process documents before attendees arrive

### ChromaDB errors
```bash
# Try clearing the database
rm -rf chroma.db
```

### Import errors
```bash
# Reinstall packages
pip install --upgrade -r requirements.txt
```

## 📝 Workshop Handout

Create a one-page handout with:

### What You Built Today
- ✅ A chatbot that runs on your own computer
- ✅ RAG (Retrieval Augmented Generation) to search documents
- ✅ Google search integration
- ✅ A complete web interface

### Key Concepts You Learned
- **Embeddings:** Converting text to numbers for smart search
- **Vector Databases:** Storage designed for similarity search
- **Tool Use:** Giving AI access to external information
- **Session State:** Keeping data between page refreshes

### Next Steps
- [ ] Upload different documents and test
- [ ] Customize the UI (colors, layout)
- [ ] Add to GitHub portfolio
- [ ] Try different AI models
- [ ] Share with friends/colleagues

### Resources
- Streamlit docs: https://docs.streamlit.io
- Ollama models: https://ollama.com/library
- LangChain tutorials: https://python.langchain.com
- Your workshop code: [GitHub link]

## 🎯 Success Metrics

**Attendees should leave able to:**
1. Explain what RAG is in simple terms
2. Run the chatbot on their own computer
3. Upload documents and ask questions about them
4. Understand how embeddings enable semantic search
5. Have working code they can add to their portfolio

## 💡 Extension Ideas for Advanced Students

1. **Add conversation memory across sessions**
   - Save to SQLite database
   - Load previous conversations

2. **Multi-document comparison**
   - Upload multiple PDFs
   - Ask "What do these documents agree/disagree on?"

3. **Citation tracking**
   - Show which document chunk was used
   - Display page numbers

4. **Image understanding**
   - Use vision-capable models
   - Upload images and ask questions

5. **Voice interface**
   - Add speech-to-text
   - Text-to-speech for responses

## 📧 Follow-up Email Template

```
Subject: AI Chatbot Workshop - Code & Resources

Hi everyone!

Great job today building your AI chatbot! 🎉

Here's what we covered:
• Basic chatbot with Ollama
• RAG (document search and retrieval)
• Google search integration
• Complete web interface with Streamlit

Your code is available at: [GitHub link]

Next steps:
1. Customize your chatbot
2. Add it to your portfolio
3. Experiment with different models
4. Join our next workshop: [link]

Questions? Reply to this email or join our Discord: [link]

Keep building!
Gus
```
