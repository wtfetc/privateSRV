from datetime import datetime, timedelta
from time import time, sleep
from random import randint
import json
import base64
import requests

# from web_app_4dk.tools import send_bitrix_request
from mods.tools import send_bitrix_request
from fast_bitrix24 import Bitrix


def fill_task_title(req, event):
    task_id = req['data[FIELDS_AFTER][ID]']
    task_info = send_bitrix_request('tasks.task.get', { # читаем инфо о задаче
        'taskId': task_id,
        'select': ['*', 'UF_*']
    })
    print("00")
    if not task_info or 'task' not in task_info or not task_info['task']:
        print("0") # если задача удалена или в иных ситуациях
        return
    
    task_info = task_info['task']
  

    if 'ufCrmTask' not in task_info or not task_info['ufCrmTask']:
        print("1") # ufCrmTask - связь с сущностью (список)
        return

    company_crm = list(filter(lambda x: 'CO' in x, task_info['ufCrmTask']))
    uf_crm_task = []
    if not company_crm:
        print("2")
        contact_crm = list(filter(lambda x: 'C_' in x, task_info['ufCrmTask']))
        if not contact_crm:
            print("3")
            return
        
        # если к задаче прикреплен только контакт
        contact_crm = contact_crm[0][2:]
        main_company = send_bitrix_request('crm.contact.get', {'id': contact_crm, 'select': ['UF_CRM_1709218047']}) # читаем поле Основная компания
        print(main_company)

        if main_company: # если основная компания заполнена, то читаем у неё поле Тип компании
            print("4")
            main_company = main_company[0][3:]
            company_info = send_bitrix_request('crm.company.get', {'id': main_company, 'select': ['COMPANY_TYPE']})
            if company_info['COMPANY_TYPE'] not in ['1']: # если тип компании = Закончился ИТС
                company_id = main_company        
        else:
            contact_companies = list(map(lambda x: x['COMPANY_ID'], send_bitrix_request('crm.contact.company.items.get', {'id': contact_crm})))
            if not contact_companies: # если нет привязанных компаний
                return
            contact_companies_info = send_bitrix_request('crm.company.list', { # читаем вес сделок всех компаний, привязанных к контакту
                'select': ['UF_CRM_1660818061808'],     # Вес сделок
                'filter': {
                    'ID': contact_companies,
                }
            })
            print(contact_companies_info)
            if contact_companies_info:
                for i in range(len(contact_companies_info)):
                    if not contact_companies_info[i]['UF_CRM_1709217643']:
                        contact_companies_info[i]['UF_CRM_1709217643'] = 0
                best_value_company = list(sorted(contact_companies_info, key=lambda x: float(x['UF_CRM_1709217643'])))
                print(best_value_company)
                best_value_company = best_value_company[-1]['ID']
                #best_value_company = list(sorted(contact_companies_info, key=lambda x: float(x['UF_CRM_1709217643'])))[-1]['ID'] # последний элемент в общем списке - с макс value ???
                uf_crm_task = ['CO_' + best_value_company, 'C_' + contact_crm] # нельзя дописать, можно толлько перезаписать обоими значениями заново
                company_id = best_value_company # это для тайтла
        
    else:
        company_id = company_crm[0][3:]


    company_info = send_bitrix_request('crm.company.get', { # читаем инфо о найденной компании
        'ID': company_id,
    })

    if company_info and company_info['TITLE'].strip() in task_info['title']: # strip() - очищает от пробелов по краям, если есть название компании в тайтле, то возрват
        return

    if not uf_crm_task: #если не заполнено CRM - если в задаче уже есть company_id и нам не нужно ее заполнять
        send_bitrix_request('tasks.task.update', {
            'taskId': task_id,
            'fields': {
                'TITLE': f"{task_info['title']} {company_info['TITLE']}" # то обновляем название задачи
                 }})
    else:
        send_bitrix_request('tasks.task.update', {
            'taskId': task_id,
            'fields': {
                'TITLE': f"{task_info['title']} {company_info['TITLE']}", # то обновляем название задачи и привязку к crm
                'UF_CRM_TASK': uf_crm_task,
            }})

    return task_info


def task_handler(req, event=None):
    try:
        task_info = fill_task_title(req, event)
        print("10")
    except:
        return
