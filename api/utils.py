import random
import base64

def pass_generator():
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    pw_length = 8
    pswd = ""
    for i in range(pw_length):
        next_index = random.randrange(len(alphabet))
        pswd += alphabet[next_index]
    return pswd



def format_africastalking_number(phone_number):
    if phone_number.startswith("+254"):
        return phone_number
    if phone_number.startswith("254"):
        return "+" + phone_number

    if phone_number.startswith("07"):
        return "+254" + phone_number[1:]

    if phone_number.startswith("7"):
        return "+254" + phone_number
    else:
        return None


def format_mpesa_number(phone_number):
    if phone_number.startswith("254"):
        return phone_number
    if phone_number.startswith("+254"):
        return phone_number[1:]
    if phone_number.startswith("07"):
        return "254" + phone_number[1:]

    if phone_number.startswith("7"):
        return "254" + phone_number
    else:
        return None

def encode_str_to_base_64(str_to_encode):
    """
    Encodes the  given string to base64
    :param str_to_encode
    :return: base64 encoded str
    """
    data = str_to_encode.encode('utf-8')
    encoded_string = str(base64.b64encode(data, 'UTF-8'))
    print(f'encoded string {encoded_string} end')
    return encoded_string

def format_date(date):
    return date.strftime("%Y%m%d%H%M%S")