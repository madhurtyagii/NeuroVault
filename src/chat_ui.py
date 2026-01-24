import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import customtkinter as ctk
import threading
from embeddings import search_documents
from ai_model import get_ai_response
from styles import COLORS, BUTTON_STYLES, FRAME_STYLES, TEXT_STYLES, INPUT_STYLES

class AnimatedLabel(ctk.CTkLabel):
    """Label with fade-in animation"""
    def __init__(self, parent, text, **kwargs):
        super().__init__(parent, text=text, **kwargs)
        self.alpha = 0
        self.animate_in()
    
    def animate_in(self):
        """Smooth fade-in animation"""
        if self.alpha < 1:
            self.alpha += 0.1
            self.after(20, self.animate_in)

class LoadingSpinner:
    """Rotating loading spinner animation"""
    FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(anchor="w", pady=5, padx=10)
        
        self.label = ctk.CTkLabel(
            self.frame,
            text="",
            font=TEXT_STYLES['heading'],
            text_color=COLORS['accent_primary']
        )
        self.label.pack(side="left", padx=5)
        
        self.current_frame = 0
        self.is_spinning = True
        self.animate()
    
    def animate(self):
        """Animate the spinner"""
        if self.is_spinning:
            self.label.configure(text=self.FRAMES[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.FRAMES)
            self.parent.after(100, self.animate)
    
    def stop(self):
        """Stop the spinner"""
        self.is_spinning = False
        try:
            self.frame.destroy()
        except:
            pass

class ToastNotification:
    """Toast notification for success/error messages"""
    def __init__(self, parent, message, notification_type="info", duration=3000):
        self.parent = parent
        self.duration = duration
        
        colors = {
            "success": COLORS['success'],
            "error": COLORS['error'],
            "warning": COLORS['warning'],
            "info": COLORS['info']
        }
        bg_color = colors.get(notification_type, COLORS['info'])
        
        self.toast_frame = ctk.CTkFrame(
            parent,
            fg_color=bg_color,
            corner_radius=8,
            height=50
        )
        self.toast_frame.pack(side="bottom", fill="x", padx=20, pady=(10, 20))
        
        ctk.CTkLabel(
            self.toast_frame,
            text=message,
            font=TEXT_STYLES['body'],
            text_color=COLORS['bg_primary'],
            wraplength=400,
            justify="left"
        ).pack(padx=15, pady=10)
        
        self.parent.after(duration, self.dismiss)
    
    def dismiss(self):
        try:
            self.toast_frame.destroy()
        except:
            pass

class ChatTab:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(fg_color=COLORS['bg_primary'])
        self.current_spinner = None
        
        self.create_chat_display()
        self.create_input_area()
        self.show_welcome_message()
    
    def create_chat_display(self):
        chat_container = ctk.CTkFrame(self.parent, **FRAME_STYLES['card'])
        chat_container.pack(fill="both", expand=True, padx=20, pady=(20, 10))
        
        self.chat_frame = ctk.CTkScrollableFrame(
            chat_container,
            fg_color="transparent",
            scrollbar_button_color=COLORS['accent_primary'],
            scrollbar_button_hover_color=COLORS['accent_hover']
        )
        self.chat_frame.pack(fill="both", expand=True, padx=15, pady=15)
    
    def create_input_area(self):
        input_container = ctk.CTkFrame(
            self.parent,
            fg_color=COLORS['bg_tertiary'],
            corner_radius=12,
            border_width=1,
            border_color=COLORS['border']
        )
        input_container.pack(fill="x", padx=20, pady=(0, 20))
        
        input_row = ctk.CTkFrame(input_container, fg_color="transparent")
        input_row.pack(fill="both", padx=15, pady=15)
        
        # FIXED: No duplicate height!
        self.input_entry = ctk.CTkEntry(
            input_row,
            placeholder_text="Ask a question about your documents...",
            **INPUT_STYLES
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", lambda e: self.send_message())
        
        self.send_btn = ctk.CTkButton(
            input_row,
            text="📤 Send",
            command=self.send_message,
            **BUTTON_STYLES['primary'],
            width=100
        )
        self.send_btn.pack(side="right")
    
    def show_welcome_message(self):
        welcome_frame = ctk.CTkFrame(
            self.chat_frame,
            fg_color=COLORS['bg_secondary'],
            corner_radius=10,
            border_width=1,
            border_color=COLORS['accent_primary']
        )
        welcome_frame.pack(fill="x", pady=10, padx=10)
        
        AnimatedLabel(
            welcome_frame,
            text="🤖 Welcome to NeuroVault Chat!\n\nAsk me anything about your uploaded documents.\nI'll search through your knowledge base and provide accurate answers with sources.",
            font=TEXT_STYLES['body'],
            text_color=COLORS['text_primary'],
            justify="left"
        ).pack(padx=20, pady=20)
    
    def send_message(self):
        query = self.input_entry.get().strip()
        if not query:
            ToastNotification(self.parent, "⚠️ Please enter a question!", "warning")
            return
        
        self.input_entry.delete(0, 'end')
        self.send_btn.configure(state="disabled", text="⏳ Thinking...")
        self.add_user_message(query)
        
        thread = threading.Thread(target=self.get_ai_response_threaded, args=(query,))
        thread.daemon = True
        thread.start()
    
    def get_ai_response_threaded(self, query):
        try:
            self.parent.after(0, self.show_loading_spinner, "🔍 Searching documents...")
            results = search_documents(query, top_k=3)
            
            if not results:
                self.parent.after(0, self.remove_loading_spinner)
                self.parent.after(0, self.show_toast, "❌ No documents found", "error")
                self.parent.after(0, self.add_ai_message, "❌ No relevant documents found. Please upload documents first!")
                self.parent.after(0, self.enable_send_button)
                return
            
            self.parent.after(0, self.remove_loading_spinner)
            self.parent.after(0, self.show_loading_spinner, "🤖 Generating answer...")
            
            sources_text = "📚 Sources:\n" + "\n".join([
                f"📄 {r.get('filename', 'Unknown')} (relevance: {r.get('score', 0):.2f})"
                for r in results
            ])
            self.parent.after(0, self.add_system_message, sources_text)
            
            context = "\n\n".join([r.get('content', '')[:500] for r in results])
            prompt = f"""Answer the user's question based ONLY on the provided context from their documents.

Context from documents:

{context}

User question: {query}

Provide a clear, accurate answer based on the context. If the context doesn't contain enough information, say so."""
            
            response = get_ai_response(prompt, max_tokens=500)
            
            self.parent.after(0, self.remove_loading_spinner)
            self.parent.after(0, self.add_ai_message, response)
            self.parent.after(0, self.show_toast, "✅ Response generated!", "success")
            
        except Exception as e:
            self.parent.after(0, self.remove_loading_spinner)
            self.parent.after(0, self.add_ai_message, f"❌ Error: {str(e)}")
            self.parent.after(0, self.show_toast, f"Error: {str(e)}", "error")
        finally:
            self.parent.after(0, self.enable_send_button)
    
    def show_loading_spinner(self, message):
        spinner_container = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        spinner_container.pack(anchor="w", pady=5, padx=10, fill="x")
        
        ctk.CTkLabel(
            spinner_container,
            text=message,
            font=TEXT_STYLES['small'],
            text_color=COLORS['text_muted']
        ).pack(anchor="w")
        
        self.current_spinner = LoadingSpinner(spinner_container)
        self.current_spinner.parent = spinner_container
        self.chat_frame._parent_canvas.yview_moveto(1.0)
    
    def remove_loading_spinner(self):
        if self.current_spinner:
            try:
                self.current_spinner.stop()
                self.current_spinner = None
            except:
                pass
    
    def add_user_message(self, message):
        msg_frame = ctk.CTkFrame(self.chat_frame, fg_color=COLORS['accent_primary'], corner_radius=10)
        msg_frame.pack(anchor="e", pady=5, padx=10, fill="x", expand=False)
        
        ctk.CTkLabel(
            msg_frame,
            text=f"👤 You\n\n{message}",
            font=TEXT_STYLES['body'],
            text_color=COLORS['bg_primary'],
            justify="left",
            wraplength=700,
            anchor="w"
        ).pack(padx=15, pady=10, anchor="w")
        self.chat_frame._parent_canvas.yview_moveto(1.0)
    
    def add_ai_message(self, message):
        msg_frame = ctk.CTkFrame(
            self.chat_frame,
            fg_color=COLORS['bg_secondary'],
            corner_radius=10,
            border_width=1,
            border_color=COLORS['border']
        )
        msg_frame.pack(anchor="w", pady=5, padx=10, fill="x", expand=False)
        
        AnimatedLabel(
            msg_frame,
            text=f"🤖 NeuroVault\n\n{message}",
            font=TEXT_STYLES['body'],
            text_color=COLORS['text_primary'],
            justify="left",
            wraplength=700,
            anchor="w"
        ).pack(padx=15, pady=10, anchor="w")
        self.chat_frame._parent_canvas.yview_moveto(1.0)
    
    def add_system_message(self, message):
        AnimatedLabel(
            self.chat_frame,
            text=message,
            font=TEXT_STYLES['small'],
            text_color=COLORS['text_muted'],
            justify="left",
            anchor="w"
        ).pack(anchor="w", pady=2, padx=15)
        self.chat_frame._parent_canvas.yview_moveto(1.0)
    
    def show_toast(self, message, notification_type="info"):
        ToastNotification(self.parent, message, notification_type)
    
    def enable_send_button(self):
        self.send_btn.configure(state="normal", text="📤 Send")
