from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ANNIEMUSIC import app
from config import BOT_USERNAME

start_txt = """**
          ✪ 𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐅𝐨𝐫 𝐃𝐮𝐫𝐮'𝐬 𝐑𝐞𝐩𝐨 ✪
 
 ➲ ᴀʟʟ ʀᴇᴘᴏ ᴇᴀ𝐬ɪʟʏ ᴅᴇᴘʟᴏʏ ᴏɴ ʜᴇʀᴏᴋᴜ ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ᴇʀʀᴏʀ ✰
 
 ➲ ɴᴏ ʜᴇʀᴏᴋᴜ ʙᴀɴ ɪ𝐬𝐬ᴜᴇ ✰
 
 ➲ ɴᴏ ɪᴅ ʙᴀɴ ɪ𝐬𝐬ᴜᴇ ✰
 
 ➲ᴜɴʟɪᴍɪᴛᴇᴅ ᴅʏɴᴏ𝐬 ✰
 
 ➲ ʀᴜɴ 24𝐱7 ʟᴀɢ ғʀᴇᴇ ᴡɪᴛʜᴏᴜᴛ 𝐬ᴛᴏᴘ ✰
 
 ► ɪғ ʏᴏᴜ ғᴀᴄᴇ ᴀɴʏ ᴘʀᴏʙʟᴇᴍ ᴛʜᴇɴ 𝐬ᴇɴᴅ 𝐬𝐬
**"""




@app.on_message(filters.command("repo", prefixes=["/", ".", "!"]))
async def start(_, msg):
    buttons = [
     
            [ 
            InlineKeyboardButton("sɴᴀᴛᴄʜ ᴍᴇ ʙᴀʙᴇs✪", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ],
     
            [
             InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/OfficialDurgesh"),
             InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/senpaibotmanagement"),
             ],
     
             [
             InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ", url="https://t.me/TheTeamVk"),          
             InlineKeyboardButton("︎ʀᴇᴘᴏ ʟɪɴᴋ", "😈APHLE JAKE DURU KO PAPA BOL😈"),
             ],
     
              ]
 
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo="https://telegra.ph/file/bf017a515fbb6a58148e5.jpg",
        caption=start_txt,
        reply_markup=reply_markup
    )
