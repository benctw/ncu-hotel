# import flask related
from flask import Flask, request, abort, url_for
from urllib.parse import parse_qsl, parse_qs
import random
from linebot.models import events
from line_chatbot_api import *
from service_actions.service import *
from service_actions.food import *

# create flask server
app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

# handle msg
import os
import speech_recognition as sr

def transcribe(wav_path):
    '''
    Speech to Text by Google free API
    language: en-US, zh-TW
    '''
    
    r = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio, language="zh-TW")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return None

@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    user_name = line_bot_api.get_profile(user_id).display_name
    # print(event.postback.data)
    postback_data = dict(parse_qsl(event.postback.data))
    # print(postback_data.get('action', ''))
    # print(postback_data.get('item', ''))
    sticker_list=[(1070, 17839), (6362, 11087920), (11537, 52002734), (8525, 16581293)]
    if postback_data.get('action')=='็ดขๅๅๅ':
        sticker_random=sticker_list[random.randint(0,len(sticker_list)-1)]
        messages=[]
        messages.append(StickerSendMessage(package_id=sticker_random[0], sticker_id=sticker_random[1]))
        messages.append(TextSendMessage(text=f'{user_name}, ๅฅฝ็ๆฒๅ้ก, ๆซๅฐๆๅไบบๅกๅฐ็กๅฟซๅนซๆจๆบๅ{postback_data.get("item", "")}'))
        messages.append(another_service_or_not)
        line_bot_api.reply_message(event.reply_token, messages)
    elif postback_data.get('action')=='้้่ฆๆๅ':
        call_service(event)
    elif postback_data.get('action')=='food':
        show_food(event, json.loads(postback_data.get('item', '')))   
    elif postback_data.get('action')=='ๆซๆๅไธ็จๅถไปๆๅ':
        messages=[]
        messages.append(StickerSendMessage(package_id=11537, sticker_id=52002734))
        messages.append(TextSendMessage(text='็ฅๆจๆๆๅฟซ็ไฝๅฎฟ้ซ้ฉ'))
        line_bot_api.reply_message(event.reply_token, messages)

@handler.add(MessageEvent)
def handle_something(event):
    if event.message.type=='text':
        recrive_text=event.message.text
        # print(recrive_text)
        if 'ๆๅ' in recrive_text:
            # print(url_for('static', filename='images/brown_1024.jpg', _external=True))
            call_service(event)
        elif '็ดขๅๅๅ' in recrive_text:
            ask_tower_or_something(event)
        elif 'ๅฎขๆฟไป็ดน' in recrive_text:
            messages=[]
            messages.append(ImageSendMessage(original_content_url='https://i.imgur.com/H8O5GVT.png', preview_image_url='https://i.imgur.com/JM2MHSi.png'))
            messages.append(TextSendMessage(text='้ๆฌกๅฅไฝ็ๆฏไธญๅคฎ้ฃฏๅบ็็ถๅธๅฎขๆฟ๏ผๅฎขๆฟ่ฃๆฝขไปฅๆบซๆ็ๅคงๅฐ่ฒ็ณป็บๅบ่ชฟ๏ผ็ฐก็ดๆๅฐ็่จญ่จ้ขจๆ?ผ๏ผๆญ้ๅคง็่ฝๅฐ็ป็็ช๏ผ่ฎ่ช็ถ้ฝๅ็ๅฅ๏ผไฝๅฎข่ฝๅจ่้ฉ็ๆฟ้ๅง๏ผ้?็บๆจนๆตท็พๆฏๅ้ฃฝ่ฆฝไธญๅฃข้ฝๆๆฏ่งใ็ฐกๆฝไฟ่ฝ็็ทๆข็ถ้็ดฐ็ฏๅ่็๏ผๅ็พๅฎขๆฟ็ฉบ้่จญ่จ็ๆๅฐๆฐๅๅๆฌ็ไน็พใ'))
            messages.append(another_service_or_not)
            line_bot_api.reply_message(event.reply_token, messages)  
        elif '็พ้ฃๅฐๅ' in recrive_text:
            call_food(event)
        elif 'ไธญๅผ้ค้ปๅฐๅ' in recrive_text:
            call_Chinese_food(event)
        elif '่ฅฟๅผ้ค้ปๅฐๅ' in recrive_text:
            call_western_food(event)
        elif '็ๆๅฐ่ฆฝ' in recrive_text:
            messages=[]
            messages.append(StickerSendMessage(package_id=446, sticker_id=2000))
            messages.append(TextSendMessage(text='ไธญๅคฎ้ฃฏๅบๆญฃๅชๅๆฐๅฏซ็จๅผ็ขผไธญ๏ผ่ซ็จๅพๅๅไพๆฅ็ๆญคๅ่ฝ~ ่ฌ่ฌๆจ~'))
            line_bot_api.reply_message(event.reply_token, messages)
        else:
            messages=[]
            messages.append(StickerSendMessage(package_id=789, sticker_id=10882))
            messages.append(TextSendMessage(text='ๆฑๆญๆๆฒ่ฝๆ~ ๅฏไปฅ็จๅถไปๆนๅผๅ่ชชไธๆฌกๅ?'))
            line_bot_api.reply_message(event.reply_token, messages)
    elif event.message.type=='sticker':
        receive_sticker_id=event.message.sticker_id
        receive_package_id=event.message.package_id
        line_bot_api.reply_message(event.reply_token, StickerSendMessage(package_id=receive_package_id, sticker_id=receive_sticker_id))
    elif event.message.type=='image':
        message_content = line_bot_api.get_message_content(event.message.id)
        with open('temp_image.png', 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
    elif event.message.type=='audio':
        filename_wav='temp_audio.wav'
        filename_mp3='temp_audio.mp3'
        message_content = line_bot_api.get_message_content(event.message.id)
        with open(filename_mp3, 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
        os.system(f'ffmpeg -y -i {filename_mp3} {filename_wav} -loglevel quiet')
        text = transcribe(filename_wav)
        # print('Transcribe:', text)
        if 'ๆๅ' in text:
            # print(url_for('static', filename='images/brown_1024.jpg', _external=True))
            call_service(event)

another_service_or_not = TemplateSendMessage(
    alt_text='Confirm template',
    template=ConfirmTemplate(
        text='่ซๅ้้่ฆๅถไปๆๅๅ?',
        actions=[
            PostbackAction(
                label='้้่ฆๆๅ',
                display_text='้้่ฆๆๅ',
                data='action=้้่ฆๆๅ'
            ),
            PostbackAction(
                label='ๆซๆๅไธ็จ',
                display_text='ๆซๆๅไธ็จ',
                data='action=ๆซๆๅไธ็จๅถไปๆๅ'
            )
        ]
    )
)

# run app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5566, debug=True)