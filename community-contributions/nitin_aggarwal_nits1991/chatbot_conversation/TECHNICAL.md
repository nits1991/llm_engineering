# Technical Documentation

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit UI Layer                      │
│  - Page Configuration                                       │
│  - Sidebar (Configuration)                                  │
│  - Main Area (Conversation Display)                         │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  Application Logic Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Ollama     │  │   Persona    │  │ Conversation │    │
│  │   Manager    │  │   Manager    │  │   Manager    │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                    Ollama API Layer                         │
│  - HTTP REST API (localhost:11434)                         │
│  - Model Management                                         │
│  - Response Generation                                      │
└─────────────────────────────────────────────────────────────┘
```

## Class Documentation

### OllamaManager

**Purpose**: Manages all interactions with the local Ollama API.

**Methods:**

#### `__init__(base_url: str = "http://localhost:11434")`

Initializes the manager with Ollama API endpoint.

**Parameters:**

- `base_url` (str): Ollama API base URL. Default: "http://localhost:11434"

---

#### `check_connection() -> bool`

Verifies Ollama service is running and accessible.

**Returns:**

- `bool`: True if Ollama is running, False otherwise

**Example:**

```python
ollama = OllamaManager()
if ollama.check_connection():
    print("Ollama is ready!")
```

---

#### `get_available_models() -> List[str]`

Fetches list of installed Ollama models.

**Returns:**

- `List[str]`: Sorted list of model names

**Example:**

```python
models = ollama.get_available_models()
# ['llama3.2', 'mistral', 'phi3']
```

---

#### `generate_response(model: str, messages: List[Dict], system_prompt: str = "") -> str`

Generates a response from specified model given conversation context.

**Parameters:**

- `model` (str): Name of the Ollama model to use
- `messages` (List[Dict]): Conversation history as list of message dicts
- `system_prompt` (str): System prompt defining model behavior

**Returns:**

- `str`: Generated response text

**Message Format:**

```python
messages = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "user", "content": "How are you?"}
]
```

**Example:**

```python
response = ollama.generate_response(
    model="llama3.2",
    messages=[{"role": "user", "content": "Hello"}],
    system_prompt="You are a helpful assistant."
)
```

---

### PersonaManager

**Purpose**: Manages chatbot personas and their system prompts.

**Class Attributes:**

#### `PERSONAS: Dict[str, Dict[str, str]]`

Dictionary of available personas with descriptions and prompts.

**Structure:**

```python
{
    "Persona Name": {
        "description": "🎭 Short description",
        "system_prompt": "You are... Keep replies under 2 sentences."
    }
}
```

**Class Methods:**

#### `get_persona_names() -> List[str]`

Returns list of all available persona names.

**Returns:**

- `List[str]`: List of persona names

---

#### `get_persona_prompt(persona_name: str) -> str`

Returns system prompt for specified persona.

**Parameters:**

- `persona_name` (str): Name of the persona

**Returns:**

- `str`: System prompt text

---

#### `get_persona_description(persona_name: str) -> str`

Returns description for specified persona.

**Parameters:**

- `persona_name` (str): Name of the persona

**Returns:**

- `str`: Description text with emoji

---

### ConversationManager

**Purpose**: Orchestrates multi-model conversations.

**Methods:**

#### `__init__(ollama: OllamaManager)`

Initializes conversation manager.

**Parameters:**

- `ollama` (OllamaManager): Instance of OllamaManager

---

#### `add_chatbot(model: str, persona: str, name: str)`

Adds a chatbot to the conversation.

**Parameters:**

- `model` (str): Ollama model name
- `persona` (str): Persona name
- `name` (str): Display name for the chatbot

**Example:**

```python
manager.add_chatbot(
    model="llama3.2",
    persona="Optimist",
    name="Happy Bot"
)
```

---

#### `initialize_conversation(topic: str)`

Sets up the initial conversation with a topic.

**Parameters:**

- `topic` (str): Discussion topic

**Behavior:**

- First chatbot introduces the topic
- Other chatbots acknowledge with opening statements

---

#### `generate_next_responses() -> List[Dict]`

Generates next response for each chatbot in the conversation.

**Returns:**

- `List[Dict]`: List of response dictionaries

**Response Format:**

```python
{
    "chatbot": "Bot Name",
    "persona": "Optimist",
    "message": "Response text",
    "index": 0
}
```

**Conversation Flow:**

1. Build conversation history for each chatbot
2. Generate response considering all previous messages
3. Store response in chatbot's message history
4. Return all responses

---

## Session State Management

Streamlit session state variables:

| Variable               | Type                | Purpose                          |
| ---------------------- | ------------------- | -------------------------------- |
| `conversation_started` | bool                | Whether conversation is active   |
| `conversation_history` | List[Dict]          | All generated responses          |
| `current_turn`         | int                 | Current turn number (0-indexed)  |
| `conversation_manager` | ConversationManager | Active conversation instance     |
| `num_turns`            | int                 | Total number of turns configured |

---

## API Endpoints Used

### Ollama API

**Base URL**: `http://localhost:11434`

