"""
Search interface for NeuroVault
Handles chat-like search UI
"""

import customtkinter as ctk
import tkinter as tk
from embeddings import search_documents

class SearchFrame(ctk.CTkFrame):
    """Search interface widget"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.search_results = []
        self.setup_ui()
    
    def setup_ui(self):
        """Build search UI"""
        # Title
        title = ctk.CTkLabel(
            self, 
            text="🔍 Search Your Knowledge", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(20,10), padx=20, anchor="w")
        
        # Search input
        search_container = ctk.CTkFrame(self)
        search_container.pack(pady=10, padx=20, fill="x")
        
        self.search_entry = ctk.CTkEntry(
            search_container,
            placeholder_text="Ask anything about your uploaded files...",
            height=40
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0,10))
        
        self.search_btn = ctk.CTkButton(
            search_container,
            text="🔎 Search",
            command=self.perform_search,
            width=100
        )
        self.search_btn.pack(side="right")
        
        # Bind Enter key
        self.search_entry.bind('<Return>', lambda e: self.perform_search())
        
        # Results area
        results_label = ctk.CTkLabel(
            self,
            text="Search Results:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        results_label.pack(pady=(20,10), padx=20, anchor="w")
        
        # Results listbox
        results_container = ctk.CTkFrame(self)
        results_container.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.results_listbox = tk.Listbox(
            results_container,
            height=10,
            font=("Consolas", 11),
            bg="#2b2b2b",
            fg="#ffffff",
            selectbackground="#1f538d"
        )
        scrollbar = tk.Scrollbar(results_container, command=self.results_listbox.yview)
        self.results_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.results_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind result selection
        self.results_listbox.bind('<<ListboxSelect>>', self.on_result_select)
        
        # Result preview
        preview_label = ctk.CTkLabel(
            self,
            text="Selected Result Preview:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        preview_label.pack(pady=(10,5), padx=20, anchor="w")
        
        self.preview_text = tk.Text(
            self,
            height=6,
            font=("Consolas", 10),
            bg="#2b2b2b",
            fg="#ffffff",
            wrap=tk.WORD
        )
        self.preview_text.pack(pady=(0,20), padx=20, fill="both", expand=True)
    
    def perform_search(self):
        """Execute search"""
        query = self.search_entry.get().strip()
        
        if not query:
            return
        
        # Show loading
        self.results_listbox.delete(0, tk.END)
        self.results_listbox.insert(tk.END, "🔄 Searching your knowledge...")
        self.update()
        
        # Search ChromaDB
        results = search_documents(query, top_k=5)
        
        # Display results
        self.results_listbox.delete(0, tk.END)
        self.search_results = results
        
        if not results:
            self.results_listbox.insert(tk.END, "❌ No results found. Try different search terms.")
            self.preview_text.delete("1.0", tk.END)
            return
        
        for i, result in enumerate(results):
            score_pct = int(result['similarity'] * 100)
            display = f"[{score_pct}%] {result['source']} - {result['text'][:50]}..."
            self.results_listbox.insert(tk.END, display)
    
    def on_result_select(self, event):
        """Show selected result preview"""
        selection = self.results_listbox.curselection()
        if not selection or not self.search_results:
            return
        
        idx = selection[0]
        result = self.search_results[idx]
        
        preview = f"📄 Source: {result['source']}\n"
        preview += f"🎯 Relevance: {int(result['similarity'] * 100)}%\n"
        preview += f"━━━━━━━━━━━━━━━━━━━\n\n"
        preview += result['text']
        
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert("1.0", preview)
