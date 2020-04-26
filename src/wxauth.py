import web
import hashlib
import aiohttp
import asyncio
import time
from functools import wraps
from src.httputils import build_path

   
class WxToken:
    def __init__(self):
        return

    def GET(self):
        data = web.input()
        try:
            if len(data) == 0:
                return "err"
            print(data)
            signature = data.signature.strip()
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "123"

            list = [token, timestamp, nonce]
            list.sort()
            str_list = "".join([item for item in list])
            sha1 = hashlib.sha1()
            sha1.update(str_list.encode())
            hashcode = sha1.hexdigest().strip()

            if signature == hashcode:
                print(echostr)
                return echostr
            else:
                return ""
        except Exception:
            return  

class wxauth:
    def __init__(self, appid, secret):
        self.appid = appid
        self.secret = secret
        self.loop = asyncio.new_event_loop()
        self.token = None
        self.token_time = None
        asyncio.set_event_loop(self.loop)
        self.session = aiohttp.ClientSession()
        return
 
    async def aio_get(self, url):
        async with self.session.get(url) as resp:
            json_body = await resp.json()
            self.token = json_body["access_token"]

    def set_token(self, url="https://api.weixin.qq.com/cgi-bin/token"):
        '''
            url: WeChat auth restful api
        '''
        parms = {
            "grant_type":"client_credential", 
            "appid":self.appid, 
            "secret":self.secret
        }
        url = build_path(url, parms)
        self.loop.run_until_complete(self.aio_get(url))
        return
  
    def get_token(self):
        now = time.time()
        if (self.token_time == None) or ((now - self.token_time) > 4800):
            self.set_token()
            self.token_time = now
        return self.token

global_auth = wxauth(appid="wx52aa33f21750a6ac", secret="aac7201a5d9506fdb0ca57c0b7c4cf0f")