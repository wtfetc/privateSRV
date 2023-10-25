import json
import base64
from mods.tools import send_bitrix_request
from fast_bitrix24 import Bitrix
webhook = "https://vc1c.bitrix24.ru/rest/479/mjmdi5w3wvl9jo5g/"
b = Bitrix(webhook)


def test_job(req, event=None):
    try:
       b.call('im.notify.system.add', {
        'USER_ID': "1",
        'MESSAGE': 'вам поставлена задача'})
    except:
        return
