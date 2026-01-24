import customtkinter as ctk
import tkinter as tk
from threading import Thread
import time

class ChatFrame(ctk.CTkFrame):
    """AI Chat interface for querying documents"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.setup_ui()
        self.chat_history = []
    
    def setup_ui(self):
        """Build chat interface"""
        # Header
        header = ctk.CTkLabel(
            self, 
            text="💬 Chat with Your Knowledge Base",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.pack(pady=(10,5))
        
        subtitle = ctk.CTkLabel(
            self,
            text="Ask questions about your uploaded documents - AI will search and answer",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle.pack(pady=(0,10))
        
        # Chat display area (FIXED HEIGHT)
        chat_container = ctk.CTkFrame(self, height=400)
        chat_container.pack(fill="both", expand=True, padx=20, pady=(0,10))
        chat_container.pack_propagate(False)  # IMPORTANT: Prevent resizing
        
        # Chat history text box
        self.chat_display = tk.Text(
            chat_container,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            bg="#1a1a1a",
            fg="#ffffff",
            padx=15,
            pady=15,
            state="disabled",
            spacing1=5,
            spacing3=5
        )
        
        scrollbar = tk.Scrollbar(chat_container, command=self.chat_display.yview)
        self.chat_display.configure(yscrollcommand=scrollbar.set)
        
        self.chat_display.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure text tags for styling
        self.chat_display.tag_config("user", foreground="#4a9eff", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("ai", foreground="#00ff88", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("context", foreground="#999999", font=("Segoe UI", 10, "italic"))
        self.chat_display.tag_config("timestamp", foreground="#666666", font=("Segoe UI", 9))
        
        # Input area (FIXED AT BOTTOM)
        input_frame = ctk.CTkFrame(self, height=100)
        input_frame.pack(fill="x", padx=20, pady=(0,10))
        input_frame.pack_propagate(False)  # IMPORTANT: Keep fixed height
        
        self.input_box = ctk.CTkTextbox(
            input_frame,
            height=70,
            font=ctk.CTkFont(size=13),
            wrap="word"
        )
        self.input_box.pack(side="left", fill="both", expand=True, padx=(0,10), pady=5)
        self.input_box.bind("<Return>", self.on_enter)
        self.input_box.bind("<Shift-Return>", lambda e: None)
        
        # Send button
        self.send_btn = ctk.CTkButton(
            input_frame,
            text="Send 🚀",
            command=self.send_message,
            width=100,
            height=70,
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.send_btn.pack(side="right", pady=5)
        
        # Status label (ALWAYS VISIBLE AT BOTTOM)
        self.status_label = ctk.CTkLabel(
            self,
            text="💡 Tip: Ask specific questions about your documents for best results",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            height=25
        )
        self.status_label.pack(pady=(0,5), fill="x", padx=20)
        
        # Add welcome message
        self.add_system_message(
            "👋 Welcome! Upload documents in the Files tab, then ask me questions here. "
            "I'll search through your knowledge base and provide accurate answers with sources."
        )
    
    def on_enter(self, event):
        """Handle Enter key press"""
        if not event.state & 0x1:  # Check if Shift is NOT pressed
            self.send_message()
            return "break"  # Prevent newline insertion
    
    def send_message(self):
        """Send user message and get AI response"""
        query = self.input_box.get("1.0", "end-1c").strip()
        
        if not query:
            return
        
        # Clear input
        self.input_box.delete("1.0", "end")
        
        # Add user message
        self.add_user_message(query)
        
        # Disable send while processing
        self.send_btn.configure(state="disabled", text="Thinking...")
        self.status_label.configure(text="🔍 Searching your documents...")
        
        # Process in background thread
        Thread(target=self.process_query, args=(query,), daemon=True).start()
    
    def process_query(self, query):
        """Process query with RAG and stream response"""
        try:
            from embeddings import search_documents
            from ai_model import get_ai_response
            
            # Search for relevant context
            results = search_documents(query, top_k=3)
            
            if not results:
                self.add_ai_message(
                    "❌ I couldn't find any relevant information in your knowledge base. "
                    "Try uploading some documents first!"
                )
                self.reset_ui()
                return
            
            # Build context from search results
            context_parts = []
            sources = []
            
            for i, result in enumerate(results, 1):
                context_parts.append(f"[Source {i}] {result['text']}")
                sources.append(f"📄 {result['filename']} (relevance: {result['distance']:.2f})")
            
            context = "\n\n".join(context_parts)
            
            # Show sources
            self.add_context_message(
                f"Found {len(results)} relevant passages:\n" + "\n".join(sources)
            )
            
            # Get AI response
            self.status_label.configure(text="🤖 Generating answer...")
            
            prompt = f"""You are a helpful AI assistant. Answer the user's question based ONLY on the provided context from their documents.

Context from documents:
{context}

User question: {query}

Instructions:
- Answer directly and concisely
- Use information from the context above
- If the context doesn't contain enough information, say so
- Cite sources by mentioning document names when relevant

Answer:"""
            
            response = get_ai_response(prompt)
            
            # Stream the response
            self.stream_ai_message(response)
            
        except Exception as e:
            self.add_ai_message(f"❌ Error: {str(e)}")
            print(f"Chat error: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.reset_ui()
    
    def add_user_message(self, message):
        """Add user message to chat"""
        self.chat_display.configure(state="normal")
        
        timestamp = time.strftime("%H:%M")
        
        self.chat_display.insert("end", f"\n🙋 You ", "user")
        self.chat_display.insert("end", f"({timestamp})\n", "timestamp")
        self.chat_display.insert("end", f"{message}\n")
        
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
    
    def add_ai_message(self, message):
        """Add AI message to chat"""
        self.chat_display.configure(state="normal")
        
        timestamp = time.strftime("%H:%M")
        
        self.chat_display.insert("end", f"\n🤖 AI Assistant ", "ai")
        self.chat_display.insert("end", f"({timestamp})\n", "timestamp")
        self.chat_display.insert("end", f"{message}\n")
        
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
    
    def stream_ai_message(self, message):
        """Stream AI message word by word"""
        self.chat_display.configure(state="normal")
        
        timestamp = time.strftime("%H:%M")
        
        self.chat_display.insert("end", f"\n🤖 AI Assistant ", "ai")
        self.chat_display.insert("end", f"({timestamp})\n", "timestamp")
        
        # Stream words
        words = message.split()
        for word in words:
            self.chat_display.insert("end", word + " ")
            self.chat_display.see("end")
            self.chat_display.update()
            time.sleep(0.03)  # Typing effect
        
        self.chat_display.insert("end", "\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
    
    def add_context_message(self, message):
        """Add context/system message"""
        self.chat_display.configure(state="normal")
        
        self.chat_display.insert("end", f"\n📚 Sources:\n", "context")
        self.chat_display.insert("end", f"{message}\n", "context")
        
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
    
    def add_system_message(self, message):
        """Add system message"""
        self.chat_display.configure(state="normal")
        
        self.chat_display.insert("end", f"\n💡 System:\n{message}\n")
        
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
    
    def reset_ui(self):
        """Reset UI after response"""
        self.send_btn.configure(state="normal", text="Send 🚀")
        self.status_label.configure(
            text="💡 Tip: Ask specific questions about your documents for best results"
        )
