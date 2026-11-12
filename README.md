# AI Helpers

[🇫🇷](https://github.com/warith-harchaoui/ai-helpers/blob/main/LISEZMOI.md) · [🇬🇧](https://github.com/warith-harchaoui/ai-helpers/blob/main/README.md)

[![GitHub stars](https://img.shields.io/github/stars/warith-harchaoui/ai-helpers?style=social)](https://github.com/warith-harchaoui/ai-helpers)
[![License: BSD-3-Clause](https://img.shields.io/badge/license-BSD--3--Clause-blue.svg)](LICENSE)
[![17 packages on PyPI](https://img.shields.io/badge/PyPI-17%20packages-3775A9?logo=pypi&logoColor=white)](https://pypi.org/user/warith-harchaoui/)
[![6 crates on crates.io](https://img.shields.io/badge/crates.io-6%20crates-orange?logo=rust)](https://crates.io/users/warith-harchaoui)

**Eighteen Python libraries that each do one AI or media job, on your own machine.** Transcribe a meeting with who said what, read a text aloud, download a talk, turn Markdown into a Word document, pick the local model that fits your laptop. No account, no telemetry, no server of ours in the loop. Six of the eighteen also exist in Rust, for the phones and small boxes Python does not reach.

🌍 **Website, documentation and FAQ: [deraison.ai/ai-helpers](https://deraison.ai/ai-helpers/)**

⭐ **If the suite has earned a place in your toolbox, star this repository.** One click, no newsletter in return. It tells the next developer who lands here that the detour is worth it. Did one helper save your afternoon? Its own repository deserves a star too.

---

## What do you want to do?

| You want to… | Reach for |
|---|---|
| transcribe a meeting and know who said what, live or after the fact | [`vocal-helper`](https://github.com/warith-harchaoui/vocal-helper) |
| read a text aloud, stream a reply or clone a voice | [`speaker-helper`](https://github.com/warith-harchaoui/speaker-helper) |
| talk to a local model out loud and interrupt it mid-sentence | [`discussion-helper`](https://github.com/warith-harchaoui/discussion-helper) |
| load, convert, cut, join or separate audio | [`audio-helper`](https://github.com/warith-harchaoui/audio-helper) |
| extract frames or subtitles from a video | [`video-helper`](https://github.com/warith-harchaoui/video-helper) |
| record the webcam or the microphone | [`capture-helper`](https://github.com/warith-harchaoui/capture-helper) |
| download a video, its audio or its thumbnail from YouTube, Vimeo, SoundCloud… | [`youtube-helper`](https://github.com/warith-harchaoui/youtube-helper) |
| read any audio stream (a podcast feed, a radio, a URL) as samples | [`podcast-helper`](https://github.com/warith-harchaoui/podcast-helper) |
| push files to S3, MinIO, R2 or another bucket | [`bucket-helper`](https://github.com/warith-harchaoui/bucket-helper) |
| move files over SFTP, with strict host-key checks | [`sftp-helper`](https://github.com/warith-harchaoui/sftp-helper) |
| turn Markdown into a Word, PowerPoint or PDF document (and back) | [`md2star`](https://github.com/warith-harchaoui/md2star) |
| stop paying twice for the same API call or slow model | [`wallet-helper`](https://github.com/warith-harchaoui/wallet-helper) |
| place competitors on a positioning map from a comparison table | [`standpoint`](https://github.com/warith-harchaoui/standpoint) |
| find which local LLM or vision model fits this machine | [`best-engine-ai-helper`](https://github.com/warith-harchaoui/best-engine-ai-helper) |
| choose a vector-search backend from measured criteria | [`ann-router`](https://github.com/warith-harchaoui/ann-router) |
| search a private corpus from your website, PHP only, without publishing it | [`web-search-helper`](https://github.com/warith-harchaoui/web-search-helper) |
| find the elbow of a curve or hear that there is none | [`elbow-helper`](https://github.com/warith-harchaoui/elbow-helper) |
| handle files, processes, hashing, config and timers on any OS | [`os-helper`](https://github.com/warith-harchaoui/os-helper) |

## Quick start

Every helper is its own package on PyPI, except the newest, `web-search-helper`, installed from GitHub for now. Install the one you need; it brings `os-helper`, the shared foundation, along with it.

```bash
pip install youtube-helper audio-helper vocal-helper md2star
```

You need Python 3.10 to 3.13. The media helpers call `ffmpeg`, so put it on your PATH first (`brew install ffmpeg` on macOS). md2star drives Pandoc.

Four helpers, one chain: a YouTube talk becomes a Word document and a PDF.

```python
import youtube_helper as yth   # acquisition
import audio_helper as ah      # decoding
import vocal_helper as voh     # speech to text

URL = "https://www.youtube.com/watch?v=YE7VzlLtp-4"

yth.download_audio(URL, "talk.mp3", target_sample_rate=16000)
pcm, sr = ah.load_audio("talk.mp3", target_sample_rate=16000, to_mono=True, to_numpy=True)
transcript = voh.transcribe_pcm(pcm, sr, language="en")

with open("talk.md", "w", encoding="utf-8") as fh:
    fh.write(f"# Talk transcript\n\n_Source: {URL}_\n\n{transcript}\n")
```

```bash
md2docx talk.md   # talk.docx
md2pdf  talk.md   # talk.pdf
```

## The eighteen helpers

| Group | Helper | Its one job | Links |
|---|---|---|---|
| 🧱 Core | [`os-helper`](https://github.com/warith-harchaoui/os-helper) | The foundation every other helper imports: OS and hardware detection, processes, paths, hashing, config, timers | [PyPI](https://pypi.org/project/os-helper/) · [Docs](https://deraison.ai/ai-helpers/docs/os-helper-doc/modules.html) |
| 🔊 Audio & voice | [`audio-helper`](https://github.com/warith-harchaoui/audio-helper) | Load, resample, convert, split, join and separate audio | [PyPI](https://pypi.org/project/audio-helper/) · [Docs](https://deraison.ai/ai-helpers/docs/audio-helper-doc/modules.html) |
| | [`vocal-helper`](https://github.com/warith-harchaoui/vocal-helper) | Audio in, diarized and transcribed utterances out, live or over a whole recording | [PyPI](https://pypi.org/project/vocal-helper/) · [Docs](https://deraison.ai/ai-helpers/docs/vocal-helper-doc/modules.html) |
| | [`speaker-helper`](https://github.com/warith-harchaoui/speaker-helper) | Text in, speech out, with a router that picks the engine from measurements | [PyPI](https://pypi.org/project/speaker-helper/) · [Docs](https://deraison.ai/ai-helpers/docs/speaker-helper-doc/modules.html) |
| | [`discussion-helper`](https://github.com/warith-harchaoui/discussion-helper) | A spoken conversation at the microphone, barge-in included | [PyPI](https://pypi.org/project/discussion-helper/) · [Docs](https://deraison.ai/ai-helpers/docs/discussion-helper-doc/modules.html) |
| 🎬 Video & capture | [`video-helper`](https://github.com/warith-harchaoui/video-helper) | Frames, conversions and subtitles, with the extraction backend chosen for you | [PyPI](https://pypi.org/project/video-helper/) · [Docs](https://deraison.ai/ai-helpers/docs/video-helper-doc/modules.html) |
| | [`capture-helper`](https://github.com/warith-harchaoui/capture-helper) | Live camera and microphone, on every OS | [PyPI](https://pypi.org/project/capture-helper/) · [Docs](https://deraison.ai/ai-helpers/docs/capture-helper-doc/modules.html) |
| 🌐 Media acquisition | [`youtube-helper`](https://github.com/warith-harchaoui/youtube-helper) | Videos, audio and thumbnails from YouTube and its cousins | [PyPI](https://pypi.org/project/youtube-helper/) · [Docs](https://deraison.ai/ai-helpers/docs/youtube-helper-doc/modules.html) |
| | [`podcast-helper`](https://github.com/warith-harchaoui/podcast-helper) | Any audio stream, read as the samples a speech model expects | [PyPI](https://pypi.org/project/podcast-helper/) · [Docs](https://deraison.ai/ai-helpers/docs/podcast-helper-doc/modules.html) |
| 🗄️ Storage & transfer | [`bucket-helper`](https://github.com/warith-harchaoui/bucket-helper) | S3 and every S3-compatible store | [PyPI](https://pypi.org/project/bucket-helper/) · [Docs](https://deraison.ai/ai-helpers/docs/bucket-helper-doc/modules.html) |
| | [`sftp-helper`](https://github.com/warith-harchaoui/sftp-helper) | SFTP transfers with strict host-key verification | [PyPI](https://pypi.org/project/sftp-helper/) · [Docs](https://deraison.ai/ai-helpers/docs/sftp-helper-doc/modules.html) |
| 📄 Documents | [`md2star`](https://github.com/warith-harchaoui/md2star) | Markdown to DOCX, PPTX and PDF with branded templates; documents back to Markdown too | [PyPI](https://pypi.org/project/md2star/) · [Docs](https://deraison.ai/ai-helpers/docs/md2star-doc/modules.html) |
| ♻️ Cache | [`wallet-helper`](https://github.com/warith-harchaoui/wallet-helper) | Never run the same expensive call twice | [PyPI](https://pypi.org/project/wallet-helper/) · [Docs](https://deraison.ai/ai-helpers/docs/wallet-helper-doc/modules.html) |
| 🧩 Misc | [`standpoint`](https://github.com/warith-harchaoui/standpoint) | A comparison table in, a positioning map and its coordinates out | [PyPI](https://pypi.org/project/standpoint/) · [Docs](https://deraison.ai/ai-helpers/docs/standpoint-doc/modules.html) |
| | [`best-engine-ai-helper`](https://github.com/warith-harchaoui/best-engine-ai-helper) | The best local model for this machine, pulled and checked | [PyPI](https://pypi.org/project/best-engine-ai-helper/) · [Docs](https://deraison.ai/ai-helpers/docs/best-engine-ai-helper-doc/modules.html) |
| | [`ann-router`](https://github.com/warith-harchaoui/ann-router) | The right nearest-neighbour backend, with the reasons written out | [PyPI](https://pypi.org/project/ann-router/) · [Docs](https://deraison.ai/ai-helpers/docs/ann-router-doc/modules.html) |
| | [`web-search-helper`](https://github.com/warith-harchaoui/web-search-helper) | Search a private corpus from a website with PHP only: excerpts that answer, or an honest refusal | [GitHub](https://github.com/warith-harchaoui/web-search-helper) (PyPI soon) |
| | [`elbow-helper`](https://github.com/warith-harchaoui/elbow-helper) | A knee with its uncertainty or an explicit abstention | [PyPI](https://pypi.org/project/elbow-helper/) · [Docs](https://deraison.ai/ai-helpers/docs/elbow-helper-doc/modules.html) |

## The same shape everywhere

![How the AI Helpers suite fits together: sixteen helpers with one job each, on one shared foundation](https://raw.githubusercontent.com/warith-harchaoui/ai-helpers/main/assets/diagrams/how-it-works.png)

Learn one helper and you know how to drive the other seventeen. Each one exposes:

- a **Python API**;
- a **command line** built with click (os-helper, the foundation, ships none);
- a **FastAPI HTTP server**;
- an **MCP tool set** for AI agents, mounted at `/mcp` on that same server, so every tool is a route and the two never drift apart;
- an installable **agent skill** for Claude Code or OpenCode;
- where auditing the output in a browser helps, a small **GUI at `/gui`**, with no build step and no external call.

Thirteen of the eighteen also ship a Dockerfile with a `docker-compose.yml` that brings the companion they need: MinIO for Bucket, a throwaway SFTP server for SFTP, Ollama for Standpoint and Best Engine, Qdrant and pgvector for ANN Router.

Each repository carries a `TRIGGERS.md`: the full list of what should reach for that helper and what should leave it alone. It is mirrored into the skill; a test fails the moment the two copies disagree. Your agent learns when to call the helper; it also learns not to transcribe a spreadsheet.

## Local-first, with the exceptions written down

- **Entirely on your machine:** os, audio, video, capture, vocal, speaker, discussion, md2star and wallet. A few of them download a model or a template once, then work offline.
- **Only what you ask for:** youtube-helper and podcast-helper contact the sites and feeds you name. They upload nothing about you.
- **Remote by design:** bucket-helper and sftp-helper send your files to the storage you choose. That is their job; the endpoint is yours, never a hidden default.
- **Your machine, then your host:** web-search-helper indexes on your machine and answers from your own PHP hosting; the visitor's browser fetches the sentence encoder once, from a CDN.

Vocal and Speaker also know a few paid hosted engines (Gladia, ElevenLabs, pyannoteAI). They call one only when you name it and supply its key; the automatic routing never picks them.

## Rust ports

Six helpers also exist as independent Rust rewrites, on [crates.io](https://crates.io/users/warith-harchaoui):

```bash
cargo add audio-helper-rs capture-helper-rs podcast-helper-rs youtube-helper-rs
cargo add vocal-helper-rs --features onnx
cargo install md2star-rs   # md2star-rs, md2docx, md2pptx: no Pandoc, no Python
```

| Crate | What it does |
|---|---|
| [`vocal-helper-rs`](https://github.com/warith-harchaoui/vocal-helper-rs) | Streaming diarization and transcription through ONNX Runtime, with the execution provider (CUDA, TensorRT, CoreML, DirectML, OpenVINO or CPU) measured on the device |
| [`capture-helper-rs`](https://github.com/warith-harchaoui/capture-helper-rs) | A live microphone as a stream of PCM packets, through the OS's own audio stack |
| [`audio-helper-rs`](https://github.com/warith-harchaoui/audio-helper-rs) | File-level audio utilities on `ffmpeg` and `ffprobe` |
| [`podcast-helper-rs`](https://github.com/warith-harchaoui/podcast-helper-rs) | Any audio source in, the PCM a speech model expects out |
| [`youtube-helper-rs`](https://github.com/warith-harchaoui/youtube-helper-rs) | A typed Rust interface around `yt-dlp` |
| [`md2star-rs`](https://github.com/warith-harchaoui/md2star-rs) | Markdown to DOCX, PPTX and PDF in one static binary, plus `twin` and `audit` |

**Why Rust, then?** For the devices Python does not reach. A phone has no interpreter; compiled wheels exist one platform at a time; `torch` alone weighs gigabytes. Rust cross-compiles to macOS, Linux, Windows, iOS and Android from the same tree. It ships one file that runs with nothing installed.

**And speed?** Rarely. We measured before anyone got excited: in vocal-helper's diarization, 99.8 % of the time goes to ONNX Runtime, which Rust calls exactly as Python does, so a rewrite gains 0.2 % at most. vocal-helper-rs even transcribes more slowly than its Python twin on an M2 Max CPU (real-time factor 0.05 against 0.022 to 0.028). Each crate is checked against the Python it mirrors; vocal-helper-rs matches its diarization probabilities within 1.9e-6.

The full story, accelerator by accelerator, is on [the website](https://deraison.ai/ai-helpers/#rust).

## Who

[Warith Harchaoui](https://deraison.ai), [Mohamed Chelali](https://mchelali.github.io/) and [Bachir Zerroug](https://www.linkedin.com/in/bachirzerroug/), publishing since April 2024. Write to warithmetics@deraison.ai for a bug, an idea or a project that needs the suite wired in. A human reads every message.

## License

BSD-3-Clause, the license of numpy and scikit-learn: read it, fork it, ship it. See [LICENSE](LICENSE).
