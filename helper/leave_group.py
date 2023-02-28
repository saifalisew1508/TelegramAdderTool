import asyncio
import json, os
from pyrogram import Client, enums 
from pyrogram.errors import YouBlockedUser, RPCError, FloodWait, ChatAdminRequired, PeerFlood, PeerIdInvalid, UserIdInvalid, UserPrivacyRestricted, UserRestricted, ChannelPrivate, UserNotMutualContact, PhoneNumberBanned, UserChannelsTooMuch, UserKicked
from pathlib import Path
from datetime import datetime, timedelta
import logging
from helper.logs import log
async def leave(phone, api_id, api_hash, group_source_id):
    # create logger
    PYRO = log('PYRO-Login-Signup')
    PYRO.propagate = False
    async with Client(phone, api_id, api_hash, workdir='session')as app:
        if await app.get_me():
            PYRO.info(f'{phone} is logined')
            try:
                await app.leave_chat(group_source_id)
            except BaseException as e:
                    PYRO.info("could not Leave source group")
            await asyncio.sleep(.1)
        else:
            PYRO.info(phone, 'login failed')
async def leave2(phone, api_id, api_hash, group_source_id,  group_target_id):
    # create logger
    PYRO = log('PYRO-Login-Signup')
    PYRO.propagate = False
    async with Client(phone, api_id, api_hash, workdir='session')as app:
        if await app.get_me():
            PYRO.info(f'{phone} is logined')
            try:
                await app.leave_chat(group_source_id)
            except BaseException as e:
                    PYRO.info("could not Leave source group")
            try:
                await app.leave_chat(group_target_id)
            except BaseException as e:
                PYRO.info("could not leave target group")
            await asyncio.sleep(.1)
        else:
            PYRO.info(phone, 'login failed')

