from wechat.official import WxApplication, WxTextResponse
from secret import Secret


class WxApp(WxApplication):
    """docstring for WxApp"""
    SECRET_TOKEN = Secret.SECRET_TOKEN
    APP_ID = Secret.APP_ID
    ENCODING_AES_KEY = Secret.ENCODING_AES_KEY

    def on_text(self, req):
        return WxTextResponse(req.Content, req)
