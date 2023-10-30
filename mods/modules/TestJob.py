import json
import base64
from mods.tools import send_bitrix_request
from fast_bitrix24 import Bitrix
import requests

webhook = "aHR0cHM6Ly92YzFjLmJpdHJpeDI0LnJ1L3Jlc3QvNDc5L21qbWRpNXczd3ZsOWpvNWcv"
decip = base64.b64decode(webhook).decode('utf-8')
b = Bitrix(decip)
TOKEN = "6830145088:AAFZyKZIeqg0JhtVNCjP3QteEByxptrv6oE"
#chat_id = "-4033252882"
chat_id = "176393496"

def test_job(req, event=None):
    print ("1")
    try:
       print ("2")
       print (req['userid']) 
       useridformatted = str([req['userid']])
       useridformatted = useridformatted[7:(len(useridformatted)-2)]
       print (useridformatted)
       message_text =  f'Внимание! У клиента uiiu заканчивается оплата по договору. Пожалуйста, свяжитесь с клиентом.\n' \
                       f'https://vc4dk.bitrix24.ru/crm/deal/details/' \
                       f'Внимание! У клиента uiiu заканчивается оплата по договору. Пожалуйста, свяжитесь с клиентом.\n' \
                       f'https://vc4dk.bitrix24.ru/crm/deal/details/'
       b.call('im.notify.system.add', {
        'USER_ID': useridformatted,
        'MESSAGE':  message_text
       })
       print ("4")
       message = f"Новая задача {req['name']}\nСсылка на задачу - https://vc1c.bitrix24.ru/company/personal/user/479/tasks/task/view/{req['id']}/" 
       #message = "лррр"
       url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
       requests.get(url).json()
    except:
        print ("3")
        return
