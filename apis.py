# Requier Modules 
from pyrogram import Client as PyClient , types, filters
from telethon.sync import TelegramClient, types
from telethon.sessions import StringSession
import requests 
# Requier helper and Plugins 
from config import Config


async def CHECK_PYROGRAM_SESSIONS(sessions: str):
    # client  config 
    app = PyClient(
        name=':memory:', 
        api_id=Config.API_ID, 
        api_hash=Config.API_HASH, 
        session_string=sessions, 
        workers=20, 
        no_updates=True
    )
    # start Client 
    try : 
        await app.start()
    except Exception as Errs: 
        print(f'Errs : {Errs}')
        return (True, None, None)
        
    # get infos 
    new_sessions = await app.export_session_string()
    me = await app.get_me()
    try:
        await app.stop() 
    except: pass
    return (True, new_sessions, me)



async def CHECK_TELETHON_SESSIONS(sessions: str):
    # client config 
    try:
        app = TelegramClient(
            StringSession(sessions),
            api_id=Config.API_ID,
            api_hash=Config.API_HASH
        )
    except Exception as Errs:
        print(f'Errs : {Errs}')
        return (False, None ,None)
    # start Client
    try: 
        await app.start()
    except Exception as Errs:
        print(f'Errs : {Errs}')
        return (True, None, None)
    
    # new_session = await app.
    me = await app.get_me()
    try:
        await app.disconnect()
    except : pass
    
    return (True, None, me)


# CHECK MEMEBER JOIN CHANNLS
async def CHECK_JOIN_MEMBER(user_id: int, channls: list, API_KEY: str):
    """
    user_id : The member telegram id 
    channls : list channls 
    API_KEY : Bot Token
    """
    states = ['administrator','creator','member','restricted']
    # Start Loop
    for channl in channls:
        api =f"https://api.telegram.org/bot{API_KEY}/getChatMember?chat_id=@{channl}&user_id={user_id}"
        respons = requests.get(api).json()
        # Check Status 
        if respons['result']['status'] not in states:
            return (False, channl)
    return (True, None)


        

