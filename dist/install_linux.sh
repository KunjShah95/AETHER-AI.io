#!/bin/bash
# AETHER-AI Installation Script for Linux
# This script installs AETHER-AI and its dependencies

set -e  # Exit on error

echo "========================================"
echo "  AETHER-AI Installation for Linux"
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
    echo "Please install Python 3.9 or higher:"
    echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip"
    echo "  Fedora/RHEL: sudo dnf install python3 python3-pip"
    echo "  Arch: sudo pacman -S python python-pip"
    exit 1
fi

echo -e "${GREEN}[INFO]${NC} Python found. Checking version..."
python3 --version

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.9"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}[ERROR]${NC} Python $REQUIRED_VERSION or higher is required (found $PYTHON_VERSION)"
    echo "Please upgrade Python:"
    echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3.9"
    echo "  Fedora/RHEL: sudo dnf install python39"
    exit 1
fi

echo -e "${GREEN}[INFO]${NC} Python version is compatible"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}[WARNING]${NC} pip is not installed"
    echo "Installing pip..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y python3-pip
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3-pip
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3-pip
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm python-pip
    else
        echo -e "${RED}[ERROR]${NC} Unable to install pip automatically"
        echo "Please install pip manually and run this script again"
        exit 1
    fi
fi

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}[WARNING]${NC} Git is not installed"
    echo "You can install it with your package manager:"
    echo "  Ubuntu/Debian: sudo apt install git"
    echo "  Fedora/RHEL: sudo dnf install git"
    echo "  Arch: sudo pacman -S git"
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
    
    # Check for curl or wget
    if command -v curl &> /dev/null; then
        curl -L -o repo.zip https://github.com/KunjShah95/AETHER-AI.io/archive/refs/heads/main.zip
    elif command -v wget &> /dev/null; then
        wget -O repo.zip https://github.com/KunjShah95/AETHER-AI.io/archive/refs/heads/main.zip
    else
        echo -e "${RED}[ERROR]${NC} Neither curl nor wget is installed"
        echo "Please install one of them and run this script again"
        exit 1
    fi
    
    # Check if unzip is installed
    if ! command -v unzip &> /dev/null; then
        echo -e "${RED}[ERROR]${NC} unzip is not installed"
        echo "Please install it:"
        echo "  Ubuntu/Debian: sudo apt install unzip"
        echo "  Fedora/RHEL: sudo dnf install unzip"
        echo "  Arch: sudo pacman -S unzip"
        exit 1
    fi
    
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
python3 -m pip install --upgrade pip --user
echo ""

# Install dependencies
echo -e "${GREEN}[INFO]${NC} Installing dependencies..."
echo "This may take several minutes..."
echo ""

# Check if requirements.txt exists in terminal directory
if [ -f "terminal/requirements.txt" ]; then
    python3 -m pip install -r terminal/requirements.txt --user
elif [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt --user
else
    echo -e "${YELLOW}[WARNING]${NC} No requirements.txt found, installing basic dependencies..."
    python3 -m pip install --user requests PyYAML rich python-dotenv google-generativeai groq ollama
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

# Create symlink in ~/.local/bin if it exists
if [ -d "$HOME/.local/bin" ]; then
    ln -sf "$INSTALL_DIR/launch-aetherai.sh" "$HOME/.local/bin/aetherai"
    echo -e "${GREEN}[INFO]${NC} Created symlink: $HOME/.local/bin/aetherai"
    
    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo -e "${YELLOW}[INFO]${NC} Add $HOME/.local/bin to your PATH by adding this to ~/.bashrc or ~/.zshrc:"
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
elif [ -w "/usr/local/bin" ]; then
    ln -sf "$INSTALL_DIR/launch-aetherai.sh" /usr/local/bin/aetherai
    echo -e "${GREEN}[INFO]${NC} Created symlink: /usr/local/bin/aetherai"
else
    echo -e "${YELLOW}[INFO]${NC} To add AETHER-AI to your PATH, run:"
    echo "  mkdir -p ~/.local/bin"
    echo "  ln -sf $INSTALL_DIR/launch-aetherai.sh ~/.local/bin/aetherai"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\"  # Add to ~/.bashrc or ~/.zshrc"
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
if [ -f "$HOME/.local/bin/aetherai" ] || [ -L "/usr/local/bin/aetherai" ]; then
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
