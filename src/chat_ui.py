import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import customtkinter as ctk
import threading
from embeddings import search_documents
from ai_model import get_ai_response
from styles import COLORS, BUTTON_STYLES, FRAME_STYLES, TEXT_STYLES, INPUT_STYLES

class ChatTab:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(fg_color=COLORS['bg_primary'])
        
        # Create modern layout
        self.create_chat_display()
        self.create_input_area()
        
        # Show welcome message
        self.show_welcome_message()
        
    def create_chat_display(self):
        """Modern chat display area"""
        # Container
        chat_container = ctk.CTkFrame(
            self.parent,
            **FRAME_STYLES['card']
        )
        chat_container.pack(fill="both", expand=True, padx=20, pady=(20, 10))
        
        # Scrollable chat area
        self.chat_frame = ctk.CTkScrollableFrame(
            chat_container,
            fg_color="transparent",
            scrollbar_button_color=COLORS['accent_primary'],
            scrollbar_button_hover_color=COLORS['accent_hover']
        )
        self.chat_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
    def create_input_area(self):
        """Modern input area with send button"""
        input_container = ctk.CTkFrame(
            self.parent,
            fg_color=COLORS['bg_tertiary'],
            corner_radius=12,
            border_width=1,
            border_color=COLORS['border_medium']
        )
        input_container.pack(fill="x", padx=20, pady=(0, 20))
        
        # Input row
        input_row = ctk.CTkFrame(input_container, fg_color="transparent")
        input_row.pack(fill="both", padx=15, pady=15)
        
        # Text input
        self.input_entry = ctk.CTkEntry(
            input_row,
            placeholder_text="Ask a question about your documents...",
            **INPUT_STYLES
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", lambda e: self.send_message())
        
        # Send button
        self.send_btn = ctk.CTkButton(
            input_row,
            text="📤 Send",
            command=self.send_message,
            **BUTTON_STYLES['primary'],
            width=100
        )
        self.send_btn.pack(side="right")
        
    def show_welcome_message(self):
        """Show welcome message"""
        welcome_frame = ctk.CTkFrame(
            self.chat_frame,
            fg_color=COLORS['bg_secondary'],
            corner_radius=10,
            border_width=1,
            border_color=COLORS['accent_primary']
        )
        welcome_frame.pack(fill="x", pady=10, padx=10)
        
        welcome_text = ctk.CTkLabel(
            welcome_frame,
            text="🤖 Welcome to NeuroVault Chat!\n\nAsk me anything about your uploaded documents.\nI'll search through your knowledge base and provide accurate answers with sources.",
            font=TEXT_STYLES['body'],
            text_color=COLORS['text_primary'],
            justify="left"
        )
        welcome_text.pack(padx=20, pady=20)
        
    def send_message(self):
        """Send user message and get AI response"""
        query = self.input_entry.get().strip()
        
        if not query:
            return
            
        # Clear input
        self.input_entry.delete(0, 'end')
        
        # Disable send button
        self.send_btn.configure(state="disabled", text="⏳ Thinking...")
        
        # Display user message
        self.add_user_message(query)
        
        # Get response in background thread
        thread = threading.Thread(target=self.get_ai_response_threaded, args=(query,))
        thread.daemon = True
        thread.start()
        
    def get_ai_response_threaded(self, query):
        """Get AI response in background thread"""
        try:
            # Show searching message
            self.parent.after(0, self.add_system_message, "🔍 Searching your documents...")
            
            # Search for relevant documents
            results = search_documents(query, top_k=3)
            
            if not results:
                self.parent.after(0, self.add_ai_message, "❌ No relevant documents found. Please upload documents first!")
                self.parent.after(0, self.enable_send_button)
                return
                
            # Show sources
            sources_text = "📚 Sources:\n" + "\n".join([
                f"📄 {r.get('filename', 'Unknown')} (relevance: {r.get('score', 0):.2f})"
                for r in results
            ])
            self.parent.after(0, self.add_system_message, sources_text)
            
            # Prepare context from search results
            context = "\n\n".join([r.get('content', '')[:500] for r in results])
            
            # Create prompt
            prompt = f"""Answer the user's question based ONLY on the provided context from their documents.

            Context from documents:
            {context}

            User question: {query}

            Format your response clearly using:
            - Use numbered lists (1. 2. 3.) for sequential points
            - Use bullet points (- or •) for non-sequential items
            - Add a header line ending with : before grouped information
            - Keep paragraphs concise (2-3 sentences max)
            - Use line breaks between sections

            Provide a clear, well-structured answer. If the context doesn't contain enough information, say so."""
            
            # Show generating message
            self.parent.after(0, self.add_system_message, "🤖 Generating answer...")
            
            # Get AI response
            response = get_ai_response(prompt, max_tokens=500)
            
            # Display AI response
            self.parent.after(0, self.add_ai_message, response)
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.parent.after(0, self.add_ai_message, error_msg)
            
        finally:
            # Re-enable send button
            self.parent.after(0, self.enable_send_button)
            
    def add_user_message(self, message):
        """Add user message bubble"""
        msg_frame = ctk.CTkFrame(
            self.chat_frame,
            fg_color=COLORS['accent_primary'],
            corner_radius=10
        )
        msg_frame.pack(anchor="e", pady=5, padx=10, fill="x", expand=False)
        
        msg_label = ctk.CTkLabel(
            msg_frame,
            text=f"👤 You\n\n{message}",
            font=TEXT_STYLES['body'],
            text_color='#ffffff',
            justify="left",
            wraplength=700,
            anchor="w"
        )
        msg_label.pack(padx=15, pady=10, anchor="w")
        
        self.chat_frame._parent_canvas.yview_moveto(1.0)
        
    def add_ai_message(self, message):
        """Add AI message bubble with formatting"""
        msg_frame = ctk.CTkFrame(
            self.chat_frame,
            fg_color=COLORS['bg_secondary'],
            corner_radius=10,
            border_width=1,
            border_color=COLORS['border_subtle']
        )
        msg_frame.pack(anchor="w", pady=5, padx=10, fill="x", expand=False)
        
        # Header with icon
        header = ctk.CTkLabel(
            msg_frame,
            text="🤖 NeuroVault",
            font=TEXT_STYLES['heading'],
            text_color=COLORS['accent_primary'],
            anchor="w"
        )
        header.pack(anchor="w", padx=15, pady=(10, 5))
        
        # Parse and render formatted content
        self.render_formatted_text(msg_frame, message)
        
        self.chat_frame._parent_canvas.yview_moveto(1.0)
        
    def render_formatted_text(self, parent, text):
        """Render text with enhanced Markdown-like formatting"""
        lines = text.split('\n')
        
        content_frame = ctk.CTkFrame(parent, fg_color='transparent')
        content_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if not line:
                i += 1
                continue
            
            # **Bold headers** or *Bold:*
            if (line.startswith('**') and line.endswith('**')) or (line.startswith('*') and line.endswith('*')):
                # Remove ** or *
                clean_line = line.replace('**', '').replace('*', '')
                
                label = ctk.CTkLabel(
                    content_frame,
                    text=clean_line,
                    font=TEXT_STYLES['subtitle'],
                    text_color=COLORS['text_primary'],
                    anchor="w",
                    justify="left"
                )
                label.pack(anchor="w", pady=(12, 4))
            
            # Headers ending with : (but not bullets)
            elif line.endswith(':') and len(line) < 70 and not line.startswith('-') and not line.startswith('*'):
                label = ctk.CTkLabel(
                    content_frame,
                    text=line,
                    font=TEXT_STYLES['heading'],
                    text_color=COLORS['accent_primary'],
                    anchor="w",
                    justify="left"
                )
                label.pack(anchor="w", pady=(10, 4))
            
            # Numbered lists (1. 2. 3.)
            elif len(line) > 2 and line[0].isdigit() and line[1] in ['.', ')']:
                # Extract number and text
                sep = '.' if '.' in line[:4] else ')'
                parts = line.split(sep, 1)
                
                if len(parts) == 2:
                    num, txt = parts
                    txt = txt.strip()
                    
                    list_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
                    list_frame.pack(anchor="w", pady=3, fill="x")
                    
                    # Number badge
                    num_label = ctk.CTkLabel(
                        list_frame,
                        text=f"{num}",
                        font=TEXT_STYLES['body'],
                        text_color='#ffffff',
                        fg_color=COLORS['accent_primary'],
                        corner_radius=4,
                        width=28,
                        height=28
                    )
                    num_label.pack(side="left", anchor="n", pady=2)
                    
                    # Text
                    text_label = ctk.CTkLabel(
                        list_frame,
                        text=txt,
                        font=TEXT_STYLES['body'],
                        text_color=COLORS['text_primary'],
                        anchor="w",
                        justify="left",
                        wraplength=630
                    )
                    text_label.pack(side="left", fill="x", expand=True, padx=(10, 0))
            
            # Bullet points (- or * or •)
            elif line.startswith('- ') or line.startswith('* ') or line.startswith('• '):
                txt = line[2:].strip()
                
                bullet_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
                bullet_frame.pack(anchor="w", pady=3, fill="x")
                
                # Bullet
                bullet_label = ctk.CTkLabel(
                    bullet_frame,
                    text="●",
                    font=('Segoe UI', 14, 'bold'),
                    text_color=COLORS['accent_primary'],
                    width=28,
                    anchor="center"
                )
                bullet_label.pack(side="left", anchor="n")
                
                # Text
                text_label = ctk.CTkLabel(
                    bullet_frame,
                    text=txt,
                    font=TEXT_STYLES['body'],
                    text_color=COLORS['text_primary'],
                    anchor="w",
                    justify="left",
                    wraplength=630
                )
                text_label.pack(side="left", fill="x", expand=True, padx=(10, 0))
            
            # Regular paragraph
            else:
                # Handle inline **bold**
                if '**' in line:
                    # For now, just show as is (advanced: split and render separately)
                    pass
                
                label = ctk.CTkLabel(
                    content_frame,
                    text=line,
                    font=TEXT_STYLES['body'],
                    text_color=COLORS['text_secondary'],
                    anchor="w",
                    justify="left",
                    wraplength=680
                )
                label.pack(anchor="w", pady=4)
            
            i += 1
        
    def add_system_message(self, message):
        """Add system message (non-bubble)"""
        msg_label = ctk.CTkLabel(
            self.chat_frame,
            text=message,
            font=TEXT_STYLES['caption'],
            text_color=COLORS['text_tertiary'],
            justify="left",
            anchor="w"
        )
        msg_label.pack(anchor="w", pady=2, padx=15)
        
        self.chat_frame._parent_canvas.yview_moveto(1.0)
        
    def enable_send_button(self):
        """Re-enable send button"""
        self.send_btn.configure(state="normal", text="📤 Send")
