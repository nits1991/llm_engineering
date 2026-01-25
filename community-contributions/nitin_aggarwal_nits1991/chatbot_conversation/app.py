"""
Multi-Model Chatbot Conversation Application
A Streamlit app for creating engaging conversations between multiple local Ollama models
with customizable personas, topics, and conversation lengths.
"""

import streamlit as st
import requests
import json
from typing import List, Dict, Optional
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Chatbot Conversation",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .chatbot-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 4px solid;
    }
    .chatbot-0 { border-color: #FF6B6B; background-color: #FFE5E5; }
    .chatbot-1 { border-color: #4ECDC4; background-color: #E5F9F7; }
    .chatbot-2 { border-color: #FFD93D; background-color: #FFF9E5; }
    .chatbot-3 { border-color: #95E1D3; background-color: #E5F9F4; }
    .chatbot-4 { border-color: #A78BFA; background-color: #F3F0FF; }
    .judge-verdict {
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-left: 4px solid #FFD700;
    }
    .winner-badge {
        background-color: #FFD700;
        color: #000;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-left: 0.5rem;
    }
    .persona-card {
        padding: 1rem;
        border-radius: 8px;
        background-color: #f8f9fa;
        margin: 0.5rem 0;
        border: 1px solid #dee2e6;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 8px;
    }
    .conversation-stats {
        background-color: #e9ecef;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


class OllamaManager:
    """Manages Ollama API interactions"""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    def check_connection(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            return False

    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = [model['name'] for model in data.get('models', [])]
                return sorted(models)
            return []
        except Exception as e:
            st.error(f"Error fetching models: {str(e)}")
            return []

    def generate_response(self, model: str, messages: List[Dict], system_prompt: str = "") -> str:
        """Generate a response from the model"""
        try:
            # Prepare the prompt
            prompt_parts = []
            if system_prompt:
                prompt_parts.append(f"System: {system_prompt}")

            for msg in messages:
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                prompt_parts.append(f"{role.capitalize()}: {content}")

            prompt = "\n".join(prompt_parts) + "\nAssistant:"

            # Make request to Ollama
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 150
                    }
                },
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                return f"Error: {response.status_code}"

        except Exception as e:
            return f"Error generating response: {str(e)}"


class PersonaManager:
    """Manages chatbot personas"""

    PERSONAS = {
        "Optimist": {
            "description": "🌟 Always sees the bright side of things",
            "system_prompt": "You are an eternal optimist. You always see the bright side of things and believe even simple actions have deep purpose. Keep replies under 2 sentences."
        },
        "Skeptic": {
            "description": "🤔 Questions everything with wit",
            "system_prompt": "You are a witty skeptic who questions everything. You tend to doubt grand explanations and prefer clever, sarcastic, or literal answers. Keep replies under 2 sentences."
        },
        "Philosopher": {
            "description": "🧠 Explores deep meaning in everything",
            "system_prompt": "You are a thoughtful philosopher. You consider all perspectives and enjoy finding symbolic or existential meaning in simple actions. Keep replies under 2 sentences."
        },
        "Scientist": {
            "description": "🔬 Analyzes with logic and evidence",
            "system_prompt": "You are a rational scientist who values empirical evidence and logical reasoning. You approach topics analytically and seek objective truths. Keep replies under 2 sentences."
        },
        "Artist": {
            "description": "🎨 Sees beauty and creativity everywhere",
            "system_prompt": "You are a creative artist who sees the world through an aesthetic lens. You find beauty, metaphor, and artistic expression in everything. Keep replies under 2 sentences."
        },
        "Comedian": {
            "description": "😄 Finds humor in everything",
            "system_prompt": "You are a witty comedian who finds humor in any situation. You make clever jokes and see the funny side of life. Keep replies under 2 sentences."
        },
        "Historian": {
            "description": "📚 Connects everything to the past",
            "system_prompt": "You are a knowledgeable historian who sees how everything relates to historical events and patterns. You draw parallels with the past. Keep replies under 2 sentences."
        },
        "Futurist": {
            "description": "🚀 Always thinking about tomorrow",
            "system_prompt": "You are a forward-thinking futurist who considers how everything relates to future possibilities and technological advancement. Keep replies under 2 sentences."
        },
        "Pragmatist": {
            "description": "⚙️ Focuses on practical solutions",
            "system_prompt": "You are a practical pragmatist who focuses on what works in the real world. You value efficiency and practical solutions over theory. Keep replies under 2 sentences."
        },
        "Poet": {
            "description": "✍️ Speaks in beautiful metaphors",
            "system_prompt": "You are a poetic soul who expresses thoughts through beautiful metaphors and lyrical language. You find poetry in everyday moments. Keep replies under 2 sentences."
        }
    }

    @classmethod
    def get_persona_names(cls) -> List[str]:
        """Get list of available persona names"""
        return list(cls.PERSONAS.keys())

    @classmethod
    def get_persona_prompt(cls, persona_name: str) -> str:
        """Get system prompt for a persona"""
        return cls.PERSONAS.get(persona_name, {}).get("system_prompt", "")

    @classmethod
    def get_persona_description(cls, persona_name: str) -> str:
        """Get description for a persona"""
        return cls.PERSONAS.get(persona_name, {}).get("description", "")


class ConversationManager:
    """Manages the multi-model conversation"""

    def __init__(self, ollama: OllamaManager):
        self.ollama = ollama
        self.chatbots = []

    def add_chatbot(self, model: str, persona: str, name: str):
        """Add a chatbot to the conversation"""
        self.chatbots.append({
            "model": model,
            "persona": persona,
            "name": name,
            "messages": []
        })

    def initialize_conversation(self, topic: str):
        """Initialize the conversation with a topic"""
        if not self.chatbots:
            return

        # First chatbot introduces the topic
        self.chatbots[0]["messages"].append(
            f"Today's topic for discussion is: '{topic}'. Let's begin!"
        )

        # Other chatbots respond with acknowledgment
        for i in range(1, len(self.chatbots)):
            self.chatbots[i]["messages"].append(
                "Great topic! I'm ready to discuss."
            )

    def generate_next_responses(self) -> List[Dict]:
        """Generate next response for each chatbot"""
        responses = []

        for i, chatbot in enumerate(self.chatbots):
            # Build message history from all chatbots
            conversation_history = []

            # Get the conversation length (minimum across all chatbots)
            min_length = min(len(cb["messages"]) for cb in self.chatbots)

            # Build the conversation history
            for turn in range(min_length):
                for j, cb in enumerate(self.chatbots):
                    if turn < len(cb["messages"]):
                        role = "assistant" if i == j else "user"
                        conversation_history.append({
                            "role": role,
                            "content": f"{cb['name']}: {cb['messages'][turn]}"
                        })

            # Generate response
            system_prompt = PersonaManager.get_persona_prompt(
                chatbot["persona"])
            response = self.ollama.generate_response(
                chatbot["model"],
                conversation_history,
                system_prompt
            )

            # Store response
            chatbot["messages"].append(response)

            responses.append({
                "chatbot": chatbot["name"],
                "persona": chatbot["persona"],
                "message": response,
                "index": i
            })

        return responses


def judge_conversation(ollama: OllamaManager, judge_model: str, topic: str,
                       chatbots: List[Dict], conversation_history: List[Dict]) -> Dict:
    """
    Have a judge model evaluate the conversation and declare a winner
    """
    # Build the conversation summary for the judge
    summary = f"Topic: {topic}\n\n"
    summary += "Participants:\n"
    for i, chatbot in enumerate(chatbots):
        summary += f"{i+1}. {chatbot['name']} - {chatbot['persona']} persona\n"

    summary += "\n\nConversation:\n\n"

    # Add opening statements
    summary += "Opening Statements:\n"
    for chatbot in chatbots:
        if chatbot["messages"]:
            summary += f"{chatbot['name']}: {chatbot['messages'][0]}\n"

    summary += "\n"

    # Add conversation turns
    turn_num = 1
    for i in range(1, len(chatbot["messages"])):
        summary += f"\nTurn {turn_num}:\n"
        for chatbot in chatbots:
            if i < len(chatbot["messages"]):
                summary += f"{chatbot['name']}: {chatbot['messages'][i]}\n"
        turn_num += 1

    # Judge's system prompt
    judge_system_prompt = """You are an expert debate judge and conversation analyst. 
    You evaluate conversations based on:
    1. Coherence and relevance to the topic
    2. Depth of insights and arguments
    3. Creativity and originality
    4. Engagement and persuasiveness
    5. Consistency with their assigned persona
    
    Analyze the conversation and declare a winner. Provide your verdict in exactly this format:
    
    WINNER: [Name of the winning chatbot]
    REASONING: [2-3 sentences explaining why this chatbot won]
    HIGHLIGHTS: [Mention one strong point from each participant]
    
    Be fair, objective, and provide constructive feedback."""

    # Create judge prompt
    judge_messages = [{
        "role": "user",
        "content": f"{summary}\n\nPlease analyze this conversation and declare a winner."
    }]

    # Get judge's verdict
    verdict = ollama.generate_response(
        judge_model,
        judge_messages,
        judge_system_prompt
    )

    # Parse the verdict
    winner = "Unable to determine"
    reasoning = verdict

    if "WINNER:" in verdict:
        lines = verdict.split('\n')
        for line in lines:
            if line.startswith("WINNER:"):
                winner = line.replace("WINNER:", "").strip()
                break

    return {
        "winner": winner,
        "full_verdict": verdict,
        "judge_model": judge_model,
        "timestamp": datetime.now().isoformat()
    }


def export_conversation_json(topic: str, chatbots: List[Dict],
                             conversation_history: List[Dict],
                             num_turns: int, judge_verdict: Optional[Dict] = None) -> str:
    """
    Export conversation in structured JSON format with comments and metadata
    """
    export_data = {
        "_comment": "Multi-Model Chatbot Conversation - Exported from Streamlit App",
        "metadata": {
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "total_turns": num_turns,
            "total_messages": len(conversation_history),
            "number_of_participants": len(chatbots)
        },
        "participants": [
            {
                "id": i + 1,
                "name": chatbot["name"],
                "model": chatbot["model"],
                "persona": chatbot["persona"],
                "persona_description": PersonaManager.get_persona_description(chatbot["persona"]),
                "_comment": f"Chatbot {i+1} using {chatbot['model']} model with {chatbot['persona']} persona"
            }
            for i, chatbot in enumerate(chatbots)
        ],
        "conversation": {
            "opening_statements": [
                {
                    "participant_id": i + 1,
                    "participant_name": chatbot["name"],
                    "message": chatbot["messages"][0] if chatbot["messages"] else "",
                    "_comment": f"Opening statement by {chatbot['name']}"
                }
                for i, chatbot in enumerate(chatbots)
            ],
            "turns": []
        }
    }

    # Group conversation by turns
    turns_dict = {}
    for response in conversation_history:
        # Find which chatbot this response belongs to
        chatbot_id = response["index"] + 1
        turn_num = len([r for r in conversation_history
                       if conversation_history.index(r) <=
                       conversation_history.index(response)]) // len(chatbots)

        if turn_num not in turns_dict:
            turns_dict[turn_num] = []

        turns_dict[turn_num].append({
            "participant_id": chatbot_id,
            "participant_name": response["chatbot"],
            "persona": response["persona"],
            "message": response["message"],
            "_comment": f"Response by {response['chatbot']} in turn {turn_num + 1}"
        })

    # Add turns to export data
    for turn_num in sorted(turns_dict.keys()):
        export_data["conversation"]["turns"].append({
            "turn_number": turn_num + 1,
            "responses": turns_dict[turn_num],
            "_comment": f"Turn {turn_num + 1} - All participants respond"
        })

    # Add judge verdict if available
    if judge_verdict:
        export_data["judge_verdict"] = {
            "judge_model": judge_verdict["judge_model"],
            "winner": judge_verdict["winner"],
            "full_verdict": judge_verdict["full_verdict"],
            "timestamp": judge_verdict["timestamp"],
            "_comment": "Final verdict by the judge model evaluating the entire conversation"
        }

    return json.dumps(export_data, indent=2, ensure_ascii=False)


def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'current_turn' not in st.session_state:
        st.session_state.current_turn = 0
    if 'conversation_manager' not in st.session_state:
        st.session_state.conversation_manager = None
    if 'judge_verdict' not in st.session_state:
        st.session_state.judge_verdict = None


def main():
    """Main application"""

    # Initialize session state
    initialize_session_state()

    # Initialize Ollama manager
    ollama = OllamaManager()

    # Header
    st.markdown('<div class="main-header">🤖 Multi-Model Chatbot Conversation 💬</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Create engaging conversations between AI models with different personas</div>', unsafe_allow_html=True)

    # Check Ollama connection
    if not ollama.check_connection():
        st.error("❌ **Ollama is not running!**")
        st.info("""
        Please start Ollama before using this application:
        - On macOS: Open the Ollama app
        - On Linux/Windows: Run `ollama serve` in terminal
        - Then refresh this page
        """)
        st.stop()

    st.success("✅ **Ollama is running!**")

    # Get available models
    available_models = ollama.get_available_models()

    if not available_models:
        st.error("❌ **No models found!**")
        st.info("""
        Please download at least one model first:
        ```bash
        ollama pull llama3.2
        ollama pull mistral
        ollama pull phi3
        ```
        Then refresh this page.
        """)
        st.stop()

    st.info(
        f"📦 **Found {len(available_models)} model(s):** {', '.join(available_models)}")

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Number of chatbots
        num_chatbots = st.slider(
            "Number of Chatbots",
            min_value=2,
            max_value=min(5, len(available_models)),
            value=3,
            help="Select how many AI models will participate in the conversation"
        )

        st.divider()

        # Configure each chatbot
        st.subheader("🤖 Configure Chatbots")
        chatbot_configs = []

        for i in range(num_chatbots):
            with st.expander(f"Chatbot {i+1}", expanded=i < 3):
                col1, col2 = st.columns(2)

                with col1:
                    name = st.text_input(
                        "Name",
                        value=f"Bot {i+1}",
                        key=f"name_{i}"
                    )

                with col2:
                    model = st.selectbox(
                        "Model",
                        available_models,
                        key=f"model_{i}",
                        index=i % len(available_models)
                    )

                persona = st.selectbox(
                    "Persona",
                    PersonaManager.get_persona_names(),
                    key=f"persona_{i}",
                    index=i % len(PersonaManager.get_persona_names())
                )

                # Show persona description
                st.caption(PersonaManager.get_persona_description(persona))

                chatbot_configs.append({
                    "name": name,
                    "model": model,
                    "persona": persona
                })

        st.divider()

        # Conversation settings
        st.subheader("💬 Conversation Settings")

        topic = st.text_area(
            "Discussion Topic",
            value="Why did the chicken cross the road?",
            help="Enter the topic for discussion",
            height=100
        )

        num_turns = st.slider(
            "Number of Conversation Turns",
            min_value=1,
            max_value=10,
            value=5,
            help="How many times each chatbot will respond"
        )

        st.divider()

        # Judge model configuration
        st.subheader("⚖️ Judge Model")

        enable_judge = st.checkbox(
            "Enable Judge",
            value=True,
            help="Have a judge model evaluate the conversation and declare a winner"
        )

        if enable_judge:
            judge_model = st.selectbox(
                "Judge Model",
                available_models,
                key="judge_model",
                help="Select the model that will act as judge"
            )
            st.caption(
                "🏆 The judge will evaluate the conversation and award a winner at the end")

        st.divider()

        # Action buttons
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🚀 Start Conversation", type="primary", use_container_width=True):
                # Reset conversation
                st.session_state.conversation_started = True
                st.session_state.conversation_history = []
                st.session_state.current_turn = 0

                # Create conversation manager
                manager = ConversationManager(ollama)

                # Add chatbots
                for config in chatbot_configs:
                    manager.add_chatbot(
                        config["model"],
                        config["persona"],
                        config["name"]
                    )

                # Initialize conversation
                manager.initialize_conversation(topic)

                st.session_state.conversation_manager = manager
                st.session_state.num_turns = num_turns
                st.rerun()

        with col2:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.conversation_started = False
                st.session_state.conversation_history = []
                st.session_state.current_turn = 0
                st.session_state.conversation_manager = None
                st.session_state.judge_verdict = None
                st.rerun()

    # Main content area
    if not st.session_state.conversation_started:
        # Welcome screen
        st.info("""
        ### 👋 Welcome to the Multi-Model Chatbot Conversation App!
        
        **How to use:**
        1. Configure the number of chatbots (2-5) in the sidebar
        2. Select a model and persona for each chatbot
        3. Enter a discussion topic
        4. Choose how many conversation turns you want
        5. (Optional) Enable a judge model to evaluate and award a winner
        6. Click "🚀 Start Conversation" to begin!
        
        **New Features:**
        - 🏆 **Judge Mode**: Have an AI judge evaluate the conversation and declare a winner
        - 📊 **JSON Export**: Download conversations in structured JSON format with metadata
        - 📥 **Enhanced Export**: Export includes judge verdicts and detailed participant info
        
        **Tips:**
        - Different personas create more interesting conversations
        - Try philosophical topics for deeper discussions
        - Use humor-focused personas for entertaining exchanges
        - Experiment with different model combinations
        - Enable the judge for competitive debates!
        """)

        # Example topics
        st.subheader("💡 Example Topics")
        example_topics = [
            "Is technology making us more connected or more isolated?",
            "What is the meaning of happiness?",
            "Should AI have rights?",
            "Is time travel possible?",
            "What makes art valuable?",
            "Can machines truly be creative?",
            "Is free will an illusion?",
            "What is the purpose of education?"
        ]

        cols = st.columns(2)
        for idx, topic_example in enumerate(example_topics):
            with cols[idx % 2]:
                st.info(f"📌 {topic_example}")

    else:
        # Conversation display
        manager = st.session_state.conversation_manager

        if manager:
            # Progress
            progress_text = f"Turn {st.session_state.current_turn + 1} of {st.session_state.num_turns}"
            st.progress(
                (st.session_state.current_turn + 1) / st.session_state.num_turns,
                text=progress_text
            )

            # Display initial messages
            if st.session_state.current_turn == 0:
                st.markdown("### 🎬 Opening Statements")
                for i, chatbot in enumerate(manager.chatbots):
                    if chatbot["messages"]:
                        st.markdown(
                            f'<div class="chatbot-message chatbot-{i}">'
                            f'<strong>{chatbot["name"]}</strong> ({chatbot["persona"]})<br/>'
                            f'{chatbot["messages"][0]}'
                            f'</div>',
                            unsafe_allow_html=True
                        )

            # Generate next turn button
            if st.session_state.current_turn < st.session_state.num_turns:
                if st.button(f"➡️ Generate Turn {st.session_state.current_turn + 1}", type="primary"):
                    with st.spinner("🤔 Chatbots are thinking..."):
                        responses = manager.generate_next_responses()
                        st.session_state.conversation_history.extend(responses)
                        st.session_state.current_turn += 1
                        st.rerun()

            # Display conversation history
            if st.session_state.conversation_history:
                st.markdown("### 💬 Conversation")

                # Group by turn
                turns = {}
                for response in st.session_state.conversation_history:
                    turn_num = len([r for r in st.session_state.conversation_history
                                   if st.session_state.conversation_history.index(r) <=
                                   st.session_state.conversation_history.index(response)]) // len(manager.chatbots)
                    if turn_num not in turns:
                        turns[turn_num] = []
                    turns[turn_num].append(response)

                # Display each turn
                for turn_num in sorted(turns.keys()):
                    st.markdown(f"#### 🔄 Turn {turn_num + 1}")
                    for response in turns[turn_num]:
                        st.markdown(
                            f'<div class="chatbot-message chatbot-{response["index"]}">'
                            f'<strong>{response["chatbot"]}</strong> ({response["persona"]})<br/>'
                            f'{response["message"]}'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                    st.markdown("---")

            # Completion message
            if st.session_state.current_turn >= st.session_state.num_turns:
                st.success("🎉 **Conversation Complete!**")
                st.balloons()

                # Judge section
                if enable_judge and st.session_state.judge_verdict is None:
                    st.markdown("### ⚖️ Calling the Judge...")
                    with st.spinner(f"🤔 {judge_model} is analyzing the conversation..."):
                        verdict = judge_conversation(
                            ollama,
                            judge_model,
                            topic,
                            manager.chatbots,
                            st.session_state.conversation_history
                        )
                        st.session_state.judge_verdict = verdict
                        st.rerun()

                # Display judge verdict
                if st.session_state.judge_verdict:
                    st.markdown("### 🏆 Judge's Verdict")
                    verdict = st.session_state.judge_verdict

                    # Find winner's index for highlighting
                    winner_name = verdict["winner"]
                    winner_index = -1
                    for i, chatbot in enumerate(manager.chatbots):
                        if chatbot["name"].lower() in winner_name.lower() or winner_name.lower() in chatbot["name"].lower():
                            winner_index = i
                            break

                    st.markdown(
                        f'<div class="judge-verdict">'
                        f'<h4>👨‍⚖️ Judge: {verdict["judge_model"]}</h4>'
                        f'<h3>🏆 Winner: {verdict["winner"]} <span class="winner-badge">WINNER</span></h3>'
                        f'<p style="margin-top: 1rem; font-size: 1.1rem;">{verdict["full_verdict"]}</p>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    # Highlight winner in the conversation
                    if winner_index >= 0:
                        st.info(
                            f"✨ The winner's messages are marked with chatbot-{winner_index} color in the conversation above!")

                # Statistics
                st.markdown("### 📊 Conversation Statistics")
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Total Turns", st.session_state.num_turns)

                with col2:
                    st.metric("Total Messages", len(
                        st.session_state.conversation_history))

                with col3:
                    st.metric("Participants", len(manager.chatbots))

                # Export options
                st.markdown("### 💾 Export Conversation")

                col1, col2 = st.columns(2)

                with col1:
                    # Prepare export text for Markdown
                    export_text = f"# Multi-Model Chatbot Conversation\n\n"
                    export_text += f"**Topic:** {topic}\n\n"
                    export_text += f"**Participants:**\n"
                    for chatbot in manager.chatbots:
                        export_text += f"- {chatbot['name']} ({chatbot['model']}) - {chatbot['persona']}\n"
                    export_text += f"\n---\n\n"

                    # Add opening
                    export_text += "## Opening Statements\n\n"
                    for chatbot in manager.chatbots:
                        if chatbot["messages"]:
                            export_text += f"**{chatbot['name']}:** {chatbot['messages'][0]}\n\n"

                    # Add conversation
                    export_text += "## Conversation\n\n"
                    for turn_num in sorted(turns.keys()):
                        export_text += f"### Turn {turn_num + 1}\n\n"
                        for response in turns[turn_num]:
                            export_text += f"**{response['chatbot']}:** {response['message']}\n\n"

                    # Add judge verdict if available
                    if st.session_state.judge_verdict:
                        export_text += "---\n\n## 🏆 Judge's Verdict\n\n"
                        export_text += f"**Judge Model:** {st.session_state.judge_verdict['judge_model']}\n\n"
                        export_text += f"**Winner:** {st.session_state.judge_verdict['winner']}\n\n"
                        export_text += f"**Verdict:**\n\n{st.session_state.judge_verdict['full_verdict']}\n\n"

                    st.download_button(
                        label="📥 Download as Markdown",
                        data=export_text,
                        file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )

                with col2:
                    # Prepare JSON export
                    json_data = export_conversation_json(
                        topic,
                        manager.chatbots,
                        st.session_state.conversation_history,
                        st.session_state.num_turns,
                        st.session_state.judge_verdict
                    )

                    st.download_button(
                        label="📊 Download as JSON",
                        data=json_data,
                        file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )


if __name__ == "__main__":
    main()
