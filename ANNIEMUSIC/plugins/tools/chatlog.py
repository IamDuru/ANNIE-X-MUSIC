import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import LOGGER_ID as LOG_GROUP_ID
from ANNIEMUSIC import app 
from pyrogram.errors import RPCError
from typing import Union, Optional
from PIL import Image, ImageDraw, ImageFont
import asyncio, os, aiohttp
from pathlib import Path
from pyrogram.enums import ParseMode

photo = [
    "https://telegra.ph/file/3c9c23857075dcaea5892.jpg",
    "https://telegra.ph/file/f4e58cd6133a033ecd749.jpg",
    "https://telegra.ph/file/e4645653125f3fbe0ad70.jpg",
    "https://telegra.ph/file/cd205021bf40f44ad78e4.jpg",
    "https://telegra.ph/file/05144a16d058f9a7401e5.jpg",
]

@app.on_message(filters.new_chat_members, group=2)
async def join_watcher(_, message):    
    chat = message.chat
    link = await app.export_chat_invite_link(chat.id)
    for member in message.new_chat_members:
        if member.id == app.id:
            count = await app.get_chat_members_count(chat.id)
            msg = (
                f"🌟 **Welcome to Your New Musical Journey!** 🌟\n\n"
f"━━━━━━━ 💫 **The Music Bot Has Arrived!** 💫 ━━━━━━━\n\n"
f"🎤 **Group Name:**\n"
f"   ┗━ 🏷️ `{chat.title}`\n"
f"🆔 **Group ID:**\n"
f"   ┗━ 🆔 `{chat.id}`\n"
f"🔒 **Username:**\n"
f"   ┗━ 🔐 @{chat.username}\n"
f"🌐 **Invite Link:**\n"
f"   ┗━ 🌍 [Tap to Join]({link})\n\n"
f"👥 **Members Count:**\n"
f"   ┗━ 👥 `{count}`\n"
f"🙌 **Added By:**\n"
f"   ┗━ 🙋‍♂️ {message.from_user.mention}\n\n"
f"🎧 **What’s in Store:**\n"
f"   ┏━ 🎵 **Seamless Playback:** Enjoy uninterrupted music.\n"
f"   ┣━ 🔊 **High-Quality Audio:** Crystal-clear sound.\n"
f"   ┣━ 🎶 **Custom Playlists:** Share your own vibes.\n"
f"   ┗━ 🎯 **Instant Requests:** Play your favorite tracks.\n"
f"🔥 **Exclusive Features:**\n"
f"   ┏━ 🎛️ **Auto DJ Mode:** Let the bot mix the tracks.\n"
f"   ┣━ 🎸 **Genre Selection:** Choose by genre.\n"
f"   ┣━ 🎤 **Karaoke Mode:** Sing along with lyrics.\n"
f"   ┗━ 🎮 **Music Trivia:** Test your knowledge with quizzes.\n\n"
f"✨ **Get Ready to Rock!** ✨\n\n"
f"🎶 **Turn Every Moment into a Musical Experience!** 🎶\n\n"
f"🔊 **Let’s Make the Beats Drop!** 🔊"

            )
            await app.send_photo(LOG_GROUP_ID, photo=random.choice(photo), caption=msg, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"sᴇᴇ ɢʀᴏᴜᴘ👀", url=f"{link}")]
            ]))

@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    if (await app.get_me()).id == message.left_chat_member.id:
        remove_by = message.from_user.mention if message.from_user else "𝐔ɴᴋɴᴏᴡɴ 𝐔sᴇʀ"
        title = message.chat.title
        username = f"@{message.chat.username}" if message.chat.username else "𝐏ʀɪᴠᴀᴛᴇ 𝐂ʜᴀᴛ"
        chat_id = message.chat.id
        left = f"✫ <b><u>#𝐋ᴇғᴛ_𝐆ʀᴏᴜᴘ</u></b> ✫\n\n𝐂ʜᴀᴛ 𝐓ɪᴛʟᴇ : `{title}`\n\n𝐂ʜᴀᴛ 𝐈ᴅ : `{chat_id}`\n\n𝐑ᴇᴍᴏᴠᴇᴅ 𝐁ʏ : `{remove_by}`\n\n𝐁ᴏᴛ : @{app.username}"
        await app.send_photo(LOG_GROUP_ID, photo=random.choice(photo), caption=left)
        
