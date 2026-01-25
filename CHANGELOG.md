# Changelog

All notable changes to NeuroVault will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.0] - 2026-01-25

### Added
- 🎤 **Voice Input** - Speak your questions using microphone
- 💬 **Streaming AI Responses** - Watch AI think in real-time, word by word
- 🔄 **Multiple AI Models** - Switch between llama-3.3-70b, mixtral, gemma2, and local Ollama models
- 💾 **Chat History** - Save and load conversation sessions
- 📝 **Document Summarization** - AI-generated TL;DR for any document
- ⚖️ **Document Comparison** - Side-by-side analysis of two documents
- 🏷️ **Tags & Categories** - Organize files with custom tags
- 🔍 **Search History** - Track and re-run past searches
- 🎁 **Standalone Executable** - No Python installation required
- 💿 **Professional Installer** - One-click Windows installation

### Changed
- Complete UI redesign with modern dark theme
- Improved animations and micro-interactions
- Better error handling and toast notifications
- Enhanced loading indicators with spinners
- Optimized database queries with proper indexing

### Fixed
- Memory leaks in chat interface
- Search result display issues
- File upload validation

## [3.0.0] - 2026-01-24

### Added
- 🌙 Dark/Light theme toggle
- 🔔 Toast notifications system
- ⏳ Loading indicators and spinners
- 📊 Word count display for documents

### Changed
- Migrated to CustomTkinter for modern UI
- Improved responsive layouts

## [2.0.0] - 2026-01-23

### Added
- 🤖 RAG chatbot functionality
- 🔎 Semantic search with ChromaDB vector database
- 📄 OCR support for scanned PDFs (pytesseract)
- 📚 Support for PDF, DOCX, TXT, and Python files

### Changed
- Switched from keyword search to vector embeddings
- Added sentence-transformers for embeddings

## [1.0.0] - 2026-01-22

### Added
- 📁 Initial release
- File upload and parsing
- Basic chat interface
- SQLite database for document storage
