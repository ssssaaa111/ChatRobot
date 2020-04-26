import asyncio
import aiohttp

def build_path(base_url, parm_dict):
    url = base_url + '?'
    for key, val in parm_dict.items():
        url = url + key + '=' + val + '&'
    return url[:-1]