---

🚀 YT-Downloader-Pro

Professional YouTube Video & Playlist Downloader
Advanced YouTube downloader with single video and full playlist support, colorful interface, and smart options.

https://img.shields.io/badge/Python-3.7%2B-blue
https://img.shields.io/badge/License-MIT-green
https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Android-brightgreen

---

✨ Features

· ✅ Single video download with multiple quality options
· ✅ Full playlist support – choose specific videos by number or range
· ✅ Smart detection – automatically detects if URL is a video or playlist
· ✅ Rich colored interface using rich library
· ✅ Video options – Best, 1080p, 720p, 480p; MP4/MKV
· ✅ Audio only – MP3 with 320/192/128 kbps quality
· ✅ Progress bars for each download
· ✅ Organized output – Playlists saved in separate folders
· ✅ Android friendly – auto-detects /storage/emulated/0/Download
· ✅ Auto install missing dependencies – no manual setup

---

📸 Screenshots

(Add your own screenshots after running the script)

Playlist selection Download progress
https://via.placeholder.com/400x200?text=Playlist+Menu https://via.placeholder.com/400x200?text=Progress+Bar

---

🔧 Installation

1. Clone or download

```bash
git clone https://github.com/sadikmahedi88/YT-Downloader-Pro.git
cd YT-Downloader-Pro
```

2. Run the script (auto-installs dependencies)

```bash
python yt_downloader.py
```

No need to manually install yt-dlp or rich – the script does it automatically.

3. On Android (Termux)

```bash
pkg update && pkg upgrade
pkg install python ffmpeg
python yt_downloader.py
```

---

🎮 Usage

1. Launch the script
2. Enter YouTube URL (video or playlist)
3. Choose download type (Video / Audio)
4. Select quality settings
5. If playlist – choose which videos:
   · 1,3,5 → specific videos
   · 1-5 → range
   · 99 → all videos
6. Wait for download to complete

---

🧪 Example

```
🔗 Enter YouTube URL: https://youtube.com/playlist?list=PLabc123
✅ Playlist detected: "Python Tutorials" (12 videos)

┌────┬────────────────────────────┐
│ #  │ Video Title                │
├────┼────────────────────────────┤
│ 1  │ Introduction               │
│ 2  │ Variables                  │
│ 3  │ Loops                      │
│ ...│ ...                        │
└────┴────────────────────────────┘

Enter video numbers (1,3,5 or 1-5 or 99): 1-3,5
✅ Downloading videos 1,2,3,5...
```

---

📁 Output Structure

```
Download/
├── video_title.mp4                 (single video)
└── Playlist Name/
    ├── 1 - Introduction.mp4
    ├── 2 - Variables.mp4
    └── ...
```

---

❓ FAQ

Q: Does it work on Android?
Yes, fully compatible with Termux.

Q: Can I download only audio?
Yes, choose "Audio Only" and select MP3 quality.

Q: What if my playlist has 200 videos?
The script shows first 30 titles, then asks for your selection. You can download all (99) or a range.

Q: Does it support YouTube shorts?
Yes, Shorts URLs work as single videos.

---

🛠️ Requirements (auto-installed)

· yt-dlp – YouTube downloading engine
· rich – colored terminal interface
· ffmpeg – required for merging video/audio (install manually if needed)

---

👨‍💻 Developer

sadikmahedi88

· GitHub: github.com/sadikmahedi88
· Telegram: t.me/Murphython

---

📜 License

MIT License – free to use, modify, and share.

---

⭐ Support

If you like this tool, give it a star ⭐ on GitHub and share with friends!

---

📁 Final File Structure

```
YT-Downloader-Pro/
├── yt_downloader.py     (main script)
└── README.md            (this file)
```

---
