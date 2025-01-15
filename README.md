# PDF Processing and Audio Visualization System

## Overview
This project is a comprehensive system for processing PDFs, generating audio content, and creating scene visualizations. It provides end-to-end functionality from text extraction to audio generation and scene visualization.

## Components
### 1. PDF Processor (pdf_processor.py)

- Extracts text from PDFs using PyMuPDF
- Preserves advanced text formatting (headings, quotes, italics)
- Generates metadata-rich text outputs

### 2. Audio Processor (audio_processor.py)

- Integrates Tortoise TTS for speech generation
- Converts formatted text to speech
- Dynamically adjusts voice characteristics based on text formatting
- Creates audiobooks with contextually appropriate pauses

### 3. Scene Visualizer (scene_visualizer.py)

- Implements scene visualization using DALL-E
- Provides interactive chatbot interface
- Generates images based on textual descriptions

### 4. Main Application (main.py)

- Central application entry point
- Supports multiple operational modes
- Handles command-line arguments
- Offers interactive chat functionality

## Prerequisites

- Python 3.8+
- OpenAI API Key (for DALL-E integration)

## Installation

Clone the repository + install dependencies:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```