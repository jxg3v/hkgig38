from pyrogram import Client as app , filters, types 

# Requier Helpers and plugin bot .
from config import Config,jsdata
from helpers import Message, Keyboard
from Plugins.functions import apis

# admin start [/admin]
@app.on_message(filters.regex('^/admin$') & filters.private)
async def ADMIN_PANL(app: app, message :types.Message):
    if message.from_user.id != Config.SUDO:
        return
    userscount = jsdata.GET_USERSCOUNT()
    sessionscount = jsdata.GET_DATA()['statistics']['sessions']
    await app.send_message(
        chat_id=message.chat.id,
        text=Message.ADMIN_MESSAGE['HOME'],
        reply_markup=Keyboard.ADMIN_KEYBOARD.PANEL(userscount, sessionscount)
    )