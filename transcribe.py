import whisper # type: ignore
from tqdm import tqdm # type: ignore
import warnings
import os

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

        text = correct_text(segment['text']) if use_autocorrect == "Y" else segment['text']
        
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