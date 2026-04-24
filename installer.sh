#!/bin/bash
# GlobalInstaKiller Auto-Installer v2.0

echo "=================================="
echo "🌍 GlobalInstaKiller Installer"
echo "=================================="

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
elif [[ -f "/data/data/com.termux" ]]; then
    OS="termux"
else
    OS="unknown"
fi

echo "Detected: $OS"

# Install packages
case $OS in
    "linux")
        sudo apt update -y
        sudo apt install -y python3 python3-pip tor git curl wget
        ;;
    "termux")
        pkg update -y
        pkg install -y python tor git curl wget
        ;;
    "mac")
        brew install python tor
        ;;
esac

# Python dependencies
pip3 install requests fake-useragent

echo "Starting TOR..."
service tor start 2>/dev/null || tor &

# Permissions
chmod +x GlobalInstaKiller.py

echo "=================================="
echo "✅ Installation Complete!"
echo "Usage: python3 GlobalInstaKiller.py -t target_user -c IN -i 8"
echo "=================================="
