from typing import List, Optional
import openai
from pdf_processor import TextElement
import re

class SceneVisualizer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key
    
    def extract_scene_description(self, elements: List[TextElement], character_name: Optional[str] = None, scene_context: Optional[str] = None
    ) -> str:
        """ Extract relevant scene description based on character or context.
        """
        # First, try to identify the relevant section of text
        relevant_text = []
        in_relevant_section = False
        
        for elem in elements:
            # Look for character name mentions or scene context keywords
            if character_name and character_name.lower() in elem.content.lower():
                in_relevant_section = True
                relevant_text.append(elem.content)
            elif scene_context and scene_context.lower() in elem.content.lower():
                in_relevant_section = True
                relevant_text.append(elem.content)
            elif in_relevant_section:
                # Continue collecting text until we hit a new section
                if elem.is_heading:
                    in_relevant_section = False
                else:
                    relevant_text.append(elem.content)
                    
        return " ".join(relevant_text)

class ChatbotInterface:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key
        self.scene_visualizer = SceneVisualizer(api_key)
        self.context = []