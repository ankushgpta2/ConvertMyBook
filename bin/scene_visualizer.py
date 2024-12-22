from typing import List, Optional
import openai
from pdf_processor import TextElement
import re

class SceneVisualizer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key

class ChatbotInterface:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key
        self.scene_visualizer = SceneVisualizer(api_key)
        self.context = []