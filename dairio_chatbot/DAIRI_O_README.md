# 🍔 Dairi-O Nutrition Assistant

An **unofficial, educational demo** showcasing how AI can help customers make informed menu choices. Built as a workshop example of branded chatbot development.

![Demo Status](https://img.shields.io/badge/Status-Educational%20Demo-yellow)
![Not Affiliated](https://img.shields.io/badge/Affiliation-Unofficial-red)

## ⚠️ Important Disclaimer

This is a **demonstration project** created for AI literacy workshops. It is:
- ❌ **NOT** affiliated with Dairi-O restaurant
- ❌ **NOT** official nutritional advice
- ✅ **FOR** educational purposes only
- ✅ **TO** demonstrate RAG chatbot development

Always verify nutritional information with official Dairi-O sources.

## 🎯 What Makes This Special?

This isn't just a generic chatbot - it's a **branded, domain-specific application** that demonstrates:

### 1. Custom Styling & Branding
- Dairi-O green color scheme (`#8BC34A`, `#689F38`)
- Custom CSS for professional appearance
- Branded header and UI elements
- Responsive layout with modern design

### 2. Domain-Specific Features
- **Nutritional focus**: Specialized prompting for food/nutrition queries
- **Quick questions**: Pre-loaded common queries
- **Dietary filters**: UI for preference-based filtering (demo)
- **Comparison mode**: Built-in support for comparing menu items
- **Recommendation engine**: Suggests items based on goals

### 3. Enhanced User Experience
- Welcome message with clear capabilities
- Quick action buttons in sidebar
- Visual stat boxes and nutrition tips
- Emoji integration for friendly tone
- Mobile-responsive design

### 4. RAG Optimizations
- Table-aware extraction (using pdfplumber)
- Nutrition-specific chunking strategies
- Enhanced retrieval for structured data
- Domain-tuned system prompts

## 🚀 How to Run

```bash
# Install dependencies
pip install streamlit ollama sentence-transformers chromadb PyPDF2 pdfplumber

# Make sure Ollama is running
ollama serve

# Run the chatbot
streamlit run dairi_o_chatbot.py
```

## 📖 How to Use

1. **Upload Menu Data**
   - Click "Upload Dairi-O nutritional PDF" in sidebar
   - Select the nutritional information PDF
   - Click "Process Menu Data"
   - Wait for "✅ Menu data loaded!"

2. **Ask Questions**
   - Type in the chat: "What's in the grilled chicken sandwich?"
   - Use quick questions: Click any sidebar button
   - Compare items: "Compare the burger and turkey dog"
   - Get recommendations: "What's your healthiest option?"

3. **Explore Features**
   - Try dietary preference filters (UI demo)
   - Clear chat and start fresh
   - Read nutrition tips in the interface

## 💡 Example Questions

**Nutritional Information:**
- "What are the macros for the plain grilled chicken sandwich?"
- "How much protein is in the veggie burger?"
- "Which item has the least sodium?"

**Comparisons:**
- "Compare calories between hamburger and double burger"
- "What's healthier: crispy or grilled chicken?"
- "Show me all chicken options with their protein content"

**Recommendations:**
- "What's the best high-protein, low-calorie option?"
- "I want something under 400 calories"
- "What vegetarian options do you have?"

**General:**
- "Tell me about your salads"
- "What comes on the All The Way topping?"
- "Explain the nutritional table"

## 🎨 Customization Guide

Want to create your own branded chatbot? Here's what I customized:

### Colors
```python
# Primary brand color
--primary-green: #8BC34A
--dark-green: #689F38
--light-green: #E8F5E9

# Update these in the st.markdown() CSS section
```

### Branding Elements
1. **Page config**: Title, icon, layout
2. **Header**: Custom HTML with gradient background
3. **Sidebar**: Quick actions and filters
4. **Footer**: Stats boxes and attribution
5. **Chat avatars**: Custom emojis (🤖 and 👤)

### System Prompt
Located in `chat_with_ai()` function - customize for your domain:
```python
system_message = """You are a helpful nutrition assistant for [YOUR BRAND]...
```

### Quick Questions
Edit the `quick_questions` list in the sidebar:
```python
quick_questions = [
    "Your question here",
    "Another question",
    ...
]
```

## 🏗️ Architecture

```
User Interface (Streamlit)
        ↓
Custom CSS Styling (Brand colors, layout)
        ↓
Chat Interface (Messages back and forth)
        ↓
RAG System:
  1. PDF Upload → pdfplumber extraction
  2. Text → Chunks (1000 chars, preserving tables)
  3. Chunks → Embeddings (sentence-transformers)
  4. Embeddings → Vector DB (ChromaDB)
        ↓
User Query → Vector Search → Relevant Chunks
        ↓
Chunks + Query → Ollama (llama3.2)
        ↓
AI Response → Display to User
```

## 🎓 Workshop Teaching Points

This demo illustrates:

### 1. **From Generic to Branded**
- Shows transformation of basic chatbot to branded application
- Demonstrates importance of UX in AI applications
- Highlights domain-specific customization

### 2. **RAG in Practice**
- Real-world use case: restaurant nutritional data
- Table handling challenges and solutions
- Importance of accurate retrieval for factual data

### 3. **User Experience Matters**
- Quick actions reduce friction
- Clear disclaimers build trust
- Visual design enhances engagement

### 4. **Domain Expertise**
- Custom prompting for nutrition queries
- Specialized vocabulary and formatting
- Context-aware responses

## 📊 Features Breakdown

| Feature | Purpose | Implementation |
|---------|---------|----------------|
| Custom CSS | Professional branding | `st.markdown()` with styles |
| Welcome message | Set expectations | Pre-loaded in `messages` |
| Quick questions | Reduce typing | Sidebar buttons |
| Dietary filters | Visual demo | `st.multiselect()` |
| Stat boxes | Visual appeal | HTML + CSS |
| Enhanced RAG | Table accuracy | pdfplumber + custom chunking |
| Domain prompts | Better responses | Specialized system message |

## 🔧 Technical Stack

- **Frontend**: Streamlit (with custom CSS)
- **AI Model**: Ollama (llama3.2)
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB
- **PDF Processing**: pdfplumber (tables), PyPDF2 (fallback)
- **Styling**: Custom CSS in-line

## 🎯 Use Cases for This Demo

1. **Workshop demonstrations**
   - Show attendees what they can build
   - Inspire customization ideas
   - Demonstrate branding importance

2. **Portfolio projects**
   - Example of domain-specific AI application
   - Shows technical + design skills
   - Demonstrates end-to-end thinking

3. **Prototyping**
   - Quick mockup for restaurant chatbot concept
   - Test RAG with real menu data
   - Validate user experience

4. **Teaching tool**
   - Illustrate prompt engineering
   - Show table handling in RAG
   - Demonstrate UI/UX principles

## 🚧 Limitations & Disclaimers

**This is a demo, not a production app:**
- ⚠️ No user authentication
- ⚠️ No data persistence between sessions
- ⚠️ No API rate limiting
- ⚠️ No error logging
- ⚠️ Dietary filters are UI-only (not functional)
- ⚠️ Requires manual PDF upload each session

**Accuracy considerations:**
- AI responses may contain errors
- Always verify nutritional info with official sources
- Not suitable for medical/dietary advice
- Numbers should be cross-referenced with menu

## 📝 License & Attribution

This is an educational demo created for AI literacy workshops in Winston-Salem, NC.

**NOT affiliated with Dairi-O restaurant.**

Feel free to use this as a template for your own branded chatbots, but:
- Don't claim affiliation with brands you don't represent
- Always include disclaimers
- Use for educational purposes
- Replace branding when adapting for other businesses

## 🎉 Credits

- Built for Winston-Salem AI Literacy Workshops
- Dairi-O nutritional data used for educational demonstration
- Powered by: Streamlit, Ollama, ChromaDB, Anthropic Claude (Replit version)

---

**Remember:** This demo shows what's possible, but always get permission before creating branded applications for real businesses!
