# ASR Subtitles

## Introduction

This project uses the Automatic Speech Recognition (ASR) model [OpenAI Whisper](https://github.com/openai/whisper) to create subtitles for talks and and other video's. Whisper correctly transcribes most words and sentences, but not everything, so manual correction MUST be performed at a later time. An example of wrong recognition is that it can in some cases recognize the word 'batch' as 'patch', read the [Whisper model card](https://github.com/openai/whisper/blob/main/model-card.md) for more information on transcription precision.

Fetch a talk from [media.ccc.de](https://media.ccc.de/) to test the program out.

Much inspiration have been drawn from [Whisper-ASR-youtube-subtitles](https://huggingface.co/spaces/Finnish-NLP/Whisper-ASR-youtube-subtitles).

## Get started

### Install dependencies
As noted in the [OpenAI Whisper](https://github.com/openai/whisper) repository, the library should work with Python 3.7 and later.
```bash
# Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg python3.8 python3.8-venv

# Arch Linux
sudo pacman -S ffmpeg, python, python-virtualenv
```


Create a virtual environment and install dependencies.
Look into the [OpenAI Whisper setup](https://github.com/openai/whisper#setup) if you encounter dependency errors.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install git+https://github.com/openai/whisper.git 
```

### Run
Enter virtual environment and run
```bash
source venv/bin/activate
python app.py
```

Exit virtual environment
```bash
deactivate
```


### Miscellaneous
Update Whisper library
```bash
pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
```