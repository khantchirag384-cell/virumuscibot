from pyrogram import Client

async def is_owner(app: Client, user_id: int, owner_id: int) -> bool:
    return user_id == owner_id
