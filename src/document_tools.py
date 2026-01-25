"""
NeuroVault Document Tools
AI-powered document summarization and comparison
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from ai_model import get_ai_response_stream, get_ai_response


def summarize_document(content, max_sentences=5):
    """
    Generate AI summary of a document
    
    Args:
        content: Document text content
        max_sentences: Maximum sentences in summary
    
    Returns:
        str: AI-generated summary
    """
    # Truncate very long documents to avoid timeout
    truncated_content = content[:10000] if len(content) > 10000 else content
    
    prompt = f"""Summarize the following document in {max_sentences} sentences or less.
Focus on:
- Main ideas and key points
- Important conclusions or findings
- Critical information the reader needs to know

Document:
{truncated_content}

Summary:"""
    
    try:
        summary = get_ai_response(prompt, max_tokens=400)
        return summary.strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"


def compare_documents(doc1_content, doc1_name, doc2_content, doc2_name):
    """
    Compare two documents using AI
    
    Args:
        doc1_content: First document text
        doc1_name: First document filename
        doc2_content: Second document text
        doc2_name: Second document filename
    
    Returns:
        str: AI comparison analysis
    """
    # Truncate to avoid timeout
    doc1_truncated = doc1_content[:5000] if len(doc1_content) > 5000 else doc1_content
    doc2_truncated = doc2_content[:5000] if len(doc2_content) > 5000 else doc2_content
    
    prompt = f"""Compare these two documents and provide a concise analysis:

📄 DOCUMENT 1: {doc1_name}
{doc1_truncated}

📄 DOCUMENT 2: {doc2_name}
{doc2_truncated}

Please provide:
1. **Main Similarities** - What themes/topics do both documents share?
2. **Key Differences** - How do they differ in content, tone, or focus?
3. **Which is more comprehensive?** - Brief assessment of depth/coverage

Keep the analysis concise and actionable."""
    
    try:
        comparison = get_ai_response(prompt, max_tokens=600)
        return comparison.strip()
    except Exception as e:
        return f"Error comparing documents: {str(e)}"


def extract_key_points(content, num_points=5):
    """
    Extract key bullet points from a document
    
    Args:
        content: Document text
        num_points: Number of key points to extract
    
    Returns:
        str: Bullet-point list of key points
    """
    truncated = content[:8000] if len(content) > 8000 else content
    
    prompt = f"""Extract the {num_points} most important key points from this document.
Format as a numbered list.

Document:
{truncated}

Key Points:"""
    
    try:
        points = get_ai_response(prompt, max_tokens=400)
        return points.strip()
    except Exception as e:
        return f"Error extracting key points: {str(e)}"
