"""
Core Jarvis functionality - main assistant logic
"""

import logging
from typing import Optional, Dict, List
from jarvis.api import OpenAIClient
from jarvis.voice import VoiceHandler
from jarvis.search import WebSearch
from jarvis.system import SystemCommands
from jarvis.memory import ConversationMemory
from jarvis.utils import format_response


logger = logging.getLogger(__name__)


class Jarvis:
    """Main Jarvis AI Assistant"""
    
    def __init__(self, config: Dict):
        """Initialize Jarvis with configuration"""
        self.config = config
        self.name = "Jarvis"
        
        # Initialize components
        self.api_client = OpenAIClient(config.get("openai", {}))
        self.voice_handler = VoiceHandler(config.get("voice", {}))
        self.web_search = WebSearch(config.get("search", {}))
        self.system_commands = SystemCommands(config.get("system", {}))
        self.memory = ConversationMemory(config.get("memory", {}))
        
        logger.info(f"{self.name} initialized successfully")
    
    def start(self):
        """Start interactive Jarvis session"""
        print(f"\n{'='*60}")
        print(f"  {self.name} - AI Assistant for macOS")
        print(f"{'='*60}")
        print(f"\nCommands:")
        print(f"  'voice' - Enable voice input")
        print(f"  'search <query>' - Search the web")
        print(f"  'exec <command>' - Execute system command")
        print(f"  'memory' - Show conversation memory")
        print(f"  'clear' - Clear conversation history")
        print(f"  'quit' or 'exit' - Exit Jarvis")
        print(f"\n{'='*60}\n")
        
        while True:
            try:
                # Get user input
                user_input = self._get_user_input()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if self._handle_special_commands(user_input):
                    continue
                
                # Process user query
                response = self._process_query(user_input)
                
                # Display and speak response
                self._output_response(response)
                
                # Store in memory
                self.memory.add_exchange(user_input, response)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                print(f"Error: {e}")
    
    def _get_user_input(self) -> str:
        """Get user input from voice or text"""
        if self.config.get("voice", {}).get("input_enabled", False):
            print("\n🎤 Listening... (speak now or type)")
            voice_input = self.voice_handler.recognize_speech()
            if voice_input:
                print(f"You: {voice_input}")
                return voice_input
        
        user_input = input("\nYou: ").strip()
        return user_input
    
    def _handle_special_commands(self, user_input: str) -> bool:
        """Handle special commands, return True if handled"""
        user_input_lower = user_input.lower()
        
        if user_input_lower in ["quit", "exit"]:
            print(f"\n{self.name}: Goodbye! Have a great day.")
            exit(0)
        
        if user_input_lower == "memory":
            self._show_memory()
            return True
        
        if user_input_lower == "clear":
            self.memory.clear()
            print(f"\n{self.name}: Conversation history cleared.")
            return True
        
        if user_input_lower == "voice":
            enabled = self.config["voice"]["input_enabled"]
            self.config["voice"]["input_enabled"] = not enabled
            status = "enabled" if not enabled else "disabled"
            print(f"\n{self.name}: Voice input {status}.")
            return True
        
        if user_input_lower.startswith("search "):
            query = user_input[7:].strip()
            results = self.web_search.search(query)
            self._display_search_results(results)
            return True
        
        if user_input_lower.startswith("exec "):
            command = user_input[5:].strip()
            result = self.system_commands.execute(command)
            print(f"\n{self.name}: {result}")
            return True
        
        return False
    
    def _process_query(self, user_input: str) -> str:
        """Process user query and get AI response"""
        # Check if query involves web search
        if any(keyword in user_input.lower() for keyword in ["search", "weather", "news", "current", "latest"]):
            search_results = self._extract_and_search(user_input)
            context = f"\n\nWeb Search Results:\n{search_results}" if search_results else ""
        else:
            context = ""
        
        # Get system context if needed
        if any(keyword in user_input.lower() for keyword in ["system", "info", "memory", "storage", "battery"]):
            system_info = self.system_commands.get_system_info()
            context += f"\n\nSystem Information:\n{system_info}"
        
        # Get conversation context
        conversation_context = self.memory.get_context()
        
        # Call OpenAI API
        response = self.api_client.chat(
            user_input,
            context=context,
            conversation_history=conversation_context,
            assistant_name=self.name
        )
        
        return response
    
    def _extract_and_search(self, user_input: str) -> str:
        """Extract search query and perform search"""
        try:
            results = self.web_search.search(user_input)
            return self.web_search.format_results(results)
        except Exception as e:
            logger.error(f"Search error: {e}")
            return ""
    
    def _output_response(self, response: str):
        """Output response to user via text and voice"""
        formatted = format_response(response, self.name)
        print(f"\n{formatted}")
        
        # Speak response if enabled
        if self.config.get("voice", {}).get("output_enabled", False):
            self.voice_handler.speak(response)
    
    def _show_memory(self):
        """Display conversation memory"""
        messages = self.memory.get_messages()
        if not messages:
            print(f"\n{self.name}: No conversation history yet.")
            return
        
        print(f"\n{self.name}: Conversation History:")
        print("="*60)
        for msg in messages:
            role = "You" if msg["role"] == "user" else self.name
            print(f"\n{role}: {msg['content'][:100]}...")
        print("\n" + "="*60)
    
    def _display_search_results(self, results: List[Dict]):
        """Display formatted search results"""
        if not results:
            print(f"\n{self.name}: No results found.")
            return
        
        print(f"\n{self.name}: Search Results:")
        print("="*60)
        for i, result in enumerate(results[:5], 1):
            print(f"\n{i}. {result.get('title', 'No title')}")
            print(f"   {result.get('snippet', 'No snippet')}")
            print(f"   🔗 {result.get('link', '')}")
        print("\n" + "="*60)
