#!/bin/bash
# AETHER-AI Installation Script for macOS
# This script installs AETHER-AI and its dependencies

set -e  # Exit on error

echo "========================================"
echo "  AETHER-AI Installation for macOS"
echo "========================================"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python 3 is not installed"
    echo "Please install Python 3.9 or higher from https://www.python.org/downloads/"
    echo "Or use Homebrew: brew install python@3.9"
    exit 1
fi

echo -e "${GREEN}[INFO]${NC} Python found. Checking version..."
python3 --version

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.9"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}[ERROR]${NC} Python $REQUIRED_VERSION or higher is required (found $PYTHON_VERSION)"
    echo "Please upgrade Python from https://www.python.org/downloads/"
    exit 1
fi

echo -e "${GREEN}[INFO]${NC} Python version is compatible"
echo ""

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}[WARNING]${NC} Git is not installed"
    echo "You can install it with: xcode-select --install"
    echo "Or with Homebrew: brew install git"
    echo "Installation will continue without Git..."
    HAS_GIT=0
else
    echo -e "${GREEN}[INFO]${NC} Git found"
    git --version
    HAS_GIT=1
fi
echo ""

# Create installation directory
INSTALL_DIR="$HOME/AETHER-AI"
echo -e "${GREEN}[INFO]${NC} Installing AETHER-AI to: $INSTALL_DIR"
echo ""

if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}[WARNING]${NC} Installation directory already exists"
    echo "This will update your existing installation"
    echo ""
    read -p "Continue? (Y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled"
        exit 0
    fi
    echo ""
else
    mkdir -p "$INSTALL_DIR"
fi

# Clone or download the repository
cd "$INSTALL_DIR"

if [ $HAS_GIT -eq 1 ]; then
    echo -e "${GREEN}[INFO]${NC} Cloning repository..."
    if [ -d ".git" ]; then
        echo -e "${GREEN}[INFO]${NC} Updating existing repository..."
        git pull origin main || echo -e "${YELLOW}[WARNING]${NC} Failed to update repository"
    else
        git clone https://github.com/KunjShah95/AETHER-AI.io.git .
    fi
else
    echo -e "${GREEN}[INFO]${NC} Downloading repository archive..."
    curl -L -o repo.zip https://github.com/KunjShah95/AETHER-AI.io/archive/refs/heads/main.zip
    unzip -q repo.zip
    mv AETHER-AI.io-main/* .
    mv AETHER-AI.io-main/.* . 2>/dev/null || true
    rm -rf AETHER-AI.io-main
    rm repo.zip
fi

if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR]${NC} Failed to download repository"
    exit 1
fi
echo ""

# Upgrade pip
echo -e "${GREEN}[INFO]${NC} Upgrading pip..."
python3 -m pip install --upgrade pip
echo ""

# Install dependencies
echo -e "${GREEN}[INFO]${NC} Installing dependencies..."
echo "This may take several minutes..."
echo ""

# Install dependencies using pyproject.toml
if [ -f "pyproject.toml" ]; then
    echo -e "${GREEN}[INFO]${NC} Installing from pyproject.toml..."
    python3 -m pip install -e .
else
    echo -e "${YELLOW}[WARNING]${NC} No pyproject.toml found, installing basic dependencies..."
    python3 -m pip install requests PyYAML rich python-dotenv google-generativeai groq ollama
fi

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[WARNING]${NC} Some dependencies failed to install"
    echo "You may need to install them manually"
    echo ""
fi

# Create .env file from example
echo -e "${GREEN}[INFO]${NC} Setting up configuration..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}[INFO]${NC} Created .env file from template"
        echo "Please edit .env and add your API keys"
    elif [ -f "terminal/.env.example" ]; then
        cp terminal/.env.example .env
        echo -e "${GREEN}[INFO]${NC} Created .env file from template"
        echo "Please edit .env and add your API keys"
    fi
else
    echo -e "${GREEN}[INFO]${NC} .env file already exists"
fi
echo ""

# Create launcher script
echo -e "${GREEN}[INFO]${NC} Creating launcher script..."
cat > "$INSTALL_DIR/launch-aetherai.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 terminal/main.py "$@"
EOF
chmod +x "$INSTALL_DIR/launch-aetherai.sh"

# Create symlink in /usr/local/bin if possible
if [ -w "/usr/local/bin" ]; then
    ln -sf "$INSTALL_DIR/launch-aetherai.sh" /usr/local/bin/aetherai
    echo -e "${GREEN}[INFO]${NC} Created symlink: /usr/local/bin/aetherai"
else
    echo -e "${YELLOW}[INFO]${NC} To add AETHER-AI to your PATH, run:"
    echo "  sudo ln -sf $INSTALL_DIR/launch-aetherai.sh /usr/local/bin/aetherai"
fi
echo ""

echo "========================================"
echo "  Installation Complete!"
echo "========================================"
echo ""
echo "Installation directory: $INSTALL_DIR"
echo ""
echo "To start AETHER-AI:"
echo "  1. Edit $INSTALL_DIR/.env and add your API keys"
echo "  2. Run: $INSTALL_DIR/launch-aetherai.sh"
if [ -L "/usr/local/bin/aetherai" ]; then
    echo "  Or simply: aetherai"
fi
echo "  Or: cd $INSTALL_DIR && python3 terminal/main.py"
echo ""
echo "To get API keys:"
echo "  - Gemini: https://makersuite.google.com/app/apikey"
echo "  - Groq: https://console.groq.com/keys"
echo "  - HuggingFace: https://huggingface.co/settings/tokens"
echo "  - OpenAI: https://platform.openai.com/api-keys"
echo ""
echo "For more information, see README.md in the installation directory"
echo ""
