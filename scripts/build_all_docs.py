#!/usr/bin/env python3
"""Regenerate the Sphinx API-doc sites for the whole AI Helpers suite.

Module summary
--------------
Single source of truth for the suite's documentation website. For every helper
it builds a Sphinx (autodoc + napoleon, Read the Docs theme) HTML site from that
package's NumPy-style docstrings, then writes a streamlined ``index.html``
landing page — all into the local web folder that gets uploaded by FTP to
``https://harchaoui.org/warith/ai-helpers/docs/``.

Maintenance workflow
--------------------
When a helper's API changes, just re-run this script; the manifest below is the
only thing to edit when a helper is added, renamed, or re-described::

    python scripts/build_all_docs.py                 # default output dir
    python scripts/build_all_docs.py /path/to/docs   # custom output dir

Prerequisites
-------------
``pip install sphinx sphinx-rtd-theme`` (declared in the ``docs`` extra).

Author
------
Warith HARCHAOUI.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

# Default output folder: the local mirror of the FTP docs tree. Override with a
# CLI argument when testing into a scratch directory.
DEFAULT_OUT = Path.home() / "web/harchaoui.org/warith/ai-helpers/docs"

# Root under which every ``<name>-helper`` repository is checked out.
REPO_ROOT = Path.home()

# Golden brand logos live here as ``<short>-logo.png`` (e.g. ``os-logo.png``).
# They are copied into ``<out>/logos/<slug>.png`` so the docs folder is a
# self-contained FTP upload.
LOGO_SRC = Path.home() / "web/harchaoui.org/warith/ai-helpers"

# Heavy/optional third-party deps used across the suite. autodoc imports each
# package to read its docstrings; mocking these means the build never needs the
# heavy stack installed. Light, ubiquitous deps (numpy, scipy, requests, yaml)
# are deliberately NOT mocked so real signatures render.
MOCKS: list[str] = [
    "torch", "torchaudio", "torchvision", "torchcodec", "av", "cv2", "vidgear",
    "PIL", "whisper", "faster_whisper", "pywhispercpp", "TTS", "pyannote",
    "nemo", "nemo_toolkit", "silero_vad", "sounddevice", "pyaudio", "soundcard",
    "feedparser", "podcastparser", "yt_dlp", "boto3", "botocore", "paramiko",
    "fastapi", "uvicorn", "fastapi_mcp", "starlette", "deepeval", "giskard",
    "ollama", "demucs", "librosa", "soundfile", "transformers",
    "huggingface_hub", "click",
]


@dataclass(frozen=True)
class Helper:
    """One documented helper package.

    Parameters
    ----------
    slug : str
        Distribution / repo name, e.g. ``os-helper``. The doc folder is
        ``<slug>-doc`` and the repo is ``~/<slug>``.
    pkg : str
        Importable package name, e.g. ``os_helper``.
    title : str
        Human title shown in the docs and on the landing card.
    category : str
        Landing-page grouping (mirrors the suite README).
    blurb : str
        One-line description for the landing card.
    src_layout : bool
        True when the package lives under ``src/`` (e.g. notes-helper).
    """

    slug: str
    pkg: str
    title: str
    category: str
    blurb: str
    src_layout: bool = False

    @property
    def short(self) -> str:
        """Short name (slug minus the ``-helper`` suffix); the logo file stem."""
        return self.slug.rsplit("-helper", 1)[0]

    @property
    def repo(self) -> Path:
        """Absolute path to the repository checkout."""
        return REPO_ROOT / self.slug

    @property
    def parent(self) -> Path:
        """Directory to put on ``sys.path`` so ``pkg`` imports."""
        # src-layout packages import from ``<repo>/src``; flat ones from the repo.
        return self.repo / "src" if self.src_layout else self.repo

    @property
    def pkg_path(self) -> Path:
        """Filesystem path of the package (input to ``sphinx-apidoc``)."""
        return self.parent / self.pkg


# The manifest — the ONE place to edit when the suite changes. Order defines the
# landing-page order within each category.
HELPERS: list[Helper] = [
    Helper("os-helper", "os_helper", "OS Helper", "Core",
           "Cross-platform file, system, hash, config and timing/profiling "
           "utilities — the base every other helper builds on."),
    Helper("audio-helper", "audio_helper", "Audio Helper", "Audio & Voice",
           "Load, convert, split and concatenate audio; optional source separation."),
    Helper("vocal-helper", "vocal_helper", "Vocal Helper", "Audio & Voice",
           "Live PCM → Voice Activity Detection → online speaker diarization → "
           "Speech to Text → optional LLM summary."),
    Helper("speaker-helper", "speaker_helper", "Speaker Helper", "Audio & Voice",
           "Offline + streaming Speech Synthesis over a local engine, with voice "
           "cloning — the inverse of vocal-helper."),
    Helper("video-helper", "video_helper", "Video Helper", "Video & Capture",
           "Video conversion, handling and frame extraction."),
    Helper("capture-helper", "capture_helper", "Capture Helper", "Video & Capture",
           "Camera and microphone capture with a uniform streaming interface."),
    Helper("youtube-helper", "youtube_helper", "YouTube Helper", "Acquisition",
           "yt-dlp-based media acquisition — download and stream from YouTube and hundreds of other sites."),
    Helper("podcast-helper", "podcast_helper", "Podcast Helper", "Acquisition",
           "Universal audio-stream consumer."),
    Helper("bucket-helper", "bucket_helper", "Bucket Helper", "Storage & Transfer",
           "S3-compatible object storage: upload, download, mirror and stage-and-share patterns."),
    Helper("sftp-helper", "sftp_helper", "SFTP Helper", "Storage & Transfer",
           "SFTP: upload, download, mirror."),
    Helper("md2star", "md2star", "md2star", "Notes & Docs",
           "Markdown → DOCX/PPTX/PDF bridge on Pandoc, with curated styling, "
           "Mermaid rendering and bibliography support."),
    Helper("wallet-helper", "wallet_helper", "Wallet Helper", "Cache",
           "Never run the same heavy call twice: persistent, content-addressed "
           "memoization + single-flight. A toolbox, close in spirit to os-helper."),
    Helper("notes-helper", "notes_helper", "Notes Helper", "Notes & Docs",
           "Turn recordings into structured notes: transcription, diarization and LLM "
           "synthesis into Markdown / DOCX / vault outputs.", src_layout=True),
]

# conf.py template — rendered per package into a throwaway source directory.
CONF_TEMPLATE = '''\
import sys
sys.path.insert(0, r"{parent}")
project = "{title}"
author = "Warith HARCHAOUI"
copyright = "2026, Warith HARCHAOUI"
extensions = [
    "sphinx.ext.autodoc", "sphinx.ext.napoleon",
    "sphinx.ext.viewcode", "sphinx.ext.intersphinx",
]
napoleon_numpy_docstring = True
napoleon_google_docstring = False
autodoc_default_options = {{"members": True, "undoc-members": True, "show-inheritance": True}}
autodoc_typehints = "description"
autodoc_mock_imports = {mocks!r}
intersphinx_mapping = {{"python": ("https://docs.python.org/3", None)}}
html_theme = "sphinx_rtd_theme"
html_title = "{title} Documentation"
html_show_sourcelink = True
'''


def build_one(helper: Helper, out_root: Path) -> int:
    """Build a single helper's HTML docs; return the HTML page count (0 = fail)."""
    out = out_root / f"{helper.slug}-doc"
    src = Path(tempfile.mkdtemp())
    # Render conf.py for this package.
    (src / "conf.py").write_text(
        CONF_TEMPLATE.format(parent=helper.parent, title=helper.title, mocks=MOCKS)
    )
    # Generate per-module .rst stubs (-e = one page per module, -f = overwrite).
    subprocess.run(
        ["sphinx-apidoc", "-f", "-e", "-o", str(src), str(helper.pkg_path)],
        check=False, capture_output=True,
    )
    # Landing page for this package: title + a toctree into the module index.
    underline = "=" * (len(helper.title) + len(" Documentation"))
    (src / "index.rst").write_text(
        f"{helper.title} Documentation\n{underline}\n\n"
        f"Auto-generated API reference for the ``{helper.pkg}`` package, part of "
        f"the `AI Helpers <https://harchaoui.org/warith/ai-helpers/>`_ suite.\n\n"
        ".. toctree::\n   :maxdepth: 3\n   :caption: API Reference\n\n   modules\n"
    )
    # Build; surface only real errors (mock-related warnings are expected noise).
    result = subprocess.run(
        ["sphinx-build", "-q", "-b", "html", str(src), str(out)],
        capture_output=True, text=True,
    )
    for line in (result.stderr or "").splitlines():
        if "ERROR" in line or "CRITICAL" in line:
            print(f"    {line}")
    return len(list(out.rglob("*.html"))) if (out / "index.html").exists() else 0


