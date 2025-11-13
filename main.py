import os
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from music_player import MusicPlayer
from helpers import is_owner

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
LOG_CHANNEL = os.getenv("LOG_CHANNEL")

app = Client("bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)
pytg = PyTgCalls(app)
player = MusicPlayer(app, pytg)

@app.on_message(filters.command("start") & filters.private)
async def start(_, message: Message):
    text = f"👋 Hi {message.from_user.first_name}!\nOwner: `{OWNER_ID}`"
    await message.reply_text(text)

@app.on_message(filters.command("profile") & filters.private)
async def profile(_, message: Message):
    user = message.from_user
    text = f"Name: {user.first_name}\nUsername: @{user.username if user.username else '—'}\nID: `{user.id}`"
    await message.reply_text(text)

@app.on_message(filters.command("play") & (filters.group | filters.channel))
async def play(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /play <youtube link or search query>")
    query = " ".join(message.command[1:])
    await message.reply_text(f"Searching for: {query}")
    await player.play(message.chat.id, query, requester=message.from_user.id)

@app.on_message(filters.command("skip") & (filters.group | filters.channel))
async def skip(_, message: Message):
    allowed = await is_owner(app, message.from_user.id, OWNER_ID)
    if not allowed:
        return await message.reply_text("Only owner can use this command.")
    await player.skip(message.chat.id)
    await message.reply_text("Skipped current track.")

if __name__ == "__main__":
    app.start()
    pytg.start()
    print("Bot started")
    from pyrogram import idle
    idle()
    pytg.stop()
    app.stop()
