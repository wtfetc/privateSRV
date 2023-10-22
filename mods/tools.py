import base64

import requests

from mods.modules import authentication



def send_bitrix_request(method: str, data: dict):
    try:
        #print(requests.post(f"{authentication('Bitrix')}{method}", json=data).json()['result'])
        return requests.post(f"{authentication('Bitrix')}{method}", json=data).json()['result']
    except KeyError:
        print("eeeee")
        return 
