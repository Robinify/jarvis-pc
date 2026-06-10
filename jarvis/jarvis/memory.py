"""
Conversation Memory Management
"""

import json
import logging
from typing import Dict, List
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class ConversationMemory:
    """Manage conversation history and context"""
    
    def __init__(self, config: Dict):
        """Initialize conversation memory"""
        self.max_messages = config.get("max_messages", 10)
        self.save_history = config.get("save_history", True)
        self.history_file = Path(config.get("history_file", "~/.jarvis_history")).expanduser()
        
        self.messages: List[Dict] = []
        
        # Create history directory if needed
        if self.save_history:
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            self._load_history()
        
        logger.info("Conversation memory initialized")
    
    def add_exchange(self, user_message: str, assistant_message: str) -> None:
        """Add a user-assistant exchange to memory"""
        self.messages.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        self.messages.append({
            "role": "assistant",
            "content": assistant_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only recent messages
        if len(self.messages) > self.max_messages * 2:
            self.messages = self.messages[-(self.max_messages * 2):]
        
        # Save to file
        if self.save_history:
            self._save_history()
    
    def get_context(self) -> List[Dict]:
        """Get conversation context for API calls"""
        # Return only role and content, without timestamps
        return [{"role": msg["role"], "content": msg["content"]} for msg in self.messages]
    
    def get_messages(self) -> List[Dict]:
        """Get all messages in memory"""
        return self.messages
    
    def clear(self) -> None:
        """Clear conversation memory"""
        self.messages = []
        
        if self.save_history and self.history_file.exists():
            try:
                self.history_file.unlink()
                logger.info("Conversation history cleared")
            except Exception as e:
                logger.error(f"Error clearing history file: {e}")
    
    def _save_history(self) -> None:
        """Save conversation history to file"""
        try:
            with open(self.history_file, "w") as f:
                json.dump(self.messages, f, indent=2)
            logger.debug(f"Saved {len(self.messages)} messages to history")
        except Exception as e:
            logger.error(f"Error saving history: {e}")
    
    def _load_history(self) -> None:
        """Load conversation history from file"""
        try:
            if self.history_file.exists():
                with open(self.history_file, "r") as f:
                    self.messages = json.load(f)
                logger.info(f"Loaded {len(self.messages)} messages from history")
        except Exception as e:
            logger.error(f"Error loading history: {e}")
            self.messages = []
