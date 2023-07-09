from nanoid import generate
import requests
import json


def get_count_projects(user_id):
    params = {"user_id": user_id}
    print(user_id)
    response = requests.get("http://127.0.0.1:8000/api/v1/telegram/project/count", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    print(data)
    count = data["count"]
    return count


def get_user_projects(user_id, offset, limit):
    print(user_id)
    params = {"user_id": user_id, "offset": offset, "limit": limit}
    response = requests.get("http://127.0.0.1:8000/api/v1/telegram/project/all", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    projects = []
    for item in data:
        projects.append((item["name"], item["id"]))
    print(data)
    return projects


def get_user_project(project_id):
    params = {"project_id": project_id}
    response = requests.get("http://127.0.0.1:8000/api/v1/telegram/project/file", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.content
    file_name = response.headers.get("filename")
    return data, file_name


def checking_project_access(user_id):
    params = {"user_id": user_id}
    response = requests.get("http://127.0.0.1:8000/api/v1/telegram/project/access", params=params)
    if response.status_code != 200:
        return "Проблемы "
    data = response.json()
    status = data["status"]
    if status == 200:
        return True
    else:
        return False


def add_user_project(user_id, project_name, mimetype, model_id, prompt, file):
    system_name = generate(size=10)

    params = {"user_id": user_id, "name": project_name, "system_name": system_name, "mimetype": mimetype,
              "model_id": model_id, "prompt": prompt}
    print(file)
    response = requests.post("http://127.0.0.1:8000/api/v1/telegram/project/new", params=params, files={"file": file})

    if response.status_code != 200 or response.status_code != 201:
        return "Проблемы "
    data = response.json()
  #  return data


