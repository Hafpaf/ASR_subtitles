import whisper
import pandas as pd
import argparse

# Arguments
parser = argparse.ArgumentParser(description='Create subtitle file from video.')
parser.add_argument('-V', '--video',
                    dest='video',
                    type=str,
                    help='Video file to be processed'
                    )

# Load OpenAI Whisper base model. 
# The paper describes the precision of the models in more details: https://arxiv.org/abs/2212.04356
model = whisper.load_model("base")

# I got no idea of what this has to do with 'temperature',
#  but Whisper transcribes more precisely.
# Borrowed from here: https://huggingface.co/spaces/Finnish-NLP/Whisper-ASR-youtube-subtitles/blob/main/app.py#L28
# See https://github.com/openai/whisper/blob/main/whisper/transcribe.py#L264
transcribe_options = dict(beam_size=3, best_of=3, without_timestamps=False)

# ToDo: Fix text in start of video before speaker talks.
def transcribe_audio(video_file_path: str, transcribe_options) -> pd.DataFrame:
    """
    Load file and process the audio

    Transcribe audio to create dataframes with start time, end time and text
    Uses this for now: Whisper-ASR-youtube-subtitles: https://huggingface.co/spaces/Finnish-NLP/Whisper-ASR-youtube-subtitles
    """

    if(video_file_path == None):
        raise ValueError("Error no video input")
    print(f'video file: {video_file_path}')
    try:
        audio = whisper.load_audio(video_file_path)
    except Exception as e:
        raise RuntimeError("Error converting video to audio")
    try:
        print(f'Transcribing via local model')

        # Transcribe audio
        transcription = model.transcribe(audio, **transcribe_options)

        # Insert into Pandas frames
        df = pd.DataFrame(columns=['start','end','text'])

        for i,segment in enumerate(transcription['segments']):
            new_row = {'start': segment['start'],
                        'end': segment['end'],
                        'text': segment['text']
                    }
            df = pd.concat([df, pd.DataFrame([new_row])], axis=0, ignore_index=True)

        return (df)
    except Exception as e:
        raise RuntimeError("Error running inference with local model", e)

def time_calc(milliseconds) -> str:
    """
    Calculate start and end time from text and output in SubRip time format
    """

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    return f"{hours}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def create_srt(df: pd.DataFrame, video: str):
    """
    Format dataframes to SRT file
    SubRip file format information: https://en.wikipedia.org/wiki/SubRip
    """

    print("Starting creation SRT file")
    with open(f'{video}.srt','w', encoding="utf-8") as file:
        for i in range(len(df)):
            # Set index
            file.write(str(i+1))
            file.write('\n')

            # Set text start time
            start = df.iloc[i]['start']
            milliseconds = round(start * 1000.0)
            time_format = time_calc(milliseconds)
            file.write(time_format)

            # Set text end time
            stop = df.iloc[i]['end']
            milliseconds = round(stop * 1000.0)
            time_format = time_calc(milliseconds)
            file.write(' --> ')
            file.write(time_format)

            # Insert text
            file.write('\n')
            file.writelines(df.iloc[i]['text'])
            if int(i) != len(df)-1:
                file.write('\n\n')

    print("Subtitles have been finished")

def main():
    args = parser.parse_args()
    video = args.video

    transcribe = transcribe_audio(video, transcribe_options)
    subtitles_creation = create_srt(transcribe, video)

if __name__=="__main__":
    main()