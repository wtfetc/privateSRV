from datetime import datetime, timedelta
from time import time, sleep
from random import randint
import json

# from web_app_4dk.tools import send_bitrix_request
from tools import send_bitrix_request


def fill_task_title(req, event):
    task_id = req['data[FIELDS_AFTER][ID]']
    task_info = send_bitrix_request('tasks.task.get', {
        'taskId': task_id,
        'select': ['*', 'UF_*']
    })
    if not task_info or 'task' not in task_info or not task_info['task']: # если задача удалена или в иных ситуациях
        return
    task_info = task_info['task']
   # task_registry(task_info, event)
    '''
    if task_info['closedDate'] and task_info['ufAuto934103382947'] != '1':
        send_notification(task_info, 'Завершение')
    '''

    if 'ufCrmTask' not in task_info or not task_info['ufCrmTask']: # ufCrmTask - связь с сущностью (список)
        return

    company_crm = list(filter(lambda x: 'CO' in x, task_info['ufCrmTask']))
    uf_crm_task = []
    if not company_crm:
       
     
        contact_crm = list(filter(lambda x: 'C_' in x, task_info['ufCrmTask']))
        if not contact_crm:
            return
        contact_crm = contact_crm[0][2:]
        contact_companies = list(map(lambda x: x['COMPANY_ID'], send_bitrix_request('crm.contact.company.items.get', {'id': contact_crm})))
        if not contact_companies:
            return
           ''' 
        contact_companies_info = send_bitrix_request('crm.company.list', {
           'select': ['UF_CRM_1660818061808'],     # Вес сделок
            'filter': {
                'ID': contact_companies,
            }
            
        })
        '''
        if contact_companies_info:
            for i in range(len(contact_companies_info)):
                if not contact_companies_info[i]['UF_CRM_1660818061808']:
                    contact_companies_info[i]['UF_CRM_1660818061808'] = 0
            best_value_company = list(sorted(contact_companies_info, key=lambda x: float(x['UF_CRM_1660818061808'])))[-1]['ID'] #последний элемент в общем списке - с макс value
            uf_crm_task = ['CO_' + best_value_company, 'C_' + contact_crm] # нельзя дописать, можно толлько перезаписать обоими значениями заново
            company_id = best_value_company #Это для тайтла
            
    else:
        company_id = company_crm[0][3:]

 #   if event == 'ONTASKADD':
  #      check_similar_tasks_this_hour(task_info, company_id)


    company_info = send_bitrix_request('crm.company.get', {
        'ID': company_id,
    })
    if company_info and company_info['TITLE'].strip() in task_info['title']: # strip() - очищает от пробелов по краям, если есть название компании в тайтле, то возрват
        return

    if not uf_crm_task: #если не заполнено CRM - если в задаче уже есть company_id и нам не нужно ее заполнять
        send_bitrix_request('tasks.task.update', {
            'taskId': task_id,
            'fields': {
                'TITLE': f"{task_info['title']} {company_info['TITLE']}",
            }})
    else:
        send_bitrix_request('tasks.task.update', {
            'taskId': task_id,
            'fields': {
                'TITLE': f"{task_info['title']} {company_info['TITLE']}",
                'UF_CRM_TASK': uf_crm_task,
            }})
    return task_info


def task_handler(req, event=None):
    try:
        task_info = fill_task_title(req, event)
    except:
        return
    '''
    send_notification(task_info, 'Создание')
    '''
