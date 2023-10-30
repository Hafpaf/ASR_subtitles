import whisper
import pandas as pd
import argparse
import os

# Arguments
parser = argparse.ArgumentParser(description='Create subtitle file from video.')
parser.add_argument('-v', '--video',
                    dest='video',
                    type=str,
                    help='Video file to be processed'
                    )
parser.add_argument('-l', '--language',
                    dest='language',
                    action='store_const',
                    const='en', # ToDo: defaults to None in order for Whisper to recognize the language itself
                    help='Manually set transcription language',
                    )
parser.add_argument('-m', '--model',
                    dest='whisper_model',
                    default="base",
                    help='Set OpenAI Whisper model',
                    )

# ToDo: Fix text in start of video before speaker talks.
def transcribe_audio(video_file_path: str, model, transcribe_options) -> pd.DataFrame:
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
        print(f'Transcribing with local model')

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
    file_path = args.video
    if args.language is not None:
        language_setting = args.language
    else:
        language_setting = None

    # Load OpenAI Whisper model.
    # The paper describes the precision of the models in more details: https://arxiv.org/abs/2212.04356
    model = whisper.load_model(args.whisper_model)

    # I got no idea of what this has to do with 'temperature',
    #  but Whisper transcribes more precisely.
    # Borrowed from here: https://huggingface.co/spaces/Finnish-NLP/Whisper-ASR-youtube-subtitles/blob/main/app.py#L28
    # See https://github.com/openai/whisper/blob/f82bc59f5ea234d4b97fb2860842ed38519f7e65/whisper/transcribe.py#L263C2-L263C2
    transcribe_options = dict(beam_size=3, best_of=3, without_timestamps=False)#, language=language_setting)

    if os.path.isdir(file_path): # If directory, then loop over files
        for file in os.listdir(file_path):
            tmp_file_path=f'{file_path}{file}'
            transcribe = transcribe_audio(tmp_file_path, model, transcribe_options)
            create_srt(transcribe, tmp_file_path)
            print(f'Transcribed video: {tmp_file_path}')
    else: # Transcribe single file
        transcribe = transcribe_audio(file_path, transcribe_options)
        create_srt(transcribe, file_path)

if __name__=="__main__":
    main()
