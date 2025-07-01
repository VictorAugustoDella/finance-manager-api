import re
import unicodedata

def is_valid_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_full_name(name: str) -> bool:
    pattern = r"^[A-Za-zÀ-ÿ]+([ '-][A-Za-zÀ-ÿ]+)*$"
    return bool(re.match(pattern, name.strip())) and len(name.split()) >= 2

def is_valid_password(password: str) -> bool:
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
    return re.match(pattern, password) is not None

def validator_amount(amount):
    try:
        amount = float(amount)
        if amount <= 0:
            return False
        return True
    except (ValueError, TypeError):
        return False
    
def normalize_str(text):
    if not text:
        return ''
    # Remove acentos e deixa minúsculo
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ASCII', 'ignore').decode('utf-8')
    return text.lower().strip()