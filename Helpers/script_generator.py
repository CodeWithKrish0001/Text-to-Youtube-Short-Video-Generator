import google.generativeai as genai
from dotenv import dotenv_values
import os
import re

class ScriptGenerator:
    def __init__(self):
        env_vars = dotenv_values(".env")
        self.api_key = env_vars.get("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY not found. Check your .env file.")

        genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction="You are a professional script writer. You are given a topic and must generate a professional script on that topic for a YouTube short about 45 seconds long. Make the script engaging, start with a hook, make it curiosity, and provide only the script in plain text without any additional instructions like **(Visual: Open on a flickering lightbulb in a dusty attic. Eerie music starts softly.)**. nor this '**(Sound of tiny feet thumping), (Roaring sound)**, (Beat),(pause)...... also dont use these things. Give only the script, make it 45 seconds long, and finish the topic or video. Don't tell for a second part, and make it in easy English without hard words."
        )

        os.makedirs("Data/Scripts", exist_ok=True)

    def generate_script(self, topic):
        """Generates a script based on the given topic."""
        response = self.model.generate_content(topic)
        script_text = response.text
        with open("Data/Scripts/script.txt", "w", encoding="utf-8") as f:
            f.write(script_text) 
        return script_text

    def format_script(self, text):
        """Formats the script for better readability."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        formatted_script = "\n".join(sentence.strip() for sentence in sentences)
        return formatted_script

    def save_format_script(self, script_text):
        """Saves the formatted script to a file."""
        formatted_text = self.format_script(script_text)
        with open("Data/Scripts/script.txt", "w", encoding="utf-8") as f:
            f.write(formatted_text)

if __name__ == "__main__":
    generator = ScriptGenerator()
    topic = input("Enter a topic: ")
    script = generator.generate_script(topic)
    print("\n📝 Generated Script:\n")
    
    print(script)
    # generator.save_format_script(script)
