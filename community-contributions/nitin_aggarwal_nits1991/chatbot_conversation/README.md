# 🤖 Multi-Model Chatbot Conversation

An engaging Streamlit application that creates conversations between multiple AI models with different personas using local Ollama models.

## 🌟 Features

### Core Capabilities

- **Multiple AI Models**: Run conversations with 2-5 AI models simultaneously
- **10 Unique Personas**: Choose from Optimist, Skeptic, Philosopher, Scientist, Artist, Comedian, Historian, Futurist, Pragmatist, and Poet
- **Customizable Topics**: Discuss any topic you want - from philosophy to humor
- **Adjustable Conversation Length**: Control how many turns the conversation should last (1-10 turns)
- **🏆 Judge Mode**: Have an AI judge evaluate the conversation and declare a winner!
- **📊 JSON Export**: Download conversations in structured JSON format with metadata, model info, and comments
- **📥 Markdown Export**: Download conversations as formatted Markdown files
- **Local-Only**: Uses only local Ollama models - no external API calls required
- **Beautiful UI**: Color-coded messages for each chatbot with smooth animations

### Why This App?

- 🎯 **Educational**: Learn how different AI models respond to the same prompts
- 🎨 **Creative**: Generate unique content by mixing different personas
- 🏆 **Competitive**: Let an AI judge evaluate and crown a winner
- 🔒 **Private**: Everything runs locally - your conversations stay on your machine
- 💰 **Free**: No API costs - uses only local Ollama models
- 🚀 **Fast**: Direct connection to local models for quick responses
- 📊 **Exportable**: Save conversations in multiple formats for later analysis

## 📋 Prerequisites

### Required

- Python 3.8 or higher
- Ollama installed and running
- At least 2 Ollama models downloaded

### Installing Ollama

**macOS:**

```bash
brew install ollama
ollama serve
```

**Linux:**

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
```

**Windows:**
Download from [ollama.com](https://ollama.com)

### Downloading Models

Download at least 2 models (more is better!):

```bash
# Recommended models
ollama pull llama3.2      # Fast, good quality
ollama pull mistral       # Very capable
ollama pull phi3          # Small and fast
ollama pull gemma2        # Google's model
ollama pull qwen2         # Multilingual

