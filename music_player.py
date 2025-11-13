import asyncio
from yt_dlp import YoutubeDL

class Track:
    def __init__(self, title, url, filepath, requester):
        self.title = title
        self.url = url
        self.filepath = filepath
        self.requester = requester

class MusicPlayer:
    def __init__(self, app, pytgcalls):
        self.app = app
        self.pytgcalls = pytgcalls
        self.queues = {}  # chat_id -> list of Track
        self.lock = asyncio.Lock()
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
        }

    async def download(self, query):
        with YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            filename = ydl.prepare_filename(info)
            return info.get('title'), info.get('webpage_url'), filename

    async def play(self, chat_id, query, requester):
        title, url, filepath = await asyncio.get_event_loop().run_in_executor(None, lambda: self.download(query))
        track = Track(title, url, filepath, requester)
        q = self.queues.setdefault(chat_id, [])
        q.append(track)
        # if first track, start playing (very simplified)
        if len(q) == 1:
            await self._start_stream(chat_id, track)

    async def _start_stream(self, chat_id, track: Track):
        # placeholder: integrate pytgcalls join_group_call + ffmpeg process
        print(f"Starting stream in {chat_id}: {track.title}")

    async def skip(self, chat_id):
        q = self.queues.get(chat_id, [])
        if not q:
            return
        q.pop(0)
        if q:
            await self._start_stream(chat_id, q[0])
