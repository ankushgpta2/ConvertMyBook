# 📚 PDF Processing and Audio Visualization System

## 🌐 Overview
This project is a comprehensive system for processing PDFs, generating audio content, and creating scene visualizations. It provides end-to-end functionality from text extraction to audio generation and scene visualization.

### ✨ Key Features:

- Preserves complex text formatting
- Supports chapter-specific audio processing
- Detects and handles quotes with unique voice characteristics
- Maintains text structure in intermediate JSON format
- Interactive chatbot for scene visualization (DALL-E)

## 🧩 Components
### 📄 PDF Processor (pdf_processor.py)

- Extracts text from PDFs using PyMuPDF
- Preserves advanced text formatting (headings, quotes, italics)
- Generates metadata-rich text outputs

### 🔊 Audio Processor (audio_processor.py)

- Integrates Tortoise TTS for speech generation
- Converts formatted text to speech
- Dynamically adjusts voice characteristics based on text formatting
- Creates audiobooks with contextually appropriate pauses

### 🖼️ Scene Visualizer (scene_visualizer.py)

- Implements scene visualization using DALL-E
- Provides interactive chatbot interface
- Generates images based on textual descriptions

### 🚀 Main Application (main.py)

- Central application entry point
- Supports multiple operational modes
- Handles command-line arguments
- Offers interactive chat functionality

## 🛠️ Prerequisites

- Python 3.8+
- OpenAI API Key (for DALL-E integration)

## 💾 Installation

Clone the repository + install dependencies:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## 🖥️  Usage

### PDF Text Extraction:
```bash
python main.py --pdf_path book.pdf --output_dir output --mode pdf2text
```

### Audiobook Generation:
```bash
python main.py --output_dir output --mode text2audio
```

### Chat Interface:
```bash
python main.py --output_dir output --mode chat --openai_key YOUR_API_KEY
```