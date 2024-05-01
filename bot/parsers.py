{
    "message": {
        "dispatcher": {
            "first_name": None,
            "last_name": None,
            "work_status": True,
            "user": {
                "phonenumber": "+998996685214",
                "user_type": "dispatcher",
                "first_name": None,
                "last_name": None,
                "id": 18,
            },
        }
    },
    "status_code": 200,
}
true = True
null = None
{
    "model": "",
    "type": "b1",
    "number": "191",
    "id": 1,
    "driver": {
        "first_name": "John",
        "last_name": "Doe",
        "work_status": true,
        "work_date_period_from": null,
        "work_date_period_to": null,
        "user": {
            "phonenumber": "+998995687745",
            "user_type": "driver",
            "first_name": null,
            "last_name": null,
            "id": 16,
        },
        "id": 2,
        "routes": [],
    },
}

[
    {
        "first_name": None,
        "last_name": None,
        "work_status": True,
        "work_date_period_from": None,
        "work_date_period_to": None,
        "user": {
            "phonenumber": "+998940000000",
            "user_type": "driver",
            "first_name": None,
            "last_name": None,
            "id": 6,
        },
        "id": 1,
        "routes": [],
    }
]


def get_parsed_drivers_list(driver_list):
    """
    This function returns parsed and decorated list of drivers in list
    """
    message = ""
    for driver in driver_list:
        message += f'👤 {driver["first_name"]} {driver["last_name"]}\n'
    return message
