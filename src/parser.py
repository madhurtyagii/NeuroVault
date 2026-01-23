"""
Document parsing utilities for NeuroVault
Extracts text from PDF, DOCX, TXT, and code files
"""

import os
from pypdf import PdfReader
from docx import Document

def parse_pdf(file_path):
    """Extract text from PDF"""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page_num, page in enumerate(reader.pages, 1):
            page_text = page.extract_text()
            if page_text:
                text += f"\n--- Page {page_num} ---\n{page_text}"
        return text.strip()
    except Exception as e:
        return f"[Error reading PDF: {str(e)}]"

def parse_docx(file_path):
    """Extract text from Word document"""
    try:
        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            if para.text.strip():
                text += para.text + "\n"
        return text.strip()
    except Exception as e:
        return f"[Error reading DOCX: {str(e)}]"

def parse_text(file_path):
    """Extract text from text/code files"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Try with different encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            return f"[Error reading file: {str(e)}]"
    except Exception as e:
        return f"[Error reading file: {str(e)}]"

def parse_file(file_path):
    """
    Main parsing function - routes to appropriate parser
    Returns (content, word_count)
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.pdf':
        content = parse_pdf(file_path)
    elif ext == '.docx':
        content = parse_docx(file_path)
    elif ext in ['.txt', '.py', '.md', '.json', '.csv']:
        content = parse_text(file_path)
    else:
        content = f"[Unsupported file type: {ext}]"
    
    word_count = len(content.split()) if content else 0
    return content, word_count
