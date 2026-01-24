import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import customtkinter as ctk
from embeddings import search_documents
from styles import COLORS, BUTTON_STYLES, FRAME_STYLES, TEXT_STYLES, INPUT_STYLES

class SearchTab:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(fg_color=COLORS['bg_primary'])
        
        # Track expanded cards
        self.expanded_cards = {}
        
        # Create modern layout
        self.create_search_bar()
        self.create_results_area()
        
    def create_search_bar(self):
        """Premium search bar"""
        search_container = ctk.CTkFrame(
            self.parent,
            fg_color='transparent'
        )
        search_container.pack(fill="x", padx=30, pady=(30, 20))
        
        # Title with icon
        title_frame = ctk.CTkFrame(search_container, fg_color='transparent')
        title_frame.pack(anchor="w", pady=(0, 20))
        
        title = ctk.CTkLabel(
            title_frame,
            text="🔍  Semantic Search",
            font=TEXT_STYLES['title'],
            text_color=COLORS['text_primary']
        )
        title.pack(side="left")
        
        subtitle = ctk.CTkLabel(
            title_frame,
            text="  Find anything in your knowledge base",
            font=TEXT_STYLES['caption'],
            text_color=COLORS['text_tertiary']
        )
        subtitle.pack(side="left", padx=(10, 0))
        
        # Search input row
        input_container = ctk.CTkFrame(
            search_container,
            **FRAME_STYLES['card']
        )
        input_container.pack(fill="x")
        
        input_row = ctk.CTkFrame(input_container, fg_color='transparent')
        input_row.pack(fill="x", padx=15, pady=12)
        
        # Search entry
        self.search_entry = ctk.CTkEntry(
            input_row,
            placeholder_text="What would you like to know?",
            **INPUT_STYLES
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.search_entry.bind("<Return>", lambda e: self.perform_search())
        
        # Search button
        search_btn = ctk.CTkButton(
            input_row,
            text="Search",
            command=self.perform_search,
            **BUTTON_STYLES['primary'],
            width=120
        )
        search_btn.pack(side="right")
        
    def create_results_area(self):
        """Premium results display"""
        results_container = ctk.CTkFrame(
            self.parent,
            fg_color='transparent'
        )
        results_container.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        # Scrollable results
        self.results_frame = ctk.CTkScrollableFrame(
            results_container,
            fg_color='transparent',
            scrollbar_button_color=COLORS['accent_primary'],
            scrollbar_button_hover_color=COLORS['accent_hover']
        )
        self.results_frame.pack(fill="both", expand=True)
        
        # Initial empty state
        self.show_empty_state()
        
    def show_empty_state(self):
        """Clean empty state"""
        empty_container = ctk.CTkFrame(
            self.results_frame,
            fg_color='transparent'
        )
        empty_container.pack(expand=True, pady=80)
        
        icon = ctk.CTkLabel(
            empty_container,
            text="🔎",
            font=('Segoe UI', 48),
            text_color=COLORS['text_dim']
        )
        icon.pack()
        
        text = ctk.CTkLabel(
            empty_container,
            text="Start searching to find relevant content",
            font=TEXT_STYLES['body'],
            text_color=COLORS['text_tertiary']
        )
        text.pack(pady=(10, 0))
        
    def perform_search(self):
        """Perform semantic search"""
        query = self.search_entry.get().strip()
        
        if not query:
            return
            
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        self.expanded_cards = {}
            
        try:
            # Perform search
            results = search_documents(query, top_k=5)
            
            if not results:
                # No results
                self.show_no_results(query)
                return
                
            # Results header
            header = ctk.CTkLabel(
                self.results_frame,
                text=f"Found {len(results)} result{'s' if len(results) != 1 else ''} for '{query}'",
                font=TEXT_STYLES['body'],
                text_color=COLORS['text_secondary'],
                anchor="w"
            )
            header.pack(anchor="w", pady=(10, 20), padx=15)
            
            # Display results
            for i, result in enumerate(results):
                self.create_result_card(i, result)
                
        except Exception as e:
            self.show_error(str(e))
            
    def create_result_card(self, index, result):
        """Premium expandable result card"""
        filename = result.get('filename', 'Unknown')
        content = result.get('content', '')
        score = result.get('score', 0)
        card_id = f"card_{index}"
        
        # Main card container
        card = ctk.CTkFrame(
            self.results_frame,
            **FRAME_STYLES['card']
        )
        card.pack(fill="x", pady=10, padx=5)
        
        # Header (clickable area)
        header = ctk.CTkFrame(
            card,
            fg_color='transparent'
        )
        header.pack(fill="x", padx=15, pady=12)
        
        # Bind click to entire header
        header.bind("<Button-1>", lambda e: self.toggle_card(card_id, card, content))
        
        # Title row
        title_row = ctk.CTkFrame(header, fg_color='transparent')
        title_row.pack(fill="x")
        title_row.bind("<Button-1>", lambda e: self.toggle_card(card_id, card, content))
        
        # Number
        number = ctk.CTkLabel(
            title_row,
            text=f"{index + 1}.",
            font=TEXT_STYLES['caption'],
            text_color=COLORS['text_dim'],
            width=30
        )
        number.pack(side="left")
        number.bind("<Button-1>", lambda e: self.toggle_card(card_id, card, content))
        
        # Filename
        filename_label = ctk.CTkLabel(
            title_row,
            text=f"📄  {filename}",
            font=TEXT_STYLES['heading'],
            text_color=COLORS['text_primary'],
            cursor="hand2"
        )
        filename_label.pack(side="left")
        filename_label.bind("<Button-1>", lambda e: self.toggle_card(card_id, card, content))
        
        # Expand icon
        expand_icon = ctk.CTkLabel(
            title_row,
            text="▼ Click to expand",
            font=TEXT_STYLES['caption'],
            text_color=COLORS['text_tertiary'],
            cursor="hand2"
        )
        expand_icon.pack(side="right")
        expand_icon.bind("<Button-1>", lambda e: self.toggle_card(card_id, card, content))
        
        # Meta row
        meta_row = ctk.CTkFrame(header, fg_color='transparent')
        meta_row.pack(fill="x", pady=(8, 0))
        meta_row.bind("<Button-1>", lambda e: self.toggle_card(card_id, card, content))
        
        # Score badge
        score_badge = ctk.CTkLabel(
            meta_row,
            text=f"Relevance: {score:.1%}",
            font=TEXT_STYLES['caption'],
            text_color=COLORS['accent_primary'],
            fg_color=COLORS['bg_hover'],
            corner_radius=6,
            padx=10,
            pady=3
        )
        score_badge.pack(side="left", padx=(30, 0))
        score_badge.bind("<Button-1>", lambda e: self.toggle_card(card_id, card, content))
        
        # Store references
        self.expanded_cards[card_id] = {
            'expanded': False,
            'content_frame': None,
            'icon': expand_icon,
            'content': content
        }
        
    def toggle_card(self, card_id, card, content):
        """Toggle card expansion"""
        card_data = self.expanded_cards[card_id]
        
        if card_data['expanded']:
            # Collapse
            if card_data['content_frame']:
                card_data['content_frame'].destroy()
            card_data['icon'].configure(text="▶")
            card_data['expanded'] = False
        else:
            # Expand
            content_frame = ctk.CTkFrame(
                card,
                fg_color=COLORS['bg_secondary'],
                corner_radius=8
            )
            content_frame.pack(fill="x", padx=15, pady=(0, 15))
            
            content_text = ctk.CTkTextbox(
                content_frame,
                fg_color='transparent',
                text_color=COLORS['text_secondary'],
                font=TEXT_STYLES['body_small'],
                wrap="word",
                height=150
            )
            content_text.pack(fill="both", padx=15, pady=15)
            content_text.insert("1.0", content)
            content_text.configure(state="disabled")
            
            card_data['content_frame'] = content_frame
            card_data['icon'].configure(text="▼")
            card_data['expanded'] = True
            
    def show_no_results(self, query):
        """No results state"""
        container = ctk.CTkFrame(self.results_frame, fg_color='transparent')
        container.pack(expand=True, pady=80)
        
        icon = ctk.CTkLabel(
            container,
            text="❌",
            font=('Segoe UI', 48),
            text_color=COLORS['text_dim']
        )
        icon.pack()
        
        text = ctk.CTkLabel(
            container,
            text=f"No results found for '{query}'",
            font=TEXT_STYLES['subtitle'],
            text_color=COLORS['text_secondary']
        )
        text.pack(pady=(10, 0))
        
        hint = ctk.CTkLabel(
            container,
            text="Try different keywords or upload more documents",
            font=TEXT_STYLES['caption'],
            text_color=COLORS['text_tertiary']
        )
        hint.pack(pady=(5, 0))
        
    def show_error(self, error):
        """Error state"""
        container = ctk.CTkFrame(self.results_frame, fg_color='transparent')
        container.pack(expand=True, pady=80)
        
        icon = ctk.CTkLabel(
            container,
            text="⚠️",
            font=('Segoe UI', 48),
            text_color=COLORS['error']
        )
        icon.pack()
        
        text = ctk.CTkLabel(
            container,
            text=f"Search error: {error}",
            font=TEXT_STYLES['body'],
            text_color=COLORS['error']
        )
        text.pack(pady=(10, 0))
