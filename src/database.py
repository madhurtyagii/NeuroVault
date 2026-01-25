import sqlite3
from datetime import datetime
import os

# Database file path
DB_PATH = os.path.join("data", "neurovault.db")

def init_db():
    """Initialize database with all required tables"""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Documents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            content TEXT NOT NULL,
            upload_date TEXT NOT NULL,
            word_count INTEGER NOT NULL,
            summary TEXT
        )
    ''')
    
    # Chat sessions table for history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL,
            messages TEXT NOT NULL
        )
    ''')
    
    # Tags table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            color TEXT DEFAULT '#6b7280'
        )
    ''')
    
    # File-Tags junction table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            FOREIGN KEY (file_id) REFERENCES documents(id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
            UNIQUE(file_id, tag_id)
        )
    ''')
    
    # Search history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            results_count INTEGER DEFAULT 0
        )
    ''')
    
    # Add summary column if it doesn't exist (for existing databases)
    try:
        cursor.execute('ALTER TABLE documents ADD COLUMN summary TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
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


# ============== Chat Session Functions ==============

def save_chat_session(title, messages_json):
    """
    Save a chat session to the database
    
    Args:
        title: Session title
        messages_json: JSON string of messages array
    
    Returns:
        int: Session ID
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO chat_sessions (title, created_at, messages)
        VALUES (?, ?, ?)
    ''', (title, created_at, messages_json))
    
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return session_id


def load_chat_session(session_id):
    """
    Load a chat session by ID
    
    Args:
        session_id: Session ID to load
    
    Returns:
        tuple: (id, title, created_at, messages_json) or None
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, title, created_at, messages
        FROM chat_sessions
        WHERE id = ?
    ''', (session_id,))
    
    session = cursor.fetchone()
    conn.close()
    
    return session


def list_chat_sessions():
    """
    List all saved chat sessions
    
    Returns:
        list: List of (id, title, created_at) tuples
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, title, created_at
        FROM chat_sessions
        ORDER BY created_at DESC
    ''')
    
    sessions = cursor.fetchall()
    conn.close()
    
    return sessions


def delete_chat_session(session_id):
    """Delete a chat session by ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM chat_sessions WHERE id = ?', (session_id,))
    
    conn.commit()
    conn.close()


# ============== Summary Functions ==============

def save_summary(doc_id, summary_text):
    """Save AI-generated summary for a document"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('UPDATE documents SET summary = ? WHERE id = ?', (summary_text, doc_id))
    
    conn.commit()
    conn.close()


def get_summary(doc_id):
    """Get saved summary for a document"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT summary FROM documents WHERE id = ?', (doc_id,))
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else None


# ============== Tag Functions ==============

def add_tag(tag_name, color='#6b7280'):
    """Add a new tag (or get existing)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('INSERT OR IGNORE INTO tags (name, color) VALUES (?, ?)', (tag_name.lower(), color))
    cursor.execute('SELECT id FROM tags WHERE name = ?', (tag_name.lower(),))
    
    tag_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    
    return tag_id


def add_tag_to_file(file_id, tag_name, color='#6b7280'):
    """Add a tag to a file"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tag if doesn't exist
    cursor.execute('INSERT OR IGNORE INTO tags (name, color) VALUES (?, ?)', (tag_name.lower(), color))
    cursor.execute('SELECT id FROM tags WHERE name = ?', (tag_name.lower(),))
    tag_id = cursor.fetchone()[0]
    
    # Link tag to file
    cursor.execute('INSERT OR IGNORE INTO file_tags (file_id, tag_id) VALUES (?, ?)', (file_id, tag_id))
    
    conn.commit()
    conn.close()


def remove_tag_from_file(file_id, tag_name):
    """Remove a tag from a file"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM file_tags 
        WHERE file_id = ? AND tag_id = (SELECT id FROM tags WHERE name = ?)
    ''', (file_id, tag_name.lower()))
    
    conn.commit()
    conn.close()


def get_file_tags(file_id):
    """Get all tags for a file"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT tags.name, tags.color FROM tags
        JOIN file_tags ON tags.id = file_tags.tag_id
        WHERE file_tags.file_id = ?
        ORDER BY tags.name
    ''', (file_id,))
    
    tags = cursor.fetchall()
    conn.close()
    
    return tags  # List of (name, color) tuples


def get_all_tags():
    """Get all unique tags in the system"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT DISTINCT name, color FROM tags ORDER BY name')
    
    tags = cursor.fetchall()
    conn.close()
    
    return tags


def get_files_by_tag(tag_name):
    """Get all files with a specific tag"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT documents.id, documents.filename, documents.upload_date, documents.word_count
        FROM documents
        JOIN file_tags ON documents.id = file_tags.file_id
        JOIN tags ON file_tags.tag_id = tags.id
        WHERE tags.name = ?
        ORDER BY documents.upload_date DESC
    ''', (tag_name.lower(),))
    
    files = cursor.fetchall()
    conn.close()
    
    return files


# ============== Search History Functions ==============

def save_search(query, results_count):
    """Save a search query to history"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO search_history (query, timestamp, results_count)
        VALUES (?, ?, ?)
    ''', (query, timestamp, results_count))
    
    conn.commit()
    conn.close()


def get_search_history(limit=50, days=None):
    """
    Get search history
    
    Args:
        limit: Max number of results
        days: Only get searches from last N days (optional)
    
    Returns:
        list: (id, query, timestamp, results_count) tuples
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if days:
        cursor.execute('''
            SELECT id, query, timestamp, results_count
            FROM search_history
            WHERE timestamp >= datetime('now', ?)
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (f'-{days} days', limit))
    else:
        cursor.execute('''
            SELECT id, query, timestamp, results_count
            FROM search_history
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
    
    history = cursor.fetchall()
    conn.close()
    
    return history


def delete_search_history(search_id=None):
    """Delete search history (specific or all)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if search_id:
        cursor.execute('DELETE FROM search_history WHERE id = ?', (search_id,))
    else:
        cursor.execute('DELETE FROM search_history')
    
    conn.commit()
    conn.close()


def clear_old_search_history(days=90):
    """Delete search history older than N days"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM search_history
        WHERE timestamp < datetime('now', ?)
    ''', (f'-{days} days',))
    
    conn.commit()
    conn.close()


# Initialize database on import
init_db()