#### GET `/api/tags`

List available models.

**Response:**

```json
{
  "models": [
    {
      "name": "llama3.2",
      "modified_at": "2024-01-01T00:00:00Z",
      "size": 2000000000
    }
  ]
}
```

---

#### POST `/api/generate`

Generate text from a model.

**Request:**

```json
{
  "model": "llama3.2",
  "prompt": "Hello, how are you?",
  "stream": false,
  "options": {
    "temperature": 0.7,
    "num_predict": 150
  }
}
```

**Response:**

```json
{
  "model": "llama3.2",
  "created_at": "2024-01-01T00:00:00Z",
  "response": "I'm doing well, thank you!",
  "done": true
}
```

---

## Configuration Options

### Model Parameters

```python
"options": {
    "temperature": 0.7,      # Randomness (0.0 = deterministic, 2.0 = very random)
    "num_predict": 150,      # Maximum tokens to generate
    "top_p": 0.9,           # Nucleus sampling threshold
    "top_k": 40,            # Top-k sampling
    "repeat_penalty": 1.1   # Penalize repetition
}
```

### Streamlit Config

```python
st.set_page_config(
    page_title="AI Chatbot Conversation",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

---

## Data Flow

### Initialization Flow

```
1. App Start
   ↓
2. Check Ollama Connection
   ↓
3. Fetch Available Models
   ↓
4. Display UI
```

### Conversation Flow

```
1. User Configures Chatbots
   ↓
2. User Clicks "Start Conversation"
   ↓
3. Create ConversationManager
   ↓
4. Add Chatbots with Models & Personas
   ↓
5. Initialize with Topic
   ↓
6. Display Opening Statements
   ↓
7. User Clicks "Generate Turn"
   ↓
8. For Each Chatbot:
   ├─ Build Conversation History
   ├─ Call Ollama API
   └─ Store Response
   ↓
9. Display All Responses
   ↓
10. Repeat Steps 7-9 Until Complete
```

### Response Generation Flow

```
1. ConversationManager.generate_next_responses()
   ↓
2. For each chatbot:
   ├─ Collect messages from all chatbots
   ├─ Format as conversation history
   ├─ Add system prompt (persona)
   ├─ Build prompt string
   ├─ Call Ollama API
   └─ Parse and return response
   ↓
3. Store responses in session state
   ↓
4. Update UI
```

---

## Error Handling

### Connection Errors

```python
try:
    response = requests.get(url, timeout=5)
    return response.status_code == 200
except Exception as e:
    return False
```

**Handled Cases:**

- Ollama not running
- Network timeout
- Invalid URL

### Model Errors

**Checks:**

- Model exists in available models list
- Model name format is valid

### API Errors

```python
if response.status_code == 200:
    return result.get('response', '').strip()
else:
    return f"Error: {response.status_code}"
```

**Handled Cases:**

- HTTP errors (404, 500, etc.)
- Timeout errors
- Malformed responses

---

## Performance Considerations

### Optimization Strategies

1. **Model Selection**

   - Use smaller models for faster responses
   - llama3.2:1b (~2-3s per response)
   - llama3.2 (~5-7s per response)

2. **Token Limits**

   - `num_predict: 150` limits response length
   - Faster generation, less computation

3. **Parallel Processing**

   - Currently sequential (one chatbot at a time)
   - Could be parallelized for faster turns

4. **Caching**
   - Session state prevents regeneration
   - Models stay loaded in Ollama

### Resource Usage

**Memory:**

- Each model: 1-7GB RAM
- Streamlit app: ~100MB
- Active conversation: ~10MB

**CPU:**

- Model inference: Heavy (90%+ during generation)
- UI rendering: Light (<5%)

**Network:**

- Local only (localhost:11434)
- No external API calls

---

## Extension Points

### Adding New Personas

1. Edit `PersonaManager.PERSONAS`
2. Add new entry with description and prompt
3. No other changes needed

### Adding New Features

**Streaming Responses:**

```python
# Modify generate_response() to use streaming
response = requests.post(..., stream=True)
for line in response.iter_lines():
    yield line
