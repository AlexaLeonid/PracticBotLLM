import string

import requests


def get_user(user_id):
    response = requests.get("https://manygpt.onrender.com/api/v1/telegram/user/", params={"user_id": user_id})
    data = response.json()
    try:
        d = data["default_model"]["name"]
    except:
        d = "отсутствует"
    return data["subscription"]["name"], data["token"]["count"], d


def change_model(user_id, model_id):
    params = {'user_id': user_id, 'model_id': model_id}
    response = requests.put("https://manygpt.onrender.com/api/v1/telegram/user/default_model", params=params)
    data = response.json()
    return data


def change_plan(user_id, plan):
    params = {"user_id": user_id, "plan": plan}
    response = requests.put("https://manygpt.onrender.com/api/v1/telegram/user/plan", params=params)
    data = response.json()
    return data


def login(user_id: int, username: string):
    params = {"user_id": user_id, "username": username}
    response = requests.post("https://manygpt.onrender.com/api/v1/telegram/auth/login", params=params)
    if response.status_code != 201:
        return "Проблемы с авторизацией"
    data = response.json()
#    return data

