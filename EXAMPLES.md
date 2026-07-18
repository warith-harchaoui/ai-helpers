# AI Helpers — Composed Examples

Recipes that exercise **multiple helpers together**. For per-helper
cookbooks, see each library's own `EXAMPLES.md`:

- [os-helper/EXAMPLES.md](https://github.com/warith-harchaoui/os-helper/blob/main/EXAMPLES.md)
- [audio-helper/EXAMPLES.md](https://github.com/warith-harchaoui/audio-helper/blob/main/EXAMPLES.md)
- [video-helper/EXAMPLES.md](https://github.com/warith-harchaoui/video-helper/blob/main/EXAMPLES.md)
- [sftp-helper/EXAMPLES.md](https://github.com/warith-harchaoui/sftp-helper/blob/main/EXAMPLES.md)
- [youtube-helper/EXAMPLES.md](https://github.com/warith-harchaoui/youtube-helper/blob/main/EXAMPLES.md)
- [bucket-helper/EXAMPLES.md](https://github.com/warith-harchaoui/bucket-helper/blob/main/EXAMPLES.md)
- [podcast-helper/EXAMPLES.md](https://github.com/warith-harchaoui/podcast-helper/blob/main/EXAMPLES.md)
- [capture-helper/EXAMPLES.md](https://github.com/warith-harchaoui/capture-helper/blob/main/EXAMPLES.md)

Every snippet below assumes:

```python
import os_helper as osh
import audio_helper as ah
import video_helper as vh
import youtube_helper as yth
import podcast_helper as ph
import bucket_helper as bh
import sftp_helper as sftph

osh.verbosity(2)
```

and that `ffmpeg` is on PATH.

---

## Table of Contents

1. [Setup](#setup)
2. [YouTube video → download + frames + audio](#youtube-video--download--frames--audio)
3. [RSS podcast → live PCM transcription window](#rss-podcast--live-pcm-transcription-window)
4. [YouTube live → stream-to-PCM (no download)](#youtube-live--stream-to-pcm-no-download)
5. [Stream-to-frames on the GPU (yt-dlp + PyAV + torch)](#stream-to-frames-on-the-gpu-yt-dlp--pyav--torch)
6. [Mirror a render to S3 + SFTP partner inbox](#mirror-a-render-to-s3--sftp-partner-inbox)
7. [Stage-and-share a generated artefact](#stage-and-share-a-generated-artefact)

---

## Setup

Install the full suite in one command:

```bash
pip install --force-reinstall --no-cache-dir \
    git+https://github.com/warith-harchaoui/ai-helpers.git@v0.2.1
```

This pulls in all 8 helpers at compatible pinned versions plus their
transitive dependencies. If you only need one helper, install it
directly — the meta-package exists for the all-batteries-included case.

## YouTube video → download + frames + audio

```python
url = "https://www.youtube.com/watch?v=YE7VzlLtp-4"

# Download the video and audio independently
yth.download_video(url, "bunny.mp4")
yth.download_audio(url, "bunny.mp3")

# Inspect basic stats
print(vh.video_dimensions("bunny.mp4"))
# {'width': 1280, 'height': 720, 'duration': 596.46, 'frame_rate': 24.0, ...}
print(ah.get_audio_duration("bunny.mp3"), "s")
# 596.464 s

# Extract one frame per second for ML inference
for frame in vh.extract_frames("bunny.mp4", frame_interval=1.0):
    # frame.shape == (H, W, 3)  -- BGR uint8 (OpenCV convention)
    process(frame)
```

## RSS podcast → live PCM transcription window

```python
import asyncio
import numpy as np

async def transcribe_latest_npr(feed_url: str, window_s: float = 5.0):
    chunks: list[np.ndarray] = []
    elapsed = 0.0
    async for frame in ph.extract_audio_stream(
        feed_url,                          # podcast-helper auto-picks the latest episode
        target_sample_rate=16000,
        to_mono=True,
        frame_ms=20,
    ):
        chunks.append(frame["pcm"])
        elapsed += 0.02
        if elapsed >= window_s:
            window = np.concatenate(chunks)
            # ... pass `window` to your ASR engine (Whisper, faster-whisper, etc.) ...
            chunks.clear()
            elapsed = 0.0

asyncio.run(transcribe_latest_npr("https://feeds.npr.org/510289/podcast.xml"))
```

The same pattern works on a direct enclosure URL, a YouTube video, a
Twitch VOD — `extract_audio_stream` auto-detects the source kind.

## YouTube live → stream-to-PCM (no download)

```python
async def listen_to_live(url: str):
    async for frame in ph.extract_audio_stream(
        url,
        target_sample_rate=16000,
        to_mono=True,
    ):
        # frame["t_abs_s"] is monotonic from the moment ffmpeg latched on.
        feed_vad(frame["pcm"])

asyncio.run(listen_to_live("https://www.youtube.com/watch?v=<live-id>"))
```

Live sources are detected via yt-dlp's `is_live` flag; ffmpeg's `-re`
pacing is automatically disabled (the source paces itself).

## Stream-to-frames on the GPU (yt-dlp + PyAV + torch)

`youtube_helper.pick_video_stream(...)` resolves a yt-dlp URL into a
`VideoStreamInfo` that `video_helper.extract_frames(...)` can consume
directly via its `http_headers=` argument:

```python
import torch

stream = yth.pick_video_stream(
    "https://www.youtube.com/watch?v=YE7VzlLtp-4",
    prefer_codec="h264",
    prefer_format="mp4",
    max_fps=30,
)

for batch in vh.extract_frames(
    stream["url"],
    http_headers=stream["headers"],
    destination="torch",
    device="auto",       # cuda > mps > cpu
    batch_size=32,
    output_width=224,
    output_height=224,
):
    # batch.shape == (32, 3, 224, 224) on a GPU device
    logits = model(batch.float() / 255.0)
```

## Mirror a render to S3 + SFTP partner inbox

```python
s3_cred   = bh.credentials("path/to/s3_config.json")
sftp_cred = sftph.credentials("path/to/sftp_config.json")

# Render somewhere
ah.audio_concatenation(["intro.wav", "body.wav", "outro.wav"], "episode.mp3", overwrite=True)

# Long-term archive on S3
s3_uri = bh.upload("episode.mp3", s3_cred, "podcast/2026-06/episode.mp3")
print("Archived at", s3_uri)
# Archived at s3://my-bucket/podcast/2026-06/episode.mp3

# Mirror to SFTP partner inbox
sftph.upload("episode.mp3", sftp_cred, "/inbox/episode-2026-06.mp3")
print("Delivered to SFTP partner.")
# Delivered to SFTP partner.
```

## Stage-and-share a generated artefact

Generate a file locally, hand a public URL to a webhook, let the temp
file vanish on its own:

```python
import requests

cred = bh.credentials("path/to/s3_config.json")

with bh.remote_tempfile(cred, ext="mp4", prefix="renders") as (addr, url):
    vh.video_converter("input.mov", "input.mp4", overwrite=True)
    bh.upload("input.mp4", cred, addr, content_type="video/mp4")
    requests.post(
        "https://hook.example.com/process",
        json={"input_url": url},
    ).raise_for_status()
# Remote object is deleted on block exit, even if the webhook raised.
```
