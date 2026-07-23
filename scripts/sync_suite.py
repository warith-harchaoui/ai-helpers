"""One command to propagate a suite change everywhere it can be automated.

The docs manifest (:data:`build_all_docs.HELPERS`) is the single source of truth
for the AI Helpers suite: which helpers exist, their order, category and blurb.
When it changes (typically: a new helper joins), several derived artifacts must
follow. This orchestrator regenerates every artifact that CAN be produced
mechanically, and then prints the short list of things that still need a human
touch (hand-written marketing prose and the meta-package's dependency pins).

Regenerated automatically:
  * the Sphinx docs site           (build_all_docs)  -> docs/<slug>-doc/
  * the hero animation             (build_anim)      -> anim.apng
  * the sitemap                    (build_sitemap)   -> sitemap.xml

Still manual (prose / pins — deliberately, to keep quality high):
  * index.php  : nav entry + a card with a human-written description
  * llms.txt   : one bullet with a human-written description
  * ~/ai-helpers/pyproject.toml : the group extra + the `all` list
  * ~/ai-helpers/README.md / LISEZMOI.md : the table row + pins table
  * bump the helper's pin once it is released on PyPI

Usage
-----
>>> python scripts/sync_suite.py                 # docs (slow) + anim + sitemap  # doctest: +SKIP
>>> python scripts/sync_suite.py --skip-docs     # just anim + sitemap (fast)     # doctest: +SKIP

Author
------
Warith HARCHAOUI, https://linkedin.com/in/warith-harchaoui
"""
from __future__ import annotations

import argparse
import datetime
import sys

import build_all_docs
import build_anim
import build_sitemap

# The human-only follow-ups, printed at the end so they are never forgotten.
MANUAL_STEPS: list[str] = [
    "index.php  : add the nav entry + a card (human-written description)",
    "llms.txt   : add one bullet (human-written description)",
    "pyproject.toml : add the group extra + append to the `all` list",
    "README.md / LISEZMOI.md : add the table row + the pins-table line",
    "bump the helper's pin to its released version once it is on PyPI",
]


def main(argv: list[str]) -> int:
    """Run every manifest-driven regenerator, then print the manual checklist.

    Parameters
    ----------
    argv : list of str
        Command-line arguments (excluding the program name).

    Returns
    -------
    int
        Process exit code (0 on success).
    """
    parser = argparse.ArgumentParser(description="Propagate a suite manifest change to all derived artifacts.")
    # Docs are the slow part (Sphinx over every package); allow skipping them when
    # only the logo animation / sitemap need refreshing.
    parser.add_argument("--skip-docs", action="store_true", help="skip the (slow) Sphinx docs rebuild")
    args = parser.parse_args(argv)

    today = datetime.date.today().isoformat()

    # 1) Docs — the heaviest step; each helper's API is re-rendered by Sphinx.
    if not args.skip_docs:
        print("== docs ==")
        build_all_docs.main([])

    # 2) Hero animation — one frame per manifest logo, in order.
    print("== anim ==")
    n = build_anim.build_anim(build_anim.DEFAULT_OUT)
    print(f"wrote {build_anim.DEFAULT_OUT} ({n} frames)")

    # 3) Sitemap — home + docs index + one page per helper's docs.
    print("== sitemap ==")
    build_sitemap.main(["--date", today])

    # 4) Remind the human of the prose/pin steps that are intentionally not automated.
    print("\n== still manual (prose + pins) ==")
    for step in MANUAL_STEPS:
        print(f"  - {step}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
