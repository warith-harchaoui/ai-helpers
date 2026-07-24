# AI Helpers

[🇫🇷](https://github.com/warith-harchaoui/ai-helpers/blob/main/LISEZMOI.md) · [🇬🇧](https://github.com/warith-harchaoui/ai-helpers/blob/main/README.md)

[![CI](https://github.com/warith-harchaoui/ai-helpers/actions/workflows/ci.yml/badge.svg)](https://github.com/warith-harchaoui/ai-helpers/actions/workflows/ci.yml) [![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/warith-harchaoui/ai-helpers/blob/main/LICENSE) [![Python](https://img.shields.io/badge/python-3.10%E2%80%933.13-blue.svg)](#) [![Local-first](https://img.shields.io/badge/privacy-local--first-2f6f5e.svg)](#la-promesse)

Méta-paquet qui installe l'intégralité de la suite **AI Helpers** en une seule commande — une collection de bibliothèques Python ciblées pour le travail IA / média.

[🌍 Page de la suite AI Helpers](https://harchaoui.org/warith/ai-helpers)

## Ce qui est inclus

Les helpers sont organisés en **groupes** — installez seulement le coin dont vous avez besoin (voir [Installation](#installation)).

| Groupe | Helper | Module | Rôle |
|---|---|---|---|
| 🧱 Cœur | [os-helper](https://github.com/warith-harchaoui/os-helper) | `os_helper as osh` | Utilitaires multi-plateformes : fichiers / système / hash / config / chronométrage. |
| 🔊 Audio & voix | [audio-helper](https://github.com/warith-harchaoui/audio-helper) | `audio_helper as ah` | Chargement / conversion / découpage / concaténation audio ; séparation de sources en option. |
| 🔊 Audio & voix | [vocal-helper](https://github.com/warith-harchaoui/vocal-helper) | `vocal_helper as voh` | PCM live → détection d'activité vocale → diarisation de locuteurs en ligne → transcription (Speech to Text) → résumé LLM optionnel. |
| 🔊 Audio & voix | [speaker-helper](https://github.com/warith-harchaoui/speaker-helper) | `speaker_helper as spkh` | Synthèse vocale hors-ligne + en streaming sur un moteur local, avec clonage de voix — l'inverse de vocal-helper. |
| 🎬 Vidéo & capture | [video-helper](https://github.com/warith-harchaoui/video-helper) | `video_helper as vh` | Extraction de frames multi-backend (VidGear / PyAV / ffmpeg-pipe), conversion, sous-titres. |
| 🎬 Vidéo & capture | [capture-helper](https://github.com/warith-harchaoui/capture-helper) | `capture_helper as ch` | Couche de capture multi-sources en direct — itérateurs caméra + micro (composant avec les contrats de video-helper / podcast-helper) plus un configurateur de scènes dans le navigateur. |
| 🌐 Acquisition média | [youtube-helper](https://github.com/warith-harchaoui/youtube-helper) | `youtube_helper as yth` | Wrapper yt-dlp : téléchargements, catalogue / picker de flux, métadonnées d'engagement sans API. |
| 🌐 Acquisition média | [podcast-helper](https://github.com/warith-harchaoui/podcast-helper) | `podcast_helper as ph` | Consommateur universel de flux audio : URL en entrée → PCM en sortie (RSS, yt-dlp, direct, …). |
| 🗄️ Stockage & transfert | [bucket-helper](https://github.com/warith-harchaoui/bucket-helper) | `bucket_helper as bh` | boto3 pour AWS S3 + S3-compatibles (MinIO / R2 / B2 / Spaces / Wasabi). |
| 🗄️ Stockage & transfert | [sftp-helper](https://github.com/warith-harchaoui/sftp-helper) | `sftp_helper as sftph` | SFTP via paramiko avec vérification stricte des clés d'hôte + `remote_tempfile`. |
| 🧩 Divers | [md2star](https://github.com/warith-harchaoui/md2star) | `md2star` | Passerelle Markdown → DOCX / PPTX / PDF sur Pandoc, avec styling soigné, rendu Mermaid et support bibliographique. |
| 🧩 Divers | [wallet-helper](https://github.com/warith-harchaoui/wallet-helper) | `wallet_helper as wh` | Ne jamais relancer deux fois le même appel coûteux : mémoïsation persistante, adressée par contenu + single-flight. Une boîte à outils, proche d'os-helper dans l'esprit. |
| 🧩 Divers | [standingpoint](https://github.com/warith-harchaoui/standingpoint) | `standpoint as sp` | Transforme un tableau de comparaison en une carte de positionnement 2D étiquetée, une analyse rédigée et un YAML de coordonnées — cartes perceptuelles ACP, en une commande. |
| 🧩 Divers | [notes-helper](https://github.com/warith-harchaoui/notes-helper) | `notes_helper` | Enregistreur de réunions diarisé, 100 % local et respectueux de la vie privée. **Travail en cours** — pas encore installé par le méta-paquet. |

Les 13 paquets embarqués sont sous licence **BSD-3-Clause** (la même que scikit-learn / numpy / scipy) ; le WIP `notes-helper` est sous Apache-2.0.

## La promesse

**Local-first par conception.** Les AI Helpers traitent vos données sur *votre* machine avec des outils open source — pas de SaaS, pas de télémétrie, pas de compte, pas de verrouillage cloud. En toute honnêteté sur les limites :

- **Garanti local** — os-helper, audio-helper, video-helper, capture-helper, vocal-helper, md2star et wallet-helper tournent entièrement sur votre machine ; vos fichiers, audio, caméra/micro, documents et résultats mis en cache n'en sortent jamais.
- **Ne récupère que ce que vous demandez** — youtube-helper et podcast-helper doivent contacter les sites/flux que vous indiquez (impossible de télécharger une vidéo ou un épisode distant en local-first), mais n'envoient rien vous concernant et gardent tout en local. Quelques helpers téléchargent un modèle ou un gabarit une fois au premier lancement, puis fonctionnent hors ligne.
- **Délibérément *pas* local-first** — bucket-helper et sftp-helper servent à envoyer vos données vers un stockage / serveur distant. La souveraineté ici, c'est *vous* qui choisissez le point de terminaison : votre propre MinIO / serveur SFTP est souverain ; un cloud tiers, c'est votre choix.

## Installation

Chaque helper est sur PyPI et s'installe indépendamment, donc le chemin le
plus simple est d'installer seulement le **groupe** dont vous avez besoin —
chacun tire `os-helper` automatiquement :

```bash
# 🔊 Audio & voix
pip install audio-helper vocal-helper speaker-helper

# 🎬 Vidéo & capture
pip install video-helper capture-helper

# 🌐 Acquisition média
pip install youtube-helper podcast-helper

# 🗄️ Stockage & transfert
pip install bucket-helper sftp-helper

# 🧩 Divers (docs, cache, cartes de positionnement)
pip install md2star wallet-helper standpoint

# 🧱 Cœur seul (utilitaires de fondation)
pip install os-helper
```

Vous préférez un point d'entrée unique ? Le méta-paquet **`ai-helpers`**
expose les mêmes groupes sous forme d'extras. Son installation de base est
légère (juste `os-helper`) ; ajoutez le(s) groupe(s) voulu(s) — ou `[all]`
pour tout d'un coup (délibérément lourd, presque trop) :

```bash
# un groupe
pip install "ai-helpers[audio] @ git+https://github.com/warith-harchaoui/ai-helpers.git@v0.5.0"

# plusieurs groupes à la fois
pip install "ai-helpers[audio,video] @ git+https://github.com/warith-harchaoui/ai-helpers.git@v0.5.0"

# absolument tout
pip install "ai-helpers[all] @ git+https://github.com/warith-harchaoui/ai-helpers.git@v0.5.0"
```

Extras disponibles : `audio`, `video`, `acquire`, `storage`, `misc`, `all`.

Il vous faut toujours `ffmpeg` dans le PATH pour les helpers média (audio /
video / youtube / podcast / capture / vocal) :

- macOS 🍎 : `brew install ffmpeg`

  (installez `brew` grâce à [brew.sh](https://brew.sh/))
- Ubuntu 🐧 : `sudo apt install ffmpeg`
- Windows 🪟 : [ffmpeg.org/download.html](https://ffmpeg.org/download.html)

## Versions épinglées

Cette release suit les helpers à ces tags :

```
os-helper       @ v1.7.2
audio-helper    @ v1.6.0
video-helper    @ v1.7.0
sftp-helper     @ v2.3.0
youtube-helper  @ v1.4.0
bucket-helper   @ v0.3.0
podcast-helper  @ v0.4.0
capture-helper  @ v0.3.0
vocal-helper    @ v0.6.0
speaker-helper  @ v0.7.4
md2star         @ v2.8.0
wallet-helper   @ v0.3.0
standingpoint   @ v0.2.0
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

## Exemples composés

Les helpers sont faits pour s'enchaîner. Ici, la suite transforme **une
conférence YouTube en document Word et PDF partageables** — acquisition,
reconnaissance vocale et mise en page, chaque étape par un helper différent :

**🌐 youtube-helper → 🗣️ vocal-helper → 📄 md2star (`md2docx` / `md2pdf`)**

```python
import youtube_helper as yth      # 🌐 acquisition
import audio_helper as ah          # 🔊 décodage en PCM
import vocal_helper as voh         # 🗣️ reconnaissance vocale (Whisper)

URL = "https://www.youtube.com/watch?v=YE7VzlLtp-4"

# 1) Acquérir — récupérer l'audio de la conférence (16 kHz mono, idéal pour l'ASR).
yth.download_audio(URL, "talk.mp3", target_sample_rate=16000)

# 2) Transcrire — Whisper sur le PCM décodé (to_numpy=True → tableau float32).
pcm, sr = ah.load_audio("talk.mp3", target_sample_rate=16000, to_mono=True, to_numpy=True)
transcript = voh.transcribe_pcm(pcm, sr, language="fr")

# 3) Passer la main à md2star — écrire un fichier Markdown titré pour la mise en page.
with open("talk.md", "w", encoding="utf-8") as fh:
    fh.write(f"# Transcription de la conférence\n\n_Source : {URL}_\n\n{transcript}\n")
```

```bash
# 4) Mettre en page la transcription en document Word et en PDF (CLIs md2star).
md2docx talk.md      # → talk.docx
md2pdf  talk.md      # → talk.pdf
```

Comme le rendu `md → docx → pdf` de md2star est fidèle et réversible (voir
l'[identité d'aller-retour de md2star](https://github.com/warith-harchaoui/md2star#round-trip-fidelity)),
les documents produits peuvent être relus en Markdown sans perdre le texte de
la transcription.

## Auteur
[Warith HARCHAOUI](https://linkedin.com/in/warith-harchaoui)

## Remerciements
Remerciements chaleureux à [Mohamed Chelali](https://mchelali.github.io) et [Bachir Zerroug](https://www.linkedin.com/in/bachirzerroug) pour nos échanges fructueux.

## Licence
Ce projet est sous licence [BSD-3-Clause](https://github.com/warith-harchaoui/ai-helpers/blob/main/LICENSE).
