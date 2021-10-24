from urllib.parse import parse_qsl, parse_qs
import datetime, random, json

from linebot.models import messages
from line_chatbot_api import *

foodlist=[]
foodlist.append(('C', '廚窗 Kitchen Bliss', '324桃園市平鎮區中央路157號', '+886987078449', 24.9648154,121.1908407))
foodlist.append(('C', '阿米玲食堂', '320桃園市中壢區中央路212號', '+88634204995', 24.9644749,121.1907892))
foodlist.append(('W', '迷路義麵屋', '320桃園市平鎮區中央路151號', '+88634202713', 24.9647471,121.1907073))
foodlist.append(('W', '大中央厚切牛排', '320桃園市中壢區中央路153號', '+88634201415', 24.9647471,121.1907073))

foodstickerlist=[]
foodstickerlist.append((446, 1996))
foodstickerlist.append((446, 1997))
foodstickerlist.append((446, 1998))
foodstickerlist.append((789, 10865))
foodstickerlist.append((789, 10866))
foodstickerlist.append((789, 10863))

def call_food(event):
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            # thumbnail_image_url=url_for('static', filename='images/brown_1024.jpg', _external=True),
            thumbnail_image_url='https://i.imgur.com/mfUIthQ.png',
            title='想吃什麼，可以幫您推薦喔',
            text='可以選擇你想吃的餐飲類型，或是隨機由小編推薦',
            actions=[
                MessageAction(
                    label='中式餐點小吃',
                    text='中式餐點小吃'
                ),
                MessageAction(
                    label='西式餐點小吃',
                    text='西式餐點小吃'
                ),
                PostbackAction(
                    label='隨機推薦餐點',
                    display_text='隨機推薦餐點小吃',
                    data=f'action=food&item={json.dumps(foodlist[random.randint(0,len(foodlist)-1)])}'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)

def call_Chinese_food(event):
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            # thumbnail_image_url=url_for('static', filename='images/brown_1024.jpg', _external=True),
            thumbnail_image_url='https://i.imgur.com/mfUIthQ.png',
            title='這裡推薦幾間不錯的中式餐點',
            text='可以參考一下喔',
            actions=[
                PostbackAction(
                    label=foodlist[0][1],
                    display_text=foodlist[0][1],
                    data=f'action=food&item={json.dumps(foodlist[0])}'
                ),
                PostbackAction(
                    label=foodlist[1][1],
                    display_text=foodlist[1][1],
                    data=f'action=food&item={json.dumps(foodlist[1])}'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)

def call_western_food(event):
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            # thumbnail_image_url=url_for('static', filename='images/brown_1024.jpg', _external=True),
            thumbnail_image_url='https://i.imgur.com/mfUIthQ.png',
            title='這裡推薦幾間不錯的西式餐點',
            text='可以參考一下喔',
            actions=[
                PostbackAction(
                    label=foodlist[2][1],
                    display_text=foodlist[2][1],
                    data=f'action=food&item={json.dumps(foodlist[2])}'
                ),
                PostbackAction(
                    label=foodlist[3][1],
                    display_text=foodlist[3][1],
                    data=f'action=food&item={json.dumps(foodlist[3])}'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)

def show_food(event, food):
    foodsticker = foodstickerlist[random.randint(0,len(foodstickerlist)-1)]
    messages=[]
    messages.append(StickerSendMessage(package_id=foodsticker[0], sticker_id=foodsticker[1]))
    messages.append(TextSendMessage(text=f'為您推薦：{food[1]}，地址：{food[2]}，電話：{food[3]}'))
    # messages.append(LocationSendMessage())
    line_bot_api.reply_message(event.reply_token, messages)