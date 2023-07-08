import requests


def get_user(user_id):
    response = requests.get("http://127.0.0.1:8000/api/v1/telegram/user/", params={"user_id": user_id})
    data = response.json()
    return data


def change_model(user_id, model_id):
    params = {'user_id': user_id, 'model_id': model_id}
    response = requests.put("http://127.0.0.1:8000/api/v1/telegram/user/default_model", params=params)
    data = response.json()
    return data


def change_plan(user_id, plan_id):
    params = {"user_id": user_id, "plan_id": plan_id}
    response = requests.put("http://127.0.0.1:8000/api/v1/telegram/user/plan", params=params)
    data = response.json()
    return data


def login(user_id, username):
    params = {"id": user_id, "username": username}
    response = requests.post("http://127.0.0.1:8000/api/v1/telegram/auth/login", params=params)
    if response.status_code != 201:
        return "Проблемы с авторизацией"
    data = response.json()
#    return data


