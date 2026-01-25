<p align="center">
  <img src="assets/logo.png" width="180" alt="NeuroVault Logo">
</p>

<h1 align="center">🧠 NeuroVault v4.0</h1>

<p align="center">
  <b>Your AI-Powered Second Brain</b><br>
  <i>Local-first document management with semantic search, AI chat, and smart insights</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-4.0.0-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/python-3.11+-green?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/platform-Windows-lightgrey?style=for-the-badge&logo=windows" alt="Platform">
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-screenshots">Screenshots</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-usage">Usage</a>
</p>

---

## ✨ Features

### 🎨 Beautiful Modern UI
- **Dark Theme** - Easy on the eyes, perfect for long sessions
- **Smooth Animations** - Micro-interactions and transitions
- **Loading Indicators** - Spinners and toast notifications
- **Responsive Design** - Adapts to your window size

### 🤖 Advanced AI Capabilities
| Feature | Description |
|---------|-------------|
| 💬 **Streaming Responses** | Watch AI think in real-time, word by word |
| 🔄 **Multiple Models** | Switch between Groq (llama-3.3-70b, mixtral) and local Ollama |
| 🎤 **Voice Input** | Speak your questions using microphone |
| 💾 **Chat History** | Save and resume conversations anytime |

### 📊 Productivity Tools
| Feature | Description |
|---------|-------------|
| 📝 **AI Summarization** | One-click TL;DR of any document |
| ⚖️ **Document Comparison** | Side-by-side diff with AI analysis |
| 🏷️ **Smart Tags** | Organize files with custom categories |
| 🔍 **Search History** | Track and re-run past searches |

### 🔎 Semantic Search
- **Vector Embeddings** - Find relevant content, not just keywords
- **ChromaDB** - Fast, local vector database
- **Multi-format** - Search across PDFs, DOCX, TXT, Python files

### 🔒 Privacy First
- ✅ 100% local - No data leaves your computer
- ✅ No cloud required (except optional Groq API)
- ✅ Your documents, your control

---

## 🚀 Quick Start

### Option 1: Download Installer (Recommended)
1. Download **[NeuroVault-v4.0-Setup.exe](https://github.com/madhurtyagii/NeuroVault/releases/latest)**
2. Run the installer
3. Launch from Start Menu or Desktop
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

**Option A: Groq Cloud (Recommended - Fast & Free)**
1. Get free API key at [console.groq.com](https://console.groq.com)
2. Create `.env` file: `GROQ_API_KEY=your_key_here`
3. Enjoy blazing fast responses!

**Option B: Local Ollama**
1. Install [Ollama](https://ollama.ai)
2. Run: `ollama pull llama3.2`
3. Start Ollama service
4. Fully offline AI!

---

## 📸 Screenshots

<p align="center">
  <img src="docs/screenshots/chat.png" width="80%" alt="Chat Interface">
</p>

<p align="center">
  <i>💬 AI Chat with streaming responses and voice input</i>
</p>

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **UI Framework** | CustomTkinter |
| **AI Backend** | Groq API / Ollama |
| **Vector Database** | ChromaDB |
| **Embeddings** | sentence-transformers |
| **Database** | SQLite |
| **OCR** | Tesseract (optional) |
| **Voice** | SpeechRecognition |

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
3. Ask questions about your files
4. AI answers using document context

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

## 🗺️ Roadmap

- [x] Phase A: Visual Polish
- [x] Phase B: Advanced AI Features
- [x] Phase C: Productivity Tools
- [x] Phase D: Deployment & Packaging
- [ ] Phase E: Cloud Sync (optional)
- [ ] Phase F: Cross-platform (Mac/Linux)

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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Madhur Tyagi**

[![GitHub](https://img.shields.io/badge/GitHub-@madhurtyagii-181717?style=flat&logo=github)](https://github.com/madhurtyagii)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Madhur_Tyagi-0077B5?style=flat&logo=linkedin)](https://linkedin.com/in/madhurtyagii)

---

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) - Local LLM inference
- [Groq](https://groq.com) - Ultra-fast cloud inference
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern Python GUI
- [ChromaDB](https://www.trychroma.com/) - Vector embeddings database

---

<p align="center">
  Made with ❤️ by Madhur Tyagi
</p>

<p align="center">
  ⭐ Star this repo if you find it useful! ⭐
</p>
