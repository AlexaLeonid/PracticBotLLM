import requests
from nanoid import generate


def get_count_models(user_id):
    params = {"user_id": user_id}
    response = requests.get("http://127.0.0.1:8000/api/v1/telegram/models/count", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    return data


def get_user_models(user_id, offset, limit):
    if offset is None:
        offset = 0
    if limit is None:
        offset = 10
    params = {"user_id": user_id, "offset": offset, "limit": limit}
    response = requests.get("http://127.0.0.1:8000/api/v1/telegram/models/", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    return data


def add_user_model(user_id, model_name, base_model_id, prompt):
    system_name = generate(size=10)
    params = {"user_id": user_id, "name": model_name, "system_name": system_name, "base_model_id": base_model_id, "prompt": prompt}
    response = requests.post("http://127.0.0.1:8000/api/v1/telegram/models/new", params=params)
    if response.status_code != 200 or response.status_code != 201:
        return "Проблемы "
    data = response.json()
    return data