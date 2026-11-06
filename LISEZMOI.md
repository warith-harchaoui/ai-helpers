# AI Helpers

[🇫🇷](https://github.com/warith-harchaoui/ai-helpers/blob/main/LISEZMOI.md) · [🇬🇧](https://github.com/warith-harchaoui/ai-helpers/blob/main/README.md)

[![Étoiles GitHub](https://img.shields.io/github/stars/warith-harchaoui/ai-helpers?style=social)](https://github.com/warith-harchaoui/ai-helpers)
[![Licence : BSD-3-Clause](https://img.shields.io/badge/licence-BSD--3--Clause-blue.svg)](LICENSE)
[![17 paquets sur PyPI](https://img.shields.io/badge/PyPI-17%20paquets-3775A9?logo=pypi&logoColor=white)](https://pypi.org/user/warith-harchaoui/)
[![6 crates sur crates.io](https://img.shields.io/badge/crates.io-6%20crates-orange?logo=rust)](https://crates.io/users/warith-harchaoui)

**Dix-sept bibliothèques Python qui font chacune un travail d'IA ou de média, sur votre propre machine.** Transcrire une réunion en sachant qui a dit quoi, lire un texte à voix haute, télécharger une conférence, changer du Markdown en document Word, choisir le modèle local qui tourne sur votre portable. Aucun compte, aucune télémétrie, aucun serveur à nous dans la boucle. Six des dix-sept existent aussi en Rust, pour les téléphones et les petits boîtiers que Python n'atteint pas.

🌍 **Site, documentation et questions fréquentes : [deraison.ai/ai-helpers](https://deraison.ai/ai-helpers/index.fr.php)**

⭐ **Si la suite a gagné sa place dans votre boîte à outils, mettez une étoile à ce dépôt.** Un clic, aucune lettre d'information en retour. Le prochain développeur qui passe par là verra que le détour en valait la peine. Une brique vous a sauvé un après-midi ? Son propre dépôt mérite aussi la sienne.

---

## Que voulez-vous faire ?

| Vous voulez… | Prenez |
|---|---|
| transcrire une réunion en sachant qui a dit quoi, en direct ou après coup | [`vocal-helper`](https://github.com/warith-harchaoui/vocal-helper) |
| lire un texte à voix haute, diffuser une réponse au fil de l'eau ou cloner une voix | [`speaker-helper`](https://github.com/warith-harchaoui/speaker-helper) |
| parler à voix haute avec un modèle local et lui couper la parole | [`discussion-helper`](https://github.com/warith-harchaoui/discussion-helper) |
| charger, convertir, découper, assembler ou séparer de l'audio | [`audio-helper`](https://github.com/warith-harchaoui/audio-helper) |
| extraire les images ou les sous-titres d'une vidéo | [`video-helper`](https://github.com/warith-harchaoui/video-helper) |
| enregistrer la webcam ou le micro | [`capture-helper`](https://github.com/warith-harchaoui/capture-helper) |
| télécharger une vidéo, son audio ou sa vignette depuis YouTube, Vimeo, SoundCloud… | [`youtube-helper`](https://github.com/warith-harchaoui/youtube-helper) |
| lire n'importe quel flux audio (un podcast, une radio, une URL) sous forme d'échantillons | [`podcast-helper`](https://github.com/warith-harchaoui/podcast-helper) |
| envoyer des fichiers vers S3, MinIO, R2 ou un autre stockage objet | [`bucket-helper`](https://github.com/warith-harchaoui/bucket-helper) |
| transférer des fichiers en SFTP, avec vérification stricte de la clé d'hôte | [`sftp-helper`](https://github.com/warith-harchaoui/sftp-helper) |
| changer du Markdown en document Word, PowerPoint ou PDF (et revenir au Markdown) | [`md2star`](https://github.com/warith-harchaoui/md2star) |
| ne plus payer deux fois le même appel d'API ou le même modèle lent | [`wallet-helper`](https://github.com/warith-harchaoui/wallet-helper) |
| placer des concurrents sur une carte de positionnement à partir d'un tableau comparatif | [`standpoint`](https://github.com/warith-harchaoui/standpoint) |
| trouver le modèle de langue ou de vision local qui tourne sur cette machine | [`best-engine-ai-helper`](https://github.com/warith-harchaoui/best-engine-ai-helper) |
| choisir un moteur de recherche vectorielle à partir de critères mesurés | [`ann-router`](https://github.com/warith-harchaoui/ann-router) |
| trouver le coude d'une courbe ou apprendre qu'il n'y en a pas | [`elbow-helper`](https://github.com/warith-harchaoui/elbow-helper) |
| gérer fichiers, processus, empreintes, configuration et chronomètres sur tout système | [`os-helper`](https://github.com/warith-harchaoui/os-helper) |

## Démarrage rapide

Chaque brique est un paquet PyPI distinct. Installez celle qui vous sert : elle amène avec elle `os-helper`, le socle commun.

```bash
pip install youtube-helper audio-helper vocal-helper md2star
```

Il faut Python 3.10 à 3.13. Les briques média appellent `ffmpeg`, à installer d'abord (`brew install ffmpeg` sur macOS). md2star a aussi besoin de Pandoc.

Quatre briques, une chaîne : une conférence YouTube devient un document Word et un PDF.

```python
import youtube_helper as yth   # récupération
import audio_helper as ah      # décodage
import vocal_helper as voh     # parole vers texte

URL = "https://www.youtube.com/watch?v=YE7VzlLtp-4"

yth.download_audio(URL, "talk.mp3", target_sample_rate=16000)
pcm, sr = ah.load_audio("talk.mp3", target_sample_rate=16000, to_mono=True, to_numpy=True)
transcript = voh.transcribe_pcm(pcm, sr, language="en")

with open("talk.md", "w", encoding="utf-8") as fh:
    fh.write(f"# Talk transcript\n\n_Source: {URL}_\n\n{transcript}\n")
```

```bash
md2docx talk.md   # talk.docx
md2pdf  talk.md   # talk.pdf
```

## Les dix-sept briques

| Groupe | Brique | Son travail | Liens |
|---|---|---|---|
| 🧱 Socle | [`os-helper`](https://github.com/warith-harchaoui/os-helper) | Le socle que toutes les autres importent : détection du système et du matériel, processus, chemins, empreintes, configuration, chronomètres | [PyPI](https://pypi.org/project/os-helper/) · [Doc](https://deraison.ai/ai-helpers/docs/os-helper-doc/modules.html) |
| 🔊 Audio et voix | [`audio-helper`](https://github.com/warith-harchaoui/audio-helper) | Charger, rééchantillonner, convertir, découper, assembler et séparer l'audio | [PyPI](https://pypi.org/project/audio-helper/) · [Doc](https://deraison.ai/ai-helpers/docs/audio-helper-doc/modules.html) |
| | [`vocal-helper`](https://github.com/warith-harchaoui/vocal-helper) | De l'audio en entrée, des énoncés attribués et transcrits en sortie, en direct ou sur tout un enregistrement | [PyPI](https://pypi.org/project/vocal-helper/) · [Doc](https://deraison.ai/ai-helpers/docs/vocal-helper-doc/modules.html) |
| | [`speaker-helper`](https://github.com/warith-harchaoui/speaker-helper) | Du texte en entrée, de la parole en sortie, avec un routeur qui choisit le moteur sur mesures | [PyPI](https://pypi.org/project/speaker-helper/) · [Doc](https://deraison.ai/ai-helpers/docs/speaker-helper-doc/modules.html) |
| | [`discussion-helper`](https://github.com/warith-harchaoui/discussion-helper) | Une conversation parlée au micro, interruptions comprises | [PyPI](https://pypi.org/project/discussion-helper/) · [Doc](https://deraison.ai/ai-helpers/docs/discussion-helper-doc/modules.html) |
| 🎬 Vidéo et capture | [`video-helper`](https://github.com/warith-harchaoui/video-helper) | Images, conversions et sous-titres, avec le moteur d'extraction choisi pour vous | [PyPI](https://pypi.org/project/video-helper/) · [Doc](https://deraison.ai/ai-helpers/docs/video-helper-doc/modules.html) |
| | [`capture-helper`](https://github.com/warith-harchaoui/capture-helper) | Caméra et micro en direct, sur tous les systèmes | [PyPI](https://pypi.org/project/capture-helper/) · [Doc](https://deraison.ai/ai-helpers/docs/capture-helper-doc/modules.html) |
| 🌐 Acquisition de médias | [`youtube-helper`](https://github.com/warith-harchaoui/youtube-helper) | Vidéos, audio et vignettes depuis YouTube et ses cousins | [PyPI](https://pypi.org/project/youtube-helper/) · [Doc](https://deraison.ai/ai-helpers/docs/youtube-helper-doc/modules.html) |
| | [`podcast-helper`](https://github.com/warith-harchaoui/podcast-helper) | N'importe quel flux audio, lu sous la forme qu'attend un modèle de parole | [PyPI](https://pypi.org/project/podcast-helper/) · [Doc](https://deraison.ai/ai-helpers/docs/podcast-helper-doc/modules.html) |
| 🗄️ Stockage et transfert | [`bucket-helper`](https://github.com/warith-harchaoui/bucket-helper) | S3 et tous les stockages compatibles S3 | [PyPI](https://pypi.org/project/bucket-helper/) · [Doc](https://deraison.ai/ai-helpers/docs/bucket-helper-doc/modules.html) |
| | [`sftp-helper`](https://github.com/warith-harchaoui/sftp-helper) | Transferts SFTP avec vérification stricte de la clé d'hôte | [PyPI](https://pypi.org/project/sftp-helper/) · [Doc](https://deraison.ai/ai-helpers/docs/sftp-helper-doc/modules.html) |
| 📄 Documents | [`md2star`](https://github.com/warith-harchaoui/md2star) | Markdown vers DOCX, PPTX et PDF avec des gabarits de marque ; retour au Markdown aussi | [PyPI](https://pypi.org/project/md2star/) · [Doc](https://deraison.ai/ai-helpers/docs/md2star-doc/modules.html) |
| ♻️ Cache | [`wallet-helper`](https://github.com/warith-harchaoui/wallet-helper) | Ne jamais lancer deux fois le même appel coûteux | [PyPI](https://pypi.org/project/wallet-helper/) · [Doc](https://deraison.ai/ai-helpers/docs/wallet-helper-doc/modules.html) |
| 🧩 Divers | [`standpoint`](https://github.com/warith-harchaoui/standpoint) | Un tableau comparatif en entrée, une carte de positionnement et ses coordonnées en sortie | [PyPI](https://pypi.org/project/standpoint/) · [Doc](https://deraison.ai/ai-helpers/docs/standpoint-doc/modules.html) |
| | [`best-engine-ai-helper`](https://github.com/warith-harchaoui/best-engine-ai-helper) | Le meilleur modèle local pour cette machine, téléchargé puis vérifié | [PyPI](https://pypi.org/project/best-engine-ai-helper/) · [Doc](https://deraison.ai/ai-helpers/docs/best-engine-ai-helper-doc/modules.html) |
| | [`ann-router`](https://github.com/warith-harchaoui/ann-router) | Le bon moteur de plus proches voisins, raisons écrites à l'appui | [PyPI](https://pypi.org/project/ann-router/) · [Doc](https://deraison.ai/ai-helpers/docs/ann-router-doc/modules.html) |
| | [`elbow-helper`](https://github.com/warith-harchaoui/elbow-helper) | Un coude avec son incertitude ou une abstention explicite | [PyPI](https://pypi.org/project/elbow-helper/) · [Doc](https://deraison.ai/ai-helpers/docs/elbow-helper-doc/modules.html) |

## La même forme partout

![Comment la suite AI Helpers s'assemble : seize briques à un travail chacune, sur un socle commun](https://raw.githubusercontent.com/warith-harchaoui/ai-helpers/main/assets/diagrams/how-it-works.png)

Qui sait conduire une brique sait conduire les seize autres. Chacune offre :

- une **API Python** ;
- une **ligne de commande** écrite avec click (os-helper, le socle, n'en a pas) ;
- un **serveur HTTP FastAPI** ;
- un **jeu d'outils MCP** pour les agents d'IA, monté à `/mcp` sur ce même serveur : chaque outil est une route, les deux ne divergent jamais ;
- un **skill** à installer dans Claude Code ou OpenCode ;
- quand vérifier le résultat dans un navigateur aide vraiment, une petite **interface à `/gui`**, sans étape de construction ni appel extérieur.

Treize des dix-sept livrent aussi un Dockerfile avec un `docker-compose.yml` qui amène le compagnon nécessaire : MinIO pour Bucket, un serveur SFTP jetable pour SFTP, Ollama pour Standpoint et Best Engine, Qdrant et pgvector pour ANN Router.

Chaque dépôt contient un `TRIGGERS.md` : la liste complète des cas où appeler la brique et de ceux où la laisser tranquille. Le skill en garde une copie ; un test échoue dès que les deux copies divergent. Votre agent apprend quand appeler la brique. Il apprend aussi à ne pas transcrire un tableur.

## Local d'abord, exceptions écrites

- **Entièrement sur votre machine :** os, audio, video, capture, vocal, speaker, discussion, md2star et wallet. Quelques-unes téléchargent une fois un modèle ou un gabarit, puis travaillent hors ligne.
- **Seulement ce que vous demandez :** youtube-helper et podcast-helper contactent les sites et les flux que vous désignez. Elles n'envoient rien sur vous.
- **À distance par construction :** bucket-helper et sftp-helper envoient vos fichiers vers le stockage que vous choisissez. C'est leur métier ; la destination vous appartient, jamais un réglage caché.

Vocal et Speaker connaissent aussi quelques moteurs hébergés payants (Gladia, ElevenLabs, pyannoteAI). Elles n'en appellent un que si vous le nommez avec sa clé. Le routage automatique ne les choisit jamais.

## Les réécritures Rust

Six briques existent aussi en réécritures Rust indépendantes, sur [crates.io](https://crates.io/users/warith-harchaoui) :

```bash
cargo add audio-helper-rs capture-helper-rs podcast-helper-rs youtube-helper-rs
cargo add vocal-helper-rs --features onnx
cargo install md2star-rs   # md2star-rs, md2docx, md2pptx : ni Pandoc ni Python
```

| Crate | Ce qu'elle fait |
|---|---|
| [`vocal-helper-rs`](https://github.com/warith-harchaoui/vocal-helper-rs) | Diarisation et transcription en flux par ONNX Runtime, avec le fournisseur d'exécution (CUDA, TensorRT, CoreML, DirectML, OpenVINO ou processeur) mesuré sur l'appareil |
| [`capture-helper-rs`](https://github.com/warith-harchaoui/capture-helper-rs) | Un micro en direct sous forme de paquets PCM, par la pile audio du système |
| [`audio-helper-rs`](https://github.com/warith-harchaoui/audio-helper-rs) | Utilitaires audio sur fichiers, au-dessus de `ffmpeg` et `ffprobe` |
| [`podcast-helper-rs`](https://github.com/warith-harchaoui/podcast-helper-rs) | N'importe quelle source audio en entrée, le PCM qu'attend un modèle de parole en sortie |
| [`youtube-helper-rs`](https://github.com/warith-harchaoui/youtube-helper-rs) | Une interface Rust typée autour de `yt-dlp` |
| [`md2star-rs`](https://github.com/warith-harchaoui/md2star-rs) | Markdown vers DOCX, PPTX et PDF dans un seul binaire statique, avec `twin` et `audit` |

**Pourquoi Rust, alors ?** Pour les appareils que Python n'atteint pas. Un téléphone n'a pas d'interpréteur ; les roues compilées existent une plateforme à la fois ; `torch` pèse à lui seul plusieurs gigaoctets. Rust compile depuis le même arbre pour macOS, Linux, Windows, iOS et Android. Il livre un seul fichier qui tourne sans rien installer.

**Et la vitesse ?** Rarement. Nous avons vérifié avant que quiconque se fasse des idées : dans la diarisation de vocal-helper, 99,8 % du temps passe dans ONNX Runtime, que Rust appelle exactement comme Python. Une réécriture gagne donc 0,2 % au mieux. vocal-helper-rs transcrit même plus lentement que son jumeau Python sur le processeur d'un M2 Max (facteur temps réel de 0,05 contre 0,022 à 0,028). Chaque crate est comparée au Python qu'elle reprend ; vocal-helper-rs retrouve ses probabilités de diarisation à 1,9e-6 près.

L'histoire complète, accélérateur par accélérateur, se lit sur [le site](https://deraison.ai/ai-helpers/index.fr.php#rust).

## Qui

[Warith Harchaoui](https://deraison.ai), [Mohamed Chelali](https://mchelali.github.io/) et [Bachir Zerroug](https://www.linkedin.com/in/bachirzerroug/), qui publient la suite depuis avril 2024. Écrivez à warithmetics@deraison.ai pour un bogue, une idée ou un projet où brancher la suite. Un humain lit chaque message.

## Licence

BSD-3-Clause, la licence de numpy et de scikit-learn : lisez, forkez, livrez. Voir [LICENSE](LICENSE).
