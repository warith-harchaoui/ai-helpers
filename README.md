# AI Helpers

**A suite of local-first Python libraries for AI and media work** — one clear job each, the same shape everywhere.

## 🌍 [harchaoui.org/warith/ai-helpers](https://harchaoui.org/warith/ai-helpers/)

**The website is the home of the suite** — overview, documentation, and a positioning map for every helper. Start there.

---

Every helper is its own package on **PyPI**, so you install only the corner you need (each pulls in `os-helper` automatically):

| Group | Helpers |
|---|---|
| 🧱 Core | `os-helper` |
| 🔊 Audio & voice | `audio-helper` · `vocal-helper` |
| 🎬 Video & capture | `video-helper` · `capture-helper` |
| 🌐 Media acquisition | `youtube-helper` · `podcast-helper` |
| 🗄️ Storage & transfer | `bucket-helper` · `sftp-helper` |
| 🧩 Misc | `md2star` · `wallet-helper` · `standpoint` · `best-engine-ai-helper` · `ann-router` |

```bash
pip install audio-helper vocal-helper   # install a group
pip install os-helper                    # or just the foundation
```

Each helper exposes the **same surfaces** — a Python API, two CLIs (argparse + click), a FastAPI HTTP server, and an MCP tool set — and runs **local-first**: your files, audio, camera/mic and documents are processed on your machine, with no SaaS, no telemetry, no account. (Bucket and SFTP are the honest exception — their job is to move data to storage *you* choose.)

## License

BSD-3-Clause — see [LICENSE](LICENSE).
