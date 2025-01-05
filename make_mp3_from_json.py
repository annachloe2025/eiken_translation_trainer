import json
from gtts import gTTS
import os

def create_mp3_from_json(json_file_path):
    # Load JSON data
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Extract title and best_answer
    title = data.get("title", "Untitled")
    best_answer = data.get("best_answer", "")

    # Prepare text for speech synthesis
    text_to_convert = f"Title: {title}. Best Answer: {best_answer}"

    # Create the output file name
    sanitized_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_"))
    output_file_name = f"{sanitized_title}.mp3"

    # Generate speech using gTTS
    tts = gTTS(text=text_to_convert, lang='en', tld='com')  # 'com' ensures American English accent
    tts.save(output_file_name)

    print(f"MP3 file '{output_file_name}' has been created.")

# Example usage
json_file_path = "data.json"  # Replace with your JSON file path
create_mp3_from_json(json_file_path)
