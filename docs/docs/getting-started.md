# Getting Started

## Prerequisites
- Python 3.9+
- Internet access for cloud models (Gemini, Groq, HuggingFace, ChatGPT, MCP)
- Optional: Ollama installed and running for local models

## Installation

### Option A: One-click OS scripts
- Windows: `dist/install_windows.bat`
- macOS: `dist/install_mac.sh`
- Linux: `dist/install_linux.sh`

Verify SHA256 checksums in `dist/SHA256SUMS.txt` before running installers.

### Option B: From source (recommended for development)
```bash
# Clone
 git clone https://github.com/KunjShah95/NEXUS-AI.io.git
 cd NEXUS-AI.io

# Install dependencies
 pip install -r requirements.txt

# Configure environment
 cp .env.example .env   # set your API keys

# Run
 python terminal/main.py
```

## Quick Start
- Type `/help` to see the full command catalog
- Switch models anytime with `/switch [model]`
- Use `/ollama-models` to list your local Ollama models
