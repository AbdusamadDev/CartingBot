#!/bin/bash
cd /srv/project/carting.uz-bot/
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart carding.bot.service
