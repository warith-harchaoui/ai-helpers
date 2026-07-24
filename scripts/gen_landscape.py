#!/usr/bin/env python3
"""Regenerate a helper's landscape docs FROM its committed CSV source of truth.

`assets/landscape.csv` (English) and `assets/paysage.csv` (French) are the single
source of truth: integer star ratings, the first header cell being the domain
label. From them this script regenerates, in LANDSCAPE.md / PAYSAGE.md:

  1. the ⭐ star table, between  <!-- TABLE:START --> / <!-- TABLE:END -->
  2. the positioning figure (standingpoint), assets/landscape.png / paysage.png
  3. the commentary, between   <!-- FIGURE:START --> / <!-- FIGURE:END -->

standingpoint is used as a local dev tool (never a dependency of the helper).
Axis names come from the LLM by default (`--model`), the deterministic column
fallback with `--no-llm`. The figure title/legend are forced to the domain label
(standpoint's own pluralizer mangles acronyms). Prose outside the two managed
regions is left untouched. Idempotent: run `make landscape` any time the CSV
changes.

Usage: gen_landscape.py <repo_dir> [--no-llm] [--model NAME]
"""
import argparse
import csv as csvmod
import json
import os
import re
import subprocess
import sys
import tempfile

STAR = "⭐"
DEFAULT_MODEL = "qwen3:8b"


def read_csv(path):
    with open(path) as f:
        rows = [r for r in csvmod.reader(f) if r]
    header, body = rows[0], rows[1:]
    return header, body


def render_table(header, body):
    """CSV → markdown star table. First body row is the reference (bold)."""
    cols = len(header)
    sep = "| " + " | ".join(["---"] + [":---:"] * (cols - 1)) + " |"
    out = ["| " + " | ".join(header) + " |", sep]
    for i, row in enumerate(body):
        name = f"**{row[0]}**" if i == 0 else row[0]
        cells = [STAR * int(v) if v.strip().isdigit() else v for v in row[1:]]
        out.append("| " + " | ".join([name] + cells) + " |")
    return "\n".join(out)


def replace_region(text, start, end, payload):
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    block = f"{start}\n{payload}\n{end}"
    if pat.search(text):
        return pat.sub(lambda _: block, text)
    raise SystemExit(f"markers {start}/{end} not found")


def standpoint(csv_path, outdir, model, use_llm):
    """Run standpoint with a timeout + one retry; fall back to --no-llm once."""
    py = os.path.expanduser("~/miniconda3/bin/python")
    base = [py, "-m", "standpoint", csv_path, "--outdir", outdir]
    attempts = ([base + ["--model", model]] * 2 + [base + ["--no-llm"]]
                if use_llm else [base + ["--no-llm"]])
    for i, cmd in enumerate(attempts):
        try:
            subprocess.run(cmd, cwd=os.path.dirname(csv_path) or ".",
                           timeout=360, capture_output=True, check=True)
            return "no-llm" if "--no-llm" in cmd else "llm"
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            if i == len(attempts) - 1:
                raise
    return None


def axis_names(md_dir):
    md = next(p for p in os.listdir(md_dir) if p.endswith(".md"))
    txt = open(os.path.join(md_dir, md)).read()
    m = re.search(r"## Axes\n(.*?)(?:\n## |\Z)", txt, re.S)
    poles = []
    for line in (m.group(1).splitlines() if m else []):
        mm = re.match(r"\s*-\s*(\*\*.*?\*\*)", line)
        if mm:
            poles.append(re.sub(r"\s*\(\d+\s*%[^)]*\).*", "", mm.group(1)).rstrip())
    return poles[:2]


def patch_png(vl_json, out_png, title, legend):
    import vl_convert as vlc
    spec = json.load(open(vl_json))
    spec.setdefault("title", {})
    if isinstance(spec["title"], dict):
        spec["title"]["text"] = title
    else:
        spec["title"] = {"text": title}

    def fix(n):
        if isinstance(n, dict):
            if isinstance(n.get("legend"), dict) and "title" in n["legend"]:
                n["legend"]["title"] = legend
            for v in n.values():
                fix(v)
        elif isinstance(n, list):
            for v in n:
                fix(v)
    fix(spec)
    open(out_png, "wb").write(vlc.vegalite_to_png(vl_spec=spec, scale=2))


NUM_EN = {6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven",
          12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen",
          16: "sixteen", 17: "seventeen"}


def commentary(lang, ref, ncrit, poles, url):
    alt = "Positioning map" if lang == "en" else "Carte de positionnement"
    if lang == "fr":
        line = (f"La carte est un résumé en 2D des {ncrit} critères : à lire comme "
                f"une forme, pas comme un classement. « {ref} » se situe dans le "
                f"coin en haut à droite.")
        if len(poles) == 2:
            line += f" Les axes se lisent {poles[0]} et {poles[1]}."
        return f"Représentation 2D du tableau ci-dessus.\n\n![{alt}]({url})\n\n{line}"
    n = NUM_EN.get(ncrit, str(ncrit))
    line = (f"The map is a 2-D summary of the {n} criteria, so read it as a shape, "
            f"not a scoreboard. `{ref}` is at the top-right corner.")
    if len(poles) == 2:
        line += f" The axes read {poles[0]} and {poles[1]}."
    return f"2D representation of the table above.\n\n![{alt}]({url})\n\n{line}"


def do_side(repo, slug, lang, csv_name, md_name, png_name, dfr_suffix, model, use_llm):
    csv_path = os.path.join(repo, "assets", csv_name)
    md_path = os.path.join(repo, md_name)
    header, body = read_csv(csv_path)
    domain = header[0]
    ref = body[0][0]
    ncrit = len(header) - 1
    raw = f"https://raw.githubusercontent.com/warith-harchaoui/{slug}/main/assets/{png_name}"

    text = open(md_path).read()
    text = replace_region(text, "<!-- TABLE:START -->", "<!-- TABLE:END -->",
                          render_table(header, body))

    tmp = tempfile.mkdtemp()
    mode = standpoint(csv_path, tmp, model, use_llm)
    vl = next(os.path.join(tmp, p) for p in os.listdir(tmp) if p.endswith(".vl.json"))
    title = f"{domain} {'in the Quadrant' if lang == 'en' else 'dans le quadrant'}"
    patch_png(vl, os.path.join(repo, "assets", png_name), title, domain)
    poles = axis_names(tmp)

    text = replace_region(text, "<!-- FIGURE:START -->", "<!-- FIGURE:END -->",
                          commentary(lang, ref, ncrit, poles, raw))
    open(md_path, "w").write(text)
    return mode, poles


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    a = ap.parse_args()
    repo = os.path.abspath(a.repo)
    slug = os.path.basename(repo)
    use_llm = not a.no_llm
    en = do_side(repo, slug, "en", "landscape.csv", "LANDSCAPE.md",
                 "landscape.png", "", a.model, use_llm)
    fr = do_side(repo, slug, "fr", "paysage.csv", "PAYSAGE.md",
                 "paysage.png", "", a.model, use_llm)
    print(f"{slug}: EN {en[0]} axes={en[1]} | FR {fr[0]} axes={fr[1]}")


if __name__ == "__main__":
    main()
