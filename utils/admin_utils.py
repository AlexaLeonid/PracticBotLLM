import requests
import json


def change_limits(admin_id, tariff_name, limit):

    params = {'token': admin_id, 'name': tariff_name, 'limit': limit}
    response = requests.post("http://127.0.0.1:8000/api/v1/telegram/admin/limits", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    return data


def give_access(admin_id, user_id, plan_id):

    params = {'token': admin_id, 'user_id': user_id, 'plan_id': plan_id}
    response = requests.post("http://127.0.0.1:8000/api/v1/telegram/admin/access", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    return data