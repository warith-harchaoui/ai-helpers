# AI Helpers

[🇫🇷](LISEZMOI.md) · [🇬🇧](README.md)

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](LICENSE) [![Python](https://img.shields.io/badge/python-3.10%E2%80%933.13-blue.svg)](#)

Meta-package that installs the full **AI Helpers** suite in one command — a collection of focused Python libraries for AI / media work.

[🕸️ AI Helpers landing page](https://harchaoui.org/warith/ai-helpers)

## What's included

| Helper | Module | What it does |
|---|---|---|
| [os-helper](https://github.com/warith-harchaoui/os-helper) | `os_helper as osh` | Cross-platform file / system / hash / config / timing utilities. |
| [audio-helper](https://github.com/warith-harchaoui/audio-helper) | `audio_helper as ah` | Load / convert / split / concat audio; optional Demucs source separation. |
| [video-helper](https://github.com/warith-harchaoui/video-helper) | `video_helper as vh` | Multi-backend frame extraction (VidGear / PyAV / ffmpeg-pipe), conversion, subtitles. |
| [sftp-helper](https://github.com/warith-harchaoui/sftp-helper) | `sftp_helper as sftph` | Paramiko-based SFTP with strict host-key verification + `remote_tempfile`. |
| [youtube-helper](https://github.com/warith-harchaoui/youtube-helper) | `youtube_helper as yth` | yt-dlp wrapper: downloads, stream catalog / picker, no-API engagement metadata. |
| [bucket-helper](https://github.com/warith-harchaoui/bucket-helper) | `bucket_helper as bh` | boto3 for AWS S3 + S3-compatible (MinIO / R2 / B2 / Spaces / Wasabi). |
| [podcast-helper](https://github.com/warith-harchaoui/podcast-helper) | `podcast_helper as ph` | Universal audio stream consumer: URL-in → PCM-out (RSS, yt-dlp, direct, …). |
| [capture-helper](https://github.com/warith-harchaoui/capture-helper) | `capture_helper as ch` | OBS-inspired capture / process / publish layer (scaffold). |

All licensed under **BSD-3-Clause** (same as scikit-learn / numpy / scipy).

## Install

```bash
pip install --force-reinstall --no-cache-dir \
  git+https://github.com/warith-harchaoui/ai-helpers.git@v0.1.0
```

This pulls in all 8 helpers at compatible pinned versions plus their
transitive dependencies (`yt-dlp`, `ffmpeg-python`, `boto3`, `paramiko`,
`opencv-python`, `vidgear`, `feedparser`, `podcastparser`, …).

You still need `ffmpeg` on PATH for the media helpers (audio / video /
youtube / podcast / capture):

- macOS 🍎 : `brew install ffmpeg`

  (install `brew` thanks to [brew.sh](https://brew.sh/))
- Ubuntu 🐧 : `sudo apt install ffmpeg`
- Windows 🪟 : [ffmpeg.org/download.html](https://ffmpeg.org/download.html)

## Pinned versions

This release tracks the helpers at these tags:

```
os-helper       @ v1.3.0
audio-helper    @ v1.4.2
video-helper    @ v1.5.1
sftp-helper     @ v2.1.0
youtube-helper  @ v1.1.2
bucket-helper   @ v0.1.0
podcast-helper  @ v0.1.3
capture-helper  @ v0.0.1
```

A meta-package release will follow each helper release. If you only need
one helper, install it directly — the meta-package exists for the
all-batteries-included case.

## Quick example

```python
import os_helper as osh
import audio_helper as ah
import video_helper as vh
import youtube_helper as yth

osh.verbosity(2)

# Download a YouTube video + extract audio + load PCM samples
yth.download_video("https://www.youtube.com/watch?v=YE7VzlLtp-4", "bunny.mp4")
yth.download_audio("https://www.youtube.com/watch?v=YE7VzlLtp-4", "bunny.mp3")
audio, sr = ah.load_audio("bunny.mp3")
print(vh.video_dimensions("bunny.mp4"))
# {'width': 1280, 'height': 720, 'duration': 596.458, 'frame_rate': 24.0, 'has_sound': True}
```

# Author
[Warith HARCHAOUI](https://linkedin.com/in/warith-harchaoui)

# Acknowledgements
Special thanks to [Mohamed Chelali](https://mchelali.github.io) and [Bachir Zerroug](https://www.linkedin.com/in/bachirzerroug) for fruitful discussions.

# License
This project is licensed under the terms of the [BSD-3-Clause](LICENSE) license.
