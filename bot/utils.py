import re
import requests

def is_valid(input_string):
    # Check if input starts with '+'
    if not input_string.startswith('+'):
        return False
    
    # Check if length is exactly 13 characters
    if len(input_string) != 14:
        return False
    
    # Check if all characters after '+' are digits
    if not input_string[1:].isdigit():
        return False
    
    # If all conditions are met, return True
    return True

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
    print(is_valid("998940055565"))