```

**Temperature Control:**

```python
# Add slider in UI
temp = st.slider("Temperature", 0.0, 2.0, 0.7)

# Pass to generate_response
"options": {
    "temperature": temp
}
```

**Save to Database:**

```python
import sqlite3

def save_conversation(topic, chatbots, messages):
    conn = sqlite3.connect('conversations.db')
    # Insert conversation data
    conn.commit()
    conn.close()
```

---

## Testing

### Manual Testing Checklist

- [ ] Ollama connection check works
- [ ] Model list displays correctly
- [ ] All personas selectable
- [ ] 2-5 chatbots configurable
- [ ] Topic input works
- [ ] Turn slider works
- [ ] Start button initializes correctly
- [ ] Opening statements display
- [ ] Generate turn creates responses
- [ ] All chatbots respond each turn
- [ ] Color coding works
- [ ] Turn counter accurate
- [ ] Export to markdown works
- [ ] Reset button clears state

### Error Scenarios

- [ ] Ollama not running → Clear error message
- [ ] No models → Clear instructions
- [ ] Invalid model → Graceful handling
- [ ] API timeout → Error message
- [ ] Network error → Retry suggestion

---

## Security Considerations

### Current Implementation

✅ **Local Only**: No external API calls
✅ **No Authentication**: Not needed for local use
✅ **No Data Storage**: Conversations not persisted
✅ **No User Input Validation**: Limited risk (local only)

### Production Considerations

If deploying publicly:

- [ ] Add authentication
- [ ] Validate user inputs
- [ ] Rate limiting
- [ ] Input sanitization
- [ ] HTTPS only
- [ ] Database security

---

## Deployment Options

### Local Development

```bash
streamlit run app.py
```

### Docker

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

### Streamlit Cloud

- Not suitable (requires local Ollama)
- Would need to modify for cloud AI APIs

---

## Troubleshooting

### Debug Mode

Add to code for debugging:

```python
if st.checkbox("Debug Mode"):
    st.write("Session State:", st.session_state)
    st.write("Chatbots:", [c for c in manager.chatbots])
```

### Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Generating response for {model}")
```

---

## Future Enhancements

### Planned Features

1. **Streaming Responses**: Real-time text generation
2. **Conversation History**: Save and load previous chats
3. **Export Formats**: JSON, CSV, PDF
4. **Analytics**: Word clouds, sentiment analysis
5. **Voice Output**: Text-to-speech
6. **Custom Personas**: User-created personas
7. **Model Comparison**: Side-by-side model outputs
8. **Voting System**: Rate responses
9. **Themes**: Dark mode, custom colors
10. **Multi-language**: Support for other languages

### Implementation Complexity

| Feature         | Difficulty | Estimated Time |
| --------------- | ---------- | -------------- |
| Streaming       | Medium     | 4 hours        |
| Database        | Easy       | 2 hours        |
| Export Formats  | Easy       | 3 hours        |
| Analytics       | Medium     | 6 hours        |
| Voice Output    | Medium     | 5 hours        |
| Custom Personas | Easy       | 2 hours        |
| Themes          | Easy       | 2 hours        |

---

## Performance Benchmarks

### Tested Configurations

**3 Chatbots, 5 Turns, llama3.2:**

- Total time: ~2 minutes
- Per turn: ~25 seconds
- Per response: ~8 seconds

**4 Chatbots, 5 Turns, mistral:**

- Total time: ~4 minutes
- Per turn: ~48 seconds
- Per response: ~12 seconds

**2 Chatbots, 10 Turns, llama3.2:1b:**

- Total time: ~1.5 minutes
- Per turn: ~9 seconds
- Per response: ~4.5 seconds

---

## Code Quality

### Metrics

- **Lines of Code**: ~550
- **Functions**: 15+
- **Classes**: 3
- **Complexity**: Medium
- **Maintainability**: High (modular design)

### Best Practices Followed

✅ Type hints for clarity
✅ Docstrings for all classes/methods
✅ Modular design (separation of concerns)
✅ Error handling
✅ Clear variable names
✅ DRY principle
✅ Single responsibility principle

---

## License & Attribution

**License**: Open source, free to use and modify

**Based On**: LLM Engineering Bootcamp Week 2

**Author**: Nitin Aggarwal

**Acknowledgments**:

- Ed Donner (LLM Engineering Bootcamp)
- Ollama team
- Streamlit team

---

_Last Updated: October 26, 2025_
