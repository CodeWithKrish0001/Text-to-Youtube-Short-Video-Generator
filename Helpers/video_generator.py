import os
import json
import whisper
from moviepy.editor import *
from moviepy.video.fx.all import crop

class VideoGenerator:
    def __init__(self):
        self.audio_file = "Data/Speech/speech.mp3"
        os.makedirs("Video", exist_ok=True)

    def apply_zoom_effect(self, clip, zoom_in=True):
        """Apply a smooth zoom-in or zoom-out effect while keeping it centered."""
        w, h = clip.size

        def zoom_effect(get_frame, t):
            zoom_factor = 1 + (0.2 * (t / clip.duration)) if zoom_in else 1.2 - (0.2 * (t / clip.duration))
            zoomed_clip = clip.resize(zoom_factor)

            new_w, new_h = zoomed_clip.size
            x_center, y_center = new_w // 2, new_h // 2
            return crop(zoomed_clip, width=w, height=h, x_center=x_center, y_center=y_center).get_frame(t)

        return clip.fl(zoom_effect)

    def load_script_lines(self, script_file="Scripts/script.txt"):
        """Load the script from the file and return a list of lines."""
        with open(script_file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]

    def transcribe_audio_with_script(self, script_file="Data/Scripts/script.txt", output_file="Data/Timestamps/timestamps.json"):
        """
        Transcribes the audio to get the total duration and then distributes timestamps
        to the script lines proportionally so that they exactly cover the audio duration.
        """
        print("⏳ Transcribing audio and generating timestamps...")
        model = whisper.load_model("small")
        result = model.transcribe(self.audio_file)

        total_audio_duration = result["segments"][-1]["end"] if result["segments"] else 52.0
        script_lines = self.load_script_lines(script_file)

        estimated_durations = [max(1.0, 0.25 * len(line.split())) for line in script_lines]
        total_estimated = sum(estimated_durations)

        scale_factor = total_audio_duration / total_estimated
        scaled_durations = [d * scale_factor for d in estimated_durations]

        matched_segments = []
        last_end = 0.0
        for line, duration in zip(script_lines, scaled_durations):
            segment = {"start": last_end, "end": last_end + duration, "text": line}
            matched_segments.append(segment)
            last_end += duration

        os.makedirs("Data", exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(matched_segments, f, indent=4)

        print(f"✅ Timestamps saved to {output_file}")
        return matched_segments

    def generate_video(self, topic):
        """Generates the video and renames output.mp4."""
        timestamps = self.transcribe_audio_with_script()

        image_clips = []
        
        for i, segment in enumerate(timestamps, start=1):
            image_path = f"Data/Generated_Images/image_{i}.jpg"
            if not os.path.exists(image_path):
                continue

            duration = segment["end"] - segment["start"]
            image_clip = self.apply_zoom_effect(ImageClip(image_path).set_duration(duration), zoom_in=(i % 2 == 1))
            image_clips.append(image_clip)

        if image_clips:
            video = concatenate_videoclips(image_clips, method="compose")
            audio = AudioFileClip("Data/Speech/speech.mp3")
            video = video.set_audio(audio)

            os.makedirs("Video", exist_ok=True)
            output_filename = f"Video/{topic}.mp4"

            video.write_videofile(output_filename, fps=24, preset="ultrafast", threads=4)
            print(f"✅ Video successfully saved as '{output_filename}'")
            return output_filename

if __name__ == "__main__":
    topic = input("Enter the topic: ")
    generator = VideoGenerator()
    generator.generate_video(topic) 
