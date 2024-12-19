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