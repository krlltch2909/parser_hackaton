import os
import requests
import sys


API_BASE_URL = os.getenv("API_BASE_URL")
if API_BASE_URL is None:
    sys.exit("Incorrect API url")


def get_token() -> str:
    data = {
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD")
    }
    response = requests.post(url=API_BASE_URL + "auth/token/login/",
                             data=data)

    if response.status_code == 400:
        requests.post(url=API_BASE_URL + "auth/users/",
                      data=data)
        response = requests.post(url=API_BASE_URL + "auth/token/login/", 
                                 data=data)
        json_data = response.json()
        return json_data["auth_token"]
    else:
        json_data = response.json()
        return json_data["auth_token"]
