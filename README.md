# ASR Subtitles

## Introduction

This project uses the Automatic Speech Recognition (ASR) model [OpenAI Whisper](https://github.com/openai/whisper) to create subtitles for talks and similar video's.
Whisper correctly transcribes most words and sentences with the base model, but the Word Error Rate (WER) can be decreased with the larger (and more ressource hungry) models. 

This tool can potentially take much of the required workload out of transcribing subtitles, however, manual correction MUST be performed at a later time to ensure of precision.

An example of wrong word recognition with the base model, is the word 'batch' can be recognized as 'patch' in some cases, but can be correctly recognized with the medium model. Read the [OpenAI Whisper model card](https://github.com/openai/whisper/blob/main/model-card.md) and the paper [Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) by Radford et al. for more information on transcription precision.

Fetch a talk from [media.ccc.de](https://media.ccc.de/) to test the program out.

### Performance
Performance have been tested on the 18 minute talk "[This years badge](https://media.ccc.de/v/bornhack2022-4192-this-years-badge)" by Thomas Flummer from Bornhack2022.

|  Processor | Model | Computation duration |
| --- | --- | --- |
|3 GHz CPU | base model | 15 min 12 sec |
| Nvidia Tesla M60, 1 core | base model | 1 min 36 sec |
| Nvidia Tesla M60, 1 core | medium model | 7 min 11 sec |


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
python app.py --video <video_file>
```

The program outputs a [SRT](https://en.wikipedia.org/wiki/SubRip) file named `<video_file>.srt`. You can use VLC or other media players to play the video and add the subtitles.

Exit virtual environment
```bash
deactivate
```


### Miscellaneous
Update Whisper library
```bash
pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
```


# Thanks to
- [OpenAI Whisper](https://github.com/openai/whisper) for their wonderful models
- Much inspiration have been drawn from [Whisper-ASR-youtube-subtitles](https://huggingface.co/spaces/Finnish-NLP/Whisper-ASR-youtube-subtitles)
