import os
import requests


def login() -> str:
    data = {
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD")
    }
    response = requests.post(url=os.getenv("API_BASE_URL") + "auth/token/login/",
                            data=data)

    if response.status_code == 400:
        requests.post(url=os.getenv("API_BASE_URL") + "auth/users/",
                                data=data)
        response = requests.post(url=os.getenv("API_BASE_URL") + "auth/token/login/", 
                                data=data)
        json_data = response.json()
        return json_data["auth_token"]
    else:
        json_data = response.json()
        return json_data["auth_token"]
