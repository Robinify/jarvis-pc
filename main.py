# Jarvis - AI Assistant for macOS

A comprehensive AI assistant for your macOS PC with voice input/output, web search, system integration, and more.

## Features

- 🎤 **Voice Input & Output**: Speak to Jarvis and hear responses
- 💬 **Text Chat**: Interactive text-based conversations
- 🌐 **Web Search**: Real-time information from the internet
- 📊️ **System Integration**: Execute commands, check system info, manage files
- 🧠 **AI-Powered**: Uses OpenAI's GPT-4/GPT-3.5 for intelligent responses
- 📝 **Context Memory**: Maintains conversation history
- ⚙️ **Customizable**: Easy configuration for API keys and preferences

## Prerequisites

- macOS 10.13+
- Python 3.8+
- OpenAI API key
- Internet connection

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Robinify/jarvis-pc.git
   cd jarvis-pc
  python3 -m venv venv
source venv/bin/activate
  pip install -r requirements.txt
  cp config.example.yaml config.yaml
  openai_api_key: "your-api-key-here"
  python main.py
  # OpenAI Configuration
openai_api_key: "your-key"
model: "gpt-4"  # or gpt-3.5-turbo
temperature: 0.7

# Voice Configuration
voice_enabled: true
voice_input_enabled: true
voice_output_enabled: true
voice_rate: 200  # words per minute

# System Configuration
max_context_messages: 10
enable_web_search: true
enable_system_commands: true
max_search_results: 5
jarvis-pc/
├── main.py              # Entry point
├── config.yaml          # Configuration (create from config.example.yaml)
├── config.example.yaml  # Configuration template
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── jarvis/
    ├── __init__.py
    ├── core.py         # Main Jarvis logic
    ├── voice.py        # Voice I/O handling
    ├── api.py          # OpenAI API integration
    ├── search.py       # Web search functionality
    ├── system.py       # System commands and info
    ├── memory.py       # Conversation memory
    └── utils.py        # Utility functions
    
