import asyncio
import edge_tts
import os
from dotenv import dotenv_values

class VoiceOverGenerator:
    def __init__(self):
        env_vars = dotenv_values(".env")
        self.assistant_voice = env_vars.get("AssistantVoice")
        os.makedirs("Data", exist_ok=True)

    async def text_to_audio(self, text):
        file_path = "Data/Speech/speech.mp3"
        if os.path.exists(file_path):
            os.remove(file_path)
        
        communicate = edge_tts.Communicate(text, self.assistant_voice, pitch='+5Hz', rate='+13%')
        await communicate.save(file_path)

    def generate_voiceover(self, text):
        asyncio.run(self.text_to_audio(text))

if __name__ == "__main__":
    generator = VoiceOverGenerator()
    text = input("Enter text for voiceover: ")
    generator.generate_voiceover(text)
