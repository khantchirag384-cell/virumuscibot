from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.input_stream import InputAudioStream
from yt_dlp import YoutubeDL

import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

bot = Client("musicbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call = PyTgCalls(bot)

@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply("🎵 **Music Bot is alive!**\nUse /play [song name or URL]")

@bot.on_message(filters.command("play") & filters.user(OWNER_ID))
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("Usage: /play song_name_or_url")
    query = " ".join(message.command[1:])
    with YoutubeDL({'format': 'bestaudio'}) as ydl:
        info = ydl.extract_info(query, download=False)
        url = info['url']
    chat_id = message.chat.id
    await call.join_group_call(
        chat_id,
        InputAudioStream(url)
    )
    await message.reply(f"▶️ Playing: **{info['title']}**")

@bot.on_message(filters.command("stop") & filters.user(OWNER_ID))
async def stop(_, message):
    chat_id = message.chat.id
    await call.leave_group_call(chat_id)
    await message.reply("⏹️ Stopped playback")

print("🎧 Music bot started...")
bot.start()
call.start()
bot.idle()

