# 🚀 Usage
Basic Command
bash
python audio_toolkit.py
Input CSV Format
Create a CSV file with YouTube URLs and optional metadata:

```csv
https://www.youtube.com/watch?v=VIDEO_ID1,Custom Name 1,segments1.csv
https://www.youtube.com/watch?v=VIDEO_ID2,Custom Name 2,segments2.csv
Segment CSV Format
For precise audio extractions, provide a segments CSV:

```csv
Start,End,Segment Name
0:00,1:30,Introduction
2:15,4:45,Main Content
5:00,end,Conclusion
⚙️ Configuration Options
Parameter	Description	Default
bitrate	Audio quality (128k-320k)	256k
output_format	File format (mp3/m4a/wav)	mp3
sample_rate	Audio sample rate (Hz)	48000
channels	Audio channels (1=mono, 2=stereo)	2
📂 Output Structure
```text
youtube_audio_TIMESTAMP/
├── full_audio/            # Complete downloaded tracks
│   ├── seo-name-1.mp3
│   └── seo-name-2.mp3
└── segments/              # Extracted audio segments
    ├── introduction.mp3
    └── main-content.mp3

**🔍 SEO Optimization Features**
Automatic filename cleaning (special characters removal)

Smart hyphenation for readability

ASCII normalization for international characters

Length optimization (max 80 chars)

Consistent lowercase formatting

🤝 Contributing
Fork the project

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some amazing feature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

