# AI-Generated Short Video Creator

This project automates the process of generating short AI-powered videos. It takes a topic as input and performs the following steps:
1. Generates a script using AI.
2. Creates a voiceover.
3. Generates AI images based on script scenes.
4. Compiles images and voiceovers into a video.
5. Adds captions to the final video.

## Features
- **Automated Script Writing**: Uses AI to generate engaging scripts.
- **AI Voiceover Generation**: Converts scripts into high-quality speech.
- **AI Image Generation**: Creates visuals based on script content.
- **Video Compilation**: Combines images and voiceover to create a short video.
- **Captioning System**: Adds word-level synced captions to videos.

## Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg installed (required for MoviePy)
- CUDA-enabled GPU (optional for faster processing with WhisperX)

### Install Dependencies
Clone the repository and install the required packages:
```sh
pip install -r requirements.txt
```

## Usage

### 1. Set Up API Keys
Create a `.env` file in the project root and add the following:
```
GEMINI_API_KEY=your_gemini_api_key
AssistantVoice=your_preferred_voice
```

### 2. Run the Video Creation Pipeline
```sh
python main.py
```
You will be prompted to enter a topic, and the system will generate the video automatically.

## Project Structure
```
├── main.py                # Main execution file
├── Helpers/
│   ├── captions_adder.py       # Adds captions to videos
│   ├── image_generator.py      # AI-based image generation
│   ├── script_generator.py     # AI script writing module
│   ├── video_generator.py      # Video compilation logic
│   ├── voiceover_generator.py  # AI voiceover system
├── requirements.txt        # List of dependencies
├── Data/                   # Stores generated scripts, images, and voiceovers
├── Video/                  # Stores generated videos
├── .env                    # API keys and configurations
```

## Dependencies
- `edge-tts` (Text-to-Speech)
- `google-generativeai` (AI-generated scripts & images)
- `moviepy` (Video editing)
- `numpy` (Image processing)
- `Pillow` (Text rendering)
- `python-dotenv` (Environment variables)
- `requests` (Downloading AI-generated images)
- `torch` (AI processing)
- `whisper` & `whisperx` (Audio transcription)

## Contribution
Feel free to fork this project, submit issues, or create pull requests!

## Contribution
Feel free to fork this project, submit issues, or create pull requests!

## Next-Level Development
If you want to take this project to the next level, feel free to DM me on Telegram: [@Krish_GFX](https://t.me/Krish_GFX). Your contributions and ideas are always welcome!

## License
This project is licensed under the MIT License.

