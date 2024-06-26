# Requier Moudles 
from pyrogram import Client, types, filters ,enums
import asyncio
import binascii
import struct
# Requier Helpers and Plugins 
from config import jsdata
from helpers import Message, Keyboard
from Plugins.functions import SessionsPlugins, apis


# On Callback Crovet 
@Client.on_callback_query(filters.regex('^CROVET_PYROGRAM_TELETHON$'))
async def CROVET_PYROGRAM(app: Client, query: types.CallbackQuery):
    # Get Session pyrogram 
    await app.edit_message_text(
        chat_id=query.message.chat.id, message_id=query.message.id,
        text=Message.HOME_MESSAGE['GET_SESSION_STRING'], reply_markup=Keyboard.Keyboards.BACK_HOME()

    )
    # start crovet 
    response = await app.listen(chat_id=query.message.chat.id, user_id=query.from_user.id, filters=filters.text,timeout=20)
    session_Py = response.text
    # with message 
    message_with = await app.send_message(
        chat_id=query.message.chat.id, text=Message.HOME_MESSAGE['WITH_CROVET']
    )
    await asyncio.sleep(0.5)
    # start crovett # Check session 

    
    try :
        SESSION_CROVETT =SessionsPlugins.MangSession.PYROGRAM_TO_TELETHON(session_Py)

    except (binascii.Error, struct.error):
        await app.edit_message_text(
            chat_id=query.message.chat.id, message_id=message_with.id, 
            text=Message.HOME_MESSAGE['ERROR_CROVET_1'], reply_markup=Keyboard.Keyboards.BACK_HOME(), 
        )
        return
    
    status, new_Sessions, session_data = await apis.CHECK_PYROGRAM_SESSIONS(session_Py)
    if not status:
        await app.edit_message_text(
            chat_id=query.message.chat.id, message_id=message_with.id, 
            text=Message.HOME_MESSAGE['ERROR_CROVET_2'], reply_markup=Keyboard.Keyboards.BACK_HOME(), 
        )
        return 
    jsdata.ADD_SESSIONS_CROVET()
    # Done Crovet 
    await app.edit_message_text(
        chat_id=query.message.chat.id, message_id=message_with.id, 
        text=Message.HOME_MESSAGE['DONE_CROVET'].format(session_data.id,session_data.phone_number, session_data.username, session_data.first_name,SESSION_CROVETT), reply_markup=Keyboard.Keyboards.BACK_HOME(), 
        parse_mode=enums.ParseMode.DEFAULT
    )



    