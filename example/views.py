from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from example.models import *

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
import datetime

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                uid = event.source.user_id
                profile = line_bot_api.get_profile(uid)
                name = profile.display_name
                text = event.message.text

                message=[]
                if not user_message.objects.filter(uid=uid).exists():
                    user_message.objects.create(uid=uid, name=name, message=text)
                    message.append(TextSendMessage(text='資料新增完畢'))
                else:
                    user_message.objects.filter(uid=uid, name=name).update(message=text, time=datetime.datetime.now())
                    # obj = user_message.objects.get(uid=uid)
                    # obj.message = text
                    # obj.save()                
                    message.append(TextSendMessage(text='資料修改完畢'))

                line_bot_api.reply_message(event.reply_token, message)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()