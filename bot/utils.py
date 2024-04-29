import re

def is_valid(phone_number):
    # Define the regex pattern for Uzbek phone numbers
    uzbek_pattern = r"^(?:\+?998)?9[01234579]\d{7}$"

    # Check if the phone number matches the pattern
    if re.match(uzbek_pattern, phone_number):
        return True
    else:
        return False
    

if __name__ == "__main__":
    print(is_valid("+99840055565"))
