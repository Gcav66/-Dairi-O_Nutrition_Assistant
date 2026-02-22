# Replit Setup Guide - Claude Haiku 4.5 Version

## 🎯 Quick Overview

These Replit versions use **Claude Haiku 4.5** instead of Ollama, making them perfect for cloud workshops. Haiku is:
- ⚡ **Fast** - Near-instant responses
- 💰 **Cheap** - ~$0.80 per million input tokens, ~$4 per million output tokens
- 🌐 **Cloud-native** - Works on any platform
- 🎓 **Perfect for workshops** - No local installation needed


### Step 1: Create Your Repl

1. Go to https://replit.com
2. Click "Create Repl"
3. Choose "Python" template
4. Name it: "AI Chatbot Workshop" or "Dairi-O Nutrition Assistant"

### Step 2: Upload Files

**For Workshop Version:**
- Upload `chatbot_workshop_replit.py` → Rename to `main.py`
- Upload `requirements_replit_haiku.txt` → Rename to `requirements.txt`

**For Dairi-O Version:**
- Upload `dairi_o_chatbot_replit.py` → Rename to `main.py`
- Upload `requirements_replit_haiku.txt` → Rename to `requirements.txt`

### Step 3: Get Anthropic API Key

1. Go to https://console.anthropic.com
2. Sign up (it's free!)
3. Click "Get API Keys"
4. Create a new key
5. Copy it (you won't see it again!)

**Free Credits:**
- New accounts get $5 free credit
- That's ~6,250 workshop conversations with Haiku!
- More than enough for testing and workshops

### Step 4: Add API Key to Replit Secrets

1. In Replit, look for the **lock icon (🔒)** in the left sidebar
2. Click "Secrets"
3. Click "New Secret"
4. **Key:** `ANTHROPIC_API_KEY`
5. **Value:** (paste your API key)
6. Click "Add Secret"

### Step 5: Configure & Run

1. Click the three dots (⋮) next to "Run"
2. Select "Configure the Run button"
3. Set run command to: `streamlit run main.py`
4. Click "Done"
5. Click "Run"! 🎉

Your chatbot should now be running!


## 🔧 Testing Your Repl


```bash
# 1. Click Run - should show Streamlit interface
# 2. Upload a test PDF
# 3. Click "Process Documents"
# 4. Ask a question: "What's in this document?"
# 5. Verify you get a response

If everything works, you're ready! ✅
```

Use your own API key (recommended for continued learning)
1. Create free Anthropic account: https://console.anthropic.com
2. Get API key (you get $5 free credit!)
3. Fork the Repl: [YOUR REPL FORK LINK]
4. Add your API key to Secrets (lock icon 🔒)
5. Click "Run"


## 🐛 Common Issues & Solutions

### "API Key Error"
**Problem:** ANTHROPIC_API_KEY not set
**Solution:**
1. Check Secrets (lock icon)
2. Make sure key name is exactly: `ANTHROPIC_API_KEY`
3. Make sure you pasted the full key
4. Click "Run" again

### "Rate Limit Error"
**Problem:** Too many requests from shared key
**Solution:**
- Wait 60 seconds and try again
- Or have attendees use their own API keys

### "Module Not Found"
**Problem:** Dependencies not installed
**Solution:**
1. Check requirements.txt is present
2. Click "Shell" tab
3. Run: `pip install -r requirements.txt`
4. Click "Run" again

### "Chatbot Won't Load"
**Problem:** Port or Streamlit issue
**Solution:**
1. Stop the Repl (Stop button)
2. Hard refresh browser (Cmd+Shift+R or Ctrl+Shift+R)
3. Click "Run" again

### "Can't Upload PDF"
**Problem:** File uploader not working
**Solution:**
- Refresh the page
- Try a smaller PDF (<5MB)
- Check PDF isn't password-protected


## 🎨 Customization Tips

**Want to use a different model?**

Change this line in the code:
```python
model="claude-haiku-4-5-20251001",  # Current
```

To:
```python
model="claude-sonnet-4-5-20250929",  # More powerful, ~5x more expensive
```

**Note:** Haiku is perfect for this workshop - fast and cheap!

## 🆚 Haiku vs. Ollama Comparison

Help attendees understand the trade-offs:

| Feature | Claude Haiku (Replit) | Ollama (Local) |
|---------|----------------------|----------------|
| **Speed** | ~1 second | ~3-5 seconds |
| **Setup** | 30 seconds | 30+ minutes |
| **Cost** | ~$1/workshop | Free forever |
| **Where runs** | Cloud | Your computer |
| **Workshop friendly** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Long-term use** | Costs money | Completely free |
| **Installation** | None | Complex |

**Teaching point:** 
"Haiku is perfect for workshops because it's instant. But Ollama is great for personal projects because it's free forever. Same RAG concepts, different infrastructure!"

## 📚 Additional Resources

**For Attendees:**
- Anthropic docs: https://docs.anthropic.com
- Claude API pricing: https://www.anthropic.com/pricing
- Replit docs: https://docs.replit.com
- Your GitHub repo: [YOUR LINK]

**For Instructors:**
- Monitor usage: https://console.anthropic.com/settings/usage
- API status: https://status.anthropic.com
- Replit status: https://status.replit.com

## ✅ Pre-Workshop Checklist

Workshop morning:
- [ ] Open master Repl
- [ ] Verify it still runs
- [ ] Have fork link copied
- [ ] API usage dashboard open
- [ ] Ready to screen share

## 🎉 Success Metrics

It's working when:
- ✅ 80%+ of attendees see chatbot in first 5 minutes
- ✅ People can upload PDFs and get answers
- ✅ Quick questions work from sidebar
- ✅ Total workshop cost < $2
- ✅ Attendees can fork and keep their own version

**Most important:** Attendees leave with working code they can customize!

## 🚀 Next Steps

After your workshop:
1. Share the local Ollama version for free long-term use
2. Encourage customization (colors, prompts, features)
3. Provide this guide for self-hosting
4. Collect feedback for next workshop

---

**Questions?** Check:
- Replit docs: https://docs.replit.com
- Anthropic docs: https://docs.anthropic.com
- Workshop GitHub: [YOUR REPO]

**Happy teaching! 🎓**
