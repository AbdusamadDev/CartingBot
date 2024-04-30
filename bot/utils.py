import re
import requests


def is_valid(phone_number):
    # Define the regex pattern for Uzbek phone numbers
    uzbek_pattern = r"^(?:\+?998)?9[01234579]\d{7}$"

    # Check if the phone number matches the pattern
    if re.match(uzbek_pattern, phone_number):
        return True
    else:
        return False


def get_districts(regions, selected_region):
    districts = []
    for region in regions:
        if region["pk"] == int(selected_region):
            districts.extend(region["district"])
            break
    return districts


def make_multiselect(markup, selected_district):
    for item in markup["inline_keyboard"]:
        for inner_item in item:
            if inner_item["callback_data"] == f"district:{selected_district}":
                if "✅" in inner_item["text"]:
                    inner_item["text"] = inner_item["text"].replace("✅ ", "")
                else:
                    inner_item["text"] = "✅ " + inner_item["text"]
    return markup


def get_selected_districts(markup):
    districts = []
    for item in markup["inline_keyboard"]:
        for inner_item in item:
            if "✅" in inner_item["text"]:
                districts.append(int(inner_item["callback_data"].split(":")[-1]))
    return districts


def url_to_blob(image_url):
    try:
        # Send a GET request to download the image
        response = requests.get(image_url)
        # Check if the request was successful
        if response.status_code == 200:
            # Return the raw image data (blob)
            return response.content
        else:
            print("Failed to download the image. Status code:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None


if __name__ == "__main__":
    print(is_valid("+99840055565"))
