# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2026-07-23

### Added
- `wallet-helper` (`wallet_helper as wh`) joins the suite — never run the same
  heavy call twice: persistent, content-addressed memoization plus single-flight
  (concurrent identical calls collapse into one), across process restarts and,
  optionally, across processes. A small toolbox, close in spirit to os-helper.
  Installable via the new `cache` extra (`pip install "ai-helpers[cache]"`) and
  bundled in `[all]`. BSD-3-Clause, like the other bundled packages.

### Changed
- Pinned-versions table and install snippets track `wallet-helper 0.2.2`; git
  install refs bumped to `@v0.4.0`. The suite now bundles 12 packages.
- **CI made deliberately light.** As a meta-package with no source of its own,
  the server gate no longer installs the full suite or the media toolchain
  (ffmpeg + pandoc + LibreOffice). It now only builds the package, `twine
  check`s it, and `pip install --dry-run ".[all]"` to prove the whole suite
  graph still resolves on PyPI. The heavy, real end-to-end example tests moved
  fully local, to the `.githooks/pre-push` gate — catching faults on the coder's
  machine instead of on shared runners.

## [0.3.0] - 2026-07-20

### Changed
- Pinned-versions table and install snippets bumped to the current suite release:
  os-helper 1.7.2, audio-helper 1.6.0, video-helper 1.7.0, capture-helper 0.3.0,
  bucket-helper 0.3.0, sftp-helper 2.3.0, youtube-helper 1.4.0, podcast-helper 0.4.0,
  vocal-helper 0.6.0, md2star 2.8.0 (speaker-helper 0.7.4 unchanged).
- This release tracks a suite-wide upgrade: every helper now ships consistent
  surfaces — CLI (argparse + click), FastAPI API, MCP, and (where it earns its
  place) a minimal browser GUI at `/gui` — plus an installable Claude Code +
  OpenCode agent skill, a `TRIGGERS.md`, and (for the local-first helpers) an
  honest "The Promise" section stating exactly what stays on your machine.

## [0.2.1] - 2026-07-14

### Added
- `md2star` (`md2star`) joins the suite — a Markdown → DOCX/PPTX/PDF bridge on
  Pandoc, with curated styling, Mermaid rendering and bibliography support.
  Installable via the new `documents` extra (`pip install "ai-helpers[documents]"`)
  and bundled in `[all]`. BSD-3-Clause, like the other bundled packages.

### Changed
- Flip every sibling dependency from a `git+https` pin to a PyPI version
  specifier now that the whole suite is published on PyPI
  (`os-helper>=1.5.0`, `audio-helper>=1.5.6`, `video-helper>=1.6.3`,
  `sftp-helper>=2.2.3`, `youtube-helper>=1.3.4`, `bucket-helper>=0.2.3`,
  `podcast-helper>=0.3.4`, `capture-helper>=0.2.3`, `vocal-helper>=0.4.1`,
  `speaker-helper>=0.7.2`). `pip install ai-helpers[all]` now installs
  entirely from PyPI.
- Standardize the README import aliases: `vocal_helper as voh`,
  `speaker_helper as spkh`, `sftp_helper as sftph`.

### Documentation
- Resync LISEZMOI.md (French) to mirror README.md (11 helpers + md2star);
  refresh the pinned-versions table to the latest helper tags.


## [0.2.0] - 2026-07-13

### Added

- `vocal-helper` (`vocal_helper`) and `speaker-helper` (`speaker_helper`)
  join the suite — **10 helpers** total.
- **Group extras** so you install only the corner you need:
  `audio` (audio + vocal + speaker), `video` (video + capture),
  `acquire` (youtube + podcast), `storage` (bucket + sftp), and `all`
  (everything — deliberately heavy). The base install is now light —
  just `os-helper` — with each group behind its extra.
- `notes-helper` (WIP, Apache-2.0) is listed in the suite but is **not**
  a dependency of the meta-package yet.

### Changed

- Refresh every pin to the latest release: `os-helper` `v1.5.0`,
  `audio-helper` `v1.5.5`, `video-helper` `v1.6.2`, `sftp-helper` `v2.2.2`,
  `youtube-helper` `v1.3.3`, `bucket-helper` `v0.2.2`, `podcast-helper`
  `v0.3.3`, `capture-helper` `v0.2.2`, plus `vocal-helper` `v0.3.7` and
  `speaker-helper` `v0.7.1`.
- `os-helper` bumped to `v1.5.0`, which drops its FastAPI HTTP surface and
  MCP server (a low-level utility library needs neither); the domain
  helpers keep their service surfaces.

## [0.1.3] - 2026-06-29

### Changed

- Bump `podcast-helper` pin from `v0.1.4` to `v0.2.0` — adds the
  long-planned `speed=<float>` (VOD only, pitch-preserving via
  ffmpeg's `atempo=`) and `record_to=<path>` (parallel compressed
  archive of the live PCM, codec picked from the extension) knobs to
  `extract_audio_stream`.

## [0.1.2] - 2026-06-29

### Changed

- Bump `video-helper` pin from `v1.5.1` to `v1.5.2` — URL-aware
  `is_valid_video_file` + `video_dimensions(http_headers=)`, unblocks
  the documented "pick_video_stream + extract_frames" pipeline for
  yt-dlp-resolved direct URLs.
- Bump `youtube-helper` pin from `v1.1.2` to `v1.2.0` — adds
  `extract_frames_stream(url, ...)` wrapper, a one-call composition
  of `pick_video_stream` + `video_helper.extract_frames` with
  auto-wired headers.
- Bump `podcast-helper` pin from `v0.1.3` to `v0.1.4` — cascade-only
  re-pin of youtube-helper to keep the dep graph internally consistent.

## [0.1.1] - 2026-06-29

### Changed

- Bump `capture-helper` pin from `v0.0.1` to `v0.1.0` — the helper
  graduates from scaffold (types + `list_sources`) to live INPUT layer
  (`pick_source`, `iter_camera_frames`, `iter_mic_audio`,
  `ffmpeg_input_args`, `MicFrame`). Composes with `video_helper.extract_frames`
  and `podcast_helper.extract_audio_stream` contracts.

## [0.1.0] - 2026-06-29 — superseded by 0.1.1

### Documentation

- Add `EXAMPLES.md` at the repo root with composed recipes spanning
  multiple helpers (YouTube → frames + audio, RSS → live PCM, stream-to-
  frames on GPU, S3 + SFTP mirror, stage-and-share patterns); referenced
  from README + LISEZMOI.
- Every `brew install <pkg>` mention is paired with a brew.sh hint when
  not already obvious from context.
- `.gitignore` updated to drop accidental `*config.json` commits while
  keeping `*config.json.example` templates tracked (defensive — the
  meta-package itself doesn't load credentials).

## [0.1.0] - 2026-06-29

First release.

This is a **meta-package**: it has no Python code of its own. Installing
it pulls in all 8 helpers at compatible pinned versions.

### Pinned versions at release

- `os-helper @ v1.3.0`
- `audio-helper @ v1.4.2`
- `video-helper @ v1.5.1`
- `sftp-helper @ v2.1.0`
- `youtube-helper @ v1.1.2`
- `bucket-helper @ v0.1.0`
- `podcast-helper @ v0.1.3`
- `capture-helper @ v0.0.1`

### Release cadence

Each helper release will be followed by a corresponding meta-package
release that bumps the relevant pin. The meta-package will track the
**latest released** version of each helper.

Power users who don't want the full suite should install individual
helpers directly; the meta-package is for the all-batteries-included
case.
