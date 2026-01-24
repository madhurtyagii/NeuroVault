import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from database import add_document, get_all_documents, delete_document
from parser import parse_file
from embeddings import add_document_to_db, delete_document_from_db
from styles import COLORS, BUTTON_STYLES, FRAME_STYLES, TEXT_STYLES, INPUT_STYLES

class FilesTab:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(fg_color=COLORS['bg_primary'])
        
        # Create modern layout
        self.create_header()
        self.create_files_list()
        self.load_files()
        
    def create_header(self):
        """Modern header with upload button"""
        header = ctk.CTkFrame(self.parent, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        # Title
        title = ctk.CTkLabel(
            header,
            text="Your Knowledge Base",
            font=TEXT_STYLES['subtitle'],
            text_color=COLORS['text_primary']
        )
        title.pack(side="left")
        
        # Upload button (primary style)
        upload_btn = ctk.CTkButton(
            header,
            text="📤 Upload File",
            command=self.upload_file,
            **BUTTON_STYLES['primary']
        )
        upload_btn.pack(side="right")
        
    def create_files_list(self):
        """Modern card-based file list"""
        # Container frame
        list_container = ctk.CTkFrame(
            self.parent,
            **FRAME_STYLES['card']
        )
        list_container.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        # Scrollable frame for files
        self.scroll_frame = ctk.CTkScrollableFrame(
            list_container,
            fg_color="transparent",
            scrollbar_button_color=COLORS['accent_primary'],
            scrollbar_button_hover_color=COLORS['accent_hover']
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
    def load_files(self):
        """Load and display files as modern cards"""
        # Clear existing
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        files = get_all_documents()
        
        if not files:
            # Empty state
            empty_label = ctk.CTkLabel(
                self.scroll_frame,
                text="📂 No files yet\n\nUpload your first document to get started!",
                font=TEXT_STYLES['body'],
                text_color=COLORS['text_tertiary'],
                justify="center"
            )
            empty_label.pack(pady=100)
            return
            
        # Display each file as a card
        for doc_id, filename, upload_date, word_count in files:
            self.create_file_card(doc_id, filename, upload_date, word_count)
            
    def create_file_card(self, doc_id, filename, upload_date, word_count):
        """Create modern file card"""
        card = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=COLORS['bg_secondary'],
            corner_radius=10,
            border_width=1,
            border_color=COLORS['border_subtle']
        )
        card.pack(fill="x", pady=8, padx=5)
        
        # Content frame
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=12)
        
        # Left side - File info
        info_frame = ctk.CTkFrame(content, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        # Filename
        name_label = ctk.CTkLabel(
            info_frame,
            text=f"📄 {filename}",
            font=TEXT_STYLES['heading'],
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        # Metadata
        meta_text = f"📅 {upload_date}  •  📊 {word_count:,} words"
        meta_label = ctk.CTkLabel(
            info_frame,
            text=meta_text,
            font=TEXT_STYLES['caption'],
            text_color=COLORS['text_secondary'],
            anchor="w"
        )
        meta_label.pack(anchor="w", pady=(4, 0))
        
        # Right side - Actions
        actions = ctk.CTkFrame(content, fg_color="transparent")
        actions.pack(side="right")
        
        # Delete button
        delete_btn = ctk.CTkButton(
            actions,
            text="🗑️ Delete",
            command=lambda: self.delete_file(doc_id, filename),
            **BUTTON_STYLES['danger'],
            width=100
        )
        delete_btn.pack()
        
    def upload_file(self):
        """Upload file with modern feedback"""
        filepath = filedialog.askopenfilename(
            title="Select File",
            filetypes=[
                ("All Supported", "*.txt *.pdf *.docx *.py"),
                ("Text Files", "*.txt"),
                ("PDF Files", "*.pdf"),
                ("Word Documents", "*.docx"),
                ("Python Files", "*.py")
            ]
        )
        
        if not filepath:
            return
            
        try:
            # Parse file
            content, word_count = parse_file(filepath)
            filename = os.path.basename(filepath)
            
            # Add to database
            doc_id = add_document(filename, content, word_count)
            
            # Add to vector store
            add_document_to_db(doc_id, filename, content)
            
            # Success message
            messagebox.showinfo(
                "Success ✅",
                f"Uploaded: {filename}\n{word_count:,} words indexed"
            )
            
            self.load_files()
            
        except Exception as e:
            messagebox.showerror("Error ❌", f"Upload failed:\n{str(e)}")
            
    def delete_file(self, doc_id, filename):
        """Delete file with confirmation"""
        if messagebox.askyesno(
            "Confirm Delete",
            f"Delete '{filename}'?\n\nThis cannot be undone."
        ):
            try:
                delete_document(doc_id)
                delete_document_from_db(doc_id)
                messagebox.showinfo("Success ✅", f"Deleted: {filename}")
                self.load_files()
            except Exception as e:
                messagebox.showerror("Error ❌", f"Delete failed:\n{str(e)}")
