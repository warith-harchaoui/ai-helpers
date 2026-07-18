"""End-to-end tests that the documented AI Helpers examples actually run.

These exercise the code shown in ``README.md`` / ``LISEZMOI.md`` (and mirrored on
the website) so a broken snippet — like passing a torch ``Tensor`` to a function
that wants a NumPy array — is caught in CI instead of by a user.

Two kinds of test, split by cost and reliability:

* **Deterministic core** (:func:`test_composed_example_offline`) — the heart of the
  "Composed example" (``audio → transcript → docx/pdf``) run on a committed short
  speech clip, with **no network**. This is the part that must always be green.
* **Network stages** (the ``slow``-marked YouTube tests) — the acquisition step of
  the examples. YouTube is an external service that rate-limits/needs cookies from
  CI IPs, so these **skip cleanly** when the download fails rather than turning the
  build red on a flaky third party.

The module skips entirely unless the suite + ffmpeg are present; the ``docx``/``pdf``
leg additionally needs pandoc + LibreOffice (installed by the CI ``examples`` job).

Author
------
Warith HARCHAOUI.
"""

from __future__ import annotations

import importlib.util
import os
import shutil
from pathlib import Path

import pytest

# --- toolchain / dependency detection -------------------------------------
# ffmpeg backs every decode; the four packages are what the examples import.
_HAS_FFMPEG = shutil.which("ffmpeg") is not None
_HAS_PANDOC = shutil.which("pandoc") is not None
_HAS_SOFFICE = shutil.which("soffice") is not None or shutil.which("libreoffice") is not None


def _importable(name: str) -> bool:
    """Return True if module ``name`` can be imported without importing it."""
    # find_spec avoids paying the (heavy) import cost just to test availability.
    return importlib.util.find_spec(name) is not None


_HAS_SUITE = all(
    _importable(m) for m in ("youtube_helper", "audio_helper", "vocal_helper", "md2star")
)

# Whole module is meaningless without ffmpeg + the suite, so skip as a unit.
pytestmark = pytest.mark.skipif(
    not (_HAS_FFMPEG and _HAS_SUITE),
    reason="needs ffmpeg + youtube_helper/audio_helper/vocal_helper/md2star importable",
)

# A committed ~3 s speech clip ("Artificial intelligence helpers turn a recorded
# talk into a shareable document") so transcription has known words to recover
# without any network round-trip.
_FIXTURE = Path(__file__).parent / "fixtures" / "speech.wav"

# A short, stable public clip used by the network tests (keeps CI fast).
_URL = "https://www.youtube.com/watch?v=FisrbY90td0"

# YouTube bot-blocks datacenter IPs — every CI runner — with "Sign in to confirm
# you're not a bot", and per the yt-dlp tracker this fails there even WITH cookies
# (issues #12045, #15392): the block is on the IP, not the auth. So the two YouTube
# download tests run ONLY where they can actually succeed — the coder's machine on a
# residential IP — and are skipped in CI (which sets CI=true), UNLESS an authenticated
# cookies file is supplied (YOUTUBE_HELPER_COOKIES, e.g. from a YOUTUBE_COOKIES secret)
# to attempt it there anyway. This is not "avoiding" the test: it runs and passes on
# every local `pytest` run, genuinely verifying the acquisition stage — it just doesn't
# gate CI on a download YouTube refuses to serve from a datacenter. The deterministic
# offline composed test needs no network and DOES run for real in CI.
_IN_CI = os.environ.get("CI", "").strip().lower() == "true"
_HAS_YT_COOKIES = bool(os.environ.get("YOUTUBE_HELPER_COOKIES", "").strip())
_youtube_network = pytest.mark.skipif(
    _IN_CI and not _HAS_YT_COOKIES,
    reason="YouTube bot-blocks CI datacenter IPs (fails even with cookies, yt-dlp "
    "#12045/#15392); this download test runs locally on a residential IP. Set the "
    "YOUTUBE_COOKIES secret to attempt it in CI anyway.",
)


