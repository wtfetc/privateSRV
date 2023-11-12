from time import time

import requests

from web_app_4dk.modules.authentication import authentication
from web_app_4dk.tools import send_bitrix_request


def bot_send_message(req: dict) -> None:

    """
    :param req: {
    dialog_id: числовое значение id пользователя или id чата в формате <chat13>,
    message: текст сообщения,
    pass_replace: не заменять нижние подчеркивания переносом строки
    }
    :return:
    """
    dialog_id = req['dialog_id'][5:] if 'user' in req['dialog_id'] else req['dialog_id']
    message_text = req['message']
    if 'pass_replace' not in req or req['pass_replace']:
        message_text = message_text.replace('_', '\n')
    message_list_type = '2657' if 'message_list_type' not in req else req['message_list_type']
    data = {
        'BOT_ID': '497',
        'CLIENT_ID': '4c845jqm8lvb9tbb6yzluvkzc59rhwv3',
        'DIALOG_ID': 1,
        'MESSAGE': message_text,
    }