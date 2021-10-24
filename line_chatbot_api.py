from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, 
    PostbackEvent,
    TextMessage, 
    TextSendMessage, 
    ImageSendMessage, 
    StickerSendMessage, 
    LocationSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackAction,
    MessageAction,
    URIAction,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    DatetimePickerAction,
    ConfirmTemplate
)

line_bot_api = LineBotApi('f2V3d+/3MpYXb28+tUNODK+t4V+0ak9oe7GjE9KoI4Rl0cKGLbRG8tB/POdwy43kzn+7dxdYqW5RteF/cp7DobS3VW+qxAmriKoqkG2CfFje/7H+2UPQ3IMJ5uOGtkdKcsP3W2e3VMwgrCa5GNUAhwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4134a0a296fcd96427f616f80eff50af')