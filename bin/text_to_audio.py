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