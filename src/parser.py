import os
from pypdf import PdfReader
from docx import Document

# OCR imports (optional, graceful fallback)
try:
    import pytesseract
    from pdf2image import convert_from_path
    from PIL import Image
    OCR_AVAILABLE = True
    
    # Set tesseract path for Windows
    if os.name == 'nt':  # Windows
        tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        if os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️ OCR not available. Install: pip install pytesseract pdf2image Pillow")

def parse_file(file_path):
    """
    Parse various file types and extract text content
    
    Args:
        file_path: Path to file
    
    Returns:
        tuple: (content_text, word_count)
    """
    _, ext = os.path.splitext(file_path.lower())
    
    try:
        if ext == '.txt' or ext == '.py':
            return parse_text(file_path)
        elif ext == '.pdf':
            return parse_pdf(file_path)
        elif ext == '.docx':
            return parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    except Exception as e:
        raise Exception(f"Failed to parse {os.path.basename(file_path)}: {str(e)}")

def parse_text(file_path):
    """Parse text and Python files"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()
    
    word_count = len(content.split())
    return content, word_count

def parse_pdf(file_path):
    """Parse PDF files with OCR fallback for scanned documents"""
    content_parts = []
    
    try:
        # Try normal text extraction first
        reader = PdfReader(file_path)
        
        if len(reader.pages) == 0:
            raise ValueError("PDF has no pages")
        
        for page_num, page in enumerate(reader.pages):
            try:
                text = page.extract_text()
                if text and text.strip():
                    content_parts.append(text)
            except Exception as e:
                print(f"Warning: Failed to extract page {page_num + 1}: {e}")
                continue
        
        # If we got text, return it
        if content_parts:
            content = "\n\n".join(content_parts)
            word_count = len(content.split())
            return content, word_count
        
        # No text found - try OCR if available
        if OCR_AVAILABLE:
            print("📷 No text found - attempting OCR (this may take a minute)...")
            return parse_pdf_with_ocr(file_path)
        else:
            raise ValueError(
                "Could not extract any text from PDF. It might be scanned/image-based.\n"
                "Install OCR support: pip install pytesseract pdf2image Pillow\n"
                "Then install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki"
            )
    
    except Exception as e:
        raise Exception(f"PDF parsing error: {str(e)}")

def parse_pdf_with_ocr(file_path):
    """Use OCR to extract text from scanned PDFs"""
    if not OCR_AVAILABLE:
        raise ValueError("OCR dependencies not installed")
    
    try:
        # Convert PDF pages to images
        print("🔄 Converting PDF to images...")
        
        # Try to find poppler on Windows
        poppler_path = None
        if os.name == 'nt':  # Windows
            possible_paths = [
                r"C:\poppler\Library\bin",
                r"C:\Program Files\poppler\Library\bin",
                r"C:\Program Files (x86)\poppler\Library\bin",
                r"C:\poppler-24.02.0\Library\bin",
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    poppler_path = path
                    print(f"✅ Found poppler at: {path}")
                    break
            
            if not poppler_path:
                raise ValueError(
                    "Poppler not found. Download from:\n"
                    "https://github.com/oschwartz10612/poppler-windows/releases/\n"
                    "Extract to C:\\poppler and ensure C:\\poppler\\Library\\bin exists"
                )
        
        # Convert with poppler path
        images = convert_from_path(file_path, dpi=200, poppler_path=poppler_path)
        
        content_parts = []
        total_pages = len(images)
        
        # OCR each page
        for i, image in enumerate(images, 1):
            print(f"📖 OCR processing page {i}/{total_pages}...")
            text = pytesseract.image_to_string(image)
            if text and text.strip():
                content_parts.append(text.strip())
        
        if not content_parts:
            raise ValueError("OCR found no text in PDF")
        
        content = "\n\n".join(content_parts)
        word_count = len(content.split())
        
        print(f"✅ OCR complete: {word_count} words extracted from {total_pages} pages")
        return content, word_count
    
    except Exception as e:
        raise Exception(f"OCR error: {str(e)}")

def parse_docx(file_path):
    """Parse Word documents"""
    try:
        doc = Document(file_path)
        
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        
        if not paragraphs:
            raise ValueError("No text content found in document")
        
        content = "\n\n".join(paragraphs)
        word_count = len(content.split())
        
        return content, word_count
    
    except Exception as e:
        raise Exception(f"DOCX parsing error: {str(e)}")

# Test function
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        print(f"Testing parser with: {test_file}")
        print(f"OCR Available: {OCR_AVAILABLE}")
        try:
            content, words = parse_file(test_file)
            print(f"\n✅ SUCCESS: {words} words")
            print(f"\nPreview (first 500 chars):\n{content[:500]}...")
        except Exception as e:
            print(f"\n❌ FAILED: {e}")
    else:
        print("Usage: python parser.py <file_path>")
