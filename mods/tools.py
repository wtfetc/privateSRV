import base64

import requests

import authentication



def send_bitrix_request(method: str, data: dict):
    try:
        return requests.post(f"{authentication('Bitrix')}{method}", json=data).json()['result']
    except KeyError:
        return 
