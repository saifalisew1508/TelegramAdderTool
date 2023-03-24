import asyncio
import json
from itertools import dropwhile
from helper.account_handler import add_member, updatecount, addlogin
from colorama import init, Fore
import pyfiglet
import os, random

lg = Fore.LIGHTGREEN_EX
rs = Fore.RESET
r = Fore.RED
w = Fore.WHITE
cy = Fore.CYAN


info = lg + '(' + w + 'i' + lg + ')' + rs
error = lg + '(' + r + '!' + lg + ')' + rs
success = w + '(' + lg + '+' + w + ')' + rs
INPUT = lg + '(' + cy + '~' + lg + ')' + rs
colors = [lg, w, r, cy]


def banner():
    f = pyfiglet.Figlet(font='slant')
    logo = f.renderText('Tele Adder')
    print(random.choice(colors) + logo + rs)
    
def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

clr()
banner()
print(f'  {r}Version: {w}3.1 {r}| Author: {w}SAIF ALI{rs}\n')
print(f'  {r}Telegram {w}@PrinceXofficial {r}| Instagram: {w}@saifalisew1508{rs}\n')


#option for choose username or id
option = input('choose method username or id: ').lower() 
async def main():
        #loads member
        try:
            user_id = (json.load(open("data/user.json", encoding="utf-8")))
        except:
            user_id = (json.load(open("data/source_user.json", encoding="utf-8")))

        #loads users and channel info
        config = (json.load(open("config.json", encoding="utf-8")))
        
        
          
        #list to chcek active member
        activelist = ['UserStatus.RECENTLY', 'UserStatus.LAST_MONTH', 'UserStatus.LAST_WEEK', 'UserStatus.OFFLINE', 'UserStatus.RECENTLY', 'UserStatus.ONLINE' ]
        #count retrive old state             
        last_active = config["from_date_active"]
        added = 0
        active = []
        for x in dropwhile(lambda y: y != last_active, activelist):
           active.append(x)
        await add_member(user_id, config, active, option)

asyncio.run(main())
