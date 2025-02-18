import whisper # type: ignore
from tqdm import tqdm # type: ignore
import warnings
import sys
import os
import argparse

from autocorrect import *

# Argument Parsing
parser = argparse.ArgumentParser(description="Generate Macedonian subtitles from an audio/video file.")

parser.add_argument("--input", required=True, help="Path to the input audio/video file.")
parser.add_argument("--output", required=True, help="Path to save the generated subtitles.")
parser.add_argument("--words_per_line", type=int, default=5, help="Maximum words on screen at a time (default: 5)")
parser.add_argument("--autocorrect", action="store_true", help="Enable automatic text correction.")

args = parser.parse_args()

# Extracting arguments
file_path = args.input
out_path = os.path.join(args.output, "captions.srt")
max_words_per_segment = args.words_per_line
use_autocorrect = args.autocorrect

print(f"Use Autocorrect: {use_autocorrect}")
print(f"Input File: {file_path}")
print(f"Word Limit: {max_words_per_segment}")
print(f"Output File: {out_path}")


warnings.filterwarnings("ignore", category=FutureWarning)  # Ignore FutureWarnings
warnings.filterwarnings("ignore", category=UserWarning)    # Ignore UserWarnings

language = "mk"

print("Starting...")

# Function to format time in hh:mm:ss,SSS format
def format_time(seconds):
    # Convert seconds to a formatted time string (hh:mm:ss,SSS).
    #
    # Args:
    #     seconds (float): Time in seconds.
    # Returns:
    #     str: Formatted time string.

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"

# Generates SRT file from the audio
def transcribe_audio(audio_file, language=language):
    # Generates SRT file from the transcribed text
    #
    # Args:
    #   input file (audio: mp3, wav, flac, ogg, aac, m4a; video: mp4, avi, mkv, mov, flv)
    #   language (mk po default poso za makedonski e napraena alatkava)
    #               (to change language you should change the language variable and change the word list [mk_full.txt] to the appropriate language)
    #
    # Returns:
    #   str: SRT formatted string

    # Load whisper
    try:
        model = whisper.load_model("small")
    except Exception as e:
        print(f"Error loading Whisper model: {e}")
        sys.exit(1)

    # Transcribe audio
    try:
        result = model.transcribe(audio_file, language=language, verbose=True)
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        sys.exit(1)
    
    # Create a progress bar for transcription
    total_steps = len(result['segments'])
    progress_bar = tqdm(result['segments'], desc="Transcribing", total=total_steps)
    
    captions = ""
    index = 1  # Subtitle index starts from 1
    
    # SRT formatting:
    # (index)
    # (start time) --> (end time)
    # (text content)
    #
    # e.g.
    # 1
    # 00:00:01:000 --> 00:00:02:300
    # Zdravo
    for segment in progress_bar:
        start_time = segment['start']
        end_time = segment['end']

        text = correct_text(segment['text']) if use_autocorrect else segment['text']
        
        words = text.split()
        while len(words) > max_words_per_segment:
            segment_text = " ".join(words[:max_words_per_segment])
            words = words[max_words_per_segment:]
            
            segment_duration = end_time - start_time
            caption_end_time = start_time + (segment_duration * (max_words_per_segment / len(text.split())))

            captions += f"{index}\n{format_time(start_time)} --> {format_time(caption_end_time)}\n{segment_text}\n\n"
            start_time = caption_end_time  # Update start time for next segment
            index += 1
        
        if words:
            segment_text = " ".join(words)
            captions += f"{index}\n{format_time(start_time)} --> {format_time(end_time)}\n{segment_text}\n\n"
            index += 1
    
    return captions

captions = transcribe_audio(file_path, language=language)

# Write output
try:
    with open(out_path, 'w', encoding='utf-8-sig') as f:  # Use 'utf-8-sig' for proper encoding
        f.write(captions)
except Exception as e:
    print(f"Error writing output file: {e}")
    sys.exit(1)

print("Transcription complete!")
