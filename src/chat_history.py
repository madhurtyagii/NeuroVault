"""
NeuroVault Chat History Manager
Manages conversation sessions in memory and database persistence
"""

import json
from datetime import datetime


class ChatHistoryManager:
    """Manages chat session state in memory"""
    
    def __init__(self):
        self.messages = []
        self.session_id = None
        self.title = None
        self.created_at = None
    
    def add_message(self, role, content):
        """
        Add a message to the current session
        
        Args:
            role: 'user' or 'assistant'
            content: Message text
        """
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_messages(self):
        """Get all messages in current session"""
        return self.messages.copy()
    
    def clear(self):
        """Clear current session"""
        self.messages = []
        self.session_id = None
        self.title = None
        self.created_at = None
    
    def to_json(self):
        """Export messages as JSON string"""
        return json.dumps(self.messages, ensure_ascii=False)
    
    def from_json(self, json_str):
        """Load messages from JSON string"""
        try:
            self.messages = json.loads(json_str)
        except json.JSONDecodeError:
            self.messages = []
    
    def load_session(self, session_id, title, created_at, messages_json):
        """Load a saved session"""
        self.session_id = session_id
        self.title = title
        self.created_at = created_at
        self.from_json(messages_json)
    
    def get_message_count(self):
        """Get count of messages"""
        return len(self.messages)
    
    def get_last_messages(self, count=10):
        """Get last N messages for context"""
        return self.messages[-count:] if self.messages else []
    
    def generate_title(self):
        """Generate a title from first user message"""
        for msg in self.messages:
            if msg.get("role") == "user":
                content = msg.get("content", "")
                # Truncate to first 50 chars
                if len(content) > 50:
                    return content[:47] + "..."
                return content
        return f"Chat {datetime.now().strftime('%m/%d %H:%M')}"