def render_index(out_root: Path) -> None:
    """Write the streamlined landing ``index.html`` from the manifest."""
    # Group helpers by category, preserving manifest order.
    groups: dict[str, list[Helper]] = {}
    for h in HELPERS:
        groups.setdefault(h.category, []).append(h)

    # Assemble the category sections as HTML card grids.
    sections: list[str] = []
    for category, members in groups.items():
        cards = "\n".join(_card_html(h) for h in members)
        sections.append(f'  <h2>{category}</h2>\n  <div class="grid">\n{cards}\n  </div>')
    body = "\n\n".join(sections)
    (out_root / "index.html").write_text(_PAGE.format(body=body), encoding="utf-8")


def _card_html(h: Helper) -> str:
    """Return the HTML for one helper's landing-page card (logo + name + links)."""
    return (
        f'    <div class="card">\n'
        f'      <div class="card-head">'
        f'<img class="logo" src="logos/{h.slug}.png" alt="{h.slug} logo" loading="lazy">'
        f'<h3><a href="{h.slug}-doc/">{h.slug}</a></h3></div>\n'
        f'      <p>{h.blurb}</p>\n'
        f'      <div class="links"><a class="primary" href="{h.slug}-doc/">Docs</a>'
        f'<a href="https://pypi.org/project/{h.slug}/">PyPI</a>'
        f'<a href="https://github.com/warith-harchaoui/{h.slug}">GitHub</a></div></div>'
    )


