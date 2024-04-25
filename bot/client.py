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


def dispatcher_get_my_loads(token):
    request = requests.get(
        DOMAIN + "/dispatchers/loads/personal/",
        headers={"Authorization": f"Bearer {token}"},
    )
    print(request.json())
    response = request.json()
    return response


def get_client_personal_loads(token):
    request = requests.get(
        DOMAIN + "/clients/load/?state=personal",
        headers={"Authorization": f"Bearer {token}"},
    )
    print(request.json())
    response = request.json()
    return response


def request_delivery(token, load_id, user_id):
    request = requests.post(
        DOMAIN + "/notifications/create/",
        headers={"Authorization": f"Bearer {token}"},
        data={"load": int(load_id), "to_user": int(user_id)},
    )
    print("Response from driver to client request: ", request.json())
    response = request.json()
    return response


def fetch_districts_details():
    try:
        # Make GET request to fetch districts details from backend
        response = requests.get(DOMAIN + "/drivers/regions/")
        if response.status_code == 200:
            # Extract and return districts details from the response
            return response.json()
        else:
            # Handle non-200 status code
            print(
                f"Failed to fetch districts details. Status code: {response.status_code}"
            )
            return None
    except requests.RequestException as e:
        # Handle request exception
        print(f"Request to fetch districts details failed: {e}")
        return None


def get_all_loads_dispatcher(token):
    request = requests.get(
        DOMAIN + "/clients/load/",
        headers={"Authorization": f"Bearer {token}"},
    )
    print(request.json())
    response = request.json()
    return response


def show_all_drivers(token):
    request = requests.get(
        DOMAIN + "/dispatchers/drivers/",
        headers={"Authorization": f"Bearer {token}"},
    )
    print(request.json())
    response = request.json()
    return response


# def client_add_load(token, )

if __name__ == "__main__":
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwMDA3NDI2LCJpYXQiOjE3MTM5NTk0MjYsImp0aSI6IjM4NzY1ODMyZjZkMTRiMjhiMTk1ZTYyMDA4MjE2MjQ0IiwidXNlcl9pZCI6MzN9.CoYiowoB9X64a497sz5ygrQkNcjmA9tm5GS-0a6ee2Y"
    print(
        get_client_personal_loads(
            token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwMDcyODM2LCJpYXQiOjE3MTQwMjQ4MzYsImp0aSI6Ijc0MGNlZTVmZDExNTRhN2ZiMTE0ZmI1OGM0MWQzOTNiIiwidXNlcl9pZCI6NTl9.5bMEEVGJTrSrz53KEK9mCj0WcaCf3u2YjrW3cxAb8Do"
        )
    )
