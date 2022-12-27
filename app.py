import whisper
from moviepy.editor import VideoFileClip

# print(whisper.__file__)

# Load OpenAI Whisper base model
model = whisper.load_model("base")

video = "import-4192-eng-This_years_badge_hd.mp4"

# Extract audio from loaded video
def extract_audio(video: str):
  # Load the video file
  clip = VideoFileClip(video)

  # Extract the audio
  audio = clip.audio

  return audio
  
  # Save the audio as an MP3 file
  #audio.write_audiofile("path/to/audio.mp3")

# tmp = extract_audio(video)

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio(video)
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
options = whisper.DecodingOptions()
result = whisper.decode(model, mel, options)

# print the recognized text
print(result.text)