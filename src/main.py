import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import os
from datetime import datetime
from parser import parse_file
from search_ui import SearchFrame
from chat_ui import ChatFrame
from embeddings import add_document_to_db, delete_document_from_db, get_collection_stats

# App theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NeuroVault:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("NeuroVault - AI Second Brain")
        self.root.geometry("1000x750")
        
        # Database setup
        self.db_path = "data/neurovault.db"
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.init_database()
        
        self.setup_ui()
        self.load_files()
    
    def init_database(self):
        """Create documents table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL UNIQUE,
                content TEXT,
                file_path TEXT,
                file_type TEXT,
                file_size INTEGER,
                word_count INTEGER,
                added_date TEXT
            )
        ''')
        self.conn.commit()
    
    def setup_ui(self):
        """Build the user interface"""
        # Header
        header_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        header_frame.pack(pady=30, padx=20, fill="x")
        
        title = ctk.CTkLabel(header_frame, text="🧠 NeuroVault", 
                           font=ctk.CTkFont(size=42, weight="bold"))
        title.pack()
        
        subtitle = ctk.CTkLabel(header_frame, 
                              text="Your AI Second Brain - Local & Private", 
                              font=ctk.CTkFont(size=16))
        subtitle.pack(pady=(5,0))
        
        # Tab view for navigation
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Tab 1: Files
        files_tab = self.tabview.add("📚 Files")
        
        # Upload section (in Files tab)
        upload_frame = ctk.CTkFrame(files_tab)
        upload_frame.pack(pady=20, padx=20, fill="x")
        
        self.upload_btn = ctk.CTkButton(
            upload_frame, 
            text="📁 Upload File (TXT, PDF, DOCX, PY)", 
            command=self.upload_file,
            height=60,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.upload_btn.pack(pady=20)
        
        self.status_label = ctk.CTkLabel(
            upload_frame, 
            text="Ready to upload your knowledge...",
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(pady=(0,15))
        
        # File list section
        list_frame = ctk.CTkFrame(files_tab)
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        list_header = ctk.CTkLabel(
            list_frame, 
            text="📚 Your Knowledge Base:", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        list_header.pack(anchor="w", padx=20, pady=(20,10))
        
        # Listbox with scrollbar
        list_container = ctk.CTkFrame(list_frame)
        list_container.pack(fill="both", expand=True, padx=20, pady=(0,20))
        
        self.file_listbox = tk.Listbox(
            list_container, 
            height=12, 
            font=("Consolas", 12),
            bg="#2b2b2b",
            fg="#ffffff",
            selectbackground="#1f538d"
        )
        scrollbar = tk.Scrollbar(list_container, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.file_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind selection
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        
        # Action buttons
        btn_frame = ctk.CTkFrame(files_tab)
        btn_frame.pack(pady=20, padx=20, fill="x")
        
        self.preview_btn = ctk.CTkButton(
            btn_frame, 
            text="👁️ Preview", 
            command=self.preview_file,
            state="disabled",
            width=150
        )
        self.preview_btn.pack(side="left", padx=10)
        
        self.delete_btn = ctk.CTkButton(
            btn_frame, 
            text="🗑️ Delete", 
            command=self.delete_file,
            state="disabled",
            width=150,
            fg_color="#c93e3e",
            hover_color="#a32e2e"
        )
        self.delete_btn.pack(side="right", padx=10)
        
        # Tab 2: Search
        search_tab = self.tabview.add("🔍 Search")
        self.search_frame = SearchFrame(search_tab, fg_color="transparent")
        self.search_frame.pack(fill="both", expand=True)
        
        # Tab 3: AI Chat
        chat_tab = self.tabview.add("💬 Chat")
        self.chat_frame = ChatFrame(chat_tab, fg_color="transparent")
        self.chat_frame.pack(fill="both", expand=True)
    
    def upload_file(self):
        """Handle file upload with proper error handling"""
        filetypes = [
            ("All supported", "*.txt *.pdf *.docx *.py"),
            ("Text files", "*.txt"),
            ("PDF files", "*.pdf"),
            ("Word docs", "*.docx"),
            ("Python", "*.py")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Select a file to add to NeuroVault",
            filetypes=filetypes
        )
        
        if not file_path:
            return
        
        try:
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            file_type = os.path.splitext(filename)[1]
            
            # Check if file already exists
            existing = self.cursor.execute(
                'SELECT filename FROM documents WHERE filename = ?', 
                (filename,)
            ).fetchone()
            
            if existing:
                if not messagebox.askyesno(
                    "File Exists", 
                    f"{filename} already exists. Replace it?"
                ):
                    return
                # Delete old version first
                self.delete_file_by_name(filename)
            
            # Parse file
            self.status_label.configure(text=f"⏳ Parsing {filename}...")
            self.root.update()
            
            content, word_count = parse_file(file_path)
            
            # Save to SQLite
            self.cursor.execute('''
                INSERT INTO documents 
                (filename, content, file_path, file_type, file_size, word_count, added_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                filename, 
                content,
                file_path,
                file_type,
                file_size,
                word_count,
                datetime.now().isoformat()
            ))
            self.conn.commit()
            
            # Add to ChromaDB
            self.status_label.configure(text=f"⏳ Adding to AI search index...")
            self.root.update()
            
            success = add_document_to_db(filename, filename, content)
            
            if not success:
                raise Exception("Failed to add to vector database")
            
            # Verify embedding worked
            stats = get_collection_stats()
            
            self.status_label.configure(
                text=f"✅ Added: {filename} ({file_size/1024:.1f} KB, {word_count} words) | Total chunks: {stats['total_chunks']}"
            )
            self.load_files()
            messagebox.showinfo("Success", 
                              f"✅ {filename} added successfully!\n\n"
                              f"Size: {file_size/1024:.1f} KB\n"
                              f"Words: {word_count:,}\n"
                              f"Searchable: Yes 🧠\n\n"
                              f"Total indexed chunks: {stats['total_chunks']}")
            
        except Exception as e:
            # Rollback if embedding failed
            self.cursor.execute('DELETE FROM documents WHERE filename = ?', (filename,))
            self.conn.commit()
            delete_document_from_db(filename)
            
            messagebox.showerror("Upload Error", 
                               f"Failed to upload {filename}:\n\n{str(e)}\n\n"
                               f"File was not added.")
            self.status_label.configure(text="❌ Upload failed")
            print(f"Upload error: {e}")
            import traceback
            traceback.print_exc()
    
    def delete_file_by_name(self, filename):
        """Helper to delete file by name"""
        try:
            # Delete from ChromaDB first
            delete_document_from_db(filename)
            
            # Delete from SQLite
            self.cursor.execute('DELETE FROM documents WHERE filename = ?', (filename,))
            self.conn.commit()
        except Exception as e:
            print(f"Delete error: {e}")
    
    def load_files(self):
        """Load files into listbox"""
        self.file_listbox.delete(0, tk.END)
        self.cursor.execute('''
            SELECT filename, file_type, word_count, added_date 
            FROM documents 
            ORDER BY added_date DESC
        ''')
        
        for row in self.cursor.fetchall():
            display_text = f"{row[1]} {row[0]} ({row[2]:,} words) - {row[3][:16]}"
            self.file_listbox.insert(tk.END, display_text)
        
        # Update status with chunk count
        stats = get_collection_stats()
        file_count = self.cursor.execute('SELECT COUNT(*) FROM documents').fetchone()[0]
        self.status_label.configure(
            text=f"📊 {file_count} files | {stats['total_chunks']} searchable chunks"
        )
    
    def on_file_select(self, event):
        """Enable buttons when file selected"""
        if self.file_listbox.curselection():
            self.preview_btn.configure(state="normal")
            self.delete_btn.configure(state="normal")
    
    def preview_file(self):
        """Show file content preview"""
        selection = self.file_listbox.curselection()
        if not selection:
            return
        
        idx = selection[0]
        self.cursor.execute('''
            SELECT filename, content, word_count
            FROM documents 
            ORDER BY added_date DESC 
            LIMIT 1 OFFSET ?
        ''', (idx,))
        
        result = self.cursor.fetchone()
        if result:
            preview = tk.Toplevel(self.root)
            preview.title(f"Preview: {result[0]}")
            preview.geometry("700x500")
            
            info_label = tk.Label(preview, 
                                text=f"File: {result[0]} | Words: {result[2]:,}", 
                                bg="#2b2b2b", fg="#ffffff")
            info_label.pack(fill="x", padx=10, pady=10)
            
            text_widget = tk.Text(preview, wrap=tk.WORD, font=("Consolas", 11))
            text_widget.insert("1.0", result[1][:5000])
            text_widget.pack(fill="both", expand=True, padx=10, pady=(0,10))
            
            if len(result[1]) > 5000:
                note = tk.Label(preview, 
                              text="(Showing first 5000 characters)", 
                              bg="#2b2b2b", fg="#999999")
                note.pack(fill="x", padx=10, pady=(0,10))
    
    def delete_file(self):
        """Delete selected file from both databases"""
        selection = self.file_listbox.curselection()
        if not selection:
            return
        
        idx = selection[0]
        
        # Get filename
        self.cursor.execute('''
            SELECT filename FROM documents 
            ORDER BY added_date DESC 
            LIMIT 1 OFFSET ?
        ''', (idx,))
        result = self.cursor.fetchone()
        
        if not result:
            return
        
        filename = result[0]
        
        if not messagebox.askyesno("Confirm Delete", 
                                   f"Delete {filename} from NeuroVault?"):
            return
        
        try:
            # Delete from ChromaDB
            self.status_label.configure(text=f"⏳ Removing {filename} from index...")
            self.root.update()
            delete_document_from_db(filename)
            
            # Delete from SQLite
            self.cursor.execute('DELETE FROM documents WHERE filename = ?', (filename,))
            self.conn.commit()
            
            self.load_files()
            self.preview_btn.configure(state="disabled")
            self.delete_btn.configure(state="disabled")
            
            stats = get_collection_stats()
            self.status_label.configure(
                text=f"✅ Deleted {filename} | Remaining chunks: {stats['total_chunks']}"
            )
            
        except Exception as e:
            messagebox.showerror("Delete Error", f"Failed to delete:\n{str(e)}")
            print(f"Delete error: {e}")
    
    def run(self):
        """Start the app"""
        self.root.mainloop()
        self.conn.close()

# Run the app
if __name__ == "__main__":
    app = NeuroVault()
    app.run()