def test_composed_example_offline(tmp_path: Path) -> None:
    """Composed example core: ``audio → transcript → docx + pdf``, no network.

    Mirrors steps 2–4 of the README "Composed example" exactly (including the
    ``to_numpy=True`` that makes ``load_audio`` hand ``transcribe_pcm`` a NumPy
    array), on the committed speech fixture. Asserts a non-empty transcript that
    recovered real words, and that md2star produced a valid DOCX and PDF.
    """
    # md2pdf shells out to LibreOffice and md2docx to Pandoc; skip if either is
    # absent (the deterministic transcription part still needs them downstream).
    if not (_HAS_PANDOC and _HAS_SOFFICE):
        pytest.skip("needs pandoc + libreoffice (soffice) for md2docx / md2pdf")

    import audio_helper as ah
    import vocal_helper as voh
    from md2star.cli import _convert

    # 2) Transcribe — the exact documented call. ``base`` (not the heavier default)
    # keeps CI fast while still recovering the words clearly.
    pcm, sr = ah.load_audio(str(_FIXTURE), target_sample_rate=16000, to_mono=True, to_numpy=True)
    transcript = voh.transcribe_pcm(pcm, sr, model="base", language="en")

    # The transcript must be real text, and recover at least one anchor word from
    # the fixture (lenient so a minor ASR variation never flakes the build).
    assert transcript.strip(), "transcription returned empty text"
    anchors = ("intelligence", "helpers", "talk", "document", "recorded", "shareable")
    assert any(w in transcript.lower() for w in anchors), f"unexpected transcript: {transcript!r}"

    # 3) Write a titled Markdown file, then 4) typeset it to DOCX + PDF.
    md = tmp_path / "talk.md"
    md.write_text(f"# Talk transcript\n\n{transcript}\n", encoding="utf-8")
    assert _convert("docx", [str(md), "-o", str(tmp_path / "talk.docx"), "--offline"]) == 0
    assert _convert("pdf", [str(md), "-o", str(tmp_path / "talk.pdf"), "--offline"]) == 0

    # Validate the artifacts by their magic bytes: DOCX is a ZIP (``PK``), PDF is ``%PDF``.
    assert (tmp_path / "talk.docx").read_bytes()[:2] == b"PK"
    assert (tmp_path / "talk.pdf").read_bytes()[:4] == b"%PDF"


@pytest.mark.slow
@_youtube_network
def test_composed_example_youtube_acquire(tmp_path: Path) -> None:
    """Acquisition stage of the composed example: ``youtube-helper → mp3``.

    Downloads the short clip for real and asserts a non-empty audio file. Runs
    locally on a residential IP every ``pytest`` run (genuinely verifying the
    acquisition path); skipped in CI, where YouTube bot-blocks the datacenter IP
    (see :data:`_youtube_network`).
    """
    import youtube_helper as yth

    mp3 = tmp_path / "talk.mp3"
    yth.download_audio(_URL, str(mp3), target_sample_rate=16000)
    assert mp3.exists() and mp3.stat().st_size > 10_000, "downloaded audio is empty/too small"


@pytest.mark.slow
@_youtube_network
def test_quick_example(tmp_path: Path) -> None:
    """README "Quick example": download video + audio and read video dimensions.

    Local-only like :func:`test_composed_example_youtube_acquire` (YouTube blocks CI
    IPs); runs and passes on the coder's machine, skipped in CI.
    """
    import audio_helper as ah
    import video_helper as vh
    import youtube_helper as yth

    mp4 = tmp_path / "bunny.mp4"
    mp3 = tmp_path / "bunny.mp3"
    yth.download_video(_URL, str(mp4))
    yth.download_audio(_URL, str(mp3))

    # load_audio just needs to decode without error; the example prints dimensions.
    ah.load_audio(str(mp3))
    dims = vh.video_dimensions(str(mp4))
    assert dims["width"] > 0 and dims["height"] > 0 and dims["duration"] > 0
