"""
Text extraction utilities for PDF and EPUB files.
"""

import os
import re
from typing import Tuple, List

try:
    import fitz  # PyMuPDF
    FITZ_AVAILABLE = True
except ImportError:
    fitz = None
    FITZ_AVAILABLE = False

try:
    from ebooklib import epub
    from bs4 import BeautifulSoup
    EPUB_AVAILABLE = True
except ImportError:
    epub = None
    BeautifulSoup = None
    EPUB_AVAILABLE = False


def parse_document(file_path: str) -> Tuple[List[str], int]:
    """
    Parse a document (PDF or EPUB) and extract text as a list of words.
    
    Args:
        file_path: Path to the document file
        
    Returns:
        Tuple of (word_list, total_word_count) where:
        - word_list: List of words with __PARAGRAPH_BREAK__ tokens for paragraph breaks
        - total_word_count: Count of actual words (excluding break tokens)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.pdf':
        return _parse_pdf(file_path)
    elif file_ext == '.epub':
        return _parse_epub(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")


def _parse_pdf(file_path: str) -> Tuple[List[str], int]:
    """Parse PDF file and extract text."""
    if not FITZ_AVAILABLE:
        raise ImportError("PyMuPDF (fitz) is required for PDF parsing. Install with: pip install PyMuPDF")
    
    doc = fitz.open(file_path)
    text_content = []
    
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text()
        text_content.append(text)
    
    doc.close()
    
    # Join all pages and process text
    full_text = '\n'.join(text_content)
    return _process_text(full_text)


def _parse_epub(file_path: str) -> Tuple[List[str], int]:
    """Parse EPUB file and extract text."""
    if not EPUB_AVAILABLE:
        raise ImportError("ebooklib and BeautifulSoup are required for EPUB parsing. Install with: pip install ebooklib beautifulsoup4")
    
    book = epub.read_epub(file_path)
    text_content = []
    
    # Get all items that are HTML documents
    for item in book.get_items():
        # Check if this is an HTML/XHTML document item
        # EpubHtml items have MIME type 9, and we want to process them
        if (hasattr(item, 'get_content') and 
            hasattr(item, 'get_name') and
            (item.get_type() in ['application/xhtml+xml', 'text/html'] or 
             item.get_type() == 9 or  # EpubHtml items
             type(item).__name__ == 'EpubHtml')):
            # Get HTML content directly
            html_content = item.get_content()
            
            # Parse HTML and extract text
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text()
            if text.strip():  # Only add non-empty text
                text_content.append(text)
    
    # Join all chapters and process text
    full_text = '\n'.join(text_content)
    return _process_text(full_text)


def _process_text(text: str) -> Tuple[List[str], int]:
    """
    Process raw text into a list of words with paragraph break markers.
    
    Args:
        text: Raw text content
        
    Returns:
        Tuple of (word_list, total_word_count)
    """
    # Normalize whitespace and split into paragraphs
    # Replace multiple whitespace with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Split by double newlines or multiple newlines to identify paragraphs
    paragraphs = re.split(r'\n\s*\n+', text)
    
    word_list = []
    total_word_count = 0
    
    for i, paragraph in enumerate(paragraphs):
        # Clean paragraph text
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        # Split paragraph into words
        words = re.findall(r'\b\w+\b', paragraph)
        
        # Add words to the list
        word_list.extend(words)
        total_word_count += len(words)
        
        # Add paragraph break marker (except for the last paragraph)
        if i < len(paragraphs) - 1 and words:  # Only add break if paragraph has words
            word_list.append("__PARAGRAPH_BREAK__")
    
    return word_list, total_word_count
