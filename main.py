import argparse
from pdf_processor import PDFProcessor
import os


def main():
    parser = argparse.ArgumentParser(description='PDF to Audio/Visual Processing System')
    parser.add_argument('--pdf_path', type=str, help='Path to input PDF file')
    parser.add_argument('--output_dir', type=str, default='output', help='Output directory')
    parser.add_argument('--openai_key', type=str, help='OpenAI API key')
    parser.add_argument('--mode', choices=['pdf2text', 'text2audio', 'chat'], 
                      help='Processing mode')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)


if __name__ == "__main__":
    main()