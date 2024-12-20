import fitz
import re
from typing import Dict, List, Tuple
import spacy
from dataclasses import dataclass


@dataclass
class TextElement:
    content: str
    is_heading: bool = False
    is_quote: bool = False
    is_italic: bool = False
    is_capitalized: bool = False
    font_size: float = 0
    font_name: str = ""


class PDFProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
    def extract_text_with_formatting(self, pdf_path: str) -> List[TextElement]:
        """ Extract text while preserving formatting information.
        """
        doc = fitz.open(pdf_path)
        formatted_text = []
        
        for page in doc:
            # Get text blocks with formatting information
            blocks = page.get_text("dict")["blocks"]
            
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if not text:
                                continue
                                
                            # Analyze formatting
                            is_heading = span["size"] > 12  # Arbitrary threshold
                            is_italic = "italic" in span["font"].lower()
                            is_capitalized = text.isupper()
                            
                            # Detect quotes using spaCy
                            doc = self.nlp(text)
                            is_quote = any(token.is_quote for token in doc)
                            
                            element = TextElement(
                                content=text,
                                is_heading=is_heading,
                                is_quote=is_quote,
                                is_italic=is_italic,
                                is_capitalized=is_capitalized,
                                font_size=span["size"],
                                font_name=span["font"]
                            )
                            formatted_text.append(element)
        
        return formatted_text