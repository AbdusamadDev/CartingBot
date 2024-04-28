#!/bin/bash
cd /srv/project/carting.uz-bot/
source .venv/bin/activate
pip install -r requirements.txt
sudo chown -R www-data:www-data /srv/project/carting.uz-bot
sudo systemctl restart carding.bot.service
