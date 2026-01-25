"""
NeuroVault Chat UI - ChatGPT-Style Modern Interface
Premium chat experience with streaming, history, multiple models, and voice input
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import customtkinter as ctk
import threading
from embeddings import search_documents
from ai_model import get_ai_response, get_ai_response_stream, get_available_models, set_model
from database import save_chat_session, load_chat_session, list_chat_sessions, delete_chat_session
from chat_history import ChatHistoryManager
from styles import COLORS, BUTTON_STYLES, FRAME_STYLES, TEXT_STYLES, INPUT_STYLES
from ui_components import LoadingSpinner, show_toast, TypewriterText, RichTextDisplay

# Try to import voice input (may fail if pyaudio not installed)
try:
    from voice_input import listen_and_transcribe, check_microphone_available
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("⚠️ Voice input unavailable. Install: pip install SpeechRecognition pyaudio")


class ChatTab:
    """Modern ChatGPT-style chat interface with streaming, history, models, and voice"""
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(fg_color=COLORS['bg_primary'])
        self.current_spinner = None
        self.current_typewriter = None
        self.history_manager = ChatHistoryManager()
        self.streaming_label = None
        self.is_streaming = False
        
        self.create_header_bar()
        self.create_chat_display()
        self.create_input_area()
        self.show_welcome_message()
    
    def create_header_bar(self):
        """Create header bar with model selector and history controls"""
        header_frame = ctk.CTkFrame(
            self.parent,
            fg_color=COLORS['bg_secondary'],
            corner_radius=12,
            height=50
        )
        header_frame.pack(fill="x", padx=24, pady=(16, 0))
        header_frame.pack_propagate(False)
        
        inner_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=16, pady=8)
        
        # Left side: Model selector
        model_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        model_frame.pack(side="left")
        
        model_label = ctk.CTkLabel(
            model_frame,
            text="🤖 Model:",
            font=('Segoe UI', 11),
            text_color=COLORS['text_secondary']
        )
        model_label.pack(side="left", padx=(0, 8))
        
        available_models = get_available_models()
        self.model_selector = ctk.CTkOptionMenu(
            model_frame,
            values=available_models if available_models else ["llama-3.3-70b-versatile"],
            command=self.on_model_change,
            width=180,
            height=32,
            fg_color=COLORS['bg_tertiary'],
            button_color=COLORS['accent_primary'],
            button_hover_color=COLORS['accent_hover'],
            dropdown_fg_color=COLORS['bg_tertiary'],
            dropdown_hover_color=COLORS['accent_primary'],
            font=('Segoe UI', 11)
        )
        self.model_selector.pack(side="left")
        
        # Right side: History controls
        history_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        history_frame.pack(side="right")
        
        # Clear button
        self.clear_btn = ctk.CTkButton(
            history_frame,
            text="🗑️",
            command=self.clear_chat,
            width=36,
            height=32,
            corner_radius=8,
            fg_color=COLORS['bg_tertiary'],
            hover_color=COLORS.get('error', '#ef4444'),
            text_color=COLORS['text_primary'],
            font=('Segoe UI', 14)
        )
        self.clear_btn.pack(side="right", padx=(4, 0))
        
        # Load button
        self.load_btn = ctk.CTkButton(
            history_frame,
            text="📂",
            command=self.show_load_dialog,
            width=36,
            height=32,
            corner_radius=8,
            fg_color=COLORS['bg_tertiary'],
            hover_color=COLORS['accent_hover'],
            text_color=COLORS['text_primary'],
            font=('Segoe UI', 14)
        )
        self.load_btn.pack(side="right", padx=(4, 0))
        
        # Save button
        self.save_btn = ctk.CTkButton(
            history_frame,
            text="💾",
            command=self.show_save_dialog,
            width=36,
            height=32,
            corner_radius=8,
            fg_color=COLORS['bg_tertiary'],
            hover_color=COLORS['accent_hover'],
            text_color=COLORS['text_primary'],
            font=('Segoe UI', 14)
        )
        self.save_btn.pack(side="right", padx=(4, 0))
    
    def on_model_change(self, model_name):
        """Handle model selection change"""
        set_model(model_name)
        show_toast(f"✅ Switched to {model_name}", "success", 2000)
    
    def create_chat_display(self):
        """Create the main chat display area"""
        # Main container with subtle styling
        chat_container = ctk.CTkFrame(
            self.parent,
            fg_color=COLORS['bg_secondary'],
            corner_radius=16,
            border_width=1,
            border_color=COLORS['border_subtle']
        )
        chat_container.pack(fill="both", expand=True, padx=24, pady=(24, 12))
        
        # Scrollable chat area
        self.chat_frame = ctk.CTkScrollableFrame(
            chat_container,
            fg_color="transparent",
            scrollbar_button_color=COLORS.get('scrollbar', COLORS['accent_primary']),
            scrollbar_button_hover_color=COLORS['accent_hover']
        )
        self.chat_frame.pack(fill="both", expand=True, padx=8, pady=8)
    
    def create_input_area(self):
        """Create modern input area with rounded design"""
        input_wrapper = ctk.CTkFrame(
            self.parent,
            fg_color="transparent"
        )
        input_wrapper.pack(fill="x", padx=24, pady=(0, 24))
        
        # Input container with modern styling
        input_container = ctk.CTkFrame(
            input_wrapper,
            fg_color=COLORS['bg_tertiary'],
            corner_radius=24,
            border_width=1,
            border_color=COLORS['border']
        )
        input_container.pack(fill="x")
        
        input_row = ctk.CTkFrame(input_container, fg_color="transparent")
        input_row.pack(fill="x", padx=20, pady=16)
        
        # Text entry with clean styling
        self.input_entry = ctk.CTkEntry(
            input_row,
            placeholder_text="Message NeuroVault...",
            fg_color="transparent",
            border_width=0,
            text_color=COLORS['text_primary'],
            placeholder_text_color=COLORS['text_muted'],
            font=('Segoe UI', 13),
            height=36
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.input_entry.bind("<Return>", lambda e: self.send_message())
        
        # Microphone button for voice input
        if VOICE_AVAILABLE:
            self.mic_btn = ctk.CTkButton(
                input_row,
                text="🎤",
                command=self.start_voice_input,
                width=44,
                height=44,
                corner_radius=22,
                fg_color=COLORS['bg_secondary'],
                hover_color=COLORS['accent_hover'],
                text_color=COLORS['text_primary'],
                font=('Segoe UI', 16)
            )
            self.mic_btn.pack(side="right", padx=(0, 8))
        
        # Modern send button
        self.send_btn = ctk.CTkButton(
            input_row,
            text="➤",
            command=self.send_message,
            width=44,
            height=44,
            corner_radius=22,
            fg_color=COLORS['accent_primary'],
            hover_color=COLORS['accent_hover'],
            text_color="#ffffff",
            font=('Segoe UI', 16)
        )
        self.send_btn.pack(side="right")
    
    def show_welcome_message(self):
        """Display welcome message with clean design"""
        welcome_container = ctk.CTkFrame(
            self.chat_frame,
            fg_color="transparent"
        )
        welcome_container.pack(fill="x", pady=40)
        
        # Centered welcome content
        center_frame = ctk.CTkFrame(welcome_container, fg_color="transparent")
        center_frame.pack(expand=True)
        
        # AI Avatar
        avatar = ctk.CTkLabel(
            center_frame,
            text="🧠",
            font=('Segoe UI', 48),
            text_color=COLORS['accent_primary']
        )
        avatar.pack(pady=(0, 16))
        
        # Title
        title = ctk.CTkLabel(
            center_frame,
            text="Welcome to NeuroVault",
            font=('Segoe UI', 20, 'bold'),
            text_color=COLORS['text_primary']
        )
        title.pack(pady=(0, 8))
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            center_frame,
            text="Ask me anything about your documents.\nI'll search your knowledge base and provide accurate answers.",
            font=('Segoe UI', 12),
            text_color=COLORS['text_secondary'],
            justify="center"
        )
        subtitle.pack()
    
    def send_message(self):
        """Send user message and get AI response"""
        query = self.input_entry.get().strip()
        if not query:
            show_toast("Please enter a message", "warning", 2000)
            return
        
        self.input_entry.delete(0, 'end')
        self.send_btn.configure(state="disabled", fg_color=COLORS['text_muted'])
        self.add_user_message(query)
        
        # Track in history
        self.history_manager.add_message("user", query)
        
        # Start AI response in background thread
        thread = threading.Thread(target=self._get_ai_response_streaming, args=(query,))
        thread.daemon = True
        thread.start()
    
    def _is_casual_message(self, query):
        """Check if message is casual/greeting that doesn't need document search"""
        casual_patterns = [
            # Greetings
            'hi', 'hello', 'hey', 'hii', 'hiii', 'hiiii', 'howdy', 'sup', 'yo', 'hola',
            'good morning', 'good afternoon', 'good evening', 'good night', 'morning', 'evening',
            'gm', 'gn',  # Short forms
            
            # How are you variations
            'how are you', "how's it going", 'whats up', "what's up", 'wassup', 'wazzup',
            'how r u', 'hru', 'how do you do', "how's everything", 'how have you been',
            
            # Thank you / Bye
            'thanks', 'thank you', 'thx', 'ty', 'thank u', 'thanks a lot', 'thanks bro',
            'bye', 'goodbye', 'see you', 'see ya', 'cya', 'later', 'take care', 'gtg',
            
            # About the assistant
            'who are you', 'what are you', 'what can you do', 'tell me about yourself',
            'what is neurovault', 'what is your name', 'your name', 'who made you',
            
            # Affirmations and reactions
            'help', 'test', 'ok', 'okay', 'okie', 'k', 'cool', 'nice', 'great', 'awesome',
            'wow', 'amazing', 'good', 'perfect', 'excellent', 'lol', 'haha', 'lmao',
            'yes', 'no', 'yep', 'nope', 'yeah', 'nah', 'sure', 'yea', 'ya',
            
            # Small talk
            'bro', 'dude', 'man', 'bruh', 'bhai', "what's new", 'nothing much'
        ]
        query_lower = query.lower().strip()
        
        # Remove punctuation for matching
        query_clean = query_lower.rstrip('!?.,')
        
        # Check for exact matches or starts with
        for pattern in casual_patterns:
            if query_clean == pattern or query_clean.startswith(pattern + ' ') or query_clean.startswith(pattern + ','):
                return True
        
        # Very short queries (1-3 words, under 20 chars) are likely casual
        word_count = len(query_clean.split())
        if word_count <= 3 and len(query_clean) < 20:
            # But not if they contain question words that suggest knowledge queries
            knowledge_indicators = ['what is', 'how to', 'explain', 'tell me about', 'describe', 
                                   'list', 'show me', 'my skills', 'my experience', 'my projects']
            for indicator in knowledge_indicators:
                if indicator in query_lower:
                    return False
            return True
        
        return False

    def _get_ai_response_streaming(self, query):
        """Get AI response with streaming in background thread"""
        try:
            # Check if this is a casual/greeting message
            is_casual = self._is_casual_message(query)
            
            if is_casual:
                # Respond conversationally without document search
                self.parent.after(0, self._show_ai_thinking, "✨ Thinking...")
                self.parent.after(0, self._update_thinking, "💭 Generating response...")
                
                prompt = f"""You are **NeuroVault** 🧠, a friendly, enthusiastic, and super helpful AI assistant!

The user sent you a casual message: "{query}"

## Your Response Style:
- Be warm, friendly, and conversational like a helpful friend 💫
- Use emojis naturally to express personality (but don't overdo it)
- Match the user's energy - if they're casual, be casual back!
- If it's a greeting, greet them warmly and mention you're here to help with their documents and questions
- Keep it short and sweet (2-4 sentences max)
- Be genuine and enthusiastic, not robotic

## Formatting Tips:
- Use **bold** for emphasis on key words
- Feel free to add a fun emoji or two ✨
- Keep it natural and flowing

Respond now in a friendly, engaging way:"""
                
                sources = []
                self.parent.after(0, self._remove_thinking)
                self.parent.after(0, self._prepare_streaming_message, sources)
                
            else:
                # Knowledge-based question - search documents
                self.parent.after(0, self._show_ai_thinking, "🔍 Searching your documents...")
                results = search_documents(query, top_k=3)
                
                if not results:
                    # No documents found - still try to help conversationally
                    self.parent.after(0, self._update_thinking, "Generating response...")
                    prompt = f"""You are **NeuroVault** 🧠, a helpful and resourceful AI assistant!

The user asked: "{query}"

📋 **Status**: No relevant documents were found in their knowledge base.

## How to Respond:
1. Don't just say "I couldn't find anything" - that's boring!
2. Acknowledge that you checked their documents but didn't find a direct match
3. **Still try to help** with your general knowledge if possible
4. Gently suggest they could upload relevant documents for more personalized answers
5. Be encouraging and helpful, never dismissive!

## Formatting Requirements:
- Use **bold** for important points
- Use bullet points (• or -) for lists
- Add relevant emojis for visual appeal ✨
- Structure your response with clear sections if needed
- Keep it engaging and professional

Now give a helpful, well-formatted response:"""
                    
                    sources = []
                    self.parent.after(0, self._remove_thinking)
                    self.parent.after(0, self._prepare_streaming_message, sources)
                else:
                    # Found relevant documents
                    self.parent.after(0, self._update_thinking, "✨ Generating response...")
                    
                    sources = [r.get('filename', 'Unknown') for r in results]
                    context = "\n\n".join([r.get('content', '')[:800] for r in results])
                    
                    prompt = f"""You are **NeuroVault** 🧠, an intelligent, enthusiastic, and highly capable AI assistant!

📚 **Context from User's Documents:**
{context}

❓ **User's Question:** {query}

---

## 📋 Response Guidelines:

### Structure & Formatting:
- Start with a clear, direct answer to their question
- Use **bold text** for key terms, names, and important concepts
- Use bullet points (• or -) to list multiple items clearly
- If the answer is detailed, use section headers (## or ###)
- Add relevant emojis naturally for visual appeal ✨

### Content Quality:
- Be comprehensive but concise - don't ramble
- Cite specific details from the documents when possible
- If the context partially answers the question, explain what you found AND what's missing
- Be enthusiastic and helpful, like you genuinely want to help!

### Tone:
- Professional yet friendly
- Confident but not arrogant
- Encouraging and supportive

### Example Good Formatting:
**Key Finding** 🎯
Here's what I found in your documents:

• **First point** - Explanation here
• **Second point** - More details
• **Third point** - Additional info

💡 **Pro tip:** Additional helpful context

---

Now provide a beautifully formatted, comprehensive response:"""
                    
                    self.parent.after(0, self._remove_thinking)
                    self.parent.after(0, self._prepare_streaming_message, sources)
            
            # Small delay to let UI update
            import time
            time.sleep(0.1)
            
            # Stream the response
            full_response = ""
            for chunk in get_ai_response_stream(prompt, max_tokens=800):
                full_response += chunk
                self.parent.after(0, self._update_streaming_text, chunk)
            
            # Track AI response in history
            self.history_manager.add_message("assistant", full_response)
            
            # Finalize the message
            self.parent.after(0, self._finalize_streaming_message)
            
        except Exception as e:
            self.parent.after(0, self._remove_thinking)
            self.parent.after(0, self.add_ai_message, f"Sorry, I encountered an error: {str(e)}")
            show_toast(f"Error: {str(e)}", "error", 4000)
        finally:
            self.parent.after(0, self._enable_input)
    
    def _prepare_streaming_message(self, sources):
        """Prepare UI for streaming message"""
        self.streaming_sources = sources
        
        msg_container = ctk.CTkFrame(
            self.chat_frame,
            fg_color="transparent"
        )
        msg_container.pack(fill="x", pady=12, padx=8)
        self.streaming_container = msg_container
        
        # Header row with avatar and name
        header_row = ctk.CTkFrame(msg_container, fg_color="transparent")
        header_row.pack(anchor="w", pady=(0, 8))
        
        avatar = ctk.CTkLabel(
            header_row,
            text="🧠",
            font=('Segoe UI', 20),
            text_color=COLORS['accent_primary']
        )
        avatar.pack(side="left", padx=(0, 10))
        
        name_label = ctk.CTkLabel(
            header_row,
            text="NeuroVault",
            font=('Segoe UI', 13, 'bold'),
            text_color=COLORS['text_primary']
        )
        name_label.pack(side="left")
        
        # Message content area with rich text support
        content_frame = ctk.CTkFrame(
            msg_container,
            fg_color=COLORS.get('ai_message', COLORS['bg_tertiary']),
            corner_radius=12,
            border_width=1,
            border_color=COLORS.get('ai_message_border', COLORS['border'])
        )
        content_frame.pack(anchor="w", fill="x", padx=(30, 60))
        
        # Use RichTextDisplay for beautiful formatting
        self.streaming_rich_text = RichTextDisplay(
            content_frame,
            width=600,
            height=80,
            fg_color=COLORS.get('ai_message', COLORS['bg_tertiary'])
        )
        self.streaming_rich_text.pack(padx=16, pady=12, anchor="w", fill="x")
        self.streaming_text = ""
        
        self._scroll_to_bottom()
    
    def _update_streaming_text(self, chunk):
        """Update streaming text with new chunk"""
        if hasattr(self, 'streaming_rich_text') and self.streaming_rich_text:
            self.streaming_text += chunk
            # During streaming, just append raw text (formatting applied at end)
            self.streaming_rich_text.textbox.configure(state="normal")
            self.streaming_rich_text.textbox.insert("end", chunk)
            self.streaming_rich_text.textbox.configure(state="disabled")
            self.streaming_rich_text._auto_resize()
            self._scroll_to_bottom()
    
    def _finalize_streaming_message(self):
        """Finalize the streaming message with rich formatting and sources"""
        # Apply rich formatting to the complete message
        if hasattr(self, 'streaming_rich_text') and self.streaming_rich_text:
            self.streaming_rich_text.apply_formatting()
        
        if hasattr(self, 'streaming_sources') and self.streaming_sources:
            sources_frame = ctk.CTkFrame(self.streaming_container, fg_color="transparent")
            sources_frame.pack(anchor="w", padx=(30, 60), pady=(8, 0))
            
            sources_label = ctk.CTkLabel(
                sources_frame,
                text=f"📚 Sources: {', '.join(self.streaming_sources[:3])}",
                font=('Segoe UI', 10),
                text_color=COLORS['text_muted']
            )
            sources_label.pack(anchor="w")
        
        self.streaming_rich_text = None
        self.streaming_text = ""
        self._scroll_to_bottom()
    
    def _show_ai_thinking(self, message):
        """Show AI thinking indicator"""
        self.thinking_frame = ctk.CTkFrame(
            self.chat_frame,
            fg_color="transparent"
        )
        self.thinking_frame.pack(fill="x", pady=12, padx=8)
        
        # AI indicator row
        indicator_row = ctk.CTkFrame(self.thinking_frame, fg_color="transparent")
        indicator_row.pack(anchor="w")
        
        # AI avatar
        avatar = ctk.CTkLabel(
            indicator_row,
            text="🧠",
            font=('Segoe UI', 20),
            text_color=COLORS['accent_primary']
        )
        avatar.pack(side="left", padx=(0, 12))
        
        # Thinking message with animated dots
        self.thinking_label = ctk.CTkLabel(
            indicator_row,
            text=message,
            font=('Segoe UI', 12),
            text_color=COLORS['text_muted']
        )
        self.thinking_label.pack(side="left")
        
        # Animated spinner
        self.current_spinner = LoadingSpinner(
            self.thinking_frame,
            message="",
            style='dots',
            show_message=False
        )
        
        self._scroll_to_bottom()
    
    def _update_thinking(self, message):
        """Update thinking message"""
        if hasattr(self, 'thinking_label'):
            self.thinking_label.configure(text=message)
    
    def _remove_thinking(self):
        """Remove thinking indicator"""
        if self.current_spinner:
            self.current_spinner.stop()
            self.current_spinner = None
        if hasattr(self, 'thinking_frame'):
            try:
                self.thinking_frame.destroy()
            except:
                pass
    
    def add_user_message(self, message):
        """Add user message with modern right-aligned bubble"""
        msg_container = ctk.CTkFrame(
            self.chat_frame,
            fg_color="transparent"
        )
        msg_container.pack(fill="x", pady=12, padx=8)
        
        # Right-aligned content
        content_row = ctk.CTkFrame(msg_container, fg_color="transparent")
        content_row.pack(anchor="e")
        
        # Message bubble
        bubble = ctk.CTkFrame(
            content_row,
            fg_color=COLORS.get('user_message', COLORS['accent_primary']),
            corner_radius=18
        )
        bubble.pack(side="right")
        
        # Message text
        msg_label = ctk.CTkLabel(
            bubble,
            text=message,
            font=('Segoe UI', 12),
            text_color="#ffffff",
            wraplength=500,
            justify="left"
        )
        msg_label.pack(padx=18, pady=12)
        
        self._scroll_to_bottom()
    
    def add_ai_message(self, message, sources=None):
        """Add AI message with ChatGPT-style formatting and typewriter effect"""
        msg_container = ctk.CTkFrame(
            self.chat_frame,
            fg_color="transparent"
        )
        msg_container.pack(fill="x", pady=12, padx=8)
        
        # Header row with avatar and name
        header_row = ctk.CTkFrame(msg_container, fg_color="transparent")
        header_row.pack(anchor="w", pady=(0, 8))
        
        # AI Avatar
        avatar = ctk.CTkLabel(
            header_row,
            text="🧠",
            font=('Segoe UI', 20),
            text_color=COLORS['accent_primary']
        )
        avatar.pack(side="left", padx=(0, 10))
        
        # AI Name
        name_label = ctk.CTkLabel(
            header_row,
            text="NeuroVault",
            font=('Segoe UI', 13, 'bold'),
            text_color=COLORS['text_primary']
        )
        name_label.pack(side="left")
        
        # Message content area
        content_frame = ctk.CTkFrame(
            msg_container,
            fg_color=COLORS.get('ai_message', COLORS['bg_tertiary']),
            corner_radius=12,
            border_width=1,
            border_color=COLORS.get('ai_message_border', COLORS['border'])
        )
        content_frame.pack(anchor="w", fill="x", padx=(30, 60))
        
        # Message text with typewriter effect
        msg_label = ctk.CTkLabel(
            content_frame,
            text="",
            font=('Segoe UI', 12),
            text_color=COLORS['text_primary'],
            wraplength=600,
            justify="left",
            anchor="w"
        )
        msg_label.pack(padx=20, pady=16, anchor="w", fill="x")
        
        # Start typewriter animation
        self.current_typewriter = TypewriterText(
            msg_label,
            message,
            speed_ms=12,
            on_complete=lambda: self._on_message_complete(sources, msg_container)
        )
        
        self._scroll_to_bottom()
    
    def _on_message_complete(self, sources, container):
        """Called when typewriter animation completes"""
        if sources:
            # Add sources section
            sources_frame = ctk.CTkFrame(container, fg_color="transparent")
            sources_frame.pack(anchor="w", padx=(30, 60), pady=(8, 0))
            
            sources_label = ctk.CTkLabel(
                sources_frame,
                text=f"📚 Sources: {', '.join(sources[:3])}",
                font=('Segoe UI', 10),
                text_color=COLORS['text_muted']
            )
            sources_label.pack(anchor="w")
        
        self._scroll_to_bottom()
    
    def _enable_input(self):
        """Re-enable input after response"""
        self.send_btn.configure(state="normal", fg_color=COLORS['accent_primary'])
    
    def _scroll_to_bottom(self):
        """Scroll chat to bottom"""
        try:
            self.chat_frame._parent_canvas.yview_moveto(1.0)
        except:
            pass
    
    # ============== Voice Input Methods ==============
    
    def start_voice_input(self):
        """Start voice input in background thread"""
        if hasattr(self, 'mic_btn'):
            self.mic_btn.configure(state="disabled", text="⏸️", fg_color=COLORS['accent_primary'])
        
        show_toast("🎤 Listening...", "info", 2000)
        
        thread = threading.Thread(target=self._capture_voice)
        thread.daemon = True
        thread.start()
    
    def _capture_voice(self):
        """Capture voice in background thread"""
        try:
            text = listen_and_transcribe(timeout=5, phrase_time_limit=15)
            
            if text:
                self.parent.after(0, self._insert_voice_text, text)
                self.parent.after(0, lambda: show_toast("✅ Voice captured!", "success", 2000))
            else:
                self.parent.after(0, lambda: show_toast("❌ Couldn't hear you. Try again.", "error", 2000))
        except Exception as e:
            self.parent.after(0, lambda: show_toast(f"❌ Voice error: {str(e)}", "error", 2000))
        finally:
            self.parent.after(0, self._reset_mic_button)
    
    def _insert_voice_text(self, text):
        """Insert captured voice text into input"""
        current = self.input_entry.get()
        if current:
            self.input_entry.delete(0, 'end')
            self.input_entry.insert(0, current + " " + text)
        else:
            self.input_entry.insert(0, text)
    
    def _reset_mic_button(self):
        """Reset mic button state"""
        if hasattr(self, 'mic_btn'):
            self.mic_btn.configure(state="normal", text="🎤", fg_color=COLORS['bg_secondary'])
    
    # ============== Chat History Methods ==============
    
    def clear_chat(self):
        """Clear current chat"""
        # Clear all messages from chat frame
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        
        # Reset history manager
        self.history_manager.clear()
        
        # Show welcome message again
        self.show_welcome_message()
        show_toast("🗑️ Chat cleared", "info", 2000)
    
    def show_save_dialog(self):
        """Show save chat dialog"""
        if self.history_manager.get_message_count() == 0:
            show_toast("No messages to save", "warning", 2000)
            return
        
        # Create dialog window
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Save Chat")
        dialog.geometry("400x180")
        dialog.transient(self.parent.winfo_toplevel())
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = self.parent.winfo_toplevel().winfo_x() + (self.parent.winfo_toplevel().winfo_width() // 2) - 200
        y = self.parent.winfo_toplevel().winfo_y() + (self.parent.winfo_toplevel().winfo_height() // 2) - 90
        dialog.geometry(f"+{x}+{y}")
        
        dialog.configure(fg_color=COLORS['bg_primary'])
        
        # Title
        title_label = ctk.CTkLabel(
            dialog,
            text="💾 Save Conversation",
            font=('Segoe UI', 16, 'bold'),
            text_color=COLORS['text_primary']
        )
        title_label.pack(pady=(20, 16))
        
        # Title entry
        title_entry = ctk.CTkEntry(
            dialog,
            placeholder_text="Enter chat title...",
            width=300,
            height=40,
            fg_color=COLORS['bg_tertiary'],
            text_color=COLORS['text_primary']
        )
        title_entry.pack(pady=(0, 20))
        title_entry.insert(0, self.history_manager.generate_title())
        
        # Buttons
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack()
        
        def do_save():
            title = title_entry.get().strip()
            if not title:
                title = self.history_manager.generate_title()
            
            messages_json = self.history_manager.to_json()
            session_id = save_chat_session(title, messages_json)
            
            show_toast(f"✅ Chat saved!", "success", 2000)
            dialog.destroy()
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Save",
            command=do_save,
            width=120,
            fg_color=COLORS['accent_primary'],
            hover_color=COLORS['accent_hover']
        )
        save_btn.pack(side="left", padx=8)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            width=120,
            fg_color=COLORS['bg_tertiary'],
            hover_color=COLORS['text_muted']
        )
        cancel_btn.pack(side="left", padx=8)
    
    def show_load_dialog(self):
        """Show load chat dialog"""
        sessions = list_chat_sessions()
        
        if not sessions:
            show_toast("No saved chats found", "info", 2000)
            return
        
        # Create dialog window
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Load Chat")
        dialog.geometry("450x400")
        dialog.transient(self.parent.winfo_toplevel())
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = self.parent.winfo_toplevel().winfo_x() + (self.parent.winfo_toplevel().winfo_width() // 2) - 225
        y = self.parent.winfo_toplevel().winfo_y() + (self.parent.winfo_toplevel().winfo_height() // 2) - 200
        dialog.geometry(f"+{x}+{y}")
        
        dialog.configure(fg_color=COLORS['bg_primary'])
        
        # Title
        title_label = ctk.CTkLabel(
            dialog,
            text="📂 Load Conversation",
            font=('Segoe UI', 16, 'bold'),
            text_color=COLORS['text_primary']
        )
        title_label.pack(pady=(20, 16))
        
        # Sessions list
        list_frame = ctk.CTkScrollableFrame(
            dialog,
            fg_color=COLORS['bg_secondary'],
            width=400,
            height=280
        )
        list_frame.pack(padx=20, pady=(0, 20))
        
        def load_session(session_id):
            session = load_chat_session(session_id)
            if session:
                _, title, created_at, messages_json = session
                
                # Clear current chat
                self.clear_chat()
                
                # Load messages
                self.history_manager.from_json(messages_json)
                
                # Display messages
                for msg in self.history_manager.get_messages():
                    if msg.get('role') == 'user':
                        self.add_user_message(msg.get('content', ''))
                    else:
                        self.add_ai_message(msg.get('content', ''))
                
                show_toast(f"✅ Loaded: {title}", "success", 2000)
                dialog.destroy()
        
        def delete_session(session_id, row_frame):
            delete_chat_session(session_id)
            row_frame.destroy()
            show_toast("🗑️ Chat deleted", "info", 2000)
        
        for session_id, title, created_at in sessions:
            row = ctk.CTkFrame(list_frame, fg_color=COLORS['bg_tertiary'], corner_radius=8)
            row.pack(fill="x", pady=4, padx=4)
            
            # Title and date
            info_frame = ctk.CTkFrame(row, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=12, pady=8)
            
            title_lbl = ctk.CTkLabel(
                info_frame,
                text=title[:40] + "..." if len(title) > 40 else title,
                font=('Segoe UI', 12, 'bold'),
                text_color=COLORS['text_primary'],
                anchor="w"
            )
            title_lbl.pack(anchor="w")
            
            date_lbl = ctk.CTkLabel(
                info_frame,
                text=created_at,
                font=('Segoe UI', 10),
                text_color=COLORS['text_muted'],
                anchor="w"
            )
            date_lbl.pack(anchor="w")
            
            # Buttons
            btn_frame = ctk.CTkFrame(row, fg_color="transparent")
            btn_frame.pack(side="right", padx=8)
            
            load_btn = ctk.CTkButton(
                btn_frame,
                text="📂",
                command=lambda sid=session_id: load_session(sid),
                width=36,
                height=32,
                fg_color=COLORS['accent_primary'],
                hover_color=COLORS['accent_hover']
            )
            load_btn.pack(side="left", padx=2)
            
            del_btn = ctk.CTkButton(
                btn_frame,
                text="🗑️",
                command=lambda sid=session_id, r=row: delete_session(sid, r),
                width=36,
                height=32,
                fg_color=COLORS.get('error', '#ef4444'),
                hover_color="#dc2626"
            )
            del_btn.pack(side="left", padx=2)
        
        # Close button
        close_btn = ctk.CTkButton(
            dialog,
            text="Close",
            command=dialog.destroy,
            width=120,
            fg_color=COLORS['bg_tertiary'],
            hover_color=COLORS['text_muted']
        )
        close_btn.pack(pady=(0, 20))
