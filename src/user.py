import web
import asyncio
import aiohttp
import json
from src.httputils import build_path
from src.wxauth import global_auth

class User:
    def __init__(self):
        self.openid = ""
        self.access_token = ""
        self.userInfo = ""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.session = aiohttp.ClientSession()
        return

    async def queryOpenid(self, code=""):
        print("redirect url code:" + code)
        parms = { 
            "appid":global_auth.appid, 
            "secret":global_auth.secret,
            "code":code,
            "grant_type":"authorization_code"
        }
        path = build_path("https://api.weixin.qq.com/sns/oauth2/access_token", parms)
        print(path)
        async with self.session.get(path) as resp:
            json_body = await resp.json(content_type='text/plain',encoding='utf-8')
            print(json_body)
            self.access_token = json_body["access_token"]
            self.openid = json_body["openid"]
        return

    async def queryUserInfo(self, openid="", access_token=""):
        parms = {
            "access_token":access_token,
            "openid":openid,
            "lang":"zh_CN"
        }
        path = build_path("https://api.weixin.qq.com/sns/userinfo", parms)
        async with self.session.get(path) as resp:
            self.userInfo = await resp.json(content_type='text/plain',encoding='utf-8')
        return 

    async def sendReq(self, openid="", company="", ass="", time="", token=""):
        parms = {
            "access_token": token
        }
        path = build_path("https://api.weixin.qq.com/cgi-bin/message/template/send", parms)
        print(path)
        req = {
            "touser":openid,
            "template_id":"XX5RqVkLBxoI2liF4LA8j824bzWA2E2IfDpyAHuvhUI",
            "data":{
                    "company": {
                        "value":company,
                        "color":"#173177"
                    },
                    "ass":{
                        "value":ass,
                        "color":"#173177"
                    },
                    "time": {
                        "value":time,
                        "color":"#173177"
                    }
            }
        }
        resp = await self.session.post(url=path, json=req)
        print(resp)
        return

    def notifyUser(self, data):
        users_list = data["data"]
        token = global_auth.get_token()
        for user in users_list:
            info = user['info']
            openid = user['openId']
            company = info['company']
            ass = info['ass']
            time = info['time']
            print("openid:{} company:{} ass:{} time:{}".format(openid, company, ass, time))
            self.loop.run_until_complete(self.sendReq(openid=openid, company=company, ass=ass, time=time, token=token))
        return

    def GET(self):
        data = web.input()
        print(data)
        self.loop.run_until_complete(self.queryOpenid(code=data.usercode))
        print("open id:" + self.openid + "; " + "token:" + self.access_token)
        self.loop.run_until_complete(self.queryUserInfo(openid=self.openid, access_token=self.access_token))
        print(self.userInfo)
        return self.openid

    def POST(self):
        data = web.input(_method='post')
        json_str = "{\"data\":" + data.data + "}"
        print(json_str)
        data_json = json.loads(json_str)
        print(data_json)
        self.notifyUser(data=data_json)