# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
