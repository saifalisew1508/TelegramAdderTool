import asyncio
import json, os
import ast
import signal
import sys
import readchar
import platform
from pyrogram import Client, enums 
from pyrogram.errors import YouBlockedUser, RPCError, FloodWait, ChatAdminRequired, PeerFlood, PeerIdInvalid, UserIdInvalid, UserPrivacyRestricted, UserRestricted, ChannelPrivate, UserNotMutualContact, PhoneNumberBanned, UserChannelsTooMuch, UserKicked, UserDeactivatedBan, UsernameNotOccupied, UserBannedInChannel
from pathlib import Path
from helper.applist import addlogin
from datetime import datetime, timedelta
import logging
from helper.logs import log
#  update the py for info
def updatecount(count):
    with open('current_count.py', 'w') as g:
        g.write(str(count))
        g.close()
        

# account rotation

async def add_member(user_id, config, active, method):
    # stop in middle 
    def handler(signum, frame):
        msg = "\033[1;31;48m Ctrl-c OR Ctrl-z was pressed. Do you really want to exit? y/n \033[1;37;48m"
        print(msg)
        res = readchar.readchar()
        if res == 'y':
            updatecount(counterall)
            PYRO.info('Bye!')
            sys.exit()
        else:
            PYRO.info(f'Okay then i will continue')
    # create logger
    PYRO = log('PYRO-Adder')
    PYRO.propagate= False
    #check if need continue
    try:
        with open('current_count.py') as f:
            data = f.read()       
            counterall = ast.literal_eval(data)    
            counter = counterall["counter"]
            added2 = counterall["added"]
            skipped2  = counterall['skipped']
            privacy2  = counterall['privacy']
            uc2  = counterall['already in too many channel/group']
    except:
            
            counter = added2 = privacy2 = uc2 = skipped2 =  0

    chat_idt = int(str(-100) +str(config['group_target']))
    g_s_id = int(str(-100) +str(config['group_source']))

    # all zero value avar initali
    added = skipped = privacy = uc = um = bot = noname = osr = 0
    try:
        waittime = config["wait_time"]
    except:
        waittime = 10

    # single function for sleep and time logger.info
    async def prints():
        updatecount(counterall)
        wait_time = str(waittime / len(applist))
        wait_time_rounded = round(float(wait_time))
        PYRO.info(f'sleep: {wait_time_rounded}')
        await asyncio.sleep(waittime / len(applist))
    #single line f string for printinf final output
    def printfinal():
        print(f"{added} : members were added\n {skipped} : members were skipped\n {privacy} : members had privacy enable or not in mutual contact\n {uc} : already in too many channel/group\n {um} : members not in mutual contat\n {bot}:  bot accont skipped")
        if method == 'username':
            PYRO.info(f"{noname} : accont has no usernames")
        updatecount(counterall)
        print(datetime.now().strftime("%H:%M:%S"))
    total_account = len(config['accounts'])
    PYRO.info(f'Total account trying to login \033[1;32;48m{total_account}\033[1;37;48m')
    await asyncio.sleep(.2)
    applist = await addlogin(config['accounts'], g_s_id)
    logined_account = len(applist)
    PYRO.info(f"Total logined account \033[1;32;48m{logined_account}\033[1;37;48m")
    await asyncio.sleep(1)
    if method[0] == 'u':
        usermethod = "username"
    else:
        usermethod = "userid"
    print(len(user_id), counter)
    # stoer 
    if platform.system() == 'Windows':
        signal.signal(signal.SIGTERM, handler)
        signal.signal(signal.SIGINT, handler)
    else:
        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGTSTP, handler)
    while len(user_id) - counter > 1:
        leftmem = len(user_id) - counter
        counterall = {'counter': int(counter), 
                      'left_to_add': int(leftmem),
                      'added': int(added2) + int(added),
                      'skipped': int(skipped2) + int(skipped),
                      'privacy': int(privacy2) + int(privacy),
                      'already in too many channel/group':int(uc2) + int(uc)}
        for account in applist:
            try:
                if applist == False:
                    printfinal()
                    exit()
                elif added == (30 * len(applist)):
                    printfinal()
                    PYRO.info("Sleeping for 2 hours")

                    now = datetime.now()
                    end = datetime.now() + timedelta(hours=2)
                    print("Sleep started at : ", now.strftime("%H:%M:%S"))
                    print("Sleep End at : ", end.strftime("%H:%M:%S"))
                    added = 0
                    await asyncio.sleep(3600)
                    PYRO.info("1 hour left")
                    await asyncio.sleep(3600)
            except Exception as e:
                            PYRO.info(str(e))
            phone = account['phone']
            app = account['app']
            try:  
                while user_id[counter]["bot"] == True or user_id[counter][usermethod] == 'None' or user_id[counter]["status"] not in active:
                    try:
                        if user_id[counter]["status"] not in active:   
                            counter += 1
                            skipped += 1
                            updatecount(counterall)
                            PYRO.info('Inactive user skipped')
                        if user_id[counter]["bot"] == True:
                            counter += 1
                            bot += 1
                            updatecount(counterall)
                            PYRO.info("bot skipped")
                        if user_id[counter][usermethod] == 'None':
                            counter += 1
                            noname += 1
                            updatecount(counterall)
                            PYRO.info('NO USERNAME found for this user skipped')
                    except:
                        printfinal()
                        PYRO.info("Finished")
            except:
                printfinal()
                PYRO.info("Finished")
            try:
                position = applist.index(account)
                current_user = user_id[counter]["userid"]
                position2 = len(applist)
