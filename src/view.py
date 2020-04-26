import aiohttp
import asyncio
import json
from src.wxauth import global_auth
from src.httputils import build_path
class WxView:
    def __init__(self):
        return
    
    async def aio_post(self, url, data):
        async with global_auth.session.post(url, json=data) as resp:
            print(await resp.json())
        return
    
    def post_memue(self):
        parms = {
            "access_token":global_auth.get_token()
        }
        url = build_path("https://api.weixin.qq.com/cgi-bin/menu/create", parms)
        global_auth.loop.run_until_complete(self.aio_post(url=url, data={
            "button":[
                {
                    "type":"view",
                    "name":"Manage",
                    "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx52aa33f21750a6ac&redirect_uri=http://www.cgcool.science&response_type=code&scope=snsapi_userinfo#wechat_redirect"
                }
            ]
        }))
        return

    def GET(self):
        self.post_memue()
        return "Ok"