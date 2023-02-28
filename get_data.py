import asyncio
import json, os
from pyrogram.client import Client, enums
from helper.filter import filterus
from helper.data import get_data
from pathlib import Path
#workdir = 'session/'
method = input('choose method username or id: ').lower()
async def main():
     root = Path.cwd()
     config = (json.load(open(root / "config.json")))
     gp_s_id = int(str("-100")+str(config['group_source']))
     gp_t_id = int(str("-100")+str(config['group_target']))
     path_group =  root / 'data' / 'source_user.json'
     path_group2 = root / 'data' / 'target_user.json'
     path_group4 = root / 'data' / 'source_admin.json'
     await get_data(gp_s_id, gp_t_id, config, method)
     filterus(path_group,path_group2, path_group4, root)
     
asyncio.run(main())

