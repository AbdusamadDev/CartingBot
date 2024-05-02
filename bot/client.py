import requests
from bot.conf import DOMAIN


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
    status_code = request.status_code
    if "detail" in response.keys() and status_code == 400:
        print("400 TASHADI")
        return {
            "message": "Account with this phone number already registered",
            "status_code": status_code,
        }
    return {"message": response, "status_code": status_code}


def get_profile_details(token):
    request = requests.get(
        DOMAIN + "/accounts/profile/", headers={"Authorization": f"Bearer {token}"}
    )
    status_code = request.status_code
    response = request.json()
    if "code" in response and status_code == 401:
        print("401 TASHADI")
        return {"message": "token_not_valid", "status_code": status_code}
    else:
        return {"message": response, "status_code": status_code}


def login_user(phonenumber, password):
    request = requests.post(
        DOMAIN + "/accounts/login/",
        data={"phonenumber": phonenumber, "password": password},
    )
    response = request.json()
    if request.status_code == 401:
        return {
            "message": response["error"],
            "status_code": 401,
        }  # Authentication failed
    return {"message": response, "status_code": 200}


def client_confirm_load_delivery(notification_id, token):
    request = requests.post(
        DOMAIN + "/notifications/confirm/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "notification_id": notification_id,
            "status": "yes",
            "action": "confirmation",
        },
    )
    response = request.json()
    return response


def get_my_loads(token):
    request = requests.get(
        DOMAIN + "/drivers/loads/personal/",
        headers={"Authorization": f"Bearer {token}"},
    )
    response = request.json()
    return response


def dispatcher_get_my_loads(token):
    request = requests.get(
        DOMAIN + "/dispatchers/loads/personal/",
        headers={"Authorization": f"Bearer {token}"},
    )
    response = request.json()
    return response


def get_client_personal_loads(token):
    request = requests.get(
        DOMAIN + "/clients/load/?state=personal",
        headers={"Authorization": f"Bearer {token}"},
    )
    response = request.json()
    return response


def get_notifications(token):
    request = requests.get(
        DOMAIN + "/notifications/loads_notify/",
        headers={"Authorization": f"Bearer {token}"},
    )
    response = request.json()
    return response


def request_delivery(token, load_id, user_id, action):
    print(
        "_______________________________________________________________________________________________"
    )
    print("TO USER IS BEING: ", user_id)
    request = requests.post(
        DOMAIN + "/notifications/create/",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "load_id": int(load_id),
            "to_user": int(user_id),
            "action": action,
        },
    )
    response = request.json()
    return response


def fetch_districts_details(token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(DOMAIN + "/drivers/regions/", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.RequestException as e:
        return None


def get_all_loads_dispatcher(token):
    request = requests.get(
        DOMAIN + "/dispatchers/loads/search/",
        headers={"Authorization": f"Bearer {token}"},
    )
    response = request.json()
    return {"message": response, "status_code": request.status_code}


def get_driver_details(token, driver_id):
    request = requests.get(
        DOMAIN + f"/dispatchers/driver/{driver_id}/",
        headers={"Authorization": f"Bearer {token}"},
    )
    response = request.json()
    status_code = request.status_code
    return {"message": response, "status_code": status_code}


def get_drivers_car_details(driver_id):
    request = requests.get(
        DOMAIN + f"/drivers/car/{driver_id}/",
    )
    response = request.json()
    status_code = request.status_code
    return {"message": response, "status_code": status_code}


def show_all_drivers(token):
    request = requests.get(
        DOMAIN + "/dispatchers/drivers/",
        headers={"Authorization": f"Bearer {token}"},
    )
    response = request.json()
    return response


def get_one_load_details(token, load_id):
    request = requests.get(
        DOMAIN + f"/clients/load/{load_id}/?status=all",
        headers={"Authorization": f"Bearer {token}"},
    )
    return {"message": request.json(), "status_code": request.status_code}


def client_add_load(token, data, image_blob):
    try:
        django_url = DOMAIN + "/clients/load/"
        data["product_image"] = image_blob
        response = requests.post(
            django_url,
            headers={"Authorization": f"Bearer {token}"},
            data=data,
        )

        return response.json()
    except Exception as e:
        print("An error occurred:", e)
        return None


if __name__ == "__main__":
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwMDA3NDI2LCJpYXQiOjE3MTM5NTk0MjYsImp0aSI6IjM4NzY1ODMyZjZkMTRiMjhiMTk1ZTYyMDA4MjE2MjQ0IiwidXNlcl9pZCI6MzN9.CoYiowoB9X64a497sz5ygrQkNcjmA9tm5GS-0a6ee2Y"
