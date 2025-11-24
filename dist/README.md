# AETHER-AI Installation Files

This directory contains installation scripts for different operating systems.

## Installation Instructions

### Windows

1. Download `install_windows.zip`
2. Extract the ZIP file
3. Right-click on `install_windows.bat` and select "Run as administrator"
4. Follow the on-screen instructions

### macOS

1. Download `install_mac.zip`
2. Extract the ZIP file
3. Open Terminal and navigate to the extracted folder
4. Run: `chmod +x install_mac.sh && ./install_mac.sh`
5. Follow the on-screen instructions

### Linux

1. Download `install_linux.zip`
2. Extract the ZIP file
3. Open Terminal and navigate to the extracted folder
4. Run: `chmod +x install_linux.sh && ./install_linux.sh`
5. Follow the on-screen instructions

## What These Scripts Do

The installation scripts will:

1. Check for Python 3.9+ installation
2. Check for Git (optional but recommended)
3. Clone or download the AETHER-AI repository
4. Install required Python dependencies
5. Create a configuration file (.env) from the template
6. Create launcher scripts for easy execution
7. Optionally create system-wide shortcuts

## Requirements

- **Python**: 3.9 or higher
- **Internet Connection**: Required for downloading dependencies and cloud AI models
- **Disk Space**: At least 500MB free space
- **Optional**: Git for easier updates

## Getting API Keys

To use AETHER-AI, you'll need API keys from one or more providers:

- **Gemini**: https://makersuite.google.com/app/apikey
- **Groq**: https://console.groq.com/keys
- **HuggingFace**: https://huggingface.co/settings/tokens
- **OpenAI**: https://platform.openai.com/api-keys

You can also use **Ollama** for local AI models without any API keys:
- Install from: https://ollama.ai

## Troubleshooting

### Python Not Found
- Windows: Install from https://www.python.org/downloads/ and check "Add Python to PATH"
- macOS: Install via Homebrew: `brew install python@3.9`
- Linux: Use your package manager (apt, dnf, pacman, etc.)

### Permission Denied
- Windows: Run the script as administrator
- macOS/Linux: Run with `sudo` if installing system-wide

### Installation Fails
- Make sure you have a stable internet connection
- Try running the script again
- Check if Python and pip are properly installed
- Manually install dependencies: `pip install -e .`

## Manual Installation

If the automated scripts don't work, you can install manually:

```bash
# Clone the repository
git clone https://github.com/KunjShah95/AETHER-AI.io.git
cd AETHER-AI.io

# Install dependencies
pip install -e .

# Create configuration file
cp .env.example .env
# Edit .env and add your API keys

# Run AETHER-AI
python terminal/main.py
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/KunjShah95/AETHER-AI.io/issues
- Documentation: https://kunjshah95.github.io/AETHER-AI.io/docs.html

## Security

These installation scripts:
- Only download from official GitHub repository
- Don't require sudo/admin access (except for optional system-wide installation)
- Don't modify system files outside the installation directory
- Store all data locally in your user directory

Always verify the checksum of downloaded files before running installation scripts.
