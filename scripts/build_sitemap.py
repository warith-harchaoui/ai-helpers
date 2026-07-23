"""Regenerate ``sitemap.xml`` for the AI Helpers site from the docs manifest.

The sitemap lists the landing page, the docs index, and one page per helper's
generated Sphinx docs. All of that is derivable from :data:`build_all_docs.HELPERS`
(the single source of truth), so a new helper appears in the sitemap the moment
it is added to that manifest — no hand-editing of XML.

Usage
-----
>>> python scripts/build_sitemap.py                 # writes into the web folder  # doctest: +SKIP
>>> python scripts/build_sitemap.py --date 2026-07-23                             # doctest: +SKIP

Author
------
Warith HARCHAOUI, https://linkedin.com/in/warith-harchaoui
"""
from __future__ import annotations

import argparse
import datetime
import sys
from pathlib import Path

# Reuse the docs manifest and the web-root location — never duplicate the list.
from build_all_docs import HELPERS, LOGO_SRC

# Public base URL of the site (LOGO_SRC is the local mirror of this path).
BASE: str = "https://harchaoui.org/warith/ai-helpers"
DEFAULT_OUT: Path = LOGO_SRC / "sitemap.xml"


def _url(loc: str, lastmod: str, priority: str) -> str:
    """Render one ``<url>`` block.

    Parameters
    ----------
    loc : str
        Absolute URL of the page.
    lastmod : str
        ``YYYY-MM-DD`` last-modified date.
    priority : str
        Sitemap priority, ``"0.0"`` to ``"1.0"``.

    Returns
    -------
    str
        The XML fragment for this URL (monthly change frequency).
    """
    return (
        "  <url>\n"
        f"    <loc>{loc}</loc>\n"
        f"    <lastmod>{lastmod}</lastmod>\n"
        "    <changefreq>monthly</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>"
    )


def build_sitemap(out: Path, lastmod: str) -> int:
    """Write the sitemap to ``out`` and return the number of URLs.

    Parameters
    ----------
    out : pathlib.Path
        Destination ``sitemap.xml`` path.
    lastmod : str
        ``YYYY-MM-DD`` date stamped on every entry.

    Returns
    -------
    int
        Count of ``<url>`` entries written.
    """
    # Home first (highest priority), then the docs index, then each helper's
    # generated docs page — in manifest order so it mirrors the landing page.
    urls = [
        _url(f"{BASE}/", lastmod, "1.0"),
        _url(f"{BASE}/docs/", lastmod, "0.8"),
    ]
    for helper in HELPERS:
        # Sphinx writes each package's API index at <slug>-doc/modules.html.
        urls.append(_url(f"{BASE}/docs/{helper.slug}-doc/modules.html", lastmod, "0.6"))

    body = "\n".join(urls)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n"
        "</urlset>\n"
    )
    out.write_text(xml, encoding="utf-8")
    return len(urls)


def main(argv: list[str]) -> int:
    """CLI entry point: regenerate the sitemap and report the URL count.

    Parameters
    ----------
    argv : list of str
        Command-line arguments (excluding the program name).

    Returns
    -------
    int
        Process exit code (0 on success).
    """
    parser = argparse.ArgumentParser(description="Rebuild sitemap.xml from the docs manifest.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help=f"output path (default: {DEFAULT_OUT})")
    parser.add_argument("--date", default=datetime.date.today().isoformat(), help="lastmod date (YYYY-MM-DD)")
    args = parser.parse_args(argv)

    count = build_sitemap(args.out, args.date)
    # Intentional CLI result output, not diagnostic logging.
    print(f"wrote {args.out} ({count} urls, lastmod {args.date})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
