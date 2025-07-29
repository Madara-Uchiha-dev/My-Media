# 🎧 My-File-Trimer

**Trim, convert, and extract audio segments** from your `.mp3`, `.m4a`, or `.webm` files with precision. This lightweight tool uses `ffmpeg` to slice specific time ranges from your media into `.mp3`, `.wav`, or `.m4a` files — all controlled via a simple CSV.

---

## 🚀 Features

- 🔥 Supports `.mp3`, `.m4a`, `.webm` input formats
- 🎯 Precise segment extraction based on time ranges
- 📁 Output in `.mp3` (default), or `.wav` / `.m4a` via flag
- 🕒 Accepts multiple time formats:
  - `SS`, `MM:SS`, `HH:MM:SS`, `HH:MM:SS.sss`
- 📝 CSV-controlled batch processing
- 💡 No need for headers

---

## 📦 Setup Guide

### 1. Clone the repo

```bash
git clone https://github.com/your-username/My-File-Trimer.git
cd My-File-Trimer
2. Create a virtual environment
bash
Copy
Edit
python -m venv myenv
Activate it:
Windows

bash
Copy
Edit
.\myenv\Scripts\activate
Linux/macOS

bash
Copy
Edit
source myenv/bin/activate
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
🛠️ Install ffmpeg
Ubuntu/Debian
bash
Copy
Edit
sudo apt update && sudo apt install ffmpeg
macOS (with Homebrew)
bash
Copy
Edit
brew install ffmpeg
Windows (with Chocolatey)
bash
Copy
Edit
choco install ffmpeg
📑 CSV Format (No Header Required)
sql
Copy
Edit
start,end,"Name of file"
00:30,01:15,"Intro Music"
01:20,02:00,"Verse 1"
Use "" around file names if they contain spaces.

Flexible time formats supported: SS, MM:SS, HH:MM:SS, HH:MM:SS.sss

⚙️ Usage
Basic Command
bash
Copy
Edit
python extract_audio.py songs.mp4 segments.csv --no-header --name-col 2 --start-col 0 --end-col 1
Arguments Breakdown:
Argument	Description
songs.mp4	Input video/audio file (.webm, .mp4, .mp3, etc.)
segments.csv	CSV file defining start/end times and output names
--no-header	CSV has no header row
--name-col 2	Output name is in the 3rd column (0-indexed)
--start-col 0	Start times are in the 1st column
--end-col 1	End times are in the 2nd column

Change Output Format (e.g. WAV, M4A)
bash
Copy
Edit
python extract_audio.py songs.mp4 segments.csv --no-header --name-col 2 -f wav
Change Output Directory
bash
Copy
Edit
python extract_audio.py songs.mp4 segments.csv -o ./my_audio --no-header --name-col 2
💡 Pro Tips
Filenames are sanitized automatically.

Output defaults to the current directory if not specified.

Can handle long videos and large segment lists.

📜 License
Uchiha License — use freely, contribute kindly. ❤️
