import asyncio
import json
from helper.login import login, create
from helper.logs import log
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


#load config for accounts
config=json.load(open('config.json', 'r'))
group_source_id=str(config['group_source_username'])
group_target_id=str(config['group_target_username'])
auto_join=bool(config['auto_join'])
option = input('Login or Signup type one : ')
async def createall():
    PYRO = log('PYRO-START_LOGIN')
    PYRO.propagate = False
    for account in config['accounts']:
        phone = account['phone']
        api_id = int(account['api_id'])
        api_hash = account['api_hash']
        PYRO.info(phone)
        await create(phone, api_id, api_hash)
async def loginall():
    PYRO = log('PYRO-START_LOGIN')
    PYRO.propagate = False
    for account in config['accounts']:
        phone = account['phone']
        api_id = int(account['api_id'])
        api_hash = account['api_hash']
        PYRO.info(phone)
        await login(phone, api_id, api_hash, auto_join, group_source_id,  group_target_id)
if option.lower()[0] == 'l':
    asyncio.run(loginall())
elif option.lower()[0] == 's':
    asyncio.run(createall())