#                PYRO.info(f"trying to add {current_user} by : {phone} account-position : {position + 1} / {position2}")
                PYRO.info(f"Adding: \033[1;32;48m{current_user}\033[1;37;48m by: \033[1;32;48m{phone}\033[1;37;48m \033[1;32;48m - Added successfull\033[1;37;48m - Account: {position + 1}/{position2}")
                await app.add_chat_members(chat_id=chat_idt, user_ids=user_id[counter][usermethod])
#                PYRO.info(f"{current_user} added success")
                counter += 1
                added += 1
                await prints()
            except UserBannedInChannel: 
                await app.stop()
                applist.remove(account)  
                PYRO.info(f'Adding: \033[1;32;48m{current_user}\033[1;37;48m by: \033[1;31;48m{phone}\033[1;37;48m \033[1;31;48m - Phone number limited\033[1;37;48m - Account: {position + 1}/{position2}')  
                await prints()
            except UsernameNotOccupied:
                PYRO.info(f"Adding: \033[1;31;48m{current_user}\033[1;37;48m by: \033[1;32;48m{phone}\033[1;37;48m \033[1;31;48m - User not using username anymorewh\033[1;37;48m - Account: {position + 1}/{position2}")
                counter +=1
                await prints()
            except UserDeactivatedBan:
                PYRO.info(f"Adding: \033[1;31;48m{current_user}\033[1;37;48m by: \033[1;32;48m{phone}\033[1;37;48m \033[1;31;48m - User removed from telegram\033[1;37;48m - Account: {position + 1}/{position2}")
                counter +=1
                await prints()
            except UserKicked:
                PYRO.info(f'Adding: \033[1;31;48m{current_user}\033[1;37;48m by: \033[1;32;48m{phone}\033[1;37;48m \033[1;31;48m - This user is banned\033[1;37;48m - Account: {position + 1}/{position2}')
                counter +=1
                await prints()
            except PhoneNumberBanned: 
                await app.stop()
                applist.remove(account)  
                PYRO.info(f'Adding: \033[1;32;48m{current_user}\033[1;37;48m by: \033[1;31;48m{phone}\033[1;37;48m \033[1;31;48m - Phone number banned {phone}\033[1;37;48m - Account: {position + 1}/{position2}')  
                await prints()
            except PeerFlood:
                applist.remove(account)
                await app.stop()
                counter +=1
                PYRO.info(f'Adding: \033[1;32;48m{current_user}\033[1;37;48m by: \033[1;31;48m{phone} Removed for this run\033[1;37;48m - Account: {position + 1}/{position2}')
                try: 
                    await prints()
                except:
                    printfinal()
            except UserChannelsTooMuch:
                counter += 1
                uc += 1
                PYRO.info(f'Adding: \033[1;31;48m{current_user}\033[1;37;48m by: \033[1;32;48m{phone}\033[1;37;48m \033[1;31;48m - User already in too many channel\033[1;37;48m - Account: {position + 1}/{position2}')
                await prints()
            except FloodWait as e:
                applist.remove(account)
                await app.stop()
                PYRO.info(f'Adding: \033[1;32;48m{current_user}\033[1;37;48m by: \033[1;31;48m{phone}\033[1;37;48m \033[1;31;48m - {e.value} seconds sleep is required for the account {phone}\033[1;37;48m - Account: {position + 1}/{position2}')
            except (ChatAdminRequired, ChannelPrivate):
                PYRO.info(f"Adding: \033[1;32;48m{current_user}\033[1;37;48m by: \033[1;31;48m{phone}\033[1;37;48m \033[1;31;48m - Chat admin permission required or Channel is private\033[1;37;48m - Account: {position + 1}/{position2}")
                applist.remove(account)
                await app.stop()
                await prints()
            except UserRestricted:
                PYRO.info(f"Adding: \033[1;32;48m{current_user}\033[1;37;48m by: \033[1;31;48m{phone}\033[1;37;48m \033[1;31;48m - Removing this restricted account\033[1;37;48m - Account: {position + 1}/{position2}")
                applist.remove(account)
                await app.stop()
            except UserIdInvalid:
                PYRO.info(f"Adding: \033[1;31;48m{current_user}\033[1;37;48m by: \033[1;32;48m{phone}\033[1;37;48m \033[1;31;48m - User invalid or you never met user\033[1;37;48m - Account: {position + 1}/{position2}")
                counter +=1
                await prints()
            except UserNotMutualContact:
                PYRO.info(f'Adding: \033[1;31;48m{current_user}\033[1;37;48m by: \033[1;32;48m{phone}\033[1;37;48m \033[1;31;48m - User is not mutual contact\033[1;37;48m - Account: {position + 1}/{position2}')
                counter += 1
                um += 1
                await prints()
            except PeerIdInvalid as e:
                PYRO.info(f"Adding: \033[1;32;48m{current_user}\033[1;37;48m by: \033[1;32;48m{phone}\033[1;37;48m \033[1;31;48m - If you see this line many times rerun the get_data.py\033[1;37;48m - Account: {position + 1}/{position2}")
                #applist.remove(account)
                counter +=1
                await prints()
            except UserPrivacyRestricted:
                PYRO.info(f"Adding: \033[1;31;48m{current_user}\033[1;37;48m by: \033[1;32;48m{phone}\033[1;37;48m \033[1;31;48m - User have privacy enabled\033[1;37;48m - Account: {position + 1}/{position2}")
                counter +=1
                privacy += 1
                await prints()
            except TimeoutError:
                PYRO.info(f'Adding: \033[1;32;48m{current_user}\033[1;37;48m by: \033[1;32;48m{phone}\033[1;37;48m \033[1;31;48m - Network problem was encounterd\033[1;37;48m - Account: {position + 1}/{position2}')
            except RPCError as e:
                PYRO.info(f"Adding: \033[1;32;48m{current_user}\033[1;37;48m by: \033[1;32;48m{phone}\033[1;37;48m \033[1;31;48m - {phone} Rpc error\033[1;37;48m - Account: {position + 1}/{position2}"")
                PYRO.info(f"{e}")
                m = user_id[counter][usermethod]
                PYRO.info(f"{m}")
                counter +=1
                await prints()
            except OSError:
                osr +=1
            except BaseException as e:
                PYRO.info(f"Adding: \033[1;32;48m{current_user}\033[1;37;48m by: \033[1;32;48m{phone}\033[1;37;48m \033[1;31;48m - Error info below\033[1;37;48m - Account: {position + 1}/{position2}")
                PYRO.info(f"{e}")
                m = user_id[counter][usermethod]
                PYRO.info(f"{m}")
                counter +=1
                await prints()
            if osr == 30:
                PYRO.info("osr is 30")
                PYRO.info(f'Adding: \033[1;32;48m{current_user}\033[1;37;48m by: \033[1;32;48m{phone}\033[1;37;48m \033[1;31;48m - This increase because of internet problem try again later\033[1;37;48m - Account: {position + 1}/{position2}')
                await prints()
                exit()
                
            
