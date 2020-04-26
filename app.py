import web
from src.view import WxView
from src.wxauth import WxToken
from src.user import User

if __name__ == "__main__":
    urls = (
        "/wx", "WxToken",
        "/view", "WxView",
        "/userinfo", "User",
        "/notify", "User",
        )
    app = web.application(urls, globals())
    app.run()