def copy_logos(out_root: Path) -> None:
    """Copy each helper's golden logo into ``<out>/logos/<slug>.png``."""
    dest = out_root / "logos"
    dest.mkdir(parents=True, exist_ok=True)
    # Pull ``<short>-logo.png`` from the brand folder; warn (don't fail) if any
    # logo is missing so the build still produces a usable page.
    for h in HELPERS:
        src = LOGO_SRC / f"{h.short}-logo.png"
        if src.exists():
            shutil.copyfile(src, dest / f"{h.slug}.png")
        else:
            print(f"  WARN missing logo {src}")


# Self-contained landing-page shell (inline CSS, dark/light aware, FTP-friendly).
_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Helpers — Documentation</title>
<meta name="description" content="API documentation for the AI Helpers suite.">
<style>
  :root{{--bg:#0e1116;--card:#171b22;--ink:#e6e9ef;--muted:#9aa4b2;--accent:#5b9dff;--line:#252b34;}}
  @media (prefers-color-scheme: light){{:root{{--bg:#f6f7f9;--card:#fff;--ink:#1a1f27;--muted:#5b6472;--accent:#2b6fdb;--line:#e6e9ef;}}}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}}
  .wrap{{max-width:1040px;margin:0 auto;padding:56px 22px 80px}}
  h1{{font-size:2rem;margin:0 0 6px;letter-spacing:-.02em}}
  .tag{{color:var(--muted);font-size:1.05rem;margin:0 0 12px}}
  .tag code{{background:var(--line);padding:.1em .4em;border-radius:5px;font-size:.9em}}
  h2{{font-size:.82rem;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);margin:38px 0 14px;font-weight:700}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}
  .card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 18px 15px;display:flex;flex-direction:column;transition:border-color .15s,transform .15s}}
  .card:hover{{border-color:var(--accent);transform:translateY(-2px)}}
  .card-head{{display:flex;align-items:center;gap:11px;margin-bottom:8px}}
  .logo{{width:40px;height:40px;border-radius:9px;object-fit:cover;flex:none;background:var(--line)}}
  .card h3{{margin:0;font-size:1.08rem}}
  .card h3 a{{color:var(--ink);text-decoration:none}}
  .card h3 a:hover{{color:var(--accent)}}
  .card p{{margin:0 0 14px;color:var(--muted);font-size:.92rem;flex:1}}
  .links{{display:flex;gap:8px;flex-wrap:wrap}}
  .links a{{font-size:.8rem;text-decoration:none;color:var(--accent);border:1px solid var(--line);border-radius:7px;padding:4px 9px}}
  .links a:hover{{border-color:var(--accent);background:rgba(91,157,255,.08)}}
  .links a.primary{{background:var(--accent);color:#fff;border-color:var(--accent)}}
  footer{{margin-top:56px;color:var(--muted);font-size:.85rem;border-top:1px solid var(--line);padding-top:20px}}
  footer a{{color:var(--accent);text-decoration:none}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>AI Helpers — Documentation</h1>
    <p class="tag">A family of small, composable Python helpers for AI &amp; media work. Install the suite with <code>pip install "ai-helpers[all]"</code>.</p>
  </header>

{body}

  <footer>
    Generated with Sphinx (autodoc + napoleon, Read the Docs theme) from each package's NumPy-style docstrings.
    &nbsp;·&nbsp; <a href="https://harchaoui.org/warith/ai-helpers/">AI Helpers home</a>
    &nbsp;·&nbsp; <a href="https://github.com/warith-harchaoui/ai-helpers">ai-helpers on GitHub</a>
  </footer>
</div>
</body>
</html>
"""


def main(argv: list[str]) -> int:
    """Build every helper's docs + the landing page into the output folder."""
    out_root = Path(argv[1]).expanduser() if len(argv) > 1 else DEFAULT_OUT
    out_root.mkdir(parents=True, exist_ok=True)
    print(f"Building suite docs into {out_root}")
    # Build each package, reporting page counts and skipping missing repos.
    failures = 0
    for helper in HELPERS:
        if not helper.pkg_path.exists():
            print(f"  SKIP {helper.slug} (missing {helper.pkg_path})")
            failures += 1
            continue
        pages = build_one(helper, out_root)
        print(f"  {'ok ' if pages else 'FAIL'} {helper.slug}-doc ({pages} pages)")
        failures += 0 if pages else 1
    # Copy brand logos, then regenerate the landing page from the manifest so
    # both the cards and their images never drift from the source of truth.
    copy_logos(out_root)
    render_index(out_root)
    print(f"  wrote {out_root / 'index.html'}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
