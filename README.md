# AI Helpers

[🇫🇷](https://github.com/warith-harchaoui/ai-helpers/blob/main/LISEZMOI.md) · [🇬🇧](https://github.com/warith-harchaoui/ai-helpers/blob/main/README.md)

[![CI](https://github.com/warith-harchaoui/ai-helpers/actions/workflows/ci.yml/badge.svg)](https://github.com/warith-harchaoui/ai-helpers/actions/workflows/ci.yml) [![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/warith-harchaoui/ai-helpers/blob/main/LICENSE) [![Python](https://img.shields.io/badge/python-3.10%E2%80%933.13-blue.svg)](#) [![Local-first](https://img.shields.io/badge/privacy-local--first-2f6f5e.svg)](#the-promise)

Meta-package that installs the full **AI Helpers** suite in one command — a collection of focused Python libraries for AI / media work.

[🌍 AI Helpers landing page](https://harchaoui.org/warith/ai-helpers)

## What's included

The helpers are organized into **groups** — install just the corner you need (see [Install](#install)).

| Group | Helper | Module | What it does |
|---|---|---|---|
| 🧱 Core | [os-helper](https://github.com/warith-harchaoui/os-helper) | `os_helper as osh` | Cross-platform file / system / hash / config / timing utilities. |
| 🔊 Audio & voice | [audio-helper](https://github.com/warith-harchaoui/audio-helper) | `audio_helper as ah` | Load / convert / split / concat audio; optional source separation. |
| 🔊 Audio & voice | [vocal-helper](https://github.com/warith-harchaoui/vocal-helper) | `vocal_helper as voh` | Live PCM → Voice Activity Detection → online speaker diarization → Speech to Text → optional LLM summary. |
| 🔊 Audio & voice | [speaker-helper](https://github.com/warith-harchaoui/speaker-helper) | `speaker_helper as spkh` | Offline + streaming Speech Synthesis over a local engine, with voice cloning — the inverse of vocal-helper. |
| 🎬 Video & capture | [video-helper](https://github.com/warith-harchaoui/video-helper) | `video_helper as vh` | Multi-backend frame extraction (VidGear / PyAV / ffmpeg-pipe), conversion, subtitles. |
| 🎬 Video & capture | [capture-helper](https://github.com/warith-harchaoui/capture-helper) | `capture_helper as ch` | Live multi-source capture layer — camera + mic iterators (composing with video-helper / podcast-helper contracts) plus a browser scene configurator. |
| 🌐 Media acquisition | [youtube-helper](https://github.com/warith-harchaoui/youtube-helper) | `youtube_helper as yth` | yt-dlp wrapper: downloads, stream catalog / picker, no-API engagement metadata. |
| 🌐 Media acquisition | [podcast-helper](https://github.com/warith-harchaoui/podcast-helper) | `podcast_helper as ph` | Universal audio stream consumer: URL-in → PCM-out (RSS, yt-dlp, direct, …). |
| 🗄️ Storage & transfer | [bucket-helper](https://github.com/warith-harchaoui/bucket-helper) | `bucket_helper as bh` | boto3 for AWS S3 + S3-compatible (MinIO / R2 / B2 / Spaces / Wasabi). |
| 🗄️ Storage & transfer | [sftp-helper](https://github.com/warith-harchaoui/sftp-helper) | `sftp_helper as sftph` | Paramiko-based SFTP with strict host-key verification + `remote_tempfile`. |
| 🧩 Misc | [md2star](https://github.com/warith-harchaoui/md2star) | `md2star` | Markdown → DOCX / PPTX / PDF bridge on Pandoc, with curated styling, Mermaid rendering and bibliography support. |
| 🧩 Misc | [wallet-helper](https://github.com/warith-harchaoui/wallet-helper) | `wallet_helper as wh` | Never run the same heavy call twice: persistent, content-addressed memoization + single-flight. A toolbox, close in spirit to os-helper. |
| 🧩 Misc | [standingpoint](https://github.com/warith-harchaoui/standingpoint) | `standpoint as sp` | Turn a comparison table into a labelled 2D positioning map, a written analysis and a YAML of coordinates — PCA perceptual maps, one command. |
| 🧩 Misc | [notes-helper](https://github.com/warith-harchaoui/notes-helper) | `notes_helper` | Fully-local, privacy-first diarized meeting recorder. **Work in progress** — not installed by the meta-package yet. |

The 13 bundled packages are licensed under **BSD-3-Clause** (same as scikit-learn / numpy / scipy); the WIP `notes-helper` is Apache-2.0.

## The Promise

**Local-first by design.** The AI Helpers process your data on *your* machine with open-source tooling — no SaaS, no telemetry, no account, no cloud lock-in. Being honest about exactly where that holds:

- **Guaranteed local** — os-helper, audio-helper, video-helper, capture-helper, vocal-helper, md2star and wallet-helper run entirely on your machine; your files, audio, camera/mic, documents and cached results never leave it.
- **Fetches only what you ask for** — youtube-helper and podcast-helper must contact the sites/feeds you point them at (there is no local-first way to download a remote video or episode), but they upload nothing about you and keep everything local. A few helpers download a model or template once on first run, then work offline.
- **Deliberately *not* local-first** — bucket-helper and sftp-helper exist to move your data to remote storage / servers. Sovereignty there means *you* choose the endpoint: your own MinIO / SFTP box is sovereign; a third-party cloud is your call.

## Install

Every helper is on PyPI and installs independently, so the simplest path is
to install just the **group** you need — each pulls in `os-helper`
automatically:

```bash
# 🔊 Audio & voice
pip install audio-helper vocal-helper speaker-helper

# 🎬 Video & capture
pip install video-helper capture-helper

# 🌐 Media acquisition
pip install youtube-helper podcast-helper

# 🗄️ Storage & transfer
pip install bucket-helper sftp-helper

# 🧩 Misc (docs, cache, positioning maps)
pip install md2star wallet-helper standpoint

# 🧱 Core only (foundation utilities)
pip install os-helper
```

Prefer a single entry point? The **`ai-helpers`** meta-package exposes the
same groups as extras. Its base install is light (just `os-helper`); add the
group(s) you want — or `[all]` for the kitchen sink (deliberately heavy,
almost too much):

```bash
# one group
pip install "ai-helpers[audio] @ git+https://github.com/warith-harchaoui/ai-helpers.git@v0.5.0"

# several groups at once
pip install "ai-helpers[audio,video] @ git+https://github.com/warith-harchaoui/ai-helpers.git@v0.5.0"

# absolutely everything
pip install "ai-helpers[all] @ git+https://github.com/warith-harchaoui/ai-helpers.git@v0.5.0"
```

Available extras: `audio`, `video`, `acquire`, `storage`, `misc`, `all`.

You still need `ffmpeg` on PATH for the media helpers (audio / video /
youtube / podcast / capture / vocal):

- macOS 🍎 : `brew install ffmpeg`

  (install `brew` thanks to [brew.sh](https://brew.sh/))
- Ubuntu 🐧 : `sudo apt install ffmpeg`
- Windows 🪟 : [ffmpeg.org/download.html](https://ffmpeg.org/download.html)

## Pinned versions

This release tracks the helpers at these tags:

```
os-helper       @ v1.7.2
audio-helper    @ v1.6.0
video-helper    @ v1.7.0
sftp-helper     @ v2.3.0
youtube-helper  @ v1.4.0
bucket-helper   @ v0.3.0
podcast-helper  @ v0.4.0
capture-helper  @ v0.3.0
vocal-helper    @ v0.6.0
speaker-helper  @ v0.7.4
md2star         @ v2.8.0
wallet-helper   @ v0.3.0
standingpoint   @ v0.2.0
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

## Composed examples

The helpers are designed to chain. Here the suite turns **a YouTube talk into a
shareable Word document and PDF** — acquisition, speech-to-text, and typesetting,
each stage a different helper:

**🌐 youtube-helper → 🗣️ vocal-helper → 📄 md2star (`md2docx` / `md2pdf`)**

```python
import youtube_helper as yth      # 🌐 acquisition
import audio_helper as ah          # 🔊 decode to PCM
import vocal_helper as voh         # 🗣️ speech-to-text (Whisper)

URL = "https://www.youtube.com/watch?v=YE7VzlLtp-4"

# 1) Acquire — pull the talk's audio (16 kHz mono is ideal for ASR).
yth.download_audio(URL, "talk.mp3", target_sample_rate=16000)

# 2) Transcribe — Whisper on the decoded PCM (to_numpy=True → float32 array).
pcm, sr = ah.load_audio("talk.mp3", target_sample_rate=16000, to_mono=True, to_numpy=True)
transcript = voh.transcribe_pcm(pcm, sr, language="en")

# 3) Hand off to md2star — write a titled Markdown file for typesetting.
with open("talk.md", "w", encoding="utf-8") as fh:
    fh.write(f"# Talk transcript\n\n_Source: {URL}_\n\n{transcript}\n")
```

```bash
# 4) Typeset the transcript as a Word document and a PDF (md2star CLIs).
md2docx talk.md      # → talk.docx
md2pdf  talk.md      # → talk.pdf
```

Because md2star's `md → docx → pdf` render is a faithful, reversible one (see the
[md2star round-trip identity](https://github.com/warith-harchaoui/md2star#round-trip-fidelity)),
the resulting documents can be read straight back to Markdown without losing the
transcript's text.

## Author
[Warith HARCHAOUI](https://linkedin.com/in/warith-harchaoui)

## Acknowledgements
Special thanks to [Mohamed Chelali](https://mchelali.github.io) and [Bachir Zerroug](https://www.linkedin.com/in/bachirzerroug) for fruitful discussions.

## License
This project is licensed under the terms of the [BSD-3-Clause](https://github.com/warith-harchaoui/ai-helpers/blob/main/LICENSE) license.
