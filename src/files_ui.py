import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import customtkinter as ctk
from tkinter import filedialog
import os
import threading
from database import (
    add_document, get_all_documents, delete_document, get_document_by_id,
    add_tag_to_file, get_file_tags, get_all_tags, get_files_by_tag,
    save_summary, get_summary
)
from parser import parse_file
from embeddings import add_document_to_db, delete_document_from_db
from styles import COLORS, BUTTON_STYLES, FRAME_STYLES, TEXT_STYLES, INPUT_STYLES
from ui_components import show_toast, LoadingSpinner, AnimatedFrame
from tags_manager import tags_manager
from document_tools import summarize_document, compare_documents


class FilesTab:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(fg_color=COLORS['bg_primary'])
        self.selected_files = {}  # {doc_id: checkbox_var}
        self.current_filter_tag = None
        
        # Create modern layout
        self.create_header()
        self.create_files_list()
        self.load_files()
        
    def create_header(self):
        """Modern header with upload button and controls"""
        header = ctk.CTkFrame(self.parent, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        # Left: Title
        title = ctk.CTkLabel(
            header,
            text="Your Knowledge Base",
            font=TEXT_STYLES['subtitle'],
            text_color=COLORS['text_primary']
        )
        title.pack(side="left")
        
        # Right: Buttons
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right")
        
        # Tag filter dropdown
        self.tag_filter_var = ctk.StringVar(value="All Tags")
        self.tag_filter = ctk.CTkOptionMenu(
            btn_frame,
            variable=self.tag_filter_var,
            values=["All Tags"],
            command=self.filter_by_tag,
            width=120,
            height=32,
            fg_color=COLORS['bg_tertiary'],
            button_color=COLORS['accent_primary'],
            button_hover_color=COLORS['accent_hover']
        )
        self.tag_filter.pack(side="left", padx=(0, 10))
        self.refresh_tag_filter()
        
        # Compare button (disabled by default)
        self.compare_btn = ctk.CTkButton(
            btn_frame,
            text="⚖️ Compare",
            command=self.compare_selected,
            **BUTTON_STYLES.get('secondary', {'fg_color': COLORS['bg_tertiary']}),
            width=100,
            state="disabled"
        )
        self.compare_btn.pack(side="left", padx=(0, 10))
        
        # Upload button
        upload_btn = ctk.CTkButton(
            btn_frame,
            text="📤 Upload File",
            command=self.show_upload_dialog,
            **BUTTON_STYLES['primary']
        )
        upload_btn.pack(side="left")
        
    def refresh_tag_filter(self):
        """Refresh tag filter dropdown with all tags"""
        all_tags = get_all_tags()
        tag_names = ["All Tags"] + [tag[0] for tag in all_tags]
        self.tag_filter.configure(values=tag_names)
        
    def filter_by_tag(self, selected_tag):
        """Filter files by selected tag"""
        if selected_tag == "All Tags":
            self.current_filter_tag = None
        else:
            self.current_filter_tag = selected_tag
        self.load_files()
        
    def create_files_list(self):
        """Modern card-based file list"""
        list_container = ctk.CTkFrame(
            self.parent,
            **FRAME_STYLES['card']
        )
        list_container.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
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
        self.selected_files = {}
            
        # Get files (filtered or all)
        if self.current_filter_tag:
            files = get_files_by_tag(self.current_filter_tag)
        else:
            files = get_all_documents()
        
        if not files:
            empty_label = ctk.CTkLabel(
                self.scroll_frame,
                text="📂 No files yet\n\nUpload your first document to get started!",
                font=TEXT_STYLES['body'],
                text_color=COLORS['text_tertiary'],
                justify="center"
            )
            empty_label.pack(pady=100)
            return
            
        for i, (doc_id, filename, upload_date, word_count) in enumerate(files):
            self.create_file_card(doc_id, filename, upload_date, word_count, delay=i * 50)
            
    def create_file_card(self, doc_id, filename, upload_date, word_count, delay=0):
        """Create modern file card with selection and actions"""
        card = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=COLORS['bg_secondary'],
            corner_radius=10,
            border_width=1,
            border_color=COLORS['border_subtle']
        )
        
        def show_card():
            card.pack(fill="x", pady=8, padx=5)
        
        if delay > 0:
            self.parent.after(delay, show_card)
        else:
            show_card()
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=12)
        
        # Left side - Checkbox + File info
        left_frame = ctk.CTkFrame(content, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Top row: checkbox + filename
        top_row = ctk.CTkFrame(left_frame, fg_color="transparent")
        top_row.pack(fill="x")
        
        # Checkbox for selection
        checkbox_var = ctk.BooleanVar(value=False)
        checkbox = ctk.CTkCheckBox(
            top_row,
            text="",
            variable=checkbox_var,
            command=lambda: self.toggle_selection(doc_id, checkbox_var),
            width=24,
            checkbox_width=20,
            checkbox_height=20
        )
        checkbox.pack(side="left", padx=(0, 10))
        self.selected_files[doc_id] = checkbox_var
        
        # Filename
        name_label = ctk.CTkLabel(
            top_row,
            text=f"📄 {filename}",
            font=TEXT_STYLES['heading'],
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        name_label.pack(side="left")
        
        # Tags row
        tags = get_file_tags(doc_id)
        if tags:
            tags_row = ctk.CTkFrame(left_frame, fg_color="transparent")
            tags_row.pack(fill="x", pady=(4, 0))
            
            for tag_name, tag_color in tags[:5]:  # Max 5 tags displayed
                tag_badge = ctk.CTkLabel(
                    tags_row,
                    text=tag_name,
                    font=('Segoe UI', 10),
                    text_color="#ffffff",
                    fg_color=tag_color or COLORS['accent_primary'],
                    corner_radius=10,
                    padx=8,
                    pady=2
                )
                tag_badge.pack(side="left", padx=(0, 5))
        
        # Metadata row
        meta_text = f"📅 {upload_date}  •  📊 {word_count:,} words"
        meta_label = ctk.CTkLabel(
            left_frame,
            text=meta_text,
            font=TEXT_STYLES['caption'],
            text_color=COLORS['text_secondary'],
            anchor="w"
        )
        meta_label.pack(anchor="w", pady=(4, 0))
        
        # Right side - Actions
        actions = ctk.CTkFrame(content, fg_color="transparent")
        actions.pack(side="right")
        
        # Summarize button
        summarize_btn = ctk.CTkButton(
            actions,
            text="📝",
            command=lambda: self.summarize_file(doc_id, filename),
            width=36,
            height=32,
            corner_radius=8,
            fg_color=COLORS['bg_tertiary'],
            hover_color=COLORS['accent_hover'],
            text_color=COLORS['text_primary']
        )
        summarize_btn.pack(side="left", padx=(0, 5))
        
        # Delete button
        delete_btn = ctk.CTkButton(
            actions,
            text="🗑️",
            command=lambda: self.delete_file(doc_id, filename),
            width=36,
            height=32,
            corner_radius=8,
            fg_color=COLORS.get('error', '#ef4444'),
            hover_color="#dc2626",
            text_color="#ffffff"
        )
        delete_btn.pack(side="left")
        
    def toggle_selection(self, doc_id, checkbox_var):
        """Toggle file selection and update compare button"""
        selected_count = sum(1 for var in self.selected_files.values() if var.get())
        
        if selected_count == 2:
            self.compare_btn.configure(state="normal", fg_color=COLORS['accent_primary'])
        else:
            self.compare_btn.configure(state="disabled", fg_color=COLORS['bg_tertiary'])
            
    def summarize_file(self, doc_id, filename):
        """Summarize a document using AI"""
        # Check for cached summary first
        cached_summary = get_summary(doc_id)
        if cached_summary:
            self.show_summary_popup(filename, cached_summary, from_cache=True)
            return
        
        show_toast("⏳ Generating summary...", "info", 2000)
        
        # Run in background thread
        def generate():
            try:
                doc = get_document_by_id(doc_id)
                if doc:
                    content = doc[2]  # content field
                    summary = summarize_document(content)
                    
                    # Cache the summary
                    save_summary(doc_id, summary)
                    
                    self.parent.after(0, lambda: self.show_summary_popup(filename, summary))
                    self.parent.after(0, lambda: show_toast("✅ Summary generated!", "success", 2000))
            except Exception as e:
                self.parent.after(0, lambda: show_toast(f"❌ Error: {str(e)}", "error", 3000))
        
        thread = threading.Thread(target=generate, daemon=True)
        thread.start()
        
    def show_summary_popup(self, filename, summary, from_cache=False):
        """Display summary in a popup window"""
        popup = ctk.CTkToplevel(self.parent)
        popup.title(f"📝 Summary: {filename}")
        popup.geometry("600x400")
        popup.configure(fg_color=COLORS['bg_primary'])
        popup.transient(self.parent.winfo_toplevel())
        popup.grab_set()
        
        # Center
        popup.update_idletasks()
        x = self.parent.winfo_toplevel().winfo_x() + (self.parent.winfo_toplevel().winfo_width() // 2) - 300
        y = self.parent.winfo_toplevel().winfo_y() + (self.parent.winfo_toplevel().winfo_height() // 2) - 200
        popup.geometry(f"+{x}+{y}")
        
        # Header
        header = ctk.CTkLabel(
            popup,
            text=f"📝 Document Summary" + (" (cached)" if from_cache else ""),
            font=('Segoe UI', 16, 'bold'),
            text_color=COLORS['text_primary']
        )
        header.pack(pady=(20, 10))
        
        # Filename
        file_label = ctk.CTkLabel(
            popup,
            text=f"📄 {filename}",
            font=('Segoe UI', 12),
            text_color=COLORS['text_secondary']
        )
        file_label.pack(pady=(0, 15))
        
        # Summary text
        text_frame = ctk.CTkFrame(popup, fg_color=COLORS['bg_secondary'], corner_radius=10)
        text_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        text_box = ctk.CTkTextbox(
            text_frame,
            fg_color="transparent",
            text_color=COLORS['text_primary'],
            font=('Segoe UI', 12),
            wrap="word"
        )
        text_box.pack(fill="both", expand=True, padx=15, pady=15)
        text_box.insert("1.0", summary)
        text_box.configure(state="disabled")
        
        # Close button
        close_btn = ctk.CTkButton(
            popup,
            text="Close",
            command=popup.destroy,
            width=100,
            fg_color=COLORS['bg_tertiary'],
            hover_color=COLORS['text_muted']
        )
        close_btn.pack(pady=(0, 20))
        
    def compare_selected(self):
        """Compare two selected documents"""
        selected_ids = [doc_id for doc_id, var in self.selected_files.items() if var.get()]
        
        if len(selected_ids) != 2:
            show_toast("Please select exactly 2 files to compare", "warning", 2000)
            return
        
        show_toast("⏳ Comparing documents...", "info", 2000)
        
        def do_compare():
            try:
                doc1 = get_document_by_id(selected_ids[0])
                doc2 = get_document_by_id(selected_ids[1])
                
                if doc1 and doc2:
                    comparison = compare_documents(
                        doc1[2], doc1[1],  # content, filename
                        doc2[2], doc2[1]
                    )
                    
                    self.parent.after(0, lambda: self.show_comparison_window(doc1, doc2, comparison))
            except Exception as e:
                self.parent.after(0, lambda: show_toast(f"❌ Error: {str(e)}", "error", 3000))
        
        thread = threading.Thread(target=do_compare, daemon=True)
        thread.start()
        
    def show_comparison_window(self, doc1, doc2, comparison):
        """Display comparison results"""
        window = ctk.CTkToplevel(self.parent)
        window.title("⚖️ Document Comparison")
        window.geometry("900x600")
        window.configure(fg_color=COLORS['bg_primary'])
        window.transient(self.parent.winfo_toplevel())
        
        # Header
        header = ctk.CTkLabel(
            window,
            text="⚖️ Document Comparison",
            font=('Segoe UI', 18, 'bold'),
            text_color=COLORS['text_primary']
        )
        header.pack(pady=(20, 15))
        
        # Documents info
        docs_frame = ctk.CTkFrame(window, fg_color="transparent")
        docs_frame.pack(fill="x", padx=20)
        
        ctk.CTkLabel(
            docs_frame,
            text=f"📄 {doc1[1]}  ↔  📄 {doc2[1]}",
            font=('Segoe UI', 12),
            text_color=COLORS['text_secondary']
        ).pack()
        
        # Comparison result
        result_frame = ctk.CTkFrame(window, fg_color=COLORS['bg_secondary'], corner_radius=12)
        result_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        result_text = ctk.CTkTextbox(
            result_frame,
            fg_color="transparent",
            text_color=COLORS['text_primary'],
            font=('Segoe UI', 12),
            wrap="word"
        )
        result_text.pack(fill="both", expand=True, padx=15, pady=15)
        result_text.insert("1.0", comparison)
        result_text.configure(state="disabled")
        
        # Close button
        ctk.CTkButton(
            window,
            text="Close",
            command=window.destroy,
            width=100,
            fg_color=COLORS['bg_tertiary'],
            hover_color=COLORS['text_muted']
        ).pack(pady=(0, 20))
        
    def show_upload_dialog(self):
        """Show upload dialog with tags input"""
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
        
        # Create dialog for tags
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Upload File")
        dialog.geometry("450x200")
        dialog.configure(fg_color=COLORS['bg_primary'])
        dialog.transient(self.parent.winfo_toplevel())
        dialog.grab_set()
        
        # Center
        dialog.update_idletasks()
        x = self.parent.winfo_toplevel().winfo_x() + (self.parent.winfo_toplevel().winfo_width() // 2) - 225
        y = self.parent.winfo_toplevel().winfo_y() + (self.parent.winfo_toplevel().winfo_height() // 2) - 100
        dialog.geometry(f"+{x}+{y}")
        
        # Filename
        filename = os.path.basename(filepath)
        ctk.CTkLabel(
            dialog,
            text=f"📄 {filename}",
            font=('Segoe UI', 14, 'bold'),
            text_color=COLORS['text_primary']
        ).pack(pady=(20, 10))
        
        # Tags input
        ctk.CTkLabel(
            dialog,
            text="Tags (comma-separated, optional):",
            font=('Segoe UI', 11),
            text_color=COLORS['text_secondary']
        ).pack(pady=(5, 5))
        
        tags_entry = ctk.CTkEntry(
            dialog,
            placeholder_text="work, important, research",
            width=350,
            height=36
        )
        tags_entry.pack(pady=(0, 15))
        
        # Buttons
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack()
        
        def do_upload():
            tags_string = tags_entry.get()
            dialog.destroy()
            self.upload_file(filepath, tags_string)
        
        ctk.CTkButton(
            btn_frame,
            text="Upload",
            command=do_upload,
            width=100,
            fg_color=COLORS['accent_primary'],
            hover_color=COLORS['accent_hover']
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            width=100,
            fg_color=COLORS['bg_tertiary'],
            hover_color=COLORS['text_muted']
        ).pack(side="left", padx=5)
        
    def upload_file(self, filepath, tags_string=""):
        """Upload file with tags"""
        show_toast("📤 Processing file...", "info", 2000)
            
        try:
            content, word_count = parse_file(filepath)
            filename = os.path.basename(filepath)
            
            # Add to database
            doc_id = add_document(filename, content, word_count)
            
            # Add tags if provided
            if tags_string:
                tags = tags_manager.parse_tags(tags_string)
                for tag in tags:
                    color = tags_manager.get_tag_color(tag)
                    add_tag_to_file(doc_id, tag, color)
            
            # Add to vector store
            add_document_to_db(doc_id, filename, content)
            
            # Success
            tag_msg = f" with {len(tags)} tags" if tags_string else ""
            show_toast(f"✓ Uploaded: {filename} ({word_count:,} words){tag_msg}", "success", 3000)
            
            self.refresh_tag_filter()
            self.load_files()
            
        except Exception as e:
            show_toast(f"Upload failed: {str(e)}", "error", 4000)
            
    def delete_file(self, doc_id, filename):
        """Delete file with confirmation dialog"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Confirm Delete")
        dialog.geometry("350x150")
        dialog.resizable(False, False)
        dialog.configure(fg_color=COLORS['bg_secondary'])
        dialog.transient(self.parent.winfo_toplevel())
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = self.parent.winfo_toplevel().winfo_x() + (self.parent.winfo_toplevel().winfo_width() // 2) - 175
        y = self.parent.winfo_toplevel().winfo_y() + (self.parent.winfo_toplevel().winfo_height() // 2) - 75
        dialog.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(
            dialog,
            text=f"🗑️ Delete '{filename}'?",
            font=TEXT_STYLES['heading'],
            text_color=COLORS['text_primary']
        ).pack(pady=(25, 5))
        
        ctk.CTkLabel(
            dialog,
            text="This cannot be undone.",
            font=TEXT_STYLES['caption'],
            text_color=COLORS['text_secondary']
        ).pack(pady=(0, 20))
        
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20)
        
        def confirm_delete():
            dialog.destroy()
            try:
                delete_document(doc_id)
                delete_document_from_db(doc_id)
                show_toast(f"✓ Deleted: {filename}", "success", 3000)
                self.load_files()
            except Exception as e:
                show_toast(f"Delete failed: {str(e)}", "error", 4000)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            **BUTTON_STYLES.get('secondary', {'fg_color': COLORS['bg_tertiary']}),
            width=100
        ).pack(side="left", expand=True, padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Delete",
            command=confirm_delete,
            **BUTTON_STYLES['danger'],
            width=100
        ).pack(side="right", expand=True, padx=5)
