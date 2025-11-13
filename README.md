# ViratMusicBot 🎵

A simple Telegram Music Bot for groups.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/khantchirag384-cell/virumuscibot)





# ViratMusicBot

Telegram Music Bot — Pyrogram + PyTgCalls starter.

## Quick start (local)
1. Copy `.env.example` to `.env` and fill tokens (locally only).
2. Install deps: `pip install -r requirements.txt`
3. Run: `python main.py`

## Deploy (Heroku)
1. Add ffmpeg buildpack.
2. Set config vars: BOT_TOKEN, API_ID, API_HASH, OWNER_ID, LOG_CHANNEL, etc.
3. Push repo and scale worker dyno.

> **Do NOT** push real tokens to GitHub.
