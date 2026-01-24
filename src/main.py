import sys
from pathlib import Path
# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

import customtkinter as ctk
from files_ui import FilesTab
from search_ui import SearchTab
from chat_ui import ChatTab
from styles import COLORS, FRAME_STYLES, TAB_STYLES, TEXT_STYLES

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NeuroVault(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("🧠 NeuroVault - AI Second Brain")
        self.geometry("1200x800")
        self.minsize(1000, 600)
        
        # Configure window background
        self.configure(fg_color=COLORS['bg_primary'])
        
        # Create UI
        self.create_header()
        self.create_main_content()
        
    def create_header(self):
        """Create modern header with gradient effect"""
        header = ctk.CTkFrame(
            self,
            height=80,
            fg_color=COLORS['bg_secondary'],
            corner_radius=0
        )
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        # Title with emoji and tagline
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", padx=30, pady=15)
        
        title = ctk.CTkLabel(
            title_frame,
            text="🧠 NeuroVault",
            font=TEXT_STYLES['title'],
            text_color=COLORS['accent_primary']
        )
        title.pack(anchor="w")
        
        tagline = ctk.CTkLabel(
            title_frame,
            text="Your AI-Powered Second Brain",
            font=TEXT_STYLES['caption'],  # Changed from 'small'
            text_color=COLORS['text_secondary']
        )
        tagline.pack(anchor="w")
        
        # Version badge
        version = ctk.CTkLabel(
            header,
            text="v2.0",
            font=TEXT_STYLES['caption'],  # Changed from 'small'
            text_color=COLORS['text_tertiary'],  # Also update this color
            fg_color=COLORS['bg_tertiary'],
            corner_radius=6,
            padx=12,
            pady=4
        )
        version.pack(side="right", padx=30)
        
    def create_main_content(self):
        """Create main content area with tabs"""
        # Main container with padding
        container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        container.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        # Create tabview with modern styling
        self.tabview = ctk.CTkTabview(
            container,
            **TAB_STYLES,
            corner_radius=12,
            border_width=1,
            border_color=COLORS['border_medium']
        )
        self.tabview.pack(fill="both", expand=True)
        
        # Add tabs with icons
        self.tabview.add("Files")
        self.tabview.add("Search")
        self.tabview.add("Chat")
        
        # Initialize tab content
        files_tab = FilesTab(self.tabview.tab("Files"))
        search_tab = SearchTab(self.tabview.tab("Search"))
        chat_tab = ChatTab(self.tabview.tab("Chat"))

if __name__ == "__main__":
    app = NeuroVault()
    app.mainloop()
