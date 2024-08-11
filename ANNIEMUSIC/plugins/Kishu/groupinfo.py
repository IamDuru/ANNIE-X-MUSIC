from pyrogram import Client, filters
from pyrogram.types import Message
from ANNIEMUSIC import app

@app.on_message(filters.command("groupinfo", prefixes=["/", ".", "!"]))
async def get_group_status(_, message: Message):
    if len(message.command) != 2:
        await message.reply("Please provide a group username. Example: /groupinfo YourGroupUsername")
        return
    
    group_username = message.command[1]
    
    try:
        group = await app.get_chat(group_username)
    except Exception as e:
        await message.reply(f"Error: {e}")
        return
    
    total_members = await app.get_chat_members_count(group.id)
    group_description = group.description or 'N/A'
    group_created_at = group.date if group.date else 'Unknown'
    privacy_settings = "Private" if group.is_private else "Public"
    theme_color = "Default"  # Example: could be retrieved or set based on custom logic
    
    # Calculate additional metrics if necessary
    premium_acc = banned = deleted_acc = bot = 0
    async for member in app.iter_chat_members(group.id):
        if member.user.is_deleted:
            deleted_acc += 1
        if member.user.is_bot:
            bot += 1
        if member.privileges and member.privileges.is_banned:
            banned += 1
        if member.user.is_premium:
            premium_acc += 1

    # Check if the group has a username and format accordingly
    if group.username:
        username_text = f"@{group.username}"
    else:
        username_text = "None"

    # Create the formatted message
    response_text = (
        "╔════════════════════════════════════════════╗\n"
        "║          🚀 GROUP INFORMATION 🚀          ║\n"
        "╠════════════════════════════════════════════╣\n"
       f"║ 📌 GROUP NAME: {group.title} ✅\n"
       f"║ 🆔 GROUP ID: {group.id}\n"
       f"║ 👥 TOTAL MEMBERS: {total_members}\n"
       f"║ 🤖 BOTS: {bot}\n"
       f"║ 🛡 BANNED MEMBERS: {banned}\n"
       f"║ 👻 DELETED ACCOUNTS: {deleted_acc}\n"
       f"║ ⭐️ PREMIUM MEMBERS: {premium_acc}\n"
        "╠════════════════════════════════════════════╣\n"
       f"║ 📝 DESCRIPTION: \n"
       f"║    {group_description}\n"
        "╠════════════════════════════════════════════╣\n"
       f"║ 📱 USERNAME: {username_text}\n"
       f"║ 🕒 CREATED AT: {group_created_at}\n"
        "╠════════════════════════════════════════════╣\n"
       f"║ 🔒 PRIVACY SETTINGS: {privacy_settings}\n"
       f"║ 🎨 THEME COLOR: {theme_color}\n"
        "╚════════════════════════════════════════════╝\n\n"
        f"✨ Thank you for being part of our community! ✨"
    )
    
    await message.reply(response_text)

# Command handler to get group status
@app.on_message(filters.command("status") & filters.group)
def group_status(client, message):
    chat = message.chat  # Chat where the command was sent
    status_text = (
        f"Group ID: {chat.id}\n"
        f"Title: {chat.title}\n"
        f"Type: {chat.type}\n"
    )
                  
    if chat.username:  # Not all groups have a username
        status_text += f"Username: @{chat.username}"
    else:
        status_text += "Username: None"

    message.reply_text(status_text)
