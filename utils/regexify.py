import random
import string

def regexify() -> str:
    first_char = random.choice(string.ascii_uppercase)
    rest_chars = ''.join(random.choices(string.digits, k=9))
    return first_char + rest_chars