import requests
import json


def ask(user_id, convo_id, request, model):
    params = {"user_id": user_id, "convo_id": convo_id, "request": request, "model": model}
    response = requests.post("http://127.0.0.1:8000/api/v1/core/ask", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    response = data["response"]
    return response


def get_models():
    response = requests.get("http://127.0.0.1:8000/api/v1/core/base_models")
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    llms = []
    for item in data:
        llms.append((item["model"], item["id"]))
    return llms
