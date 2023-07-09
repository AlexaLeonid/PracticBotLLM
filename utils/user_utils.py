import string

import requests


def get_user(user_id):
    response = requests.get("http://127.0.0.1:8000/api/v1/telegram/user/", params={"user_id": user_id})
    data = response.json()
    return data["subscription"]["name"], data["token"]["count"], data["default_model"]["name"]


def change_model(user_id, model_id):
    params = {'user_id': user_id, 'model_id': model_id}
    response = requests.put("http://127.0.0.1:8000/api/v1/telegram/user/default_model", params=params)
    data = response.json()
    return data


def change_plan(user_id, plan):
    params = {"user_id": user_id, "plan": plan}
    response = requests.put("http://127.0.0.1:8000/api/v1/telegram/user/plan", params=params)
    data = response.json()
    return data


def login(user_id: int, username: string):
    params = {"user_id": user_id, "username": username}
    response = requests.post("http://127.0.0.1:8000/api/v1/telegram/auth/login", params=params)
    if response.status_code != 201:
        return "Проблемы с авторизацией"
    data = response.json()
#    return data


