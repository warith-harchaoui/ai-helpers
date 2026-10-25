# AI Helpers

**A suite of local-first Python libraries for AI and media work** — one clear job each, the same shape everywhere.

## 🌍 [deraison.ai/ai-helpers](https://deraison.ai/ai-helpers/)

**The website is the home of the suite** — overview, documentation, and a positioning map for every helper. Start there.

---

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

Every repo carries a root `TRIGGERS.md` — the exhaustive catalogue of what should, and should not, reach for that helper — mirrored into `skills/<helper>/references/triggers.md`. A `scripts/check_triggers.py` gate keeps each skill's `description` naming every capability and carrying an explicit SKIP clause, inside the 1024-character cap the Agent Skills standard sets, and the test suite fails when the two drift apart.

## License

BSD-3-Clause — see [LICENSE](LICENSE).
