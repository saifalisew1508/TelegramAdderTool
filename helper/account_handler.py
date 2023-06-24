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
        msg = " Ctrl-c OR Ctrl-z was pressed. Do you really want to exit? y/n "
        print(msg)
        res = readchar.readchar()
        if res == 'y':
            updatecount(counterall)
            PYRO.info('Bye!')
            sys.exit()
        else:
            PYRO.info(f'Okat then i will continue')
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
        PYRO.info(f'sleep: {wait_time}')
        await asyncio.sleep(waittime / len(applist))
    #single line f string for printinf final output
    def printfinal():
        print(f"{added} : members were added\n {skipped} : members were skipped\n {privacy} : members had privacy enable or not in mutual contact\n {uc} : user banned in chat\n {um} : members not in mutual contat\n {bot}:  bot accont skipped")
        if method == 'username':
            PYRO.info(f"{noname} : accont has no usernames")
        updatecount(counterall)
        print(datetime.now().strftime("%H:%M:%S"))
    total_account = len(config['accounts'])
    PYRO.info(f'total account trying to login {total_account}')
    await asyncio.sleep(.2)
    applist = await addlogin(config['accounts'], g_s_id)
    logined_account = len(applist)
    PYRO.info(f"total logind account {logined_account}")
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
                    PYRO.info("Sleeping for two hours")

                    now = datetime.now()
                    end = datetime.now() + timedelta(hours=2)
                    print("Sleep started at : ", now.strftime("%H:%M:%S"))
                    print("Sleep End at : ", end.strftime("%H:%M:%S"))
                    added = 0
                    await asyncio.sleep(3500)
                    PYRO.info("1 hour left to continue")
                    await asyncio.sleep(3500)
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
                postiton = applist.index(account)
                current_user = user_id[counter]["userid"]
                postion2 = len(applist)
                PYRO.info(f"trying to add {current_user} by : {phone} account-postiton : {postiton + 1} / {postion2}")
                await app.add_chat_members(chat_id=chat_idt, user_ids=user_id[counter][usermethod])
                PYRO.info(f"{current_user} added success")
                counter += 1
                added += 1
                await prints()
            except UserBannedInChannel: 
                await app.stop()
                applist.remove(account)  
                PYRO.info(f'phone number limited')  
                await prints()
            except UsernameNotOccupied:
                PYRO.info("user not using username anymore")
                counter +=1
                await prints()
            except UserDeactivatedBan:
                PYRO.info("user removed from telegram")
                counter +=1
                await prints()
            except UserKicked:
                PYRO.info('this user is banned')
                counter +=1
                await prints()
            except PhoneNumberBanned: 
                await app.stop()
                applist.remove(account)  
                PYRO.info(f'phone number banned {phone}')  
                await prints()
            except PeerFlood:
                applist.remove(account)
                await app.stop()
                counter +=1
                PYRO.info(f'{phone} removed for this run')
                try: 
                    await prints()
                except:
                    printfinal()
            except UserChannelsTooMuch:
                counter += 1
                uc += 1
                PYRO.info('user already in too many channel')
                await prints()
            except FloodWait as e:
                applist.remove(account)
                await app.stop()
                PYRO.info(f'{e.value} seconds sleep is required for the account {phone}')
            except (ChatAdminRequired, ChannelPrivate):
                PYRO.info("Chat admin permission required or Channel is private")
                applist.remove(account)
                await app.stop()
                await prints()
            except UserRestricted:
                PYRO.info("removing this restricted account")
                applist.remove(account)
                await app.stop()
            except UserIdInvalid:
                PYRO.info(f"user invalid or u never met user {phone}")
                counter +=1
                await prints()
            except UserNotMutualContact:
                PYRO.info('user is not mutal contact')
                counter += 1
                um += 1
                await prints()
            except PeerIdInvalid as e:
                PYRO.info("if You see this line many time rerun the get_data.py")
                #applist.remove(account)
                counter +=1
                await prints()
            except UserPrivacyRestricted:
                PYRO.info("user have privacy enabled")
                counter +=1
                privacy += 1
                await prints()
            except TimeoutError:
                PYRO.info('network problem was encounterd')
            except RPCError as e:
                PYRO.info(f"{phone} Rpc error")
                PYRO.info(f"{e}")
                m = user_id[counter][usermethod]
                PYRO.info(f"{m}")
                counter +=1
                await prints()
            except OSError:
                osr +=1
            except BaseException as e:
                PYRO.info(phone, "error info below")
                PYRO.info(f"{e}")
                m = user_id[counter][usermethod]
                PYRO.info(f"{m}")
                counter +=1
                await prints()
            if osr == 30:
                PYRO.info("osr is 30")
                PYRO.info('This increase beacuse of internet problem try again later')
                await prints()
                exit()
                
            
