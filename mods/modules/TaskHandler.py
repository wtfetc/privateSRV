from datetime import datetime, timedelta
from time import time, sleep
from random import randint
import json
import base64
import requests

# from web_app_4dk.tools import send_bitrix_request
from mods.tools import send_bitrix_request
from fast_bitrix24 import Bitrix

webhook = "aHR0cHM6Ly92YzFjLmJpdHJpeDI0LnJ1L3Jlc3QvNDc5L21qbWRpNXczd3ZsOWpvNWcv"
decip = base64.b64decode(webhook).decode('utf-8')
b = Bitrix(decip)
TOKEN = "6830145088:AAFZyKZIeqg0JhtVNCjP3QteEByxptrv6oE"
chat_id = "-4033252882"


def fill_task_title(req, event):
    task_id = req['data[FIELDS_AFTER][ID]']
    message = f"Новая задача"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(url).json())
    task_info = b.get_all(
        'tasks.task.get', {
            'taskId': task_id,
            'select': ['*', 'UF_*']
        })
            
    # 06 12 2023
    deals_info = b.get_all('crm.deal.list', {
        'select': [
            'TITLE',
            'TYPE_ID',
            'ASSIGNED_BY_ID',
            'BEGINDATE',
            'CLOSEDATE',
            'OPPORTUNITY',
            'STAGE_ID',
            'COMPANY_ID',
        ],
        'filter': {
            'CATEGORY_ID': '4',
            'ID': '2899'}})

    if not task_info or 'task' not in task_info or not task_info['task']:  # если задача удалена или в иных ситуациях
        print("0")
        return
    task_info = task_info['task']
    
    if 'ufCrmTask' not in task_info or not task_info['ufCrmTask']:  # ufCrmTask - связь с сущностью (список)
        print("00")
        return

    company_crm = list(filter(lambda x: 'CO' in x, task_info['ufCrmTask']))
    uf_crm_task = []
    
    if not company_crm:
        print("1")
        contact_crm = list(filter(lambda x: 'C_' in x, task_info['ufCrmTask']))
        
        if not contact_crm:
            return
            
        contact_crm = contact_crm[0][2:]
        contact_companies = list(
            map(lambda x: x['COMPANY_ID'], b.get_all('crm.contact.company.items.get', {'id': contact_crm})))
        
        if not contact_companies:
            print("13")
            return

            if contact_companies:
                best_value_company = contact_companies[0]
                uf_crm_task = ['CO_' + str(best_value_company), 'C_' + str(contact_crm)]  # нельзя дописать, можно толлько перезаписать обоими значениями заново
                company_id = best_value_company  # Это для тайтла

    else:
        print("5")
        company_id = company_crm[0][3:]
    
    company_info = b.get_all(
        'crm.company.get', {
            'ID': company_id,
        })
    if company_info and company_info['TITLE'].strip() in task_info[
        'title']:  # strip() - очищает от пробелов по краям, если есть название компании в тайтле, то возрват
        print("7")
        return

    if not uf_crm_task:  # если не заполнено CRM - если в задаче уже есть company_id и нам не нужно ее заполнять
        
        b.call('tasks.task.update', {
            'taskId': task_id,
            'fields': {
                'TITLE': f"{task_info['title']} {company_info['TITLE']}",
            }})
    else:
        print("999")
        old_aud = task_info['auditors']
        old_aud.append('491')

        
    if task_info['groupId'] in ['119']: # если это определенная группа

        # если ответственный за компанию это НЕ постановщик или ответственный
        if (task_info['responsibleId'] not in company_info['ASSIGNED_BY_ID']) and (task_info['createdBy'] not in company_info['ASSIGNED_BY_ID']):
            old_aud.append(company_info['ASSIGNED_BY_ID']) # добавляем ответственного за компанию в наблюдатели

            b.call('im.notify.system.add', { # пушим ответственному за компанию
                'USER_ID': company_info['ASSIGNED_BY_ID'],
                'MESSAGE': f'Для вашего клиента {company_info["TITLE"]} была поставлена задача внешнему исполнителю: https://vc1c.bitrix24.ru/workgroups/group/119/tasks/task/view/{task_info["id"]}/'})
        
        user_info = b.get_all( # читаем отделы ответственного
            'user.get', {
                'ID': company_info['ASSIGNED_BY_ID'],
            })

        # подставить айди ГО3
        if (518 in user_info[0]['UF_DEPARTMENT'] ): # если это ГО3
            dep_info = b.get_all('department.get', { # читаем рука отдела
                'ID': '518'})
            old_aud.append(dep_info[0]['UF_HEAD']) # добавляем рука сотрудника в наблюдатели
            
            b.call('im.notify.system.add', { # пушим руку
                'USER_ID': '501', # подставить dep_info[0]['UF_HEAD']
                'MESSAGE': f'Для клиента вашего сотрудника {company_info["TITLE"]} была поставлена задача внешнему исполнителю: https://vc1c.bitrix24.ru/workgroups/group/119/tasks/task/view/{task_info["id"]}/'})


        # подставить айди ГО4
        if (99 in user_info[0]['UF_DEPARTMENT']): # если это ГО4
            dep_info = b.get_all('department.get', { # читаем рука отдела
                'ID': '99'})
            old_aud.append(dep_info[0]['UF_HEAD']) # добавляем рука сотрудника в наблюдатели

            b.call('im.notify.system.add', { # пушим руку
                'USER_ID': dep_info[0]['UF_HEAD'],
                'MESSAGE': f'Для клиента вашего сотрудника {company_info["TITLE"]} была поставлена задача внешнему исполнителю: https://vc1c.bitrix24.ru/workgroups/group/119/tasks/task/view/{task_info["id"]}/'})
          
        
        print(old_aud)
        b.call('tasks.task.update', {
            'taskId': task_id,
            'fields': {
                'TITLE': f"{task_info['title']} {company_info['TITLE']}",
                'UF_CRM_TASK': uf_crm_task,
                'AUDITORS': old_aud
            }})

        # 25102023
        b.call('im.notify.system.add', {
            'USER_ID': 479,
            'MESSAGE': f'Элементы РТиУ заполнены'})

    return task_info


def task_handler(req, event=None):
    try:
        task_info = fill_task_title(req, event)
        print("10")
    except:
        return