# More models
ollama pull llama3.2:1b   # Tiny, very fast
ollama pull codellama     # Code-focused
ollama pull neural-chat   # Conversation-focused
```

Check what models you have:

```bash
ollama list
```

## 🚀 Installation

### Step 1: Navigate to the App Directory

```bash
cd /Users/nitin.aggarwal/Documents/llm_learning_2025_bootcamp/llm_engineering/community-contributions/nitin_aggarwal_nits1991/chatbot_conversation
```

### Step 2: Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Ollama is Running

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 🎯 How to Use

### Quick Start Guide

1. **Start Ollama** (if not already running)

   ```bash
   ollama serve
   ```

2. **Launch the App**

   ```bash
   streamlit run app.py
   ```

3. **Configure Your Conversation**

   - Select number of chatbots (2-5)
   - Choose a model for each chatbot
   - Assign a persona to each chatbot
   - Enter your discussion topic
   - Set the number of conversation turns

4. **Start the Conversation**

   - Click "🚀 Start Conversation"
   - Watch as the chatbots introduce themselves
   - Click "➡️ Generate Turn" to advance the conversation
   - Continue until all turns are complete

5. **Export Your Conversation**
   - Click "📥 Download as Markdown" to save the conversation
   - Click "📊 Download as JSON" for structured data export

### 🏆 Judge Mode Feature

The application includes an optional **Judge Mode** that adds a competitive element to conversations:

**How it works:**

1. Enable "Judge" in the sidebar configuration
2. Select a judge model (can be any available Ollama model)
3. After the conversation completes, the judge analyzes all responses
4. The judge evaluates based on:
   - Coherence and relevance to the topic
   - Depth of insights and arguments
   - Creativity and originality
   - Engagement and persuasiveness
   - Consistency with assigned persona
5. The judge declares a winner with detailed reasoning

**Judge's Verdict includes:**

- 🏆 Winner announcement
- 📝 Detailed reasoning for the decision
- ✨ Highlights from each participant
- 📊 Analysis of conversation quality

**Tips for Judge Mode:**

- Use a different model for the judge than the participants
- Try larger models (like llama3.2) for more nuanced judging
- Enable judge mode for debates and competitive topics
- The judge's verdict is included in exports

### 📊 Export Formats

The application supports two export formats:

#### 1. Markdown Export (.md)

Perfect for reading and sharing:

- Human-readable format
- Includes topic and participants
- Shows all conversation turns
- Includes judge verdict (if enabled)
- Easy to read and share

#### 2. JSON Export (.json)

Perfect for analysis and processing:

- Structured data format
- Includes metadata (timestamp, turn count, etc.)
- Full participant information (models, personas, descriptions)
- Conversation organized by turns
- Judge verdict with full analysis
- Comments explaining each section
- Machine-readable for further processing

**Example JSON Structure:**

```json
{
  "_comment": "Multi-Model Chatbot Conversation",
  "metadata": {
    "topic": "Discussion topic",
    "timestamp": "2025-10-27T10:30:45",
    "total_turns": 5,
    "total_messages": 15,
    "number_of_participants": 3
  },
  "participants": [...],
  "conversation": {
    "opening_statements": [...],
    "turns": [...]
  },
  "judge_verdict": {
    "judge_model": "llama3.2",
    "winner": "Bot Name",
    "full_verdict": "...",
    "timestamp": "..."
  }
}
```

See `examples/example_export.json` for a complete example.

### Example Configurations

#### Configuration 1: Philosophy Debate

- **Topic**: "What is the meaning of happiness?"
- **Chatbots**:
  - Bot 1: llama3.2 - Philosopher
  - Bot 2: mistral - Skeptic
  - Bot 3: phi3 - Optimist
- **Turns**: 5

#### Configuration 2: Comedy Show

- **Topic**: "Why did the chicken cross the road?"
- **Chatbots**:
  - Bot 1: llama3.2 - Comedian
  - Bot 2: mistral - Pragmatist
  - Bot 3: phi3 - Poet
- **Turns**: 5

#### Configuration 3: Tech Discussion

- **Topic**: "Is technology making us more connected or isolated?"
- **Chatbots**:
  - Bot 1: llama3.2 - Futurist
  - Bot 2: mistral - Scientist
  - Bot 3: phi3 - Historian
  - Bot 4: gemma2 - Philosopher
- **Turns**: 7

## 🎭 Available Personas

| Persona            | Description                        | Best For                |
| ------------------ | ---------------------------------- | ----------------------- |
| 🌟 **Optimist**    | Sees the bright side of everything | Uplifting conversations |
| 🤔 **Skeptic**     | Questions everything with wit      | Critical analysis       |
| 🧠 **Philosopher** | Explores deep meanings             | Existential topics      |
| 🔬 **Scientist**   | Analyzes with logic                | Technical discussions   |
| 🎨 **Artist**      | Sees beauty everywhere             | Creative topics         |
| 😄 **Comedian**    | Finds humor in everything          | Light-hearted fun       |
| 📚 **Historian**   | Connects to the past               | Historical context      |
| 🚀 **Futurist**    | Thinks about tomorrow              | Technology, innovation  |
| ⚙️ **Pragmatist**  | Focuses on practical solutions     | Problem-solving         |
| ✍️ **Poet**        | Speaks in metaphors                | Artistic expression     |

## 💡 Interesting Topics to Try

### Philosophical

- What is consciousness?
- Is free will real?
- What makes something art?
- Can machines think?
- What is the purpose of life?

### Scientific

- Is time travel possible?
- Should we colonize Mars?
- Can AI be creative?
- What is the nature of reality?

### Social

- Is technology good or bad?
- What makes a good leader?
- Should robots have rights?
- Is privacy still possible?

### Fun

- Why did the chicken cross the road?
- What's the best pizza topping?
- Cats vs Dogs
- Is a hotdog a sandwich?

### Deep

- What is happiness?
- How do we measure success?
- What is the meaning of truth?
- Can love be defined?

## 🏗️ Architecture

### Components

```
app.py
├── OllamaManager        # Handles Ollama API interactions
│   ├── check_connection()
│   ├── get_available_models()
│   └── generate_response()
│
├── PersonaManager       # Manages chatbot personas
│   ├── PERSONAS (10 personas)
│   ├── get_persona_names()
│   ├── get_persona_prompt()
│   └── get_persona_description()
│
└── ConversationManager  # Orchestrates the conversation
    ├── add_chatbot()
    ├── initialize_conversation()
    └── generate_next_responses()
