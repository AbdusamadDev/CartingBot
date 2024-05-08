import requests
from bot.conf import DOMAIN


def verify_phonenumber(phonenumber, code):
    request = requests.post(
        DOMAIN + "/accounts/verify/",
        json={"phonenumber": phonenumber, "sms_code": code},
    )
    response = request.json()
    return response


def register_user(data, telegram_id):
    request = requests.post(
        DOMAIN + f"/accounts/register/?telegram_id={telegram_id}", json=data
    )
    response = request.json()
    status_code = request.status_code
    if "detail" in response.keys() and status_code == 400:
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


def user_exists_in_backend(telegram_id):
    request = requests.get(DOMAIN + f"/accounts/get-user/{telegram_id}/")
    if request.status_code == 200:
        return True
    return False


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
        }
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


def get_transaction(load_id):
    request = requests.get(DOMAIN + f"/dispatchers/transactions/{load_id}")
    response = request.json()
    return {"message": response, "status_code": request.status_code}


def get_my_loads(token, page):
    request = requests.get(
        DOMAIN + f"/drivers/loads/personal/?page={page}",
        headers={"Authorization": f"Bearer {token}"},
    )
    response = request.json()
    return {"message": response, "status_code": request.status_code}


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
    return {"message": response, "status_code": request.status_code}


def get_notifications(token):
    request = requests.get(
        DOMAIN + "/notifications/loads_notify/",
        headers={"Authorization": f"Bearer {token}"},
    )
    response = request.json()
    return response


def finished_delivery_request(token, transaction_id):
    request = requests.post(
        DOMAIN + "/notifications/confirm/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "transaction_id": transaction_id,
            "action": "finish",
        },
    )
    response = request.json()
    return {"message": response, "status_code": request.status_code}


def request_delivery(token, load_id, action):
    request = requests.post(
        DOMAIN + "/notifications/create/",
        headers={"Authorization": f"Bearer {token}"},
        data={"load_id": int(load_id), "action": action},
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


[
    {
        "uuid": "2e20218a-8e37-46e3-b19a-b115c5477a7e",
        "load": {
            "receiver_phone_number": "+998991234567",
            "product_count": 1.0,
            "date_delivery": "2020-01-01T00:23:00+05:00",
            "product_name": "noutbuk",
            "product_info": "gaming",
            "product_type": "dona",
            "from_location": ["aa"],
            "to_location": ["bb"],
            "address": "yupiter",
            "status": "wait",
            "product_image": "http://localhost:8000/media/load_images/18048af4-fa45-45da-bb36-fd983d3cccfb.jpg",
            "id": 1,
            "client": {
                "first_name": None,
                "last_name": None,
                "obj_status": "available",
                "user": {
                    "phonenumber": "+998940055565",
                    "user_type": "client",
                    "first_name": None,
                    "last_name": None,
                    "telegram_id": 6634409389,
                    "id": 1,
                },
            },
        },
        "created_at": "2024-05-06T12:04:02+05:00",
        "updated_at": "2024-05-06T12:04:02+05:00",
        "obj_status": "available",
        "status": "wait_driver",
        "review": 0,
        "driver": {
            "user": {
                "phonenumber": "+998990041122",
                "first_name": None,
                "last_name": None,
                "telegram_id": 2003049919,
            }
        },
        "dispatcher": None,
    },
    {
        "uuid": "2e20218a-8537-46e3-b19a-b115c5477a7e",
        "load": {
            "receiver_phone_number": "+998940055565",
            "product_count": 5.0,
            "date_delivery": "2020-01-01T00:23:00+05:00",
            "product_name": "Load name 5",
            "product_info": "Load info 5",
            "product_type": "m",
            "from_location": ["aa"],
            "to_location": ["bb"],
            "address": "Address 5",
            "status": "active",
            "product_image": "http://localhost:8000/media/load_images/8fc21bd3-3ea0-4471-834d-505bca9bce00.jpg",
            "id": 10,
            "client": {
                "first_name": None,
                "last_name": None,
                "obj_status": "available",
                "user": {
                    "phonenumber": "+998940055565",
                    "user_type": "client",
                    "first_name": None,
                    "last_name": None,
                    "telegram_id": 6634409389,
                    "id": 1,
                },
            },
        },
        "created_at": "2024-05-06T12:04:02+05:00",
        "updated_at": "2029-02-11T03:44:05+05:00",
        "obj_status": "available",
        "status": "finished",
        "review": 0,
        "driver": {
            "user": {
                "phonenumber": "+998990041122",
                "first_name": None,
                "last_name": None,
                "telegram_id": 2003049919,
            }
        },
        "dispatcher": None,
    },
]


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


def client_FINISH_all_processes_request(token, transaction_id, status, action):
    request = requests.post(
        DOMAIN + "/notifications/confirm/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "transaction_id": transaction_id,
            "status": status,
            "action": action,
        },
    )
    response = request.json()
    return {"message": response, "status_code": request.status_code}


def client_add_load(token, data, image_blob):
    try:
        django_url = DOMAIN + "/clients/load/"
        data["product_image"] = image_blob
        response = requests.post(
            django_url,
            headers={"Authorization": f"Bearer {token}"},
            data=data,
        )

        return {"message": response.json(), "status_code": response.status_code}
    except Exception as e:
        print("An error occurred:", e)
        return None


if __name__ == "__main__":
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwMDA3NDI2LCJpYXQiOjE3MTM5NTk0MjYsImp0aSI6IjM4NzY1ODMyZjZkMTRiMjhiMTk1ZTYyMDA4MjE2MjQ0IiwidXNlcl9pZCI6MzN9.CoYiowoB9X64a497sz5ygrQkNcjmA9tm5GS-0a6ee2Y"
    print(user_exists_in_backend(2003049919))
