# AI Helpers

**A suite of local-first libraries for AI and media work** — one clear job each, the same shape everywhere. Python throughout, with [Rust ports](#rust-ports) for the corners that have to run where Python cannot.

## 🌍 [deraison.ai/ai-helpers](https://deraison.ai/ai-helpers/)

**The website is the home of the suite** — overview, documentation, and a positioning map for every helper. Start there.

---

## How it works

![How the AI Helpers suite fits together: sixteen helpers with one job each, on one shared foundation](https://raw.githubusercontent.com/warith-harchaoui/ai-helpers/main/assets/diagrams/how-it-works.png)

Every helper is its own package on **PyPI**, so you install only the corner you need (each pulls in `os-helper` automatically):

| Group | Helpers |
|---|---|
| 🧱 Core | `os-helper` |
| 🔊 Audio & voice | `audio-helper` · `vocal-helper` · `speaker-helper` · `discussion-helper` |
| 🎬 Video & capture | `video-helper` · `capture-helper` |
| 🌐 Media acquisition | `youtube-helper` · `podcast-helper` |
| 🗄️ Storage & transfer | `bucket-helper` · `sftp-helper` |
| 🧩 Misc | `md2star` · `wallet-helper` · `standpoint` · `best-engine-ai-helper` · `ann-router` · `elbow-helper` |

```bash
pip install audio-helper vocal-helper   # install a group
pip install os-helper                    # or just the foundation
```

Each helper exposes the **same four surfaces** — a Python API, one CLI built with click, a FastAPI HTTP server, an MCP tool set mounted on that same app, and an **agent skill** (Claude / OpenCode) — and runs **local-first**: your files, audio, camera/mic and documents are processed on your machine, with no SaaS, no telemetry, no account. (Bucket and SFTP are the honest exception — their job is to move data to storage *you* choose.)

## Rust ports — the same promise, on every machine

Local-first means the work happens on **your** machine. But a person's machines are not only
laptops: they are a phone in a pocket, a tablet on a kitchen counter, a small box in a studio. A
suite written only in Python keeps its promise on computers and quietly breaks it everywhere else —
and that gap is the whole reason some helpers also exist as Rust crates.

It is not a side experiment. It is the same promise, carried to the devices people actually hold.

### Why Python makes this hard

Not a criticism of Python — a consequence of how it ships. Five things stand between a Python
library and an arbitrary device:

- **It needs an interpreter at the destination.** A Python package is source that requires a
  compatible CPython to be present and configured. On iOS and Android there is none, and putting
  one there is a project in itself rather than a build step.
- **Compiled wheels are per-target.** The packages that do the real work — `numpy`, `onnxruntime`,
  `torch` — ship native extensions, and a wheel exists for one combination of operating system,
  C library, processor architecture and Python ABI. The matrix multiplies, and for mobile and
  embedded targets most of its cells are simply empty.
- **The scientific stack is heavy.** `torch` alone runs to gigabytes. An application bundle has a
  budget, and that budget is not gigabytes.
- **Dependencies resolve at install time, on the user's machine.** What installed cleanly here can
  fail there, months later, because a range moved. The artefact you tested is not the artefact they
  get.
- **There is no single file to hand over.** You ship an environment and hope, rather than a
  program.

Rust inverts all five. Cross-compiling is a boring, first-class operation — `cargo build --target
aarch64-apple-ios` — dependencies resolve at **build** time on the developer's machine, and the
output is one static library or binary that runs with nothing installed. The same source tree
produces artefacts for macOS, Linux, Windows, iOS and Android without the code knowing which one it
is going to.

### And the speed? Honestly, that is not the reason

A little, sometimes. But **well-accelerated Python does not need rescuing**, because it already
delegates the heavy work to native code: `numpy` computes in C, `onnxruntime` in C++, `ffmpeg` in
its own binary. A Rust port calls those very same libraries, so where the work is already native,
rewriting changes nothing.

That was measured rather than assumed. Profiling `vocal-helper`'s diarization path, **99.8 % of the
wall time is inside ONNX Runtime** — the feature front end accounts for 0.1 % and the bookkeeping
around the model for another 0.1 %. The ceiling on a Rust port's speed gain there is **0.2 %**: a
real-time factor of 0.754 instead of 0.755.

Python does lose on tight per-item loops that resist vectorisation — but that is usually a reason to
reshape the loop, not to change language. Anyone promising a Rust rewrite as a performance fix
should be asked for the profile first.

### What exists

Each crate is an **independent rewrite** of its helper's core promise — not a binding, not a
line-by-line translation — and each is verified against the Python it mirrors rather than assumed to
agree. `vocal-helper-rs`, for instance, compares its feature front end and its streaming
bookkeeping against fixtures generated by the Python, because both feed the same ONNX graph: a
silent disagreement there would produce different answers on mobile and no unit test on either side
would notice.

| Crate | Mirrors | Its own promise | Where its speed comes from |
|---|---|---|---|
| [`vocal-helper-rs`](https://github.com/warith-harchaoui/vocal-helper-rs) | `vocal-helper` | Streaming speaker diarization (Nemotron 3) and transcription (Nemotron 3.5) through their ONNX graphs (`onnx` feature), no Python and no torch | **The real accelerator story.** Since 0.2.0 each session picks its ONNX Runtime execution provider: the caller's choice, else `VOCAL_HELPER_PROVIDER`, else a **measurement on the device** kept under the graph's digest, with a fallback down to the CPU. Features `cuda`, `tensorrt`, `coreml`, `directml`, `openvino`; the NVIDIA path needs CUDA 13 and cuDNN 9. CI builds `cuda,tensorrt` on Ubuntu and proves the CPU fallback, but no NVIDIA GPU has run it yet. Diarization probabilities within 1.9e-6 of the Python twin |
| [`capture-helper-rs`](https://github.com/warith-harchaoui/capture-helper-rs) | `capture-helper` | A live microphone into a stream of PCM packets, no service in the loop | The OS's own audio stack through `cpal`: CoreAudio, WASAPI, ALSA/PulseAudio/JACK/PipeWire — no PortAudio, no `ffmpeg`, nothing extra to install |
| [`audio-helper-rs`](https://github.com/warith-harchaoui/audio-helper-rs) | `audio-helper` | File-level audio utilities on top of `ffmpeg`/`ffprobe` | The encoder of a compressed output is chosen on the machine, by trial on the real rate and channels; a platform encoder must do the same work in under two-thirds of the time to displace the preferred one, and on Apple Silicon AudioToolbox did not. A GPU build of `ffmpeg` changes nothing: NVENC, NVDEC, VAAPI and QSV handle pictures, not audio |
| [`podcast-helper-rs`](https://github.com/warith-harchaoui/podcast-helper-rs) | `podcast-helper` | URL in, PCM out — any audio source to the stream a speech model expects | Decoding is already the fast path: measured on Apple Silicon, AudioToolbox decoders are slower than `ffmpeg`'s own, and the video stream of a source is never decoded. `--decoder` or `PODCAST_HELPER_DECODER` overrides the default |
| [`youtube-helper-rs`](https://github.com/warith-harchaoui/youtube-helper-rs) | `youtube-helper` | One consistent Rust interface around invoking `yt-dlp` | No arithmetic of its own: it drives `yt-dlp` and waits on the network. The gain is the static binary and the typed interface, not speed |
| [`md2star-rs`](https://github.com/warith-harchaoui/md2star-rs) | `md2star` | Markdown → DOCX, PPTX and PDF, `twin` back to Markdown, deck `audit`, citations and native equations, in pure Rust: no Pandoc, no LibreOffice, no subprocess | Conversion is XML, text measurement and typesetting: no accelerator applies. Its hardware story is the *absence* of prerequisites — CI type-checks the library for iOS and Android, and the CLI is one static binary |

Which accelerator wins is measured, never reasoned. ONNX Runtime has no Metal provider, so on Apple
Silicon acceleration goes through CoreML — and on the diarization graph CoreML measures a real-time
factor of **1.257**, slower than real time, against **0.528** for CPU alone: it takes 1193 of 2827
nodes and splits them into **316 partitions**, so every streaming step pays that many crossings
between two engines. Forcing eight threads on an eight-performance-core machine was wrong the same
way (0.953 against 0.528). A hardcoded provider order is wrong *somewhere*, which is why
`vocal-helper` tries on the device and keeps the verdict, and why `vocal-helper-rs` now does the
same: the first open of the diarization graph on an M2 Max found the CPU ahead again (0.74 against
1.12 for CoreML), while on the transcription graph the two were level (0.084 against 0.086).

All six are on [crates.io](https://crates.io/search?q=helper-rs) — `cargo add` whichever corner
you need. `vocal-helper-rs` arrived last and is at 0.2.0: it runs both models end to end, though
the graphs weigh hundreds of megabytes and stay outside the crate: you pass their path. Speed is
not its argument, as said above: on the CPU of an M2 Max its transcription runs at a real-time
factor of 0.05, against 0.022 to 0.028 for the Python twin.

Every repo carries a root `TRIGGERS.md` — the exhaustive catalogue of what should, and should not, reach for that helper — mirrored into `skills/<helper>/references/triggers.md`. A `scripts/check_triggers.py` gate keeps each skill's `description` naming every capability and carrying an explicit SKIP clause, inside the 1024-character cap the Agent Skills standard sets, and the test suite fails when the two drift apart.

## License

BSD-3-Clause — see [LICENSE](LICENSE).
