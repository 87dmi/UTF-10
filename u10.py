import string

# =====================================================================
# ОФИЦИАЛЬНОЕ ЯДРО КОДИРОВАНИЯ UTF-10 (Сетка 12х12, Base-12)
# =====================================================================
rus_lowercase = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ALL_SYMBOLS = [" ", "\n", "=", "+", "-", "*", "/", "(", ")"] + list(string.digits) + list(rus_lowercase) + list(rus_lowercase.upper()) + list(string.ascii_lowercase) + list(string.ascii_uppercase)

CHAR_TO_UTF10 = {char: f"{i // 12},{i % 12}" for i, char in enumerate(ALL_SYMBOLS)}
UTF10_TO_CHAR = {f"{i // 12},{i % 12}": char for i, char in enumerate(ALL_SYMBOLS)}

def encode(text):
    """Преобразует текст в строку координат UTF-10"""
    return " ".join([CHAR_TO_UTF10.get(char, "0,0") for char in text])

def decode(utf10_string):
    """Преобразует координаты UTF-10 в человеческий текст"""
    if not utf10_string.strip(): return ""
    return "".join([UTF10_TO_CHAR.get(pair, "?") for pair in utf10_string.split(" ")])

def version():
    return "UTF-10 Codec Core v2.1"
