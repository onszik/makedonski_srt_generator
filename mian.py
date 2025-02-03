import whisper # type: ignore
from tqdm import tqdm # type: ignore
import warnings
import os
import sys

from autocorrect import *

if len(sys.argv) != 5:
    print(len(sys.argv))
    print("Usage: python external_script.py <boolean> <file_path> <int_value> <str_value>")
    sys.exit(1)

# Get the arguments
use_autocorrect = sys.argv[1].lower() == 'true'  # Convert the argument to boolean
file_path = sys.argv[2]
max_words_per_segment = int(sys.argv[3])
out_location = sys.argv[4]

print(f"Use Autocorrect: {use_autocorrect}")
print(f"Input File: {file_path}")
print(f"Word Limit: {max_words_per_segment}")
print(f"Output Location: {out_location}")

out_path = out_location + "\captions.srt"
print(out_path)

warnings.filterwarnings("ignore", category=FutureWarning)  # Ignore FutureWarnings
warnings.filterwarnings("ignore", category=UserWarning)    # Ignore UserWarnings

language = "mk"

print("Starting...")

# Function to format time in hh:mm:ss,SSS format
def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"

def transcribe_audio(audio_file, language=language):
    model = whisper.load_model("small")
    result = model.transcribe(audio_file, language=language, verbose=True)
    
    # Create a progress bar for transcription
    total_steps = len(result['segments'])
    progress_bar = tqdm(result['segments'], desc="Transcribing", total=total_steps)
    
    captions = ""
    index = 1  # Subtitle index starts from 1
    
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

with open(out_path, 'w', encoding='utf-8-sig') as f:  # Use 'utf-8-sig' for proper encoding
    f.write(captions)

print("Transcription complete!")
