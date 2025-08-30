# 🚀 NEXUS AI Terminal Assistant

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://kunjshah95.github.io/NEXUS-AI.io/)
[![Version](https://img.shields.io/badge/Version-3.0.1-blue)](https://github.com/KunjShah95/NEXUS-AI.io/releases)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://python.org)

---

## Professional, Scalable, Next-Gen AI Terminal Assistant

NEXUS AI Terminal Assistant is a professional, multi-model AI terminal application. It brings seamless, secure, and powerful natural language AI to your command line, supporting Google Gemini, Groq, Ollama, HuggingFace, DeepSeek, and more. With robust security, voice input, web search, and an intuitive UI, NEXUS is your all-in-one AI companion for productivity and research.

---

## ✨ Features at a Glance

- **Multi-Model AI**: Effortlessly switch between Google Gemini, Groq Mixtral, Ollama local models, HuggingFace, and DeepSeek.
- **Security First**: Comprehensive input validation, API key encryption, and command safety.
- **Voice Interaction**: State-of-the-art speech-to-text and voice command support.
- **Web Search**: Integrated real-time web search for up-to-date information.
- **Contextual Memory**: Persistent conversation memory with ChromaDB.
- **Beautiful UI**: Modern terminal interface powered by Rich, with status indicators and helpful banners.
- **Cross-Platform**: Runs on Windows, Mac, Linux. Docker support included.
- **Open Source & Extensible**: MIT-licensed, modular codebase ready for your contributions.

---

## 🚀 Quick Start

### 1. Install Python 3.9+

Download from [python.org](https://python.org), and ensure it's added to your PATH.

### 2. Download & Install (All Platforms)

- **Windows:** Use the Windows installer or run the setup script.
- **Linux:** Download and run the provided shell script (`install.sh`).
- **macOS:** Download and run the provided shell script (`install_mac.sh`).

Or clone the repo manually:

```bash
git clone https://github.com/KunjShah95/NEXUS-AI.io.git
cd NEXUS-AI.io/terminal
pip install -r requirements.txt
cp .env.example .env    # Configure your API keys as shown below
```

### 3. Configure API Keys

- **Google Gemini**: [Get key](https://makersuite.google.com/app/apikey)
- **Groq**: [Get key](https://console.groq.com/keys)
- **HuggingFace**: [Get token](https://huggingface.co/settings/tokens)
- **Ollama**: [Install locally](https://ollama.ai) (no key needed)
- **DeepSeek**: Free, no key required

Edit your `.env`:

```
GEMINI_API_KEY=...
GROQ_API_KEY=...
HUGGINGFACE_TOKEN=...
```

### 4. Launch

```bash
python main.py
```

---

## 📊 Stats

- **Downloads:** 0 (GitHub launch)
- **AI Models Supported:** 8+

---

## 🖥️ Core Commands

| Command                  | Description                              | Example                               |
|--------------------------|------------------------------------------|---------------------------------------|
| Just ask                 | Natural language question                | `What is quantum computing?`          |
| `/help`                  | Show command help                        | `/help`                               |
| `/switch <model>`        | Change the active AI model               | `/switch gemini`                      |
| `/voice`                 | Activate voice input                     | `/voice`                              |
| `/web <query>`           | Search the web                           | `/web latest AI news`                 |
| `/clear`                 | Clear the terminal                       | `/clear`                              |
| `/exit`                  | Exit NEXUS AI                            | `/exit`                               |
| `/status [-v]`           | Show system/model status                 | `/status -v`                          |
| `/models`                | List available AI models                 | `/models`                             |
| `/memory save`           | Save conversation to memory              | `/memory save`                        |
| `/memory load`           | Load previous conversation               | `/memory load`                        |

---

## 📖 Advanced Usage Guide

### � Interactive Development

**Code Generation:**

```bash
/generate function calculate_fibonacci
/generate class UserManager
/generate module database_utils
```

**Code Review:**

```bash
/review my_code.py
/review --style pep8
/review --security
```

**Debugging:**

```bash
/debug error_message
/debug --trace
/debug --suggest
```

### �🧠 Advanced AI Features

**Context-Aware Commands:**

```bash
/learn pattern recursion
/suggest optimization
/remind deadline
/analyze project
```

**Model Switching:**

```bash
/switch gemini
/switch groq
/switch ollama
/status
```

### 🎮 Games & Learning

**Coding Challenges:**

```bash
/challenge python
/challenge --difficulty hard
/challenge --topic algorithms
```

**Tutorials:**

```bash
/tutorial ai_basics
/tutorial python_advanced
/tutorial --interactive
```

**Quizzes:**

```bash
/quiz programming
/quiz ai_concepts
/achievements
```

### 🎨 Creative Tools

**ASCII Art:**

```bash
/ascii "Hello World"
/ascii --style block
/ascii --width 80
```

**Color Schemes:**

```bash
/colors generate
/colors preview
/colors export
```

**Story Generation:**

```bash
/story adventure
/story --genre sci-fi
/story --length short
```

### 🔒 Security Features

**Encryption:**

```bash
/encrypt "secret message"
/decrypt encrypted_text
/rotate_keys
```

**Authentication:**

```bash
/biometric enroll
/biometric verify
/threat_scan
```

### 📊 Analytics & Monitoring

**Usage Tracking:**

```bash
/analytics dashboard
/analytics productivity
/analytics trends
```

**System Monitoring:**

```bash
/monitor health
/monitor network
/monitor performance
```

### 🔧 Advanced Commands

**Multi-language Support:**

```bash
/translate python javascript
/refactor --language java
/polyglot analyze
```

**Collaboration:**

```bash
/share code_snippet
/review request
/workspace create
```

**External Tools:**

```bash
/git status
/docker ps
/database connect
```

## ⚙️ Configuration

Create a `config.yaml` file for advanced settings:

```yaml
# AI Model Configuration
models:
  primary: gemini
  fallback: groq
  local: ollama

# Security Settings
security:
  encryption: enabled
  key_rotation: 30d
  threat_detection: enabled

# Analytics
analytics:
  enabled: true
  retention: 90d
  export_format: json

# Learning
games:
  difficulty: medium
  achievements: enabled
  tutorials: interactive
```

## 🔧 Complete Command Reference

| Category | Command | Description |
|----------|---------|-------------|
| **Development** | `/generate` | Generate code snippets |
| | `/review` | Code review and analysis |
| | `/debug` | Debug assistance |
| | `/refactor` | Code refactoring |
| | `/docs` | Documentation generation |
| **AI** | `/switch` | Switch AI models |
| | `/learn` | Learn patterns |
| | `/suggest` | Get suggestions |
| | `/analyze` | Project analysis |
| **Creative** | `/ascii` | ASCII art generation |
| | `/colors` | Color scheme design |
| | `/story` | Story generation |
| | `/music` | Music pattern creation |
| **Games** | `/challenge` | Coding challenges |
| | `/tutorial` | Interactive tutorials |
| | `/quiz` | Knowledge quizzes |
| | `/achievements` | View achievements |
| **Security** | `/encrypt` | Message encryption |
| | `/biometric` | Biometric auth |
| | `/threat_scan` | Security scanning |
| **Analytics** | `/analytics` | Usage analytics |
| | `/monitor` | System monitoring |
| **Tools** | `/git` | Git integration |
| | `/docker` | Docker commands |
| | `/database` | Database tools |

## 🎯 Examples

### Generate a Complete Function

```bash
/generate function def fibonacci(n):
```

### Create ASCII Art

```bash
/ascii "NEXUS AI" --style block --width 60
```

### Start a Coding Challenge

```bash
/challenge python --difficulty medium --topic data_structures
```

### Analyze Project

```bash
/analyze current_project --metrics complexity --output json
```

### Generate Story

```bash
/story fantasy --genre adventure --characters hero,mage,dragon --length medium
```

### Monitor System Health

```bash
/monitor health --realtime --alerts enabled
```

---

Switch between any supported provider, including custom Ollama models:

```bash
/switch gemini                # Google Gemini 2.0 Flash
/switch groq                  # Groq Mixtral
/switch ollama                # Ollama local (default model)
/switch ollama:llama2         # Specific Ollama model
/switch deepseek              # DeepSeek (free API)
/switch huggingface           # HuggingFace models
```

---

## 🗣️ Voice Input

Speak directly to your AI assistant:

```bash
/voice
# Wait for the beep, then start speaking...
```

---

## 🌐 Web Search

Get live information from the internet:

```bash
/web What is the latest in generative AI?
```

---

## 📚 Project Structure

```
NEXUS-AI.io/
├── index.html                # Website homepage
├── app.js                    # Website functionality
├── styles.css                # Website styles
├── CHANGELOG.md              # Version history
└── terminal/                 # Main application
    ├── main.py               # Application entrypoint
    ├── requirements.txt      # Dependencies list
    ├── install.bat           # Windows installer
    ├── .env.example          # Environment template
    ├── README.md             # This documentation
    └── SECURITY.md           # Security practices
```

---

## 🛡️ Security & Reliability

- **Input Sanitization**: All user input is validated to block malicious or dangerous commands.
- **API Key Encryption**: Keys are never exposed in logs or errors.
- **Safe Command Execution**: Only whitelisted system commands allowed.
- **Timeouts & Rate Limiting**: Prevents API abuse and accidental loops.
- **Error Logging**: Comprehensive logs for troubleshooting.

---

## 🧩 Advanced Features

### 🤖 Interactive Development Environment

- **Code Generation**: Generate complete functions, classes, and modules with `/generate`
- **Code Review**: Automated code analysis and improvement suggestions with `/review`
- **Debug Assistant**: Intelligent debugging with `/debug` and error analysis
- **Refactoring Tools**: Smart code refactoring with `/refactor`
- **Documentation Generator**: Auto-generate docstrings and comments with `/docs`

### 🧠 Advanced AI Features

- **Context-Aware AI**: Learns from your interactions and provides personalized suggestions
- **Multi-Model Support**: Switch between Google Gemini, Groq, Ollama, and other providers
- **Intelligent Code Completion**: Context-aware code suggestions and auto-completion
- **Pattern Recognition**: Learns coding patterns and applies them to new projects
- **Task Reminders**: Intelligent task tracking and deadline management

---

## 🔮 Roadmap

We’re planning to add:

- Automated Testing & CI
- Linting & Code Quality
- Plugin/Extension System
- User Configuration File
- Enhanced Logging
- Usage Analytics (opt-in)
- Accessibility
- More AI Integrations
- Export/Import Conversations
- In-app Update Checker
- Multi-language Support
- Theme Customization (dark/light mode)


Have ideas? [Open an issue](https://github.com/KunjShah95/NEXUS-AI.io/issues) or join the discussion!

---

## 📝 Troubleshooting

<details>
<summary><b>Click for common issues & solutions</b></summary>

### Python Not Found

- Install Python 3.9+ from [python.org](https://python.org)
- Ensure it's in your PATH: `python --version`

### Dependency Issues

```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### API Key Errors

- Verify `.env` file exists and is correct.
- Check key validity and permissions.
- Try a different model: `/switch ollama`

### Voice/Audio Errors

- Install PyAudio: `pip install pyaudio`
- On Windows, you may need Visual C++ Build Tools.

### ChromaDB/Memory Issues

- Ensure you have disk space and correct permissions.
- Delete corrupted DB files if necessary.

</details>

---

## 🛠️ Development & Contribution

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md):

1. **Fork** this repo
2. **Create a branch**: `git checkout -b feature/your-feature`
3. **Commit & push**: `git commit -am 'Add feature'`; `git push origin feature/your-feature`
4. **Open a PR**: Describe your changes and link related issues

---

## 📜 License

MIT License – see [LICENSE](LICENSE)

---

## 🙏 Acknowledgements

- [Google Generative AI](https://ai.google.dev/)
- [Groq](https://groq.com/)
- [Ollama](https://ollama.ai/)
- [HuggingFace](https://huggingface.co/)
- [DeepSeek](https://deepseek.com/)
- [Rich](https://github.com/Textualize/rich)
- [ChromaDB](https://www.trychroma.com/)

---

<div align="center">

**Ready to elevate your terminal with next-gen AI?**

[⭐ Star this repo](https://github.com/KunjShah95/NEXUS-AI.io) &nbsp;|&nbsp; [🐛 Report Bug](https://github.com/KunjShah95/NEXUS-AI.io/issues) &nbsp;|&nbsp; [✨ Request Feature](https://github.com/KunjShah95/NEXUS-AI.io/issues)

<p>
  <a href="https://twitter.com/KunjShah95"><img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter"></a>
  <a href="https://github.com/KunjShah95"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
</p>

_Made with ❤️ by [Kunj Shah](https://github.com/KunjShah95)_

</div>
