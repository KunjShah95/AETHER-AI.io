#!/bin/bash

# NEXUS AI Terminal Assistant - Linux Installer v3.0
# Enhanced installation script for Linux

set -e

echo "=========================================="
echo "  NEXUS AI Terminal Assistant v3.0"
echo "  Linux Installation Script"
echo "=========================================="
echo

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "[ERROR] This script is for Linux only"
    exit 1
fi

# Check if Python is installed
echo "[1/6] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo
    echo "Please install Python 3.8+ using your package manager:"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "Arch: sudo pacman -S python python-pip"
    echo
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [[ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]]; then
    echo "[ERROR] Python $PYTHON_VERSION detected. Python $REQUIRED_VERSION+ required."
    exit 1
fi

echo "[INFO] Python $PYTHON_VERSION found"

# Check if pip is installed
echo "[2/6] Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    echo "[ERROR] pip3 is not installed"
    echo
    echo "Please install pip3 and rerun this script"
    echo
    exit 1
fi

# Install dependencies
echo "[3/6] Installing dependencies..."
pip3 install -r requirements.txt

# Copy .env.example if .env does not exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "[INFO] .env file created. Please add your API keys."
fi

# Make main.py executable
chmod +x main.py

echo
echo "=========================================="
echo "Installation complete!"
echo "Run: python3 main.py"
echo "=========================================="
