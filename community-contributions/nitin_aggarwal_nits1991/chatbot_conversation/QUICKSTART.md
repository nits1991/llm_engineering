# 🚀 Quick Start Guide

Get your multi-model chatbot conversation running in 3 minutes!

## ⚡ Super Quick Start (For Experienced Users)

```bash
# 1. Make sure Ollama is running
ollama serve

# 2. Navigate to directory
cd chatbot_conversation

# 3. Install and run
pip install -r requirements.txt
streamlit run app.py
```

Done! The app opens at `http://localhost:8501`

## 📋 Step-by-Step Guide (For Everyone)

### Step 1: Check Ollama (30 seconds)

**Is Ollama running?**

```bash
curl http://localhost:11434/api/tags
```

✅ **If you see JSON output** → Ollama is running, proceed to Step 2

❌ **If you get an error** → Start Ollama:

**macOS:**

```bash
open /Applications/Ollama.app
# Or in terminal:
ollama serve
```

**Linux/Windows:**

```bash
ollama serve
```

### Step 2: Check Models (30 seconds)

**Do you have models downloaded?**

```bash
ollama list
```

✅ **If you see 2+ models** → Great! Proceed to Step 3

❌ **If you see 0-1 models** → Download more:

```bash
# Quick downloads (recommended)
ollama pull llama3.2    # ~2GB, 2 minutes
ollama pull mistral     # ~4GB, 4 minutes
```

### Step 3: Install App (1 minute)

```bash
# Navigate to app directory
cd /Users/nitin.aggarwal/Documents/llm_learning_2025_bootcamp/llm_engineering/community-contributions/nitin_aggarwal_nits1991/chatbot_conversation

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Run App (30 seconds)

```bash
streamlit run app.py
```

Your browser should automatically open to `http://localhost:8501`

If not, manually go to: `http://localhost:8501`

### Step 5: Create Your First Conversation (1 minute)

1. **Leave default settings** (or customize if you want)
2. **Click** "🚀 Start Conversation"
3. **Click** "➡️ Generate Turn" to advance
4. **Watch** the chatbots discuss!
5. **Click** "📥 Download as Markdown" when done

## 🎯 Your First Conversation

Here's a fun starting configuration:

**Configuration:**

- Number of Chatbots: `3`
- Topic: `"Why did the chicken cross the road?"`
- Turns: `5`

**Chatbots:**

1. **Bot 1**: llama3.2 - Optimist
2. **Bot 2**: mistral - Skeptic
3. **Bot 3**: llama3.2 - Philosopher

**What to expect:**

- Optimist will find deep meaning
- Skeptic will question everything
- Philosopher will explore all angles
- Hilarious and insightful discussion!

## ✅ Verification Checklist

Before asking for help, check:

- [ ] Ollama is running (`ps aux | grep ollama`)
- [ ] At least 2 models downloaded (`ollama list`)
- [ ] Dependencies installed (`pip list | grep streamlit`)
- [ ] Port 8501 is available
- [ ] No errors in terminal

## ❌ Quick Fixes

### "Ollama is not running"

```bash
ollama serve
```

### "No models found"

```bash
ollama pull llama3.2
ollama pull mistral
```

### "Port already in use"

```bash
streamlit run app.py --server.port=8502
```

### "Module not found"

```bash
pip install -r requirements.txt
```

## 💡 Pro Tips

1. **Start Small**: Begin with 2-3 chatbots, 3-5 turns
2. **Mix Personas**: Different personas = more interesting conversations
3. **Use Fast Models**: llama3.2 and phi3 are quick
4. **Save Everything**: Download conversations you like
5. **Experiment**: Try different topics and personas!

## 🎭 Persona Recommendations

**For Philosophy**: Philosopher + Skeptic + Scientist
**For Comedy**: Comedian + Pragmatist + Poet
**For Tech**: Futurist + Scientist + Historian
**For Balance**: Optimist + Skeptic + Philosopher

## 📊 Expected Performance

**With llama3.2 models:**

- Turn generation: 3-10 seconds
- Total conversation (5 turns): ~1-2 minutes

**With larger models:**

- Turn generation: 10-30 seconds
- Total conversation (5 turns): ~3-5 minutes

## 🎉 You're Ready!

If everything is working, you should see:

- ✅ Green "Ollama is running" message
- ✅ List of available models
- ✅ Sidebar configuration options
- ✅ Welcome message in main area

**Now start creating amazing conversations!** 🚀

## 🆘 Still Having Issues?

1. **Check Terminal**: Look for error messages
2. **Restart Ollama**: Kill and restart the service
3. **Check RAM**: Close other applications
4. **Try Smaller Models**: Use llama3.2:1b
5. **Read Full README**: More detailed troubleshooting

## 📚 Next Steps

Once you're comfortable:

1. Try all 10 personas
2. Experiment with different topics
3. Mix different models
4. Adjust conversation length
5. Share interesting conversations!

---

**Estimated Total Time: 3-5 minutes** ⏱️

**Happy Chatting!** 🤖💬
