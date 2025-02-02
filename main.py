import argparse
from src.pdf_to_text import PDFProcessor
from src.text_to_audio import AudioProcessor
from src.scene_visualizer import ChatbotInterface
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

    if args.mode == 'pdf2text':
        # Process PDF and save formatted text
        processor = PDFProcessor()
        elements = processor.extract_text_with_formatting(args.pdf_path)
        output_path = os.path.join(args.output_dir, 'formatted_text.json')
        processor.save_formatted_text(elements, output_path)
        print(f"Formatted text saved to {output_path}")
    
    elif args.mode == 'text2audio':
        # Convert formatted text to audio
        processor = PDFProcessor()
        audio_processor = AudioProcessor()
        
        input_path = os.path.join(args.output_dir, 'formatted_text.json')
        elements = processor.load_formatted_text(input_path)
        
        output_path = os.path.join(args.output_dir, 'audiobook.wav')
        audio_processor.text_to_speech(elements, output_path=output_path)
        print(f"Audiobook saved to {output_path}")
    
    elif args.mode == 'chat':
        # Start chat interface
        processor = PDFProcessor()
        input_path = os.path.join(args.output_dir, 'formatted_text.json')
        elements = processor.load_formatted_text(input_path)
        
        chatbot = ChatbotInterface(args.openai_key)
        print("Chat interface started. Type 'quit' to exit.")
        
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                break
                
            response = chatbot.chat(user_input, elements)
            print(f"Assistant: {response}")


if __name__ == "__main__":
    main()