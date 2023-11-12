from mods.chat_bot.SendMessage import bot_send_message


def send_deal_changed_user_message(req):
    print ("1")
    bot_send_message({
        'dialog_id': '479',
        'message': f'Ответственным за сделку {req["deal_name"]} https://vc1с.bitrix24.ru/crm/deal/details/{req["deal_id"]}/ был назначен {req["user_after"]}'
    })
