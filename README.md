# 🤖 Build an AI Chatbot with RAG - Workshop

A hands-on workshop where you build a production-ready AI chatbot from scratch using Python, Streamlit, Claude AI, and RAG (Retrieval-Augmented Generation).

![Workshop](https://img.shields.io/badge/Workshop-AI%20Chatbot-blue)
![Level](https://img.shields.io/badge/Level-Beginner%20Friendly-green)
![Duration](https://img.shields.io/badge/Duration-2%20Hours-orange)
![Cloud](https://img.shields.io/badge/Platform-Replit-red)

---

## 🎯 What You'll Build

By the end of this workshop, you'll have created:

- ✅ **AI-powered chatbot** that answers questions about uploaded documents
- ✅ **RAG implementation** with vector search and semantic retrieval
- ✅ **Google search integration** for current information
- ✅ **Professional web interface** using Streamlit
- ✅ **Cloud-deployed application** that runs immediately
- ✅ **Portfolio-ready code** you can customize and share

**No AI experience required. No local installation needed. Everything runs in the cloud.**

---

## 📚 Workshop Overview

This workshop teaches you how modern AI systems actually work by building one yourself. You'll learn:

### Core Concepts
- **RAG (Retrieval-Augmented Generation)** - How AI systems search and cite documents
- **Vector embeddings** - How computers understand meaning
- **Semantic search** - Finding information by concept, not just keywords
- **Prompt engineering** - Writing effective AI instructions
- **Cloud deployment** - Shipping real applications

### Technical Stack
- **Python** - Programming language
- **Streamlit** - Web interface framework
- **Claude Haiku 4.5** - AI model (Anthropic)
- **ChromaDB** - Vector database
- **pdfplumber** - Document processing
- **Replit** - Cloud development platform

### Real-World Skills
- Building production AI applications
- Debugging RAG systems
- Handling structured data (tables)
- Creating branded, domain-specific chatbots
- Professional deployment practices

---

## 🚀 How to Use This Repository

### Step 1: Review the Workshop Slides

📊 **[Open the Workshop Presentation](./AI_Chatbot_Workshop_Feb2026.pptx)**

The slides walk you through:
1. Workshop setup (API keys & Replit)
2. The mission: Building a Dairi-O nutrition chatbot
3. Creating your first AI chatbot
4. Adding RAG for document search
5. Fixing common RAG problems with tables
6. Professional branding and deployment

### Step 2: Follow the Replit Links

The slides contain links to **three Replit projects** that progressively build the chatbot:

1. **Basic Chatbot** - Simple AI conversation
2. **RAG Chatbot** - Add document upload and search
3. **Professional Chatbot** - Branded Dairi-O nutrition assistant

Each Replit project is ready to fork and run. Just:
- Click the link in the slides
- Fork the project
- Add your Anthropic API key to Secrets
- Click "Run"

### Step 3: Build Along with the Workshop

The workshop is designed for **hands-on coding**. You'll:
- Fork each Replit project
- Upload the Dairi-O nutritional PDF
- Test queries and see the chatbot evolve
- Fix bugs (intentionally introduced to teach debugging)
- Customize the final branded version

---

## 📂 Repository Contents

```
├── AI_Chatbot_Workshop_Feb2026.pptx    # Workshop slides
├── chatbot_workshop_replit.py           # Generic workshop chatbot (cloud)
├── dairi_o_chatbot_replit.py           # Branded Dairi-O chatbot (cloud)
├── chatbot_workshop.py                  # Local version (Ollama)
├── dairi_o_chatbot.py                  # Branded local version
├── requirements_replit_haiku.txt        # Python dependencies (cloud)
├── requirements.txt                     # Python dependencies (local)
├── REPLIT_HAIKU_SETUP.md               # Cloud deployment guide
├── TABLE_HANDLING_GUIDE.md             # RAG with tables explained
├── CUSTOMIZATION_GUIDE.md              # Branding your chatbot
├── PRESENTATION_IMPROVEMENTS_GUIDE.md  # Teaching tips
└── README.md                            # You are here!
```

---

## 💡 Workshop Format

**Duration:** 2 hours  
**Format:** Hands-on coding (not a lecture)  
**Requirements:** Laptop with web browser  
**Cost:** Free Anthropic API credits ($5 per account)

### Typical Workshop Flow

| Time | Activity |
|------|----------|
| 0:00-0:10 | Setup (API keys, Replit accounts) |
| 0:10-0:30 | Build basic chatbot |
| 0:30-1:00 | Add RAG and document upload |
| 1:00-1:20 | Debug table handling issues |
| 1:20-1:40 | Fix RAG with better extraction |
| 1:40-2:00 | Add branding and polish |

---

## 🎓 What You'll Learn

### Beginner-Friendly
- How AI chatbots actually work (no magic!)
- Reading and modifying Python code
- Working with cloud platforms (Replit)
- Basic prompt engineering
- API usage and configuration

### Intermediate Topics
- RAG architecture and implementation
- Vector embeddings and semantic search
- Chunking strategies for different data types
- Debugging AI applications
- Production deployment practices

### Advanced Concepts
- Table extraction from PDFs
- Hybrid search strategies
- System prompt optimization
- Professional UI/UX patterns
- Portfolio-ready development

---

## 🛠️ Two Versions Available

### Cloud Version (Recommended for Workshops)
- **Uses:** Claude Haiku 4.5 API
- **Runs on:** Replit (no installation)
- **Cost:** ~$0.25-$1.25 per workshop with free credits
- **Best for:** Getting started quickly, workshops, demos

**Files:** `*_replit.py`, `requirements_replit_haiku.txt`

### Local Version (Free Forever)
- **Uses:** Ollama (local AI models)
- **Runs on:** Your computer
- **Cost:** Free (after initial setup)
- **Best for:** Personal projects, ongoing learning

**Files:** `*.py` (without `_replit`), `requirements.txt`

**Both versions teach the same RAG concepts!**

---

## 📖 Documentation

Comprehensive guides included:

- **[REPLIT_HAIKU_SETUP.md](./REPLIT_HAIKU_SETUP.md)** - Complete cloud setup guide
- **[TABLE_HANDLING_GUIDE.md](./TABLE_HANDLING_GUIDE.md)** - Why tables break RAG and how to fix it
- **[CUSTOMIZATION_GUIDE.md](./CUSTOMIZATION_GUIDE.md)** - Transform generic to branded
- **[PRESENTATION_IMPROVEMENTS_GUIDE.md](./PRESENTATION_IMPROVEMENTS_GUIDE.md)** - Teaching tips

---

## 🚦 Quick Start (For Self-Learners)

Want to try this on your own? Here's the fastest path:

### Option 1: Cloud Version (5 minutes)

1. **Get API key:** https://console.anthropic.com ($5 free credit)
2. **Download slides:** Click "AI_Chatbot_Workshop_Feb2026.pptx" above
3. **Follow slides:** Each has a Replit link - fork it and run!
4. **Build along:** Upload docs, ask questions, customize

### Option 2: Local Version (30 minutes)

1. **Install Ollama:** https://ollama.com/download
2. **Download model:** `ollama pull llama3.2`
3. **Clone this repo:** `git clone [repo-url]`
4. **Install packages:** `pip install -r requirements.txt`
5. **Run chatbot:** `streamlit run chatbot_workshop.py`

---

## 🤝 Contributing

This is educational material from AI literacy workshops. If you:
- Find bugs or improvements
- Have suggestions for better explanations
- Want to add features or examples
- Have questions about the code

**Please open an issue or pull request!**

---

## 🎯 Who This Is For

✅ **Complete beginners** - No AI experience needed  
✅ **Career changers** - Build a portfolio project  
✅ **Business professionals** - Understand what's possible  
✅ **Students** - Hands-on AI engineering  
✅ **Developers** - Learn RAG and vector search  
✅ **Educators** - Use these materials for teaching  

---

## 🌟 Workshop Outcomes

Attendees leave with:
- Working chatbot deployed and shareable
- Source code on GitHub
- Understanding of RAG, embeddings, vector search
- Skills to build more AI applications
- Portfolio-ready project
- Confidence to explore further

This isn't prompt tips - this is **real AI engineering** made accessible.

---

## 📧 Contact & Support

**Workshop Instructor:** Gus Cavanaugh

- 💼 **LinkedIn:** [linkedin.com/in/gustafrcavanaugh](https://www.linkedin.com/in/gustafrcavanaugh/)
- 📧 **Email:** Contact for workshop details and scheduling
- 🎓 **Workshop Series:** Winston-Salem AI Literacy

### Want to Run This Workshop?

I conduct this workshop for:
- Companies (team training)
- Meetups and conferences
- Universities and bootcamps
- Community organizations

**Contact me for:**
- Scheduling a workshop
- Customizing content for your audience
- Licensing materials for your own use
- Questions about the curriculum

---

## 📜 License

**MIT License** - Use freely for learning and teaching!

The code and materials are open-source. Feel free to:
- Use in your own workshops
- Modify for your needs
- Share with others
- Build upon for projects

**Attribution appreciated but not required.**

---

## 🙏 Acknowledgments

Built with:
- [Anthropic Claude](https://www.anthropic.com) - AI models
- [Streamlit](https://streamlit.io) - Web framework
- [ChromaDB](https://www.trychroma.com) - Vector database
- [Replit](https://replit.com) - Cloud platform
- [Ollama](https://ollama.com) - Local AI models

Special thanks to the Winston-Salem AI literacy community for feedback and support.

---

## ⭐ Support This Project

If you found this workshop helpful:
- ⭐ **Star this repository**
- 🔗 **Share with others learning AI**
- 💬 **Tell us about your chatbot!**
- 📢 **Spread the word about hands-on AI education**

---

<div align="center">

**Ready to build your first AI chatbot?**

📊 [Download the Slides](./AI_Chatbot_Workshop_Feb2026.pptx) • 💻 [Start Coding](#quick-start-for-self-learners) • 📧 [Contact Me](#contact--support)

---

*"Stop writing prompts. Start writing code."*

**Let's build together! 🚀**

</div>
