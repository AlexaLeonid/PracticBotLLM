import requests
import json

from nanoid import generate


def get_count_msg(user_id, convo_id):
    params = {"user_id": user_id, "convo_id": convo_id}
    response = requests.get("https://manygpt.onrender.com/api/v1/telegram/conversation/count", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    count = data["count"]
    return count


def get_conversation(convo_id, offset, limit):
    params = {"convo_id": convo_id, "offset": offset, "limit": limit}
    response = requests.get("https://manygpt.onrender.com/api/v1/telegram/conversation/", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    msgs = []
    for item in data:
        msgs.append((item["content"]["question"], item["content"]["answer"]))
    return msgs


def get_conversations(user_id, offset, limit):
    params = {"user_id": user_id, "offset": offset, "limit": limit}
    response = requests.get("https://manygpt.onrender.com/api/v1/telegram/conversation/all", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    chats = []
    for item in data:
        chats.append((item["name"], item["id"]))
    return chats


def get_count_conversations(user_id):
    params = {"user_id": user_id}
    response = requests.get("https://manygpt.onrender.com/api/v1/telegram/conversation/all/count", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    count = data["count"]
    return count


def add_conversation(user_id, convo_name, model_id):
    params = {"user_id": user_id, "name": convo_name, "model_id": model_id}
    response = requests.post("https://manygpt.onrender.com/api/v1/telegram/conversation/new", params=params)
    if response.status_code != 200 or response.status_code != 201:
        return "Проблемы "
    data = response.json()
  #  return data


def add_bot(user_id, bot_name, model_id, prompt):
    system_name = generate(size=10)
    params = {"user_id": user_id, "name": bot_name, "system_name": system_name,
              "model_id": model_id, "prompt": prompt}
    response = requests.post("https://manygpt.onrender.com/api/v1/telegram/conversation/new/bot", params=params)
    if response.status_code != 200 or response.status_code != 201:
        return "Проблемы "
    data = response.json()
  #  return data

