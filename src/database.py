import sqlite3
from datetime import datetime
import os

# Database file path
DB_PATH = os.path.join("data", "neurovault.db")

def init_db():
    """Initialize database with documents table"""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            content TEXT NOT NULL,
            upload_date TEXT NOT NULL,
            word_count INTEGER NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def add_document(filename, content, word_count):
    """Add a new document to the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO documents (filename, content, upload_date, word_count)
        VALUES (?, ?, ?, ?)
    ''', (filename, content, upload_date, word_count))
    
    doc_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return doc_id

def get_all_documents():
    """Get all documents from the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, filename, upload_date, word_count
        FROM documents
        ORDER BY upload_date DESC
    ''')
    
    documents = cursor.fetchall()
    conn.close()
    
    return documents

def get_document_by_id(doc_id):
    """Get a specific document by ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, filename, content, upload_date, word_count
        FROM documents
        WHERE id = ?
    ''', (doc_id,))
    
    document = cursor.fetchone()
    conn.close()
    
    return document

def delete_document(doc_id):
    """Delete a document from the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM documents WHERE id = ?', (doc_id,))
    
    conn.commit()
    conn.close()

def search_documents(query):
    """Search documents by filename or content"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, filename, upload_date, word_count
        FROM documents
        WHERE filename LIKE ? OR content LIKE ?
        ORDER BY upload_date DESC
    ''', (f'%{query}%', f'%{query}%'))
    
    documents = cursor.fetchall()
    conn.close()
    
    return documents

# Initialize database on import
init_db()
