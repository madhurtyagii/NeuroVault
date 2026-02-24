<p align="center">
  <img src="assets/logo.png" width="180" alt="NeuroVault Logo">
</p>

<h1 align="center">🧠 NeuroVault v4.1</h1>

<p align="center">
  <b>Your AI-Powered Second Brain</b><br>
  <i>Local-first document management with semantic search, AI chat, and smart insights</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-4.1.0-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/python-3.11+-green?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/platform-Windows-lightgrey?style=for-the-badge&logo=windows" alt="Platform">
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-building">Building</a>
</p>

---

## ✨ Features

### 🎨 Beautiful Modern UI
- **Dark & Light Themes** — Toggle with one click
- **Smooth Animations** — Fade-in effects, typewriter text, loading spinners
- **Toast Notifications** — Slide-in alerts for every action
- **Responsive Layout** — Adapts to any window size

### 🤖 Smart AI Chat
| Feature | Description |
|---------|-------------|
| 💬 **Streaming Responses** | Watch AI think in real-time, word by word |
| 🔄 **Multiple Models** | Switch between Groq (llama-3.3-70b, mixtral, gemma2) and local Ollama |
| 🎤 **Voice Input** | Speak your questions via microphone |
| 💾 **Chat History** | Save, load, and resume conversations |
| 🎯 **Rich Formatting** | Bold text, bullet points, emojis — ChatGPT-style responses |
| 💡 **Flexible AI** | Casual greetings get friendly replies; knowledge queries search your docs |

### 📊 Productivity Tools
| Feature | Description |
|---------|-------------|
| 📝 **AI Summarization** | One-click TL;DR of any document |
| ⚖️ **Document Comparison** | Side-by-side diff with AI analysis |
| 🏷️ **Smart Tags** | Organize files with custom categories |
| 🔍 **Search History** | Track and re-run past searches |

### 🔎 Semantic Search
- **Vector Embeddings** — Find content by meaning, not just keywords
- **ChromaDB** — Fast, local vector database
- **Multi-format** — PDFs, DOCX, TXT, Python files

### 🔒 Privacy First
- ✅ 100% local processing — no data leaves your machine
- ✅ No cloud required (Groq API is optional)
- ✅ All data stored in `~/.neurovault/` on your system

---

## 🚀 Quick Start

### Option 1: Download MSI Installer (Recommended)
1. Download **[NeuroVault-v4.1-Setup.msi](https://github.com/madhurtyagii/NeuroVault/releases/latest)**
2. Double-click to install
3. Launch from Desktop shortcut or Start Menu
4. Done! 🎉

### Option 2: Run from Source
```bash
# Clone repository
git clone https://github.com/madhurtyagii/NeuroVault.git
cd NeuroVault

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run
python src/main.py
```

### AI Setup (Choose One)

**Option A: Groq Cloud (Recommended — Fast & Free)**
1. Get free API key at [console.groq.com](https://console.groq.com)
2. Create `.env` file: `GROQ_API_KEY=your_key_here`
3. Enjoy blazing fast responses!

**Option B: Local Ollama (Fully Offline)**
1. Install [Ollama](https://ollama.ai)
2. Run: `ollama pull llama3.2`
3. Start Ollama service
4. Complete privacy, no internet needed!

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **UI Framework** | CustomTkinter |
| **AI Backend** | Groq API / Ollama |
| **Vector Database** | ChromaDB |
| **Embeddings** | sentence-transformers |
| **Database** | SQLite |
| **Voice** | SpeechRecognition + PyAudio |
| **Installer** | cx_Freeze MSI |

---

## 📖 Usage

### 📁 Upload Documents
1. Go to **Files** tab
2. Click **📤 Upload File**
3. Select PDF, DOCX, TXT, or PY files
4. Add tags: `work, important, research`

### 🔎 Search with AI
1. Go to **Search** tab
2. Type your query: *"quantum physics equations"*
3. Get semantic results (not just keywords!)
4. Click to expand any result

### 💬 Chat with Documents
1. Go to **Chat** tab
2. Select AI model from dropdown
3. Ask questions about your files — or just say hi!
4. AI answers with rich formatting: **bold**, bullets, emojis

### 🎤 Voice Input
1. Click 🎤 microphone button
2. Speak your question
3. Text appears automatically
4. Press Enter to send

---

## 📋 System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **OS** | Windows 10 | Windows 11 |
| **RAM** | 8 GB | 16 GB |
| **Storage** | 2 GB | 5 GB |
| **GPU** | Not required | NVIDIA (for local AI) |

---

## 🔨 Building

### Build Standalone Executable
```bash
.venv\Scripts\python.exe -m PyInstaller NeuroVault.spec
```

### Build MSI Installer
```bash
.venv\Scripts\python.exe build_msi.py
```
Output: `dist/NeuroVault-v4.0-Setup.msi`

---

## 📂 Project Structure

```
NeuroVault/
├── src/                    # Application source code
│   ├── main.py             # Entry point
│   ├── chat_ui.py          # AI Chat interface
│   ├── files_ui.py         # File management UI
│   ├── search_ui.py        # Semantic search UI
│   ├── ai_model.py         # Groq/Ollama AI backend
│   ├── database.py         # SQLite database layer
│   ├── embeddings.py       # ChromaDB vector search
│   ├── styles.py           # UI theme & colors
│   ├── ui_components.py    # Reusable UI widgets
│   ├── parser.py           # Document parsing
│   └── ...
├── assets/                 # Logo and icons
├── build_msi.py            # MSI installer builder
├── NeuroVault.spec         # PyInstaller config
├── requirements.txt        # Python dependencies
├── LICENSE                 # MIT License
└── README.md               # This file
```

---

## 🗺️ Roadmap

- [x] Phase A: Visual Polish & Modern UI
- [x] Phase B: Advanced AI (Streaming, Multi-model, Voice)
- [x] Phase C: Productivity Tools (Summarize, Compare, Tags)
- [x] Phase D: Deployment & MSI Installer
- [x] Phase E: Flexible AI & Rich Formatting
- [ ] Phase F: Cloud Sync (optional)
- [ ] Phase G: Cross-platform (Mac/Linux)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Madhur Tyagi**

[![GitHub](https://img.shields.io/badge/GitHub-@madhurtyagii-181717?style=flat&logo=github)](https://github.com/madhurtyagii)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Madhur_Tyagi-0077B5?style=flat&logo=linkedin)](https://linkedin.com/in/madhurtyagii)

---

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) — Local LLM inference
- [Groq](https://groq.com) — Ultra-fast cloud inference
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — Modern Python GUI
- [ChromaDB](https://www.trychroma.com/) — Vector embeddings database

---

<p align="center">
  Made with ❤️ by Madhur Tyagi
</p>

<p align="center">
  ⭐ Star this repo if you find it useful! ⭐
</p>
