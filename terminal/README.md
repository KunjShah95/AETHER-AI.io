# 🚀 NEXUS AI Terminal Assistant v3.0

A powerful, multi-model AI terminal assistant supporting Google Gemini, Groq, Ollama, HuggingFace, and DeepSeek models with enhanced security, voice input, web search, and beautiful UI.

## ✨ What's New in v3.0

- ✅ **Fixed Gemini 2.0 Flash API** - Resolved 400 errors with proper model configuration
- 🔧 **Enhanced Windows Installer** - Automated setup with better error handling
- 🔒 **Improved Security** - Enhanced input sanitization and API key validation
- 🎨 **Better UI** - Rich terminal interface with improved formatting
- 🌐 **Web Integration** - Real-time web search capabilities
- 🎤 **Voice Input** - Hands-free operation support
- 💾 **Context Memory** - ChromaDB integration for conversation persistence

## 🚀 Quick Installation

### Option 1: Windows Installer (Recommended)

1. Download the installer from [NEXUS-AI.io](https://kunjshah95.github.io/NEXUS-AI.io/)
2. Run `nexus-ai-installer.bat` as administrator
3. Follow the automated setup process
4. Edit the generated `.env` file with your API keys
5. Run `python main.py` to start

### Option 2: Linux/macOS Installer

1. Download and run the shell script for your OS:
   - **Linux:** `install.sh`
   - **macOS:** `install_mac.sh`
2. Follow the prompts to complete setup
3. Edit the generated `.env` file with your API keys
4. Run `python main.py` to start

### Option 3: Manual Installation

```bash
# Clone the repository
git clone https://github.com/KunjShah95/NEXUS-AI.io.git
cd NEXUS-AI.io/terminal

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your API keys

# Run the application
python main.py
```

## 🔑 API Keys Setup

Create a `.env` file in the terminal directory with your API keys:

```env
# Google Gemini API Key (Primary)
# Get from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_gemini_key_here
GEMINI_API_KEY=your_gemini_key_here

# Groq API Key (Fast inference)
# Get from: https://console.groq.com/keys
GROQ_API_KEY=your_groq_key_here

# HuggingFace API Key (Optional)
# Get from: https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY=your_hf_key_here
```

### 🆓 Free Options

- **Ollama**: Install locally from [ollama.ai](https://ollama.ai) - No API key needed
- **DeepSeek**: Free API with limited usage - No registration required

## 🎯 Features

### 🤖 Multi-Model Support
- **Google Gemini 2.0 Flash** - Latest Google AI model (Fixed API)
- **Groq Mixtral 8x7B** - High-performance cloud inference
- **Ollama Models** - Any local model (Llama, CodeLlama, etc.)
- **HuggingFace Models** - DialoGPT and other conversational models
- **DeepSeek** - Free OpenAI-compatible API

### 🔒 Security Features
- Input sanitization and validation
- API key validation and secure storage
- Protection against dangerous commands
- Rate limiting and timeout handling

### 🎨 User Experience
- Beautiful terminal UI with Rich library
- Syntax highlighting and formatting
- Progress indicators and status updates
- Error handling with helpful messages

## 📖 Usage Commands

### Basic Commands
```bash
/help              # Show all available commands
/switch gemini     # Switch to Gemini 2.0 Flash model
/switch groq       # Switch to Groq Mixtral model
/switch ollama     # Switch to local Ollama models
/switch openai-free # Switch to free OpenAI-compatible APIs
/clear             # Clear conversation history
/exit              # Exit the application
```

### Advanced Features
```bash
/voice             # Toggle voice input mode
/web <query>       # Perform web search
/memory save       # Save conversation to memory
/memory load       # Load previous conversation
/status            # Show current model and settings
```

## 🛠️ Troubleshooting

### Common Issues

**Python not found**
```bash
# Install Python 3.8+ from python.org
# Make sure to check 'Add Python to PATH'
python --version  # Should show Python 3.8+
```

**Dependencies installation fails**
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

**API key errors**
```bash
# Check your .env file exists and has correct keys
# Verify API keys are valid and have proper permissions
# Try switching to a different model: /switch ollama
```

**Permission errors on Windows**
```bash
# Run Command Prompt as Administrator
# Or use PowerShell with elevated privileges
```

## 📁 Project Structure

```
terminal/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── install.bat         # Windows installer script
├── .env.example        # Environment variables template
├── README.md           # This file
├── SECURITY.md         # Security documentation
└── ai_assistant.log    # Application logs
```

## 🔧 Development

### Requirements
- Python 3.8+
- pip (Python package manager)
- Internet connection for cloud models

### Key Dependencies
- `google-generativeai` - Google Gemini API
- `groq` - Groq cloud inference
- `ollama` - Local model support
- `rich` - Beautiful terminal UI
- `python-dotenv` - Environment variable management
- `requests` - HTTP requests
- `pyyaml` - Configuration management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/KunjShah95/NEXUS-AI.io/issues)
- **Discussions**: [GitHub Discussions](https://github.com/KunjShah95/NEXUS-AI.io/discussions)
- **Website**: [NEXUS-AI.io](https://kunjshah95.github.io/NEXUS-AI.io/)

## 🙏 Acknowledgments

- Google for the Gemini API
- Groq for fast inference capabilities
- Ollama team for local model support
- HuggingFace for model hosting
- Rich library for beautiful terminal UI

---

**Made with ❤️ by [Kunj Shah](https://github.com/KunjShah95)**

🚀 **Happy coding with NEXUS AI!**