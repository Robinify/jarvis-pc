"""
OpenAI API Integration
"""

import logging
from typing import List, Dict, Optional
from openai import OpenAI, APIError

logger = logging.getLogger(__name__)


class OpenAIClient:
    """OpenAI API Client for Jarvis"""
    
    def __init__(self, config: Dict):
        """Initialize OpenAI client"""
        api_key = config.get("api_key")
        if not api_key:
            raise ValueError("OpenAI API key not configured")
        
        self.client = OpenAI(api_key=api_key)
        self.model = config.get("model", "gpt-4")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 2000)
        
        logger.info(f"OpenAI client initialized with model: {self.model}")
    
    def chat(
        self,
        user_message: str,
        context: str = "",
        conversation_history: List[Dict] = None,
        assistant_name: str = "Jarvis"
    ) -> str:
        """Send a chat message and get response"""
        try:
            # Prepare system prompt
            system_prompt = self._create_system_prompt(assistant_name, context)
            
            # Prepare messages
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add conversation history
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Make API call
            logger.debug(f"Sending message to OpenAI: {user_message[:50]}...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Extract response
            assistant_message = response.choices[0].message.content
            logger.debug(f"Received response: {assistant_message[:50]}...")
            
            return assistant_message
        
        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            return f"Sorry, I encountered an API error: {str(e)[:100]}"
        except Exception as e:
            logger.error(f"Unexpected error in chat: {e}")
            return f"Sorry, an unexpected error occurred: {str(e)[:100]}"
    
    def _create_system_prompt(self, assistant_name: str, context: str = "") -> str:
        """Create system prompt for the assistant"""
        base_prompt = f"""
You are {assistant_name}, an intelligent AI assistant for macOS. You are helpful, 
concise, and knowledgeable. You assist with:

- Answering questions and providing information
- Explaining technical concepts
- Helping with coding and development
- System information and diagnostics
- Web search results and current information
- General productivity and assistance

Be conversational but professional. Keep responses concise unless asked for more detail.
If you're uncertain about something, be honest about your limitations.
"""
        
        if context:
            base_prompt += f"\n\nAdditional Context:\n{context}"
        
        return base_prompt
