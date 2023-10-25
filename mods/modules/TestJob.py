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
       print (req['userid']) 
       useridformatted = str([req['userid']])
       useridformatted = useridformatted[7:(len(useridformatted]-1)]
       print (useridformatted) 
       b.call('im.notify.system.add', {
        'USER_ID': useridformatted,
        'MESSAGE': 'вам поставлена задача'})
       print ("4")
    except:
        print ("3")
        return
