import google.generativeai as genai
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

class ImageGenerator:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.gemini_api_key:
            raise ValueError("❌ GEMINI_API_KEY not found. Check your .env file.")

        genai.configure(api_key=self.gemini_api_key)

        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction="You are an AI prompt generator. Generate detailed AI image prompts based on the given text scene. Only generate one prompt in a paragraph."
        )

        os.makedirs("Data/Generated_Images", exist_ok=True)

    def load_script_lines(self, script_file="Data/Scripts/script.txt"):
        """Loads script and splits it into individual lines."""
        if not os.path.exists(script_file):
            print(f"❌ Script file not found: {script_file}")
            return []

        with open(script_file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]

    def generate_image_prompt(self, scene_text):
        """Generates an AI image prompt for a given scene using Gemini AI."""
        response = self.model.generate_content(f"Scene: {scene_text}")
        return response.text.strip()

    def download_image(self, prompt, img_number):
        """Downloads AI-generated images from Pollinations API using Flux model."""
        width, height, seed, model = 720, 1280, 42, "flux"
        image_url = f"https://pollinations.ai/p/{prompt}?width={width}&height={height}&seed={seed}&model={model}"

        try:
            response = requests.get(image_url, timeout=35)

            if response.status_code == 200:
                filename = f"Data/Generated_Images/image_{img_number}.jpg"
                with open(filename, "wb") as file:
                    file.write(response.content)
                print(f"✅ Image {img_number} saved: {filename}")
            else:
                print(f"❌ Failed to fetch image {img_number}. Status Code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error fetching image {img_number}: {e}")

    def generate_image_prompts(self):
        """Processes script, generates image prompts, and downloads images."""
        script_lines = self.load_script_lines()
        
        for i, line in enumerate(script_lines, start=1):
            print(f"🎨 Generating prompt for line {i}/{len(script_lines)}...")
            image_prompt = self.generate_image_prompt(line)
            print(f"📜 Prompt {i}: {image_prompt}")
            
            self.download_image(image_prompt, i)
            time.sleep(1) 

if __name__ == "__main__":
    generator = ImageGenerator()
    generator.generate_image_prompts()
