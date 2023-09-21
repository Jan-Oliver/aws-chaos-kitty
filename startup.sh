#!/bin/bash
# Startup Script executed on boot of raspi
cd /home/schnidrc/aws-chaos-kitty
source venv/bin/activate
sudo python3 -m src.main


