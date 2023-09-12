import asyncio
import json
from pathlib import Path

from helper.data import get_data
from helper.filter import filterus
from init import rs, w, r, banner, clr

clr()
banner()
print(f"  {r}Version: {w}3.1 {r}| Author: {w}SAIF ALI{rs}\n")
print(f"  {r}Telegram {w}@PrinceXofficial {r}| Instagram: {w}@saifalisew1508{rs}\n")


# workdir = 'session/'
method = input("Choose Method Username or ID: ").lower()


async def main():
    root = Path.cwd()
    config = json.load(open(root / "config.json"))
    gp_s_id = int(str("-100") + str(config["group_source"]))
    gp_t_id = int(str("-100") + str(config["group_target"]))
    path_group = root / "data" / "source_user.json"
    path_group2 = root / "data" / "target_user.json"
    path_group4 = root / "data" / "source_admin.json"
    await get_data(gp_s_id, gp_t_id, config, method)
    filterus(path_group, path_group2, path_group4, root)


asyncio.run(main())
