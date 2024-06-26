# Requier Moudles 
from pyrogram import Client, types, filters ,enums
import asyncio
import binascii
import struct
# Requier Helpers and Plugins 
from config import jsdata
from helpers import Message, Keyboard
from Plugins.functions import SessionsPlugins, apis


# BACK 
@Client.on_callback_query(filters.regex('^BACK_ADMIN$'))
async def BACK_ADMIN(app: Client, query: types.CallbackQuery):
    userscount = jsdata.GET_USERSCOUNT()
    sessionscount = jsdata.GET_DATA()['statistics']['sessions']
    await app.edit_message_text(
        chat_id=query.message.chat.id, message_id=query.message.id ,
        text=Message.ADMIN_MESSAGE['HOME'], 
        reply_markup=Keyboard.ADMIN_KEYBOARD.PANEL(userscount, sessionscount)
    )


# On Callback Crovet 
@Client.on_callback_query(filters.regex('^ADMIN_BROADCASTING$'))
async def ADMIN_BROADCASTING(app: Client, query: types.CallbackQuery):
    await app.edit_message_text(
        chat_id=query.message.chat.id, message_id=query.message.id ,
        text=Message.ADMIN_MESSAGE['BROADCASTING']
    )
    # on listing 
    response = await app.listen(
        chat_id=query.message.chat.id, 
        user_id=query.from_user.id,
          filters=filters.text,timeout=20
        )
    broad_message = response.text
    
    # check message  and start broadcasting
    USERS_IDS = jsdata.GET_DATA()['users'].keys()
    message_with = await app.send_message(
        chat_id=query.message.chat.id,
        text=Message.ADMIN_MESSAGE['START_BROADCASTING'].format(0,0, 'Looding'),
        reply_markup=Keyboard.ADMIN_KEYBOARD.BACK()

    )
    # start loops
    Trues, Falses = 0, 0
    for usersid in USERS_IDS:
        try:
            await app.send_message(
                chat_id=int(usersid), 
                text=broad_message, 
            ) 
            Trues+=1
            await app.edit_message_text(
                chat_id=query.message.chat.id,message_id=message_with.id,
                text=Message.ADMIN_MESSAGE['START_BROADCASTING'].format(Trues,Falses ,'Startings')
            )
        except Exception as Err:
            print(Err)
            Falses+=1
            await app.edit_message_text(
                chat_id=query.message.chat.id,message_id=message_with.id,
                text=Message.ADMIN_MESSAGE['START_BROADCASTING'].format(Trues,Falses, 'Startings')
            )

    await app.edit_message_text(
        chat_id=query.message.chat.id,message_id=message_with.id,
        text=Message.ADMIN_MESSAGE['START_BROADCASTING'].format(Trues,Falses, 'Done'),
        reply_markup=Keyboard.ADMIN_KEYBOARD.BACK()
    )




    
