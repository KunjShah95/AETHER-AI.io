#!/bin/bash
# NEXUS AI macOS Installer
set -e

echo "\nNEXUS AI macOS Installer\n========================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python 3.9+ and rerun this script."
    exit 1
fi

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Please install pip3 and rerun this script."
    exit 1
fi

# Install dependencies
pip3 install -r requirements.txt

# Copy .env.example if .env does not exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env file created. Please add your API keys."
fi

echo "\nInstallation complete!"
echo "Run: python3 main.py"
