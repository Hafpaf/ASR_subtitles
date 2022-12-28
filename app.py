import whisper
import pandas as pd
import time

# Load OpenAI Whisper base model
model = whisper.load_model("base")
transcribe_options = dict(beam_size=3, best_of=3, without_timestamps=False)

video = "import-4192-eng-This_years_badge_hd.mp4"

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio(video)
audio = whisper.pad_or_trim(audio)

# Uses this for now: Whisper-ASR-youtube-subtitles: https://huggingface.co/spaces/Finnish-NLP/Whisper-ASR-youtube-subtitles
def speech_to_text(video_file_path, transcribe_options):

    if(video_file_path == None):
        raise ValueError("Error no video input")
    print(f'video file: {video_file_path}')
    try:
        audio = whisper.load_audio(video_file_path)
    except Exception as e:
        raise RuntimeError("Error converting video to audio")

    last_time = time.time()

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
            # df = df.append(new_row, ignore_index=True)
            df = pd.concat([df, pd.DataFrame([new_row])], axis=0, ignore_index=True)

        return (df)
    except Exception as e:
        raise RuntimeError("Error Running inference with local model", e)


# ToDo: Look into srt library
# ToDo: Fix text in start of video when there is no talking
def create_srt(df):

    print("Starting creation of video wit srt")

    with open('test.srt','w', encoding="utf-8") as file:
        for i in range(len(df)):
            file.write(str(i+1))
            file.write('\n')
            start = df.iloc[i]['start']


            milliseconds = round(start * 1000.0)

            hours = milliseconds // 3_600_000
            milliseconds -= hours * 3_600_000

            minutes = milliseconds // 60_000
            milliseconds -= minutes * 60_000

            seconds = milliseconds // 1_000
            milliseconds -= seconds * 1_000

            file.write(f"{hours}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}")

            stop = df.iloc[i]['end']


            milliseconds = round(stop * 1000.0)

            hours = milliseconds // 3_600_000
            milliseconds -= hours * 3_600_000

            minutes = milliseconds // 60_000
            milliseconds -= minutes * 60_000

            seconds = milliseconds // 1_000
            milliseconds -= seconds * 1_000


            file.write(' --> ')
            file.write(f"{hours}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}")
            file.write('\n')
            file.writelines(df.iloc[i]['text'])
            if int(i) != len(df)-1:
                file.write('\n\n')

    print("SRT DONE")

spt = speech_to_text(video, transcribe_options)
apply_subtitle = create_srt(spt)
# print(spt)
# print(apply_subtitle)