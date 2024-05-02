import requests
import base64


def is_valid(input_string):
    # Check if input starts with '+'
    if not input_string.startswith("+"):
        return False

    # Check if length is exactly 13 characters
    if len(input_string) != 13:
        return False

    # Check if all characters after '+' are digits
    if not input_string[1:].isdigit():
        return False

    # If all conditions are met, return True
    return True


def get_districts(regions, selected_region):
    # Use next to find the first matching region and return its districts
    return next(
        (
            region["district"]
            for region in regions
            if region["pk"] == int(selected_region)
        ),
        [],
    )


def make_multiselect(markup, selected_district):
    # Simplify the logic for toggling the checkmark
    for item in markup["inline_keyboard"]:
        for inner_item in item:
            if inner_item["callback_data"] == f"district:{selected_district}":
                inner_item["text"] = (
                    "✅ " + inner_item["text"].lstrip("✅ ")
                    if "✅" not in inner_item["text"]
                    else inner_item["text"].replace("✅ ", "")
                )
    return markup


def get_selected_districts(markup):
    # Use a list comprehension for cleaner code
    return [
        int(inner_item["callback_data"].split(":")[-1])
        for item in markup["inline_keyboard"]
        for inner_item in item
        if "✅" in inner_item["text"]
    ]


def url_to_base64(image_url):
    try:
        response = requests.get(image_url)
        encoded_string = base64.b64encode(response.content)
        return encoded_string.decode("utf-8")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    print(is_valid("998940055565"))
