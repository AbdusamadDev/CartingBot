import re
import requests

def is_valid(phone_number):
    # Simplified validation check
    return bool(re.match(r"^(?:\+?998)?9[01234579]\d{7}$", phone_number))

def get_districts(regions, selected_region):
    # Use next to find the first matching region and return its districts
    return next((region["district"] for region in regions if region["pk"] == int(selected_region)), [])

def make_multiselect(markup, selected_district):
    # Simplify the logic for toggling the checkmark
    for item in markup["inline_keyboard"]:
        for inner_item in item:
            if inner_item["callback_data"] == f"district:{selected_district}":
                inner_item["text"] = "✅ " + inner_item["text"].lstrip("✅ ") if "✅" not in inner_item["text"] else inner_item["text"].replace("✅ ", "")
    return markup

def get_selected_districts(markup):
    # Use a list comprehension for cleaner code
    return [int(inner_item["callback_data"].split(":")[-1]) for item in markup["inline_keyboard"] for inner_item in item if "✅" in inner_item["text"]]

def url_to_blob(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred
        return response.content
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    print(is_valid("+99840055565"))