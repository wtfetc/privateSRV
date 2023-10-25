import json
import base64
from mods.tools import send_bitrix_request
from fast_bitrix24 import Bitrix
webhook = "https://vc1c.bitrix24.ru/rest/479/mjmdi5w3wvl9jo5g/"
b = Bitrix(webhook)


def test_job(req, event=None):
    print ("1")
    try:
       print ("2")
       useridformatted = str([req['userid']])[5:]
       b.call('im.notify.system.add', {
        'USER_ID': useridformatted,
        'MESSAGE': 'вам поставлена задача'})
       print ("4")
    except:
        print ("3")
        return
