# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
