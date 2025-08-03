# 🎧 YouTube Premium Audio Toolkit

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![FFmpeg Required](https://img.shields.io/badge/requires-FFmpeg-orange)](https://ffmpeg.org/)

A powerful Python tool for downloading and processing high-quality audio from YouTube with SEO-friendly filenames, precise segment extraction, and batch processing capabilities.

## 🌟 Key Features

- **High-Quality Audio Extraction** - Download Opus/AAC audio at best available quality
- **Precision Audio Editing** - Extract exact segments with sample-accurate trimming
- **SEO-Optimized Filenames** - Automatic conversion to search-friendly filenames
- **Batch Processing** - Handle multiple URLs and segments via CSV
- **Smart CSV Detection** - Auto-recognizes start/end/name columns
- **Format Conversion** - Output to MP3, M4A, or WAV with configurable bitrate

## 📥 Installation

### Prerequisites

1. **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
2. **FFmpeg** - Required for audio processing:
   ```bash
   # Ubuntu/Debian
   sudo apt install ffmpeg

   # macOS (via Homebrew)
   brew install ffmpeg

   # Windows (via Chocolatey)
   choco install ffmpeg
