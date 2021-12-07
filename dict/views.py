from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,    #製作搜尋不到之按鈕回覆
    ButtonsTemplate,     
    MessageTemplateAction
)
from .dict_crawler import IFoodie,Dict

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
            #print(events)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                dict = Dict(event.message.text)  #使用者傳入的訊息文字
                if dict.scrape()[0]=="搜尋不到":
                    print("~~~~~")
                    Ms1 = dict.scrape()[1]
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='無搜尋結果',
                                text='您要找的是不是:',
                                actions=[
                                    MessageTemplateAction(
                                        label = Ms1[0],
                                        text = Ms1[0]
                                    ),
                                    MessageTemplateAction(
                                        label = Ms1[1],
                                        text = Ms1[1]
                                    )
                                ]
                            )
                    )
                )
                else :
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=dict.scrape()[0])
                )

                #print(dict.scrape())
        return HttpResponse()
    else:
        return HttpResponseBadRequest()