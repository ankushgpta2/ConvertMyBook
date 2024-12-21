import torch
from tortoise.api import TextToSpeech
from typing import List, Optional
import numpy as np
import soundfile as sf
from dataclasses import dataclass
from pdf_processor import TextElement

@dataclass
class AudioSegment:
    audio: np.ndarray
    sample_rate: int
    text_element: TextElement

class AudioProcessor:
    def __init__(self):
        self.tts = TextToSpeech()
        
    def text_to_speech(self, elements: List[TextElement], voice: str = "train_dreams", output_path: Optional[str] = None
    ) -> List[AudioSegment]:
        """ Convert text elements to speech while preserving structure.
        """
        audio_segments = []
        
        for element in elements:
            # Adjust speech parameters based on formatting
            conditioning_latents = self.tts.get_conditioning_latents(
                [voice]
            )
            
            # Modify voice characteristics based on formatting
            voice_samples, conditioning_latents = self._adjust_voice_for_formatting(
                element, 
                conditioning_latents
            )
            
            # Generate speech
            gen_audio = self.tts.tts_with_preset(
                element.content,
                voice_samples=voice_samples,
                conditioning_latents=conditioning_latents,
                preset="standard"
            )
            
            audio_segments.append(
                AudioSegment(
                    audio=gen_audio,
                    sample_rate=24000,  # Tortoise default
                    text_element=element
                )
            )
            
        if output_path:
            self._save_audio_book(audio_segments, output_path)
            
        return audio_segments