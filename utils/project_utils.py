from nanoid import generate
import requests
import json


def get_count_projects(user_id):
    params = {"user_id": user_id}
    response = requests.get("http://127.0.0.1:8000/api/v1/telegram/project/count", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    count = json.loads(data)["count"]
    return count


def get_user_projects(user_id, offset, limit):
    if offset is None:
        offset = 0
    if limit is None:
        offset = 10
    params = {"user_id": user_id, "offset": offset, "limit": limit}
    response = requests.get("http://127.0.0.1:8000/api/v1/telegram/project/all", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    return data


def get_user_project(user_id, project_id):
    params = {"user_id": user_id, "project_id": project_id}
    response = requests.get("http://127.0.0.1:8000/api/v1/telegram/project/file", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    return data


def checking_project_access(user_id):
    params = {"user_id": user_id}
    response = requests.get("http://127.0.0.1:8000/api/v1/telegram/project/access", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    status = json.loads(data)["status"]
    if status == "advanced":
        return True
    else:
        return False


def add_user_project(user_id, project_name, mimetype, model_id, prompt, file):
    system_name = generate(size=10)
    params = {"user_id": user_id, "name": project_name, "system_name": system_name, "mimetype": mimetype,
              "model_id": model_id, "prompt": prompt, "file": file}
    response = requests.post("http://127.0.0.1:8000/api/v1/telegram/project/new", params=params)
    if response.status_code != 200 or response.status_code != 201:
        return "Проблемы "
    data = response.json()
  #  return data


