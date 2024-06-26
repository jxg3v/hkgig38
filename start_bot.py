from pyrogram import Client as app , filters, types 

# Requier Helpers and plugin bot .
from config import Config,jsdata
from helpers import Message, Keyboard
from Plugins.functions import apis


@app.on_message(filters.private & filters.regex('^/start$'))
async def ON_START_BOT(app: app, message: types.Message):
    # check user join
    status, channl = await apis.CHECK_JOIN_MEMBER(message.from_user.id, Config.CHANNLS, Config.API_KEY)
    if not status:
        await app.send_message(
            chat_id=message.chat.id, 
            text=Message.HOME_MESSAGE['JOIN_CHAT'].format(channl)
        )
        return 
    if not jsdata.USER_EXISTS(message.from_user.id):
        jsdata.ADD_USER(message.from_user.id)
        await app.send_message(
            chat_id=Config.SUDO, text=Message.ADMIN_MESSAGE['NEWUSER'].format(message.from_user.id, message.from_user.username, message.from_user.first_name, jsdata.GET_USERSCOUNT())
        )
    await app.set_bot_commands([
        types.BotCommand('start', 'بدء  التشغيل ')
    ])
    await app.send_message(
        chat_id=message.chat.id, 
        text=Message.HOME_MESSAGE['HOME'], 
        reply_markup=Keyboard.Keyboards.HOME_KEYBOARD()
    )

