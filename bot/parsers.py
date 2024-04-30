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
