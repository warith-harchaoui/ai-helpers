# AI Helpers

[🇫🇷](LISEZMOI.md) · [🇬🇧](README.md)

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](LICENSE) [![Python](https://img.shields.io/badge/python-3.10%E2%80%933.13-blue.svg)](#)

Méta-paquet qui installe l'intégralité de la suite **AI Helpers** en une commande — une collection de bibliothèques Python ciblées pour le travail IA / média.

[🌍 Page de la suite AI Helpers](https://harchaoui.org/warith/ai-helpers)

## Ce qui est inclus

| Helper | Module | Rôle |
|---|---|---|
| [os-helper](https://github.com/warith-harchaoui/os-helper) | `os_helper as osh` | Utilitaires multi-plateformes : fichiers / système / hash / config / chronométrage. |
| [audio-helper](https://github.com/warith-harchaoui/audio-helper) | `audio_helper as ah` | Chargement / conversion / découpage / concaténation audio ; séparation de sources Demucs en option. |
| [video-helper](https://github.com/warith-harchaoui/video-helper) | `video_helper as vh` | Extraction de frames multi-backend (VidGear / PyAV / ffmpeg-pipe), conversion, sous-titres. |
| [sftp-helper](https://github.com/warith-harchaoui/sftp-helper) | `sftp_helper as sftph` | SFTP via paramiko avec vérification stricte des clés d'hôte + `remote_tempfile`. |
| [youtube-helper](https://github.com/warith-harchaoui/youtube-helper) | `youtube_helper as yth` | Wrapper yt-dlp : téléchargements, catalogue / picker de flux, métadonnées d'engagement sans API. |
| [bucket-helper](https://github.com/warith-harchaoui/bucket-helper) | `bucket_helper as bh` | boto3 pour AWS S3 + S3-compatibles (MinIO / R2 / B2 / Spaces / Wasabi). |
| [podcast-helper](https://github.com/warith-harchaoui/podcast-helper) | `podcast_helper as ph` | Consommateur universel de flux audio : URL en entrée → PCM en sortie (RSS, yt-dlp, direct, …). |
| [capture-helper](https://github.com/warith-harchaoui/capture-helper) | `capture_helper as ch` | Couche capture / traitement / diffusion inspirée d'OBS (squelette). |

Tous sous licence **BSD-3-Clause** (la même que scikit-learn / numpy / scipy).

## Installation

```bash
pip install --force-reinstall --no-cache-dir \
  git+https://github.com/warith-harchaoui/ai-helpers.git@v0.1.0
```

Cela tire les 8 helpers à leurs versions épinglées compatibles, plus leurs
dépendances transitives (`yt-dlp`, `ffmpeg-python`, `boto3`, `paramiko`,
`opencv-python`, `vidgear`, `feedparser`, `podcastparser`, …).

Il vous faut toujours `ffmpeg` dans le PATH pour les helpers média (audio /
video / youtube / podcast / capture) :

- macOS 🍎 : `brew install ffmpeg`
- Ubuntu 🐧 : `sudo apt install ffmpeg`
- Windows 🪟 : [ffmpeg.org/download.html](https://ffmpeg.org/download.html)

## Versions épinglées

Cette release suit les helpers à ces tags :

```
os-helper       @ v1.3.0
audio-helper    @ v1.4.2
video-helper    @ v1.5.1
sftp-helper     @ v2.1.0
youtube-helper  @ v1.1.2
bucket-helper   @ v0.1.0
podcast-helper  @ v0.1.3
capture-helper  @ v0.0.1
```

Une release du méta-paquet suivra chaque release de helper. Si vous n'avez
besoin que d'un seul helper, installez-le directement — le méta-paquet
existe pour le cas tout-inclus.

## Exemple rapide

```python
import os_helper as osh
import audio_helper as ah
import video_helper as vh
import youtube_helper as yth

osh.verbosity(2)

# Télécharger une vidéo YouTube + en extraire l'audio + charger les échantillons PCM
yth.download_video("https://www.youtube.com/watch?v=YE7VzlLtp-4", "bunny.mp4")
yth.download_audio("https://www.youtube.com/watch?v=YE7VzlLtp-4", "bunny.mp3")
audio, sr = ah.load_audio("bunny.mp3")
print(vh.video_dimensions("bunny.mp4"))
# {'width': 1280, 'height': 720, 'duration': 596.458, 'frame_rate': 24.0, 'has_sound': True}
```

Pour des recettes composées mêlant plusieurs helpers (YouTube → frames + audio, RSS → PCM live, stream-vers-frames sur GPU, miroir vers S3 + SFTP, patterns stage-and-share), voir [📋 EXAMPLES.md](EXAMPLES.md).

# Auteur
 - [Warith HARCHAOUI](https://linkedin.com/in/warith-harchaoui)

# Remerciements
Special thanks to [Mohamed Chelali](https://mchelali.github.io) and [Bachir Zerroug](https://www.linkedin.com/in/bachirzerroug) for fruitful discussions.