```

### Data Flow

1. **Initialization**

   - Check Ollama connection
   - Fetch available models
   - Display UI

2. **Configuration**

   - User selects models and personas
   - User enters topic and settings
   - Create conversation manager

3. **Conversation**

   - Initialize with opening statements
   - Generate responses turn by turn
   - Display with color coding
   - Track conversation history

4. **Export**
   - Format as Markdown
   - Download to file

## 🔧 Customization

### Adding New Personas

Edit `app.py` and add to the `PersonaManager.PERSONAS` dictionary:

```python
"Your Persona": {
    "description": "🎯 Your description here",
    "system_prompt": "You are... Keep replies under 2 sentences."
}
```

### Adjusting Response Length

In `OllamaManager.generate_response()`, modify:

```python
"options": {
    "temperature": 0.7,      # Creativity (0.0-2.0)
    "num_predict": 150       # Max tokens (adjust as needed)
}
```

### Changing UI Colors

Modify the CSS in the `st.markdown()` section:

```python
.chatbot-0 { border-color: #FF6B6B; background-color: #FFE5E5; }
.chatbot-1 { border-color: #4ECDC4; background-color: #E5F9F7; }
# Add more colors...
```

### Adding New Models

Just download them with Ollama:

```bash
ollama pull model-name
```

The app will automatically detect them!

## 🐛 Troubleshooting

### Problem 1: "Ollama is not running"

**Solution:**

```bash
# Start Ollama
ollama serve

# Or on macOS, open the Ollama app
open /Applications/Ollama.app
```

### Problem 2: "No models found"

**Solution:**

```bash
# Download at least 2 models
ollama pull llama3.2
ollama pull mistral

# Verify they're installed
ollama list
```

### Problem 3: Slow responses

**Solutions:**

- Use smaller models (llama3.2:1b, phi3)
- Reduce `num_predict` in the code
- Ensure Ollama has enough RAM
- Close other applications

### Problem 4: Connection timeout

**Solutions:**

- Check if Ollama is actually running: `ps aux | grep ollama`
- Restart Ollama: Kill the process and run `ollama serve`
- Check port 11434 is not blocked
- Try: `curl http://localhost:11434/api/tags`

### Problem 5: Module not found

**Solution:**

```bash
pip install -r requirements.txt
```

### Problem 6: Streamlit won't start

**Solutions:**

```bash
# Try a different port
streamlit run app.py --server.port=8502

# Clear Streamlit cache
streamlit cache clear

# Reinstall Streamlit
pip install --upgrade streamlit
```

## 📊 Performance

### Response Times (approximate)

| Model       | Size  | Speed            | Quality   |
| ----------- | ----- | ---------------- | --------- |
| llama3.2:1b | 1.3GB | ⚡⚡⚡ Very Fast | Good      |
| phi3        | 2.2GB | ⚡⚡⚡ Very Fast | Good      |
| llama3.2    | 2.0GB | ⚡⚡ Fast        | Excellent |
| mistral     | 4.1GB | ⚡⚡ Fast        | Excellent |
| gemma2      | 5.4GB | ⚡ Medium        | Excellent |
| llama3.1    | 4.7GB | ⚡ Medium        | Excellent |

### System Requirements

**Minimum:**

- RAM: 8GB
- Storage: 10GB free
- CPU: Quad-core

**Recommended:**

- RAM: 16GB+
- Storage: 20GB+ free
- CPU: 6+ cores or Apple Silicon

## 🎓 Learning Resources

### Understanding the Code

- **OllamaManager**: Handles API calls to Ollama
- **PersonaManager**: Defines chatbot personalities
- **ConversationManager**: Orchestrates multi-turn conversations
- **Streamlit**: Provides the web interface

### Key Concepts

1. **Personas**: System prompts that define chatbot behavior
2. **Conversation History**: Maintains context across turns
3. **Local Models**: No external API calls needed
4. **Streaming**: Could be added for real-time responses

### Further Exploration

- Try different model combinations
- Experiment with persona prompts
- Add new personas for your use case
- Modify the UI to your liking
- Add features like temperature control

## 🚀 Advanced Features

### Future Enhancements

Some ideas for extending the app:

1. **Streaming Responses**: Show text as it's generated
2. **Voice Output**: Text-to-speech for chatbot responses
3. **Voting System**: Users vote on best responses
4. **Save Conversations**: Database integration
5. **Share Conversations**: Generate shareable links
6. **Custom Personas**: UI for creating personas
7. **Multi-language**: Support for non-English conversations
8. **Analysis**: Sentiment analysis, word clouds
9. **Themes**: Dark mode, custom color schemes
10. **Audio Input**: Voice-to-text for topics

### Implementation Tips

**For Streaming:**

```python
# Modify generate_response to stream
response = requests.post(..., stream=True)
for line in response.iter_lines():
    # Process streaming response
```

**For Saving:**

```python
import sqlite3
# Save conversations to database
```

**For Analysis:**

```python
from wordcloud import WordCloud
# Generate word clouds from conversations
```

## 🤝 Contributing

Feel free to extend this application! Some ideas:

1. Add more personas
2. Improve the UI
3. Add new features
4. Optimize performance
5. Add tests
6. Improve documentation

## 📝 License

This project is part of the LLM Engineering Bootcamp community contributions.
Free to use, modify, and distribute.

## 👤 Author

**Nitin Aggarwal**

- Based on: LLM Engineering Bootcamp Week 2
- Inspired by: Multi-model conversation notebooks

## 🙏 Acknowledgments

- Ed Donner for the LLM Engineering Bootcamp
- Ollama team for the amazing local LLM platform
- Streamlit for the intuitive web framework
- The open-source AI community

## 📧 Support

### Getting Help

1. Check the Troubleshooting section above
2. Verify Ollama is running: `ollama list`
3. Check the Ollama logs: `ollama serve` output
4. Ensure models are downloaded

### Common Questions

**Q: Can I use OpenAI models?**
A: This app is designed for local Ollama models only. For OpenAI integration, you'd need to modify the `OllamaManager` class.

**Q: How much disk space do I need?**
A: Each model is 1-7GB. Plan for at least 10GB free space for multiple models.

**Q: Can I run this on a low-end machine?**
A: Yes! Use smaller models like llama3.2:1b or phi3.

**Q: Can chatbots remember previous conversations?**
A: Currently, no. Each conversation is independent. This could be added as a feature.

**Q: Can I export to formats other than Markdown?**
A: The code can be modified to export to JSON, CSV, or other formats.

## 🎉 Have Fun!

This app is designed to be educational and entertaining. Experiment with different combinations and see what interesting conversations emerge!

**Happy Chatting! 🤖💬**

---

_Last Updated: October 26, 2025_
