import requests
import json


def change_limits(limit):
    params = {'limit': limit}
    response = requests.put("http://127.0.0.1:8000/api/v1/telegram/admin/limits", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    return data


def give_access(user_id, plan):

    params = {'user_id': user_id, 'plan': plan}
    response = requests.put("http://127.0.0.1:8000/api/v1/telegram/user/plan", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    return data