# ASR Subtitles

## Introduction

This project uses the Automatic Speech Recognition (ASR) model [OpenAI Whisper](https://github.com/openai/whisper) to create subtitles for talks and similar video's.
Whisper correctly transcribes most words and sentences with the base model, but the Word Error Rate (WER) can be decreased with the larger (and more resource hungry) models. 

This tool can potentially take much of the required workload out of transcribing subtitles, however, manual correction MUST be performed at a later time to ensure of precision.

An example of wrong word recognition with the base model, is the word 'batch' can be recognized as 'patch' in some cases. 
While this is the case for the base and tiny model, it is not necessarily an issue in the larger models. Read the [OpenAI Whisper model card](https://github.com/openai/whisper/blob/main/model-card.md) and the paper [Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) by Radford et al. for more information on transcription precision.

Fetch a talk from [media.ccc.de](https://media.ccc.de/) to test the program out.

### Performance

Performance have been tested on the 18 minute talk "[This years badge](https://media.ccc.de/v/bornhack2022-4192-this-years-badge)" by Thomas Flummer from Bornhack 2022.

|  Processor | Model | Transcribe duration |
| --- | --- | --- |
|3 GHz CPU | base model | 15 min 12 sec |
| Nvidia Tesla M60, 1 core | base model | 1 min 36 sec |
| Nvidia Tesla M60, 1 core | medium model | 7 min 11 sec |
| Nvidia RTX 3090 | tiny model | 21 sec |
| Nvidia RTX 3090 | base model | 35 sec |
| Nvidia RTX 3090 | small model | 1 min 4 sec |
| Nvidia RTX 3090 | medium model | 2 min 3 sec |
| Nvidia RTX 3090 | large model |  2 min 53 sec |
| Nvidia RTX A4000 | tiny model |  47 sec |

## Get started

### Install dependencies
As noted in the [OpenAI Whisper](https://github.com/openai/whisper) repository, the library should work with Python 3.7 and later.

Required dependencies are ffmpeg, a Python 3 version with the virtual environment package, python dependencies listed in requirements.txt file as well as Nvidia drivers for your GPU.

#### Ubuntu 20.04 LTS

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install ffmpeg python3.9 python3.9-venv
```

**Nvidia drivers**

Install GPU drivers. In case OpenAI Whisper cannot find drivers, it will use the CPU on the machine to transcribe, which takes significantly longer.

```bash
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update
sudo apt install nvidia-common ubuntu-drivers-common -y
sudo ubuntu-drivers devices
sudo ubuntu-drivers autoinstall
```

#### Debian 12 "Bookworm"

Install the following packages

```bash
sudo apt update
sudo apt install linux-headers-amd64 ffmpeg python3.11 python3.11-venv
```

See the following [wiki article](https://wiki.debian.org/NvidiaGraphicsDrivers#bookworm-525) for Nvidia driver installation instructions.


#### Arch Linux

Install the following packages

```bash
sudo pacman -Sy ffmpeg python python-virtualenv
```

More information on the [Arch wiki](https://wiki.archlinux.org/title/NVIDIA) about Nvidia drivers.

#### Python Environment Setup

Create a virtual environment and install dependencies.
Look into the [OpenAI Whisper setup](https://github.com/openai/whisper#setup) if you encounter dependency errors.
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install git+https://github.com/openai/whisper.git 
```

### Run
Enter virtual environment and run
```bash
source venv/bin/activate
python app.py --video <video_file> --model <whipser model>
```

Parameters:
```
usage: app.py [-h] [-v VIDEO] [-l] [-m WHISPER_MODEL]

Create subtitle file from video.

options:
  -h, --help            show this help message and exit
  -v VIDEO, --video VIDEO
                        Video file to be processed
  -l, --language        Manually set transcription language
  -m WHISPER_MODEL, --model WHISPER_MODEL
                        Set OpenAI Whisper model
```

The sample below runs ASR subtitles on a directory of videos with the large OpenAI Whisper model, and times it as well:
```bash
time python app.py --video videos/ --model large
```

The program outputs a [SRT](https://en.wikipedia.org/wiki/SubRip) file named `<video_file>.srt` in the same directory as the video file. You can use [VLC](https://www.videolan.org/vlc/) or other media players to play the video and add the subtitles.

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
