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
    
    def _adjust_voice_for_formatting(self, element: TextElement, conditioning_latents):
        """ Adjust voice characteristics based on text formatting.
        """
        # These are placeholder adjustments - would need to be tuned
        if element.is_heading:
            # Make headings slightly slower and more emphatic
            conditioning_latents["speed"] = 0.9
            conditioning_latents["energy"] = 1.2
            
        if element.is_quote:
            # Slightly different voice for quotes
            conditioning_latents["voice_variation"] = 0.1
            
        if element.is_italic:
            # Add emphasis to italic text
            conditioning_latents["energy"] = 1.1
            
        return conditioning_latents
    
    def _save_audio_book(self, segments: List[AudioSegment], output_path: str):
        """ Combine audio segments and save as a single file.
        """
        # Add small pauses between segments
        pause = np.zeros(int(24000 * 0.5))  # 0.5 second pause
        
        # Combine all audio with pauses
        combined_audio = []
        for segment in segments:
            combined_audio.extend(segment.audio)
            combined_audio.extend(pause)
            
        sf.write(output_path, combined_audio, 24000)