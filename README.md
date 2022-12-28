# Whisper Subtitles

This project uses the Automatic speech recognition (ASR) model [OpenAI Whisper](https://github.com/openai/whisper) to create subtitles for talks. 


Whisper-ASR-youtube-subtitles: https://huggingface.co/spaces/Finnish-NLP/Whisper-ASR-youtube-subtitles

## Get started

Requires ffmpeg

Create a virtual environment and install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
```

Enter virtual environment
```bash
source venv/bin/activate
```

Exit virtual environment
```bash
deactivate
```