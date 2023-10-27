import json
import base64
from mods.tools import send_bitrix_request
from fast_bitrix24 import Bitrix
webhook = "aHR0cHM6Ly92YzFjLmJpdHJpeDI0LnJ1L3Jlc3QvNDc5L21qbWRpNXczd3ZsOWpvNWcv"
decip = base64.b64decode(webhook).decode('utf-8')
b = Bitrix(decip)


def test_job(req, event=None):
    print ("1")
    try:
       print ("2")
       print (req['userid']) 
       useridformatted = str([req['userid']])
       useridformatted = useridformatted[7:(len(useridformatted)-2)]
       print (useridformatted)
       message_text =  f'\nвам поставлена задача' \
                       f'\n текст' 
       b.call('im.notify.system.add', {
        'USER_ID': useridformatted,
        'MESSAGE':  message_text
       })
       print ("4")
    except:
        print ("3")
        return
