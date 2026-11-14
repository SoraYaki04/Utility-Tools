# 🛠️ Utility Tools (All-in-One)

A modern, lightweight desktop utility suite built with **Python** and **CustomTkinter**. Designed as an all-in-one "Swiss Army Knife" for everyday file manipulation, media conversion, compression, and downloading—packaged into a standalone Windows executable (`.exe`) with zero external installation required.

[![Latest Release](https://img.shields.io/github/v/release/SoraYaki04/Utility-Tools?style=for-the-badge&color=blue)](https://github.com/SoraYaki04/Utility-Tools/releases/latest)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)](https://github.com/SoraYaki04/Utility-Tools/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

---

## ✨ Key Features

### 🎨 Image Tools
* **Bulk Image Converter:** Convert multiple images simultaneously into `.png`, `.jpg`, `.webp`, `.jfif`, `.ico`, and `.bmp`.
* **Image Compressor:** Reduce image file sizes efficiently with 3 selectable quality levels.

### 📄 PDF Tools
* **PDF Merger:** Combine multiple PDF documents into a single file.
* **PDF Compressor:** Shrink PDF file sizes using stream compression and unused object cleanup (`PyMuPDF`).

### 🎬 Video Tools
* **Video Converter:** Quickly convert video files into `.mp4`, `.mkv`, `.avi`, `.mov`, `.webm`.
* **Video Compressor:** Downscale video resolution (720p, 480p, 360p) and optimize file size.
* **Video to MP3:** Extract high-quality MP3 audio directly from video files.

### 🌐 Downloader Tools
* **YouTube Downloader:** Download videos in MP4 (H.264 / AV1 up to 1080p) or extract audio in MP3 (up to 320kbps).

---

## 📥 Download & Quick Start (Windows)

No Python environment or manual FFmpeg setup is needed to use the compiled app:

1. Go to the **[Releases Page](https://github.com/SoraYaki04/Utility-Tools/releases/latest)**.
2. Download **`UtilityTools.exe`** under the **Assets** section.
3. Double-click **`UtilityTools.exe`** to launch the application.
   > *Note: If Windows SmartScreen displays a warning because the executable is not signed with a paid certificate, click **More info** $\rightarrow$ **Run anyway**.*

---

## 📁 Project Structure

This project follows a modular architecture separating UI components from core processing logic:

```text
Utility-Tools/
│
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
│
├── bin/                    # External binaries (place ffmpeg.exe here for dev/build)
│
├── gui/                    # CustomTkinter UI windows (Frontend)
│   ├── main_window.py
│   ├── image_converter_window.py
│   ├── image_compressor_window.py
│   ├── pdf_merger_window.py
│   ├── pdf_compressor_window.py
│   ├── video_converter_window.py
│   ├── video_compressor_window.py
│   ├── video_to_mp3_window.py
│   └── yt_downloader_window.py
│
└── tools/                  # Pure file/media processing logic (Backend)
```

---

## 💻 Running from Source (For Developers)

If you want to run or modify the source code locally:

### 1. Clone the Repository
```bash
git clone https://github.com/SoraYaki04/Utility-Tools.git
cd Utility-Tools
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

### 3. Add FFmpeg Binary
Download the Windows build of `ffmpeg.exe` and place it inside the `bin/` folder (`bin/ffmpeg.exe`) so the video and downloader modules can process media.

### 4. Run the Application
```bash
python main.py
```

### 5. Build Standalone `.exe` (Optional)
```bash
pip install pyinstaller
pyinstaller --clean --noconsole --onefile --add-data "bin/ffmpeg.exe;bin" --name="UtilityTools" main.py
```

---

## 🙏 Credits & Third-Party Libraries

* **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** – Modern Python UI library
* **[Pillow](https://python-pillow.org/)** – Image processing
* **[PyMuPDF](https://pymupdf.readthedocs.io/)** – PDF rendering and compression
* **[FFmpeg](https://ffmpeg.org/)** – Audio/video conversion and compression
* **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** – YouTube media extraction
