import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import customtkinter as ctk
from PIL import Image
from files_ui import FilesTab
from search_ui import SearchTab
from chat_ui import ChatTab
from styles import COLORS, FRAME_STYLES, TAB_STYLES, TEXT_STYLES, CURRENT_THEME, save_theme
from ui_components import init_toast_manager, show_toast

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NeuroVault(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("⚡ NeuroVault - AI Second Brain")
        self.geometry("1200x800")
        self.minsize(1000, 600)
        self.configure(fg_color=COLORS['bg_primary'])
        
        self.current_theme = CURRENT_THEME
        
        # Initialize global toast manager
        init_toast_manager(self)
        
        self.create_header()
        self.create_main_content()
        
    def create_header(self):
        """Create modern header with theme toggle"""
        header = ctk.CTkFrame(
            self,
            height=80,
            fg_color=COLORS['bg_secondary'],
            corner_radius=0
        )
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        # Logo and title on left
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", padx=30, pady=15)
        
        # Load and display logo image
        logo_path = Path(__file__).parent.parent / 'assets' / 'logo.png'
        if logo_path.exists():
            logo_image = ctk.CTkImage(
                light_image=Image.open(logo_path),
                dark_image=Image.open(logo_path),
                size=(50, 50)
            )
            logo_label = ctk.CTkLabel(
                title_frame,
                image=logo_image,
                text=""
            )
            logo_label.pack(side="left", padx=(0, 12))
        else:
            # Fallback to text logo if image not found
            logo_container = ctk.CTkFrame(
                title_frame, 
                fg_color=COLORS['bg_tertiary'], 
                corner_radius=8, 
                width=50, 
                height=50
            )
            logo_container.pack(side="left", padx=(0, 12))
            logo_container.pack_propagate(False)
            
            logo = ctk.CTkLabel(
                logo_container,
                text="N",
                font=('Segoe UI', 24, 'bold'),
                text_color=COLORS['accent_primary']
            )
            logo.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title text
        title_text_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        title_text_frame.pack(side="left")
        
        title = ctk.CTkLabel(
            title_text_frame,
            text="NeuroVault",
            font=TEXT_STYLES['title'],
            text_color=COLORS['accent_primary']
        )
        title.pack(anchor="w")
        
        tagline = ctk.CTkLabel(
            title_text_frame,
            text="Your AI-Powered Second Brain",
            font=TEXT_STYLES['caption'],
            text_color=COLORS['text_secondary']
        )
        tagline.pack(anchor="w")
        
        # Controls on right
        controls_frame = ctk.CTkFrame(header, fg_color="transparent")
        controls_frame.pack(side="right", padx=30, pady=15)
        
        # Theme toggle button with current theme indicator
        theme_icon = "🌙" if self.current_theme == "dark" else "☀️"
        theme_text = f"{theme_icon} Theme"
        
        theme_btn = ctk.CTkButton(
            controls_frame,
            text=theme_text,
            command=self.toggle_theme,
            width=90,
            height=36,
            corner_radius=8,
            fg_color=COLORS['bg_tertiary'],
            hover_color=COLORS['bg_hover'],
            text_color=COLORS['text_secondary'],
            border_width=1,
            border_color=COLORS['border_medium'],
            font=TEXT_STYLES['body_small']
        )
        theme_btn.pack(side="left", padx=5)
        
        # Version badge
        version = ctk.CTkLabel(
            controls_frame,
            text="v3.0",
            font=TEXT_STYLES['caption'],
            text_color=COLORS['text_tertiary'],
            fg_color=COLORS['bg_tertiary'],
            corner_radius=6,
            padx=12,
            pady=4
        )
        version.pack(side="left", padx=5)
        
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        import os
        
        # Determine new theme
        new_theme = 'light' if self.current_theme == 'dark' else 'dark'
        new_theme_name = 'Light Mode ☀️' if new_theme == 'light' else 'Dark Mode 🌙'
        
        # Show toast notification
        show_toast(f"Switching to {new_theme_name}...", "info", 2000)
        
        # Save new theme preference
        save_theme(new_theme)
        
        # Restart the app after brief delay to show toast
        def restart():
            self.destroy()
            python = sys.executable
            os.execl(python, python, *sys.argv)
        
        self.after(800, restart)
        
    def create_main_content(self):
        """Create main content area with tabs"""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        self.tabview = ctk.CTkTabview(
            container,
            **TAB_STYLES,
            corner_radius=12,
            border_width=1,
            border_color=COLORS['border_medium']
        )
        self.tabview.pack(fill="both", expand=True)
        
        self.tabview.add("Files")
        self.tabview.add("Search")
        self.tabview.add("Chat")
        
        FilesTab(self.tabview.tab("Files"))
        SearchTab(self.tabview.tab("Search"))
        ChatTab(self.tabview.tab("Chat"))

if __name__ == "__main__":
    app = NeuroVault()
    app.mainloop()
