import requests
import json


def ask(user_id, request):
    params = {"user_id": user_id, "request": request}
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
        llm = item["model"]
        if item["model"] == "chinchilla":
            llm = "ChatGPT"
        if item["model"] == "a2":
            llm = "Claude"
        llms.append((llm, item["id"]))
    return llms


def get_tariffs():
    response = requests.get("http://127.0.0.1:8000/api/v1/telegram/user/plans")
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    tariffs = []
    for item in data:
        tariffs.append((item["name"], item["id"]))
    return tariffs
