import whisperx
import torch
import json
import numpy as np
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import os

class CaptionGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.compute_type = "float32"
        self.whisper_model = whisperx.load_model("large-v2", device=self.device, compute_type=self.compute_type)

        os.makedirs("Data/Timestamps", exist_ok=True) 
        os.makedirs("Data/Speech", exist_ok=True)
        os.makedirs("Data/Fonts", exist_ok=True)
        os.makedirs("Video", exist_ok=True)

    def generate_word_timestamps(self, audio_path, output_json="Data/Timestamps/word_level_timestamps.json"):
        """Generate word-level timestamps using WhisperX."""
        if not os.path.exists(audio_path):
            print(f"❌ Audio file not found: {audio_path}")
            return None

        audio = whisperx.load_audio(audio_path)
        transcription = self.whisper_model.transcribe(audio, batch_size=16)

        model_a, metadata = whisperx.load_align_model(language_code="en", device=self.device)
        aligned_result = whisperx.align(transcription["segments"], model_a, metadata, audio, self.device)

        words_data = [{"start": w["start"], "end": w["end"], "text": w["word"]} for w in aligned_result.get("word_segments", [])]

        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(words_data, f, indent=4)

        print(f"✅ Word timestamps saved to {output_json}")
        return output_json

    def add_captions_to_video(self, video_path, timestamps_file="Data/Timestamps/word_level_timestamps.json", output_path="Video/output_with_captions.mp4"):
        """Adds perfectly synced word-level captions to the video."""
        if not os.path.exists(video_path) or not os.path.exists(timestamps_file):
            print(f"❌ File(s) not found: {video_path} or {timestamps_file}")
            return
        
        with open(timestamps_file, "r", encoding="utf-8") as f:
            captions = json.load(f)

        video = VideoFileClip(video_path)
        video_width, video_height = video.size

        font_path = "Data/Fonts/arial.ttf"
        if not os.path.exists(font_path):
            print("⚠️ Font file 'arial.ttf' not found. Using default font.")
            font_path = None

        font_size = int(video_height * 0.04)
        padding_x = int(video_width * 0.02)
        padding_top = int(video_height * 0.01)
        padding_bottom = int(video_height * 0.02)
        bg_color = (0, 0, 0, 200)

        text_clips = []

        for caption in captions:
            start, end, text = caption.get("start", 0), caption.get("end", 0), caption.get("text", "")
            text = text.upper()

            if not text.strip():
                continue

            word_duration = end - start
            text_np = self.create_text_image(text, video_width, font_size, padding_x, padding_top, padding_bottom, bg_color, font_path)

            text_clip = (ImageClip(text_np)
                         .set_duration(word_duration)
                         .set_start(start)
                         .set_position(("center", video_height - 300)))

            text_clips.append(text_clip)

        final_video = CompositeVideoClip([video] + text_clips)
        final_video.write_videofile(output_path, fps=video.fps, codec="libx264", preset="ultrafast")

        print(f"✅ Captions added! Video saved at {output_path}")

    @staticmethod
    def create_text_image(text, video_width, font_size, padding_x, padding_top, padding_bottom, bg_color, font_path):
        """Creates an image containing the text."""
        temp_img = Image.new("RGBA", (video_width, font_size + padding_top + padding_bottom), (0, 0, 0, 0))
        draw = ImageDraw.Draw(temp_img)

        try:
            font = ImageFont.truetype(font_path, font_size) if font_path and os.path.exists(font_path) else ImageFont.load_default()
        except:
            font = ImageFont.load_default()

        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = right - left, bottom - top

        bg_width = text_width + 2 * padding_x
        bg_height = text_height + padding_top + padding_bottom
        temp_img = temp_img.resize((bg_width, bg_height))
        draw = ImageDraw.Draw(temp_img)

        draw.rectangle([(0, 0), temp_img.size], fill=bg_color)

        text_x = (bg_width - text_width) // 2
        text_y = padding_top
        draw.text((text_x, text_y), text, font=font, fill="white")

        return np.array(temp_img)

    def process_video(self, video_path):
        """Extracts audio, generates timestamps, and adds captions to video."""
        if not os.path.exists(video_path):
            print(f"❌ Video file not found: {video_path}")
            return

        video = VideoFileClip(video_path)
        audio_path = "Data/Speech/temp_audio.wav"
        video.audio.write_audiofile(audio_path, codec="pcm_s16le")

        print("\n⏳ Generating word-level timestamps...")
        timestamps_file = self.generate_word_timestamps(audio_path)

        if timestamps_file:
            print("\n⏳ Adding captions to video...")
            self.add_captions_to_video(video_path, timestamps_file)

if __name__ == "__main__":
    caption_generator = CaptionGenerator()
    caption_generator.process_video("Video/output.mp4")
