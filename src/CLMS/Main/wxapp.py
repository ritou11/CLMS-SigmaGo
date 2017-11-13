from wechat.official import WxApplication, WxTextResponse


class WxApp(WxApplication):
    """docstring for WxApp"""
    SECRET_TOKEN = ''
    APP_ID = ''
    ENCODING_AES_KEY = ''

    def on_text(self, req):
        return WxTextResponse(req.Content, req)
