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
    
    def generate_scene_image(self, scene_description: str, style: str = "realistic"
    ) -> str:
        """ Generate an image of the scene using DALL-E.
        """
        try:
            response = openai.Image.create(
                prompt=f"A {style} visualization of the following scene: {scene_description}",
                n=1,
                size="1024x1024"
            )
            return response['data'][0]['url']
        except Exception as e:
            print(f"Error generating image: {e}")
            return None


class ChatbotInterface:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key
        self.scene_visualizer = SceneVisualizer(api_key)
        self.context = []
    
    def chat(self, user_input: str, elements: List[TextElement]) -> str:
        """ Process user input and generate appropriate response.
        """
        # Add user input to context
        self.context.append({"role": "user", "content": user_input})

        # Generate response using GPT
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for discussing and visualizing scenes from books. You can help find relevant passages and generate scene descriptions."},
                    *self.context
                ]
            )
            
            assistant_response = response.choices[0].message['content']
            self.context.append({"role": "assistant", "content": assistant_response})
            
            # Check if user wants to visualize something
            if any(keyword in user_input.lower() for keyword in ["show", "visualize", "picture", "image"]):
                # Extract character or scene information
                character_match = re.search(r"show\s+(\w+)", user_input.lower())
                if character_match:
                    character_name = character_match.group(1)
                    scene_description = self.scene_visualizer.extract_scene_description(
                        elements, 
                        character_name=character_name
                    )
                    image_url = self.scene_visualizer.generate_scene_image(scene_description)
                    if image_url:
                        assistant_response += f"\n\nI've generated an image of the scene: {image_url}"
                        
            return assistant_response

        except Exception as e:
            print(f"Error in chat completion: {e}")
            return "I apologize, but I encountered an error processing your request."