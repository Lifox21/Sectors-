#!/usr/bin/env bash
# ==============================================================================
# 1-Click VPS Deployment Script for HMM Continuous Trading Bot
# Works on: Ubuntu 22.04 / 24.04 LTS, Debian 12 (AWS, Oracle, DigitalOcean, etc.)
# ==============================================================================
set -e

echo "[+] Updating system packages..."
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y python3 python3-pip python3-venv git tmux

REPO_DIR="$HOME/Sectors"

if [ ! -d "$REPO_DIR" ]; then
    echo "[+] Cloning repository into $REPO_DIR..."
    git clone https://github.com/Ved-2107/Sectors.git "$REPO_DIR"
fi

cd "$REPO_DIR"

echo "[+] Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

echo "[+] Configuring systemd daemon..."
SERVICE_FILE="/etc/systemd/system/hmm_bot.service"

sudo bash -c "cat << 'EOF' > $SERVICE_FILE
[Unit]
Description=HMM Continuous Quantitative Trading Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$REPO_DIR
ExecStart=/usr/bin/python3 trading_bot.py --loop --interval 60
Restart=always
RestartSec=10
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF"

sudo systemctl daemon-reload
sudo systemctl enable hmm_bot.service
sudo systemctl restart hmm_bot.service

echo "========================================================================"
echo " [SUCCESS] HMM Trading Bot is now running 24/7 in background!"
echo " Status command : sudo systemctl status hmm_bot"
echo " Live logs      : sudo journalctl -u hmm_bot -f"
echo " Stop bot       : sudo systemctl stop hmm_bot"
echo " Restart bot    : sudo systemctl restart hmm_bot"
echo "========================================================================"
