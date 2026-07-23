"""Rebuild the landing page's hero animation (``anim.apng``) from the manifest.

The site header shows an animated PNG that cycles through every helper's logo,
one per second, looping forever. Rather than hand-edit that binary each time a
helper joins the suite, this script regenerates it from the SAME manifest that
drives the docs site (:data:`build_all_docs.HELPERS`) — so "add a helper" stays
a one-line edit in that manifest, and the animation follows automatically.

Each frame is a helper's ``<short>-logo.png`` (e.g. ``wallet-logo.png``) fit,
centered, onto a transparent 1000x1000 canvas. Frame order = manifest order, so
the animation, the docs landing page, and the README table all tell the same
story in the same sequence.

Usage
-----
>>> python scripts/build_anim.py            # writes into the web folder  # doctest: +SKIP
>>> python scripts/build_anim.py --out /tmp/anim.apng                     # doctest: +SKIP

Author
------
Warith HARCHAOUI, https://linkedin.com/in/warith-harchaoui
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from PIL import Image

# Reuse the docs manifest as the single source of truth for which helpers exist
# and in what order — never maintain a second list that can drift.
from build_all_docs import HELPERS, LOGO_SRC

# Canvas geometry and timing. The page renders this at ~240 CSS px (see the
# `.anim-hero` rule in index.php), so ~480 px covers a 2x retina display. 512 px
# gives that headroom while keeping the file a few MB — far lighter than the
# legacy 1000 px hand-made file (~11.5 MB) for an identical on-screen result.
CANVAS: int = 512           # square frame side, in pixels
FRAME_MS: int = 1000        # one second per logo
LOOP: int = 0               # 0 = loop forever

# Where the site (and its logos) live, and the animation file the page embeds.
DEFAULT_OUT: Path = LOGO_SRC / "anim.apng"


def _frame_for(logo_path: Path) -> Image.Image:
    """Return one ``CANVAS``x``CANVAS`` RGBA frame holding a single logo.

    The logo is scaled to *contain* (never crop) and centered on a fully
    transparent canvas, so logos of different native sizes all read as the same
    surface and the transparent corners match the current animation.

    Parameters
    ----------
    logo_path : pathlib.Path
        Path to a helper's square-ish ``*-logo.png``.

    Returns
    -------
    PIL.Image.Image
        A new RGBA image of size ``(CANVAS, CANVAS)``.
    """
    # Start from a transparent canvas so unused margins stay see-through.
    frame = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))

    logo = Image.open(logo_path).convert("RGBA")
    # "Contain" fit: scale by the tighter axis so nothing is cropped. Logos are
    # square today, but this keeps a non-square logo from being distorted.
    scale = min(CANVAS / logo.width, CANVAS / logo.height)
    size = (max(1, round(logo.width * scale)), max(1, round(logo.height * scale)))
    logo = logo.resize(size, Image.LANCZOS)  # LANCZOS = high-quality downscale

    # Center the scaled logo; paste through itself as the mask to keep its alpha.
    offset = ((CANVAS - logo.width) // 2, (CANVAS - logo.height) // 2)
    frame.paste(logo, offset, logo)
    return frame


def build_anim(out: Path) -> int:
    """Write the looping APNG to ``out`` and return the frame count.

    The previous file, if any, is backed up next to it (``*.bak``) first, so a
    bad run is trivially reversible.

    Parameters
    ----------
    out : pathlib.Path
        Destination ``.apng`` path.

    Returns
    -------
    int
        Number of frames written (one per manifest helper).
    """
    # One frame per helper, in manifest order (wallet sits where the manifest
    # puts it, between md2star and notes; the archived s3 logo is not listed, so
    # it naturally drops out).
    frames: list[Image.Image] = []
    for helper in HELPERS:
        logo_path = LOGO_SRC / f"{helper.short}-logo.png"
        if not logo_path.exists():
            # A missing logo is a real gap worth surfacing, not silently skipping.
            raise FileNotFoundError(f"logo not found for {helper.slug}: {logo_path}")
        frames.append(_frame_for(logo_path))

    # Keep the prior animation recoverable before overwriting it.
    if out.exists():
        shutil.copy2(out, out.with_suffix(out.suffix + ".bak"))

    # Pillow writes an APNG when save_all is set with more than one frame. disposal=1
    # clears each frame to transparent before the next, so logos never ghost-stack.
    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_MS,
        loop=LOOP,
        disposal=1,
        optimize=True,  # squeeze each frame's PNG stream
        format="PNG",
    )
    return len(frames)


def main(argv: list[str]) -> int:
    """CLI entry point: rebuild the animation, print where it went.

    Parameters
    ----------
    argv : list of str
        Command-line arguments (excluding the program name).

    Returns
    -------
    int
        Process exit code (0 on success).
    """
    parser = argparse.ArgumentParser(description="Rebuild the AI Helpers hero animation from the docs manifest.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help=f"output APNG path (default: {DEFAULT_OUT})")
    args = parser.parse_args(argv)

    count = build_anim(args.out)
    # Intentional CLI status output (not diagnostic logging) — this is the tool's result.
    print(f"wrote {args.out} ({count} frames, {FRAME_MS} ms each, loop={LOOP})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
