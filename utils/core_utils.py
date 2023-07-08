import requests
import json


def ask(user_id, convo_id, request, model):
    params = {"user_id": user_id, "convo_id": convo_id, "request": request, "model": model}
    response = requests.post("http://127.0.0.1:8000/api/v1/core/ask", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    response = json.loads(data)["response"]
    return response
