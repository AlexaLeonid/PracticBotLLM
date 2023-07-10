import requests
import json


def change_limits(limit):
    params = {'limit': limit}
    response = requests.put("https://manygpt.onrender.com/api/v1/telegram/admin/limits", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    return data


def give_access(user_id, plan):
    params = {'user_id': user_id, 'plan': plan}
    response = requests.put("https://manygpt.onrender.com/api/v1/telegram/user/plan", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    return data


def get_all_users():
    response = requests.get("https://manygpt.onrender.com/api/v1/telegram/admin/stats/all_users")
    if response.status_code != 200:
        return "Проблемы "
    data = response.content
    file_name = response.headers.get("filename")
    return data, file_name


def get_user_growth(period):
    params = {'period': period, 'plan': None}
    response = requests.get("https://manygpt.onrender.com/api/v1/telegram/admin/stats/growth", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.content
    file_name = response.headers.get("filename")
    return data, file_name


def get_user_interaction(period):
    params = {'period': period}
    response = requests.get("https://manygpt.onrender.com/api/v1/telegram/admin/stats/growth", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.content
    file_name = response.headers.get("filename")
    return data, file_name
