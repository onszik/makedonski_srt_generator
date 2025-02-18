# Macedonian Subtitle Generator

![Python](https://img.shields.io/badge/Python-3.8%2B-green)  
![License](https://img.shields.io/badge/License-MIT-blue.svg)

### Ako nekoj znajt kako da ja podobrit preciznosta pls fork i napraj to sho mislis slobodno

This Python script automatically generates and synchronizes subtitles in Macedonian for audio/video files. It uses OpenAI's Whisper model for transcription and provides options for autocorrection and subtitle segmentation.

## Features
- **Automatic Transcription**: Converts audio/video files to Macedonian subtitles.
- **Customizable Segmentation**: Splits subtitles into segments based on a user-defined word limit.
- **Autocorrection**: Optionally corrects transcribed text for improved accuracy.
- **Progress Tracking**: Displays a progress bar during transcription.

Uses OpenAI Whisper for audio transcription

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App
### GUI
To launch the GUI, run:
   ```bash
   python gui.py
   ```

### Command line use
   ```bash
   python subtitle_generator.py --input video.mp4 --output C:\Users\User\Desktop --words_per_line 5 --autocorrect
   ```
- --input takes a file path to the video or audio file to transcribe (supported formats: .mp3, .wav, .m4a, .flac, .ogg, .mp4)
- --output is the path where the .srt file will be written
- --words_per_line is the max number of words which will appear on screen at the same time (optional, default: 5)
- --autocorrect determines if autocorrection will be used for words that may be wrong (optional but recomended)

## Compiling into an EXE (Windows)
You can compile this app into an executable for Windows for those who aren't comfortable using the command line:

1. Instrall pyinstaller:
   ```bash
   pip install pyinstaller
   ```

2. Compile the code:
   ```bash
   pyinstaller --noconsole --onefile --name SubtitleGenerator gui.py
   ```

3. The compiled .exe will be in the dist/ folder
