import asyncio
import json
import os
from pyrogram import Client, enums
from pyrogram.errors import YouBlockedUser, UserDeactivatedBan, FloodWait, ChatAdminRequired, PeerFlood, PeerIdInvalid, UserIdInvalid, UserPrivacyRestricted, UserRestricted, ChannelPrivate, UserNotMutualContact, PhoneNumberBanned, UserChannelsTooMuch, UserKicked
from pathlib import Path
from datetime import datetime, timedelta
import logging
from helper.logs import log


async def addlogin(config, gp_s_id):
    # create logger
    PYRO = log('PYRO-LOGIN')
    PYRO.propagate = False
    # login starthere
    applist = []
    for account in config:
        phone = account["phone"]
        app = Client(
            phone,
            api_id=account["api_id"],
            api_hash=account["api_hash"],
            workdir="session")
        try:
            await app.start()
        except UserDeactivatedBan:
            PYRO.info(f"{phone} has been removed from telegram")
            continue
        except BaseException as e:
            PYRO.info(f"{e} Share this error to @PublicSource_Chat on telegram")
            continue
        check = await app.get_me()
        try:
            spam = config["spam_check"]
        except BaseException:
            spam = False
        if check:
            PYRO.info(f'{phone} login sucess')
            # print('\n',account["phone"], 'login sucess')
            # applist.append({'phone': phone, 'app': app})
            if spam:
                try:
                    messegespam = await app.send_message('@spambot', '/start')
                    messget = await app.get_messages('@spambot', message_ids=(int(messegespam.id) + 1)).text
                    listofnum = [
                        'sorry']
                    checktext = [x for x in listofnum if (x in messget)]
                    if checktext:
                        PYRO.info(
                            f'{phone} is limited or disabled! will no be used for this RUN')
                    else:
                        applist.append({'phone': account["phone"], 'app': app})
                except (BaseException, YouBlockedUser):
                    PYRO.info(f'could not perform spam test on this {phone}')
                    applist.append({'phone': account["phone"], 'app': app})
            else:
                try: 
                    await app.get_chat(gp_s_id)
                    applist.append({'phone': account["phone"], 'app': app})
                except:
                    PYRO.info(f"{phone} has not joined source chat or RUN get_data.py")
                
        else:
            PYRO.info(f'{phone} login failed')
            await asyncio.sleep(1)
    return applist
