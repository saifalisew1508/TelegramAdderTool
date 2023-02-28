import asyncio
import json, os
from pyrogram import Client, enums 
from pyrogram.errors import YouBlockedUser, UserDeactivatedBan, UserAlreadyParticipant, RPCError, FloodWait, ChatAdminRequired, PeerFlood, PeerIdInvalid, UserIdInvalid, UserPrivacyRestricted, UserRestricted, ChannelPrivate, UserNotMutualContact, PhoneNumberBanned, UserChannelsTooMuch, UserKicked
from pathlib import Path
from datetime import datetime, timedelta
import logging
import random
from helper.logs import log
def get_device():
    with open(Path('helper/device.json'), 'r', encoding='utf-8') as f:
        device_data = json.load(f)
        device_data = random.choice(device_data)
        device_model = device_data['device_model']
        system_version = device_data['system_version']
        return [device_model, system_version]

async def create(phone, api_id, api_hash):
    PYRO = log('PYRO-Signup')
    PYRO.propagate = False
    DATA = get_device()
    device_model = DATA[0]
    system_version = DATA[1]

    try:
        async with Client(phone, api_id, api_hash, workdir='session', app_version='7.9.2',
                                device_model=device_model, system_version=system_version, lang_code='en') as app:
            if await app.get_me():
                PYRO.info(f'{phone} is logined')
    except Exceptionas as e:
        PYRO.info(f'{e}')

async def login(phone, api_id, api_hash, auto_join, group_source_id,  group_target_id):
    # create logger
    PYRO = log('PYRO-Login')
    PYRO.propagate = False
    try:
        async with Client(phone, api_id, api_hash, workdir='session')as app:
            if await app.get_me():
                PYRO.info(f'{phone} is logined')
                if auto_join is True:
                    try:
                        await app.join_chat(group_source_id)
                    except UserAlreadyParticipant:
                        await app.get_chat(group_source_id)
                    except BaseException as e:
                        PYRO.info("could not join maybe already in source group")

                    try:
                        await app.join_chat(group_target_id)
                    except UserAlreadyParticipant:
                        pass
                    except BaseException as e:
                        PYRO.info("could not join maybe already in target group")
                else:
                    PYRO.info('auto join is off check config')
                await asyncio.sleep(.1)
            else:
                PYRO.info(phone, 'login failed')
    except UserDeactivatedBan:
        PYRO.info(f'account deleted {phone}')
    except BaseException as e:
        PYRO.info(f'error : {e}')
