from Helpers.script_generator import ScriptGenerator
from Helpers.voiceover_generator import VoiceOverGenerator
from Helpers.image_generator import ImageGenerator
from Helpers.video_generator import VideoGenerator
from Helpers.captions_adder import CaptionGenerator
import os
import shutil

class VideoCreationPipeline:
    def __init__(self):
        self.script_generator = ScriptGenerator()
        self.voiceover_generator = VoiceOverGenerator()
        self.image_generator = ImageGenerator()
        self.video_generator = VideoGenerator()
        self.caption_adder = CaptionGenerator()
        self.cleanup_folders = ["Data/Scripts", "Data/Generated_Images", "Data/Speech"]

    def clear_old_files(self):
        """Deletes all previously generated files in Data/ folders."""
        for folder in self.cleanup_folders:
            if os.path.exists(folder):
                for file in os.listdir(folder):
                    file_path = os.path.join(folder, file)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print(f"⚠️ Error deleting {file_path}: {e}")

    def run(self):
        print("🗑️ Clearing old files...")
        self.clear_old_files()

        os.makedirs("Data/Scripts", exist_ok=True)
        os.makedirs("Data/Generated_Images", exist_ok=True)
        os.makedirs("Data/Video", exist_ok=True)
        os.makedirs("Data/Speech", exist_ok=True)

        topic = input("Enter the topic: ")

        print("📝 Generating script...")
        script = self.script_generator.generate_script(topic)

        print("🎙️ Generating Voiceover...")
        self.voiceover_generator.generate_voiceover(script)

        print("Formatting Script...")
        self.script_generator.save_format_script(script)

        print("🖼️ Generating Images...")
        self.image_generator.generate_image_prompts()

        print("🎬 Generating Video...")
        video_path = self.video_generator.generate_video(topic)

        print("📝 Adding Captions...")
        self.caption_adder.process_video(video_path)

        print(f"✅ Final video with captions saved in 'Video/{topic}.mp4'")

if __name__ == "__main__":
    pipeline = VideoCreationPipeline()
    pipeline.run()
