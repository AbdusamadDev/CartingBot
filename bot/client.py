import requests
from conf import DOMAIN
import json


def verify_phonenumber(phonenumber, code):
    request = requests.post(
        DOMAIN + "/accounts/verify/",
        json={"phonenumber": phonenumber, "sms_code": code},
    )
    response = request.json()
    return response


def register_user(data):
    request = requests.post(DOMAIN + "/accounts/register/", json=data)
    response = request.json()
    return response


def get_profile_details(token):
    request = requests.get(
        DOMAIN + "/accounts/profile/", headers={"Authorization": f"Bearer {token}"}
    )
    print(request.json())
    response = request.json()
    return response


def get_my_loads(token):
    request = requests.get(
        DOMAIN + "/drivers/loads/personal/",
        headers={"Authorization": f"Bearer {token}"},
    )
    print(request.json())
    response = request.json()
    return response


def request_driver_to_client(token, load_id, client_id):
    request = requests.post(
        DOMAIN + "/notifications/create/",
        headers={"Authorization": f"Bearer {token}"},
        data={"load": int(load_id), "to_user": int(client_id)},
    )
    print(load_id, client_id)
    print("Response from driver to client request: ", request.json())
    response = request.json()
    return response


if __name__ == "__main__":
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwMDA3NDI2LCJpYXQiOjE3MTM5NTk0MjYsImp0aSI6IjM4NzY1ODMyZjZkMTRiMjhiMTk1ZTYyMDA4MjE2MjQ0IiwidXNlcl9pZCI6MzN9.CoYiowoB9X64a497sz5ygrQkNcjmA9tm5GS-0a6ee2Y"
    print(
        get_profile_details(
            token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwMDI4MDM1LCJpYXQiOjE3MTM5ODAwMzUsImp0aSI6IjJlZDc0MmQ0ZDI4NDQ3NGE4NmQ5ZjE1NDA5MTc0OTZhIiwidXNlcl9pZCI6NDh9.oW8cascZ2r31KoYNkc-2dOUPyvOGhMokkGWJCssvOKM"
        )
    